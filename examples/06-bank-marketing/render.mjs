// Offline headless render. All machine/runtime paths are caller arguments.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const args=Object.fromEntries(process.argv.slice(2).reduce((a,x,i,all)=>{if(x.startsWith('--'))a.push([x.slice(2),all[i+1]]);return a},[]));
for(const k of ['modules','chrome','out'])if(!args[k])throw new Error(`Missing --${k}`);
const require=createRequire(path.join(path.resolve(args.modules),'package.json'));
const {chromium}=require(path.join(path.resolve(args.modules),'playwright'));
const out=path.resolve(args.out), checks=path.join(out,'_inspection');fs.mkdirSync(checks,{recursive:true});
const browser=await chromium.launch({executablePath:path.resolve(args.chrome),headless:true,args:['--disable-network-service','--allow-file-access-from-files']});
const page=await browser.newPage({viewport:{width:1280,height:1000},deviceScaleFactor:1});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const requested=[];page.on('request',r=>requested.push(r.url()));
await page.goto(pathToFileURL(path.join(out,'report.html')).href,{waitUntil:'load'});
await page.pdf({path:path.join(out,'report.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:false,tagged:true});
const receipts={browser_version:browser.version(),errors,network_requests:[],surfaces:[]};
for(const width of [1280,390]){
 await page.setViewportSize({width,height:1000});await page.emulateMedia({media:'screen'});
 const pgs=page.locator('.page');
 for(let i=0;i<await pgs.count();i++)await pgs.nth(i).screenshot({path:path.join(checks,`html-${width}-page-${i+1}.png`)});
 const dom=await page.evaluate(()=>({
   width:innerWidth, documentWidth:document.documentElement.scrollWidth,
   ids:[...document.querySelectorAll('[id]')].map(x=>x.id),
   charts:[...document.querySelectorAll('svg')].filter(s=>s.getBoundingClientRect().width>0 && getComputedStyle(s.parentElement).display!=='none').map(s=>({name:s.querySelector('title').textContent,ids:s.getAttribute('aria-labelledby'),texts:[...s.querySelectorAll('text')].map(x=>x.textContent),width:s.getBoundingClientRect().width,clippedText:[...s.querySelectorAll('text')].filter(x=>{const b=x.getBBox(),v=s.viewBox.baseVal;return b.x<-.5||b.y<-.5||b.x+b.width>v.width+.5||b.y+b.height>v.height+.5}).map(x=>x.textContent)})),
   tables:[...document.querySelectorAll('table')].map(t=>({id:t.id,caption:t.caption?.textContent,headers:[...t.querySelectorAll('thead th')].map(x=>x.textContent),rows:[...t.querySelectorAll('tbody tr')].map(r=>[...r.children].map(c=>c.textContent)),narrowNumbers:[...t.querySelectorAll('td')].filter(x=>x.scrollWidth>x.clientWidth).map(x=>x.textContent)})),
   badReferences:[...document.querySelectorAll('[aria-labelledby]')].flatMap(x=>x.getAttribute('aria-labelledby').split(' ').filter(id=>!document.getElementById(id))),
   externalAssets:[...document.querySelectorAll('script[src],link[href],img[src]')].map(x=>x.src||x.href).filter(x=>/^https?:/.test(x)),
   screenText:document.body.innerText
 }));
 const cdp=await page.context().newCDPSession(page);await cdp.send('Accessibility.enable');
 const ax=await cdp.send('Accessibility.getFullAXTree');
 const chartNames=ax.nodes.filter(x=>!x.ignored&&x.role?.value==='image').map(x=>x.name?.value);
 if(dom.documentWidth>width)throw new Error(`Document overflow at ${width}: ${dom.documentWidth}`);
 if(new Set(dom.ids).size!==dom.ids.length)throw new Error('Duplicate IDs');
 if(dom.badReferences.length||dom.externalAssets.length)throw new Error('Bad references/assets');
 if(chartNames.length!==2 || !chartNames[0].includes('kết quả chiến dịch trước') || !chartNames[1].includes('số lần liên lạc'))throw new Error(`Unexpected accessible chart names: ${chartNames}`);
 for(const table of dom.tables)if(table.narrowNumbers.length)throw new Error(`Table numbers clipped: ${table.id}`);
 for(const chart of dom.charts)if(chart.clippedText.length)throw new Error(`SVG text clipped: ${chart.name}: ${chart.clippedText}`);
 if(width===390){
   for(const id of ['history-table','attempts-table','contact-check']){
     const loc=page.locator(`#${id}`).locator('..');
     const numericVisible=await loc.evaluate(region=>{
       const cells=[...region.querySelectorAll('td')];
       const bad=[];
       for(const cell of cells){
         const c=cell.getBoundingClientRect(),r=region.getBoundingClientRect();
         region.scrollLeft+=c.right-r.right+10;
         const range=document.createRange();range.selectNodeContents(cell);
         const text=range.getBoundingClientRect(),box=region.getBoundingClientRect();
         const row=cell.closest('tr'),sticky=row.firstElementChild.getBoundingClientRect();
         if(text.left<sticky.right-.5||text.right>box.right+.5)bad.push({text:cell.textContent,row:row.firstElementChild.textContent});
       }
       return {cells:cells.length,bad};
     });
     if(numericVisible.bad.length)throw new Error(`Numeric lookup not recoverable: ${id}: ${JSON.stringify(numericVisible.bad)}`);
     dom.tables.find(t=>t.id===id).numericLookup=numericVisible;
     await loc.evaluate(x=>{x.scrollLeft=(x.scrollWidth-x.clientWidth)/2});
     await loc.screenshot({path:path.join(checks,`table-${id}-390-middle.png`)});
     await loc.evaluate(x=>{x.scrollLeft=x.scrollWidth-x.clientWidth});
     await loc.screenshot({path:path.join(checks,`table-${id}-390-right.png`)});
     await loc.evaluate(x=>{x.scrollLeft=0});
   }
 }
 receipts.surfaces.push({width,...dom,chartNames,checks:{no_document_overflow:true,unique_ids:true,correct_visible_chart_names:true,numeric_cells_not_clipped:true}});
}
receipts.network_requests=requested.filter(x=>/^https?:/.test(x));if(receipts.network_requests.length||errors.length)throw new Error('Unexpected network or browser errors');
fs.writeFileSync(path.join(out,'evidence','browser-checks.json'),JSON.stringify(receipts,null,2));
await browser.close();console.log(JSON.stringify({pdf:path.join(out,'report.pdf'),screen_widths:[1280,390],screenshots:8,network_requests:receipts.network_requests,errors}));
