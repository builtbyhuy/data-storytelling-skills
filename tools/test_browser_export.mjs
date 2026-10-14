#!/usr/bin/env node
// Regression controls for real display-size checks, missing assets and full capture.
// Requires the export helper's existing Playwright/Chromium dependencies.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const usage='Usage: node tools/test_browser_export.mjs [--module-dir node_modules] [--browser chromium-executable]';
const options={};
for(let i=2;i<process.argv.length;i++){
  const arg=process.argv[i];
  if(arg==='--help'){console.log(usage);process.exit(0);}
  if(!['--module-dir','--browser'].includes(arg)||!process.argv[i+1]||process.argv[i+1].startsWith('--'))
    throw new Error(usage);
  options[arg.slice(2)]=path.resolve(process.argv[++i]);
}
const helper=fileURLToPath(new URL('../skills/business-chart-communication/scripts/export_web.mjs',import.meta.url));
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const helperBefore=await fs.readFile(helper);
const tempRoot=await fs.realpath(os.tmpdir());
const scratch=await fs.mkdtemp(path.join(tempRoot,'data-story-browser-export-'));
const wholePage=(content,extra='')=>`<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>
html,body{margin:0;font-family:Arial,sans-serif}.page{box-sizing:border-box;width:100%;padding:32px;background:white;height:600px}
h1{margin:0 0 24px;font-size:24px}svg{display:block;height:auto}${extra}
</style></head><body><main class="page"><h1 data-essential>Kiểm tra chữ tiếng Việt</h1>${content}</main></body></html>`;
const label='Chuyên cần tăng 2,5 điểm phần trăm';
const chart=(text=label,asset='')=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 240" width="960" style="width:100%">
<rect x="24" y="100" width="580" height="48" fill="#216661"/><text data-essential x="24" y="70" font-size="24">${text}</text>${asset}</svg>`;
const cases=[
  {id:'vietnamese_svg_target_size',pass:true,html:wholePage(chart()),text:label},
  {id:'same_svg_scaled_small',pass:false,html:wholePage(chart().replace('style="width:100%"','style="width:480px"')),smallFont:true},
  {id:'svg_anisotropic_transform',pass:false,smallFont:true,html:wholePage('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 240" width="960" style="width:100%"><g transform="scale(2,0.25)"><text data-essential x="24" y="200" font-size="24">Chuyên cần</text></g></svg>')},
  {id:'missing_html_image',pass:false,html:wholePage(chart()+'<img src="missing-required.png" width="240" height="120" alt="Biểu đồ bắt buộc">')},
  {id:'missing_svg_image',pass:false,html:wholePage(chart('Chuyên cần','<image href="missing-required.svg" x="650" y="100" width="240" height="120"/>'))},
  {id:'remote_required_image',pass:false,html:wholePage(chart('Chuyên cần','<image href="https://example.invalid/required.svg" x="650" y="100" width="240" height="120"/>')),blocked:true},
  {id:'horizontal_overflow',pass:false,width:1400,html:wholePage(chart(),'.page{width:1400px}')},
  {id:'whole_view_tall',pass:true,height:1400,text:'Hết trang',html:wholePage(chart()+'<p data-essential style="position:absolute;top:1330px;font-size:24px">Hết trang</p>','.page{position:relative;height:1400px}')},
  {id:'mixed_font_marked_paragraph',pass:false,smallFont:true,html:wholePage('<p data-essential style="font-size:10px">Lưu ý cần đọc <strong style="font-size:24px">Tiêu đề lớn</strong></p>')},
  {id:'html_ancestor_scaled_small',pass:false,smallFont:true,width:240,height:150,html:wholePage('<p data-essential style="font-size:24px">Chuyên cần</p>','.page{transform:scale(0.25);transform-origin:top left;}')}
];

function run(args){
  return new Promise((resolve,reject)=>{
    const child=spawn(process.execPath,args,{windowsHide:true});
    let stdout='',stderr='';
    child.stdout.on('data',bytes=>stdout+=bytes);
    child.stderr.on('data',bytes=>stderr+=bytes);
    child.on('error',reject);
    child.on('close',code=>resolve({code,stdout,stderr}));
  });
}

async function cleanScratch(){
  // Only this test's resolved, freshly-created directory may be removed.
  const resolved=await fs.realpath(scratch);
  assert.equal(path.dirname(resolved),tempRoot,'Scratch escaped the OS temp root.');
  assert.ok(path.basename(resolved).startsWith('data-story-browser-export-'));
  async function checkNoLinks(dir){
    for(const entry of await fs.readdir(dir,{withFileTypes:true})){
      const item=path.join(dir,entry.name);
      assert.ok(!(await fs.lstat(item)).isSymbolicLink(),'Preserving unexpected linked scratch content.');
      if(entry.isDirectory())await checkNoLinks(item);
    }
  }
  await checkNoLinks(resolved);
  await fs.rm(resolved,{recursive:true,force:false});
}

const results=[];
try{
  for(const test of cases){
    const dir=path.join(scratch,test.id),input=path.join(dir,'fixture.html'),out=path.join(dir,'out');
    await fs.mkdir(dir);
    await fs.writeFile(input,test.html,'utf8');
    const before=await fs.readFile(input);
    try{
      const args=[helper,'--input',input,'--out',out,'--widths','960','--min-essential','16'];
      for(const key of ['module-dir','browser'])if(options[key])args.push('--'+key,options[key]);
      const executed=await run(args);
      assert.equal(executed.code,test.pass?0:1,executed.stderr||'Unexpected exit outcome.');
      const report=JSON.parse(await fs.readFile(path.join(out,'browser-export.json'),'utf8'));
      assert.equal(report.passed,test.pass,'Unexpected inspection outcome.');
      assert.equal(report.views.length,1);
      assert.equal(report.views[0].width,960);
      assert.equal(report.source_sha256,sha(before));
      assert.deepEqual(await fs.readFile(input),before,'The source was altered.');
      assert.deepEqual(await fs.readFile(helper),helperBefore,'The helper changed during controls.');
      const errors=[...report.errors,...report.views[0].errors];
      assert.equal(errors.length===0,test.pass,'The inspection and error state disagree.');
      const visible=report.views[0].essential_text.filter(text=>text.visible);
      if(test.smallFont)assert.ok(visible.some(text=>text.font_css_px<16),'Small displayed text was not measured.');
      if(test.text)assert.ok(visible.some(text=>text.text===test.text),'Required Vietnamese text was not present in the render.');
      if(test.pass)assert.ok(visible.every(text=>text.font_css_px>=16&&!text.clipped));
      if(test.blocked)assert.ok(report.views[0].blocked_request_count>0,'Remote asset was not blocked.');
      const pngs=report.files.filter(file=>file.kind==='PNG');
      assert.equal(pngs.length,1,'Whole view should produce one capture.');
      const png=await fs.readFile(path.join(out,pngs[0].path));
      assert.deepEqual(png.subarray(0,8),Buffer.from([137,80,78,71,13,10,26,10]));
      const width=png.readUInt32BE(16),height=png.readUInt32BE(20);
      assert.equal(width,(test.width??960)*2,'Capture lost horizontal view content.');
      assert.equal(height,(test.height??600)*2,'Capture lost vertical view content.');
      results.push({id:test.id,passed:true,expected_export_pass:test.pass,png_width:width,png_height:height,source_unchanged:true,measured_essential_px:visible.map(text=>text.font_css_px)});
    }catch(error){
      results.push({id:test.id,passed:false,error:error.message});
    }
  }
}finally{
  // Every helper subprocess has exited and closed its browser before cleanup.
  await cleanScratch();
}
const passed=results.every(result=>result.passed);
console.log(JSON.stringify({schema:'browser-export-regression.v1',passed,helper_sha256:sha(helperBefore),cases:results,scratch_removed:true}));
if(!passed)process.exitCode=1;
