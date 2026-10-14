#!/usr/bin/env node
// Export authored, local HTML from its real browser render. Requires Playwright.
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';

const help = `Usage: node export_web.mjs --input page.html --out exports
  [--module-dir /path/to/node_modules] [--browser /path/to/chromium]
  [--widths 960,1280] [--min-essential 16] [--selector .page]
  [--pdf report.pdf] [--allow-network]
Exports whole-view 2x PNGs, browser PDF if requested, and an inspection receipt.
Mark essential reading nodes with data-essential (an ancestor may carry it).
The receipt does not certify data accuracy, all overlaps or human comprehension.`;
const opts = {widths:'960,1280', 'min-essential':'16', selector:'.page'};
for(let i=2;i<process.argv.length;i++){
  const arg=process.argv[i];
  if(arg==='--help'){console.log(help);process.exit(0);}
  if(arg==='--allow-network'){opts['allow-network']=true;continue;}
  if(!arg.startsWith('--') || !process.argv[i+1] || process.argv[i+1].startsWith('--'))
    throw new Error(help);
  const key=arg.slice(2);
  if(!['input','out','module-dir','browser','widths','min-essential','selector','pdf'].includes(key))
    throw new Error(`Unknown option: ${arg}`);
  opts[key]=process.argv[++i];
}
if(!opts.input || !opts.out)throw new Error(help);
const widths=opts.widths.split(',').map(Number);
const minEssential=Number(opts['min-essential']);
if(widths.some(x=>!Number.isInteger(x)||x<200||x>10000)||!Number.isFinite(minEssential)||minEssential<=0)
  throw new Error('Invalid display widths or minimum essential font size.');
const input=path.resolve(opts.input), out=path.resolve(opts.out);
if(input===out)throw new Error('Output must be a directory distinct from the input.');
const requireFrom=opts['module-dir']
  ? createRequire(path.join(path.resolve(opts['module-dir']),'package.json'))
  : createRequire(import.meta.url);
const {chromium}=requireFrom('playwright');
const bytes=await fs.readFile(input);
await fs.mkdir(out,{recursive:true});
const report={schema:'browser-visual-export.v1', source:path.basename(input),
  source_sha256:createHash('sha256').update(bytes).digest('hex'),
  renderer:'Playwright Chromium',network_allowed:!!opts['allow-network'],
  minimum_essential_css_px:minEssential,views:[],files:[],errors:[],
  limits:['Font size and bounds are measured heuristics, not human readability.',
    'Automated checks do not detect every overlap or verify data/claim accuracy.',
    'SVG binding and browser accessibility-tree checks are not a screen-reader or full accessibility audit.',
    'Essential table-cell bounds do not establish comfortable spacing or complete table semantics.',
    'Local browser export does not verify the hosted or chat-preview surface.']};
const browser=await chromium.launch({headless:true,
  ...(opts.browser?{executablePath:path.resolve(opts.browser)}:{})});
try{
  for(const width of widths){
    const context=await browser.newContext({viewport:{width,height:900},deviceScaleFactor:2});
    const page=await context.newPage();
    const blocked=[];
    if(!opts['allow-network'])await page.route(/^https?:\/\//, async route=>{
      blocked.push(route.request().url());await route.abort();
    });
    page.on('pageerror',error=>report.errors.push(`At ${width}px: ${error.message}`));
    const assetName=url=>{try{return path.basename(new URL(url).pathname);}catch{return 'asset';}};
    page.on('requestfailed',request=>report.errors.push(`At ${width}px: failed asset ${assetName(request.url())}`));
    page.on('response',response=>{
      if(response.status()>=400)report.errors.push(`At ${width}px: HTTP ${response.status()} asset ${assetName(response.url())}`);
    });
    await page.goto(pathToFileURL(input).href,{waitUntil:'networkidle'});
    await page.evaluate(()=>document.fonts.ready);
    const view=await page.evaluate(({selector,minEssential})=>{
      const errors=[];
      const roots=[...document.querySelectorAll(selector)];
      if(!roots.length)errors.push(`No capture nodes match ${selector}`);
      const normalize=text=>(text??'').replace(/\s+/g,' ').trim();
      const ids=new Map();
      for(const element of document.querySelectorAll('[id]')){
        const id=element.getAttribute('id');
        if(id)ids.set(id,[...(ids.get(id)??[]),element]);
      }
      const duplicateIds=[...ids].filter(([,elements])=>elements.length>1)
        .map(([id,elements])=>({id,count:elements.length}));
      // Responsive copies still occupy the same document ID namespace, even
      // when display:none removes one copy from the accessibility tree.
      for(const {id,count} of duplicateIds)errors.push(`Duplicate document id ${id}: ${count} elements`);
      const svgNames=[...document.querySelectorAll('svg')].map((svg,index)=>{
        const rect=svg.getBoundingClientRect(),style=getComputedStyle(svg);
        const visible=rect.width>0&&rect.height>0&&style.visibility!=='hidden'&&style.display!=='none';
        const decorative=!!svg.closest('[aria-hidden="true"]')||['none','presentation'].includes(svg.getAttribute('role'));
        const title=svg.querySelector(':scope > title');
        const desc=svg.querySelector(':scope > desc');
        const declared=svg.getAttribute('role')==='img'||svg.hasAttribute('aria-label')||
          svg.hasAttribute('aria-labelledby')||!!title;
        const resolve=attribute=>{
          const tokens=normalize(svg.getAttribute(attribute)).split(' ').filter(Boolean);
          const targets=tokens.map(token=>{
            const matches=ids.get(token)??[];
            if(!decorative&&matches.length!==1)
              errors.push(`${matches.length?'Ambiguous':'Unresolved'} SVG ${index+1} ${attribute} reference: ${token}`);
            const target=matches[0];
            // A regular external caption is valid. Reusing a different SVG's
            // title/description identifies the wrong graph even with unique IDs.
            if(!decorative&&target?.closest('svg')&&target.closest('svg')!==svg)
              errors.push(`SVG ${index+1} ${attribute} references another SVG: ${token}`);
            return normalize(target?.textContent);
          });
          return {tokens,text:normalize(targets.join(' '))};
        };
        const labelled=resolve('aria-labelledby'),described=resolve('aria-describedby');
        const name=labelled.tokens.length?labelled.text:
          normalize(svg.getAttribute('aria-label'))||normalize(title?.textContent);
        if(visible&&!decorative&&declared&&!name)errors.push(`Missing or empty SVG ${index+1} accessible name`);
        return {index:index+1,visible,decorative,requires_name:declared,
          naming_scope:decorative?'decorative':declared?'declared_image':'unclassified_svg',
          labelledby:labelled.tokens,describedby:described.tokens,
          resolved_name:name,resolved_description:described.tokens.length?described.text:normalize(desc?.textContent)};
      });
      // Text nodes preserve a paragraph's directly-owned text beside inline
      // children with a different font size; scanning only leaves misses it.
      const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
      const nodes=[];
      for(let n=walker.nextNode();n;n=walker.nextNode()){
        if(n.textContent.trim() && n.parentElement?.closest('[data-essential]') &&
          !n.parentElement.closest('script,style,template'))nodes.push(n);
      }
      const texts=nodes.map(n=>{
        const e=n.parentElement,s=getComputedStyle(e);
        const range=document.createRange();range.selectNode(n);
        const r=range.getBoundingClientRect();
        let ctm=e instanceof SVGGraphicsElement?e.getScreenCTM():new DOMMatrix();
        let unsupportedTransform=false;
        if(!(e instanceof SVGGraphicsElement)){
          for(let p=e;p;p=p.parentElement){
            const style=getComputedStyle(p);
            if(style.transform!=='none'){
              const matrix=new DOMMatrix(style.transform);
              if(!matrix.is2D)unsupportedTransform=true;
              ctm=matrix.multiply(ctm);
            }
            // Independent CSS transforms/3D perspective need a separate
            // measurement; fail conservatively rather than certify the font.
            if(style.scale!=='none'||style.rotate!=='none'||style.perspective!=='none')unsupportedTransform=true;
            const zoom=Number(style.zoom);
            if(Number.isFinite(zoom)&&zoom>0&&zoom!==1)ctm=new DOMMatrix().scale(zoom).multiply(ctm);
          }
        }
        // The smallest singular value also detects nonuniform scale/shear.
        // Horizontal scaling alone must not certify vertically crushed glyphs.
        let scale=1;
        if(ctm){
          const norm=ctm.a**2+ctm.b**2+ctm.c**2+ctm.d**2;
          const determinant=ctm.a*ctm.d-ctm.b*ctm.c;
          scale=Math.sqrt(Math.max(0,(norm-Math.sqrt(Math.max(0,norm**2-4*determinant**2)))/2));
        }
        const visible=s.display!=='none' && s.visibility!=='hidden' && r.width>0 && r.height>0;
        const size=parseFloat(s.fontSize)*scale;
        const parent=e.closest('svg')??e.closest(selector);
        const bound=parent?.getBoundingClientRect();
        let scrollX=false,scrollY=false;
        for(let p=e.parentElement;p&&p!==parent;p=p.parentElement){
          const overflow=getComputedStyle(p);
          scrollX||=['auto','scroll'].includes(overflow.overflowX)&&p.scrollWidth>p.clientWidth;
          scrollY||=['auto','scroll'].includes(overflow.overflowY)&&p.scrollHeight>p.clientHeight;
        }
        const clipped=visible && bound &&
          ((!scrollX&&(r.left<bound.left-2||r.right>bound.right+2))||
           (!scrollY&&(r.top<bound.top-2||r.bottom>bound.bottom+2)));
        const cell=e.closest('td,th'),cellBound=cell?.getBoundingClientRect();
        const exceedsCell=visible&&cellBound&&[...range.getClientRects()].some(box=>
          box.left<cellBound.left-2||box.right>cellBound.right+2||box.top<cellBound.top-2||box.bottom>cellBound.bottom+2);
        return {text:n.textContent.trim().slice(0,180),visible,
          font_css_px:Number(size.toFixed(2)),font_family:s.fontFamily,
          clipped:!!clipped,exceeds_table_cell:!!exceedsCell,unsupported_transform:unsupportedTransform};
      });
      if(!texts.some(t=>t.visible))errors.push('No visible essential text; mark required reading content with data-essential.');
      for(const t of texts.filter(t=>t.visible)){
        if(t.font_css_px<minEssential)errors.push(`Essential font ${t.font_css_px}px: ${t.text}`);
        if(t.clipped)errors.push(`Essential text exceeds its SVG/view bounds: ${t.text}`);
        if(t.exceeds_table_cell)errors.push(`Essential text exceeds its table cell: ${t.text}`);
        if(t.unsupported_transform)errors.push(`Unsupported CSS transform on essential text: ${t.text}`);
      }
      if(document.documentElement.scrollWidth>innerWidth+2)
        errors.push(`Page overflows horizontally: ${document.documentElement.scrollWidth}px at ${innerWidth}px`);
      for(const im of document.images)if(!im.complete||im.naturalWidth===0)errors.push(`Unloaded image: ${im.getAttribute('src')}`);
      return {width:innerWidth,essential_text:texts,
        duplicate_document_ids:duplicateIds,svg_names:svgNames,
        capture_count:roots.length,svg_count:document.querySelectorAll('svg').length,
        svg_image_count:document.querySelectorAll('svg image').length,errors};
    },{selector:opts.selector,minEssential});
    // Read Chromium's real accessibility tree without adding IDs/attributes or
    // changing authored DOM. Keep an unavailable API distinct from a pass.
    let cdp;
    try{
      cdp=await context.newCDPSession(page);
      await cdp.send('Accessibility.enable');
      const {root}=await cdp.send('DOM.getDocument',{depth:0});
      const {nodeIds}=await cdp.send('DOM.querySelectorAll',{nodeId:root.nodeId,selector:'svg'});
      const backendIds=await Promise.all(nodeIds.map(async nodeId=>
        (await cdp.send('DOM.describeNode',{nodeId,depth:0})).node.backendNodeId));
      const {nodes}=await cdp.send('Accessibility.getFullAXTree');
      const byBackend=new Map(nodes.filter(node=>node.backendDOMNodeId).map(node=>[node.backendDOMNodeId,node]));
      view.accessibility_tree={available:true,renderer:'Chromium CDP',screen_reader_execution:false};
      for(const [index,svg] of view.svg_names.entries()){
        const observed=byBackend.get(backendIds[index]);
        svg.ax_observed=!!observed;
        svg.ax_exposed=!!observed&&!observed.ignored;
        svg.ax_name=String(observed?.name?.value??'').replace(/\s+/g,' ').trim();
        svg.ax_role=observed?.role?.value??null;
        if(svg.visible&&!svg.decorative&&svg.requires_name){
          if(!svg.ax_exposed)view.errors.push(`SVG ${svg.index} declared image is absent from browser accessibility tree`);
          else if(!svg.ax_name)view.errors.push(`SVG ${svg.index} has an empty browser accessible name`);
          else if(svg.ax_name!==svg.resolved_name)
            view.errors.push(`SVG ${svg.index} browser accessible name differs from its declared alternative`);
        }
      }
    }catch{
      view.accessibility_tree={available:false,reason:'Browser accessibility-tree API unavailable',screen_reader_execution:false};
    }finally{if(cdp)await cdp.detach();}
    if(blocked.length)view.errors.push('External requests blocked; embed/localize required assets or explicitly allow network.');
    // URLs can contain private data. Keep only the number in the public receipt.
    view.blocked_request_count=blocked.length;
    report.views.push(view);
    const roots=page.locator(opts.selector);
    for(let i=0;i<await roots.count();i++){
      const filename=`view-${width}-${String(i+1).padStart(2,'0')}.png`;
      await roots.nth(i).screenshot({path:path.join(out,filename),animations:'disabled'});
      report.files.push({path:filename,kind:'PNG',display_width:width,device_scale_factor:2});
    }
    if(opts.pdf && width===widths[0]){
      const pdfPath=path.isAbsolute(opts.pdf)?opts.pdf:path.join(out,opts.pdf);
      await page.pdf({path:pdfPath,printBackground:true,preferCSSPageSize:true});
      report.files.push({path:path.basename(pdfPath),kind:'PDF',verified_vector:false});
    }
    await context.close();
  }
}finally{await browser.close();}
for(const f of report.files){
  const fp=f.kind==='PDF'&&path.isAbsolute(opts.pdf)?opts.pdf:path.join(out,f.path);
  const b=await fs.readFile(fp);f.bytes=b.length;
  f.sha256=createHash('sha256').update(b).digest('hex');
}
report.passed=report.errors.length===0 && report.views.every(v=>v.errors.length===0);
await fs.writeFile(path.join(out,'browser-export.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({passed:report.passed,views:report.views.map(v=>({width:v.width,errors:v.errors})),
  errors:report.errors,files:report.files.length}));
if(!report.passed)process.exitCode=1;
