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
const testSource=fileURLToPath(import.meta.url);
const testBefore=await fs.readFile(testSource);
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
  {id:'distinct_svg_names',pass:true,html:wholePage('<svg role="img" aria-labelledby="growth-title growth-desc" viewBox="0 0 960 100"><title id="growth-title">Giá trị tăng</title><desc id="growth-desc">So quý II với quý III</desc><text data-essential x="24" y="55" font-size="24">Giá trị tăng</text></svg><svg role="img" aria-labelledby="count-title count-desc" viewBox="0 0 960 100"><title id="count-title">Số mã tăng</title><desc id="count-desc">Cùng kỳ đối chiếu</desc><text data-essential x="24" y="55" font-size="24">Số mã tăng</text></svg>'),accessibleNames:['Giá trị tăng So quý II với quý III','Số mã tăng Cùng kỳ đối chiếu']},
  {id:'duplicate_svg_name_ids',pass:false,nameError:'Duplicate document id',html:wholePage('<svg role="img" aria-labelledby="title" viewBox="0 0 960 100"><title id="title">Giá trị tăng</title><text data-essential x="24" y="55" font-size="24">Giá trị tăng</text></svg><svg role="img" aria-labelledby="title" viewBox="0 0 960 100"><title id="title">Số mã tăng</title><text data-essential x="24" y="55" font-size="24">Số mã tăng</text></svg>')},
  {id:'unresolved_svg_name_reference',pass:false,nameError:'Unresolved SVG',html:wholePage('<svg role="img" aria-labelledby="missing-title" viewBox="0 0 960 100"><text data-essential x="24" y="55" font-size="24">Giá trị tăng</text></svg>')},
  {id:'wrong_svg_title_binding',pass:false,nameError:'another SVG',html:wholePage('<svg role="img" aria-labelledby="growth-title" viewBox="0 0 960 100"><title id="growth-title">Giá trị tăng</title><text data-essential x="24" y="55" font-size="24">Giá trị tăng</text></svg><svg role="img" aria-labelledby="growth-title" viewBox="0 0 960 100"><title id="count-title">Số mã tăng</title><text data-essential x="24" y="55" font-size="24">Số mã tăng</text></svg>')},
  {id:'long_number_exceeds_table_cell',pass:false,cellError:true,html:wholePage('<table data-essential style="width:260px;table-layout:fixed;border-collapse:collapse;font-size:24px"><tr><th>Quý II</th><th>Quý III</th></tr><tr><td style="white-space:nowrap">−1.907.663,75</td><td>2.383.668,24</td></tr></table>')},
  {id:'long_numbers_roomy_table',pass:true,html:wholePage('<table data-essential style="width:800px;table-layout:fixed;border-collapse:collapse;font-size:24px"><tr><th>Quý II</th><th>Quý III</th></tr><tr><td style="white-space:nowrap">−1.907.663,75</td><td style="white-space:nowrap">2.383.668,24</td></tr></table>')},
  {id:'missing_svg_name',pass:false,nameError:'Missing or empty SVG',html:wholePage('<svg role="img" viewBox="0 0 960 100"><text data-essential x="24" y="55" font-size="24">Giá trị tăng</text></svg>')},
  {id:'empty_svg_name',pass:false,nameError:'Missing or empty SVG',html:wholePage('<svg role="img" aria-label="   " viewBox="0 0 960 100"><text data-essential x="24" y="55" font-size="24">Giá trị tăng</text></svg>')},
  {id:'hidden_duplicate_svg_ids',pass:false,nameError:'Duplicate document id',html:wholePage('<svg role="img" aria-labelledby="shared-title" viewBox="0 0 960 100"><title id="shared-title">Giá trị tăng</title><text data-essential x="24" y="55" font-size="24">Giá trị tăng</text></svg><svg style="display:none" role="img" aria-labelledby="shared-title" viewBox="0 0 340 100"><title id="shared-title">Bản điện thoại</title></svg>')},
  {id:'svg_aria_label',pass:true,accessibleNames:['Giá trị ghi nhận tăng'],html:wholePage('<svg role="img" aria-label="Giá trị ghi nhận tăng" viewBox="0 0 960 100"><text data-essential x="24" y="55" font-size="24">Giá trị tăng</text></svg>')},
  {id:'svg_native_title',pass:true,accessibleNames:['Giá trị ghi nhận tăng'],html:wholePage('<svg viewBox="0 0 960 100"><title>Giá trị ghi nhận tăng</title><text data-essential x="24" y="55" font-size="24">Giá trị tăng</text></svg>')},
  {id:'svg_external_caption',pass:true,accessibleNames:['Giá trị ghi nhận tăng'],html:wholePage('<p id="graph-caption" data-essential style="font-size:24px">Giá trị ghi nhận tăng</p><svg role="img" aria-labelledby="graph-caption" viewBox="0 0 960 100"><text data-essential x="24" y="55" font-size="24">Giá trị tăng</text></svg>')},
  {id:'svg_decorative',pass:true,decorative:true,html:wholePage('<svg aria-hidden="true" viewBox="0 0 960 100"><rect x="24" y="24" width="600" height="30" fill="#216661"/></svg>')},
  {id:'unresolved_svg_description',pass:false,nameError:'Unresolved SVG',html:wholePage('<svg role="img" aria-label="Giá trị tăng" aria-describedby="missing-desc" viewBox="0 0 960 100"><text data-essential x="24" y="55" font-size="24">Giá trị tăng</text></svg>')},
  {id:'clipped_number_inside_cell',pass:false,cellError:true,html:wholePage('<table data-essential style="width:200px;table-layout:fixed;font-size:24px"><tr><td style="overflow:hidden;white-space:nowrap">−1.907.663,75</td><td>0</td></tr></table>')},
  {id:'mobile_reflowed_numbers',pass:true,viewportWidth:390,html:wholePage('<table data-essential style="width:100%;table-layout:fixed;font-size:18px"><tr><th>Quý</th><th>Giá trị GBP</th></tr><tr><td>II</td><td style="white-space:nowrap">−1.907.663,75</td></tr><tr><td>III</td><td style="white-space:nowrap">2.383.668,24</td></tr></table>')},
  {id:'mobile_controlled_table_scroll',pass:true,viewportWidth:390,html:wholePage('<div tabindex="0" role="region" aria-label="Bảng số liệu; cuộn ngang" style="width:100%;overflow-x:auto"><table data-essential style="width:800px;table-layout:fixed;font-size:24px"><tr><th>Quý II</th><th>Quý III</th></tr><tr><td style="white-space:nowrap">−1.907.663,75</td><td style="white-space:nowrap">2.383.668,24</td></tr></table></div>')},
  {id:'mobile_tiny_table',pass:false,viewportWidth:390,smallFont:true,html:wholePage('<table data-essential style="width:100%;font-size:10px"><tr><th>Quý II</th><th>Quý III</th></tr><tr><td>−1.907.663,75</td><td>2.383.668,24</td></tr></table>')},
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

function run(args,executable=process.execPath,env=process.env){
  return new Promise((resolve,reject)=>{
    const child=spawn(executable,args,{windowsHide:true,env});
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
  if(process.platform==='win32'){
    // Use ordinary Windows deletion, preserving hidden/read-only protection.
    // The target is carried as data, never interpolated into shell source.
    const cleaned=await run(['-NoProfile','-NonInteractive','-Command',
      '$ErrorActionPreference = "Stop"; $testScratch = (Resolve-Path -LiteralPath $env:DATA_STORY_TEST_SCRATCH).Path; $testTemp = (Resolve-Path -LiteralPath $env:DATA_STORY_TEST_TEMP).Path; if ([IO.Path]::GetDirectoryName($testScratch) -ne $testTemp -or [IO.Path]::GetFileName($testScratch) -notlike "data-story-browser-export-*") { throw "Scratch target escaped its validated scope." }; Remove-Item -LiteralPath $testScratch -Recurse -ErrorAction Stop'],
      'pwsh.exe',{...process.env,DATA_STORY_TEST_SCRATCH:resolved,DATA_STORY_TEST_TEMP:tempRoot});
    assert.equal(cleaned.code,0,cleaned.stderr||'Preserving scratch after native cleanup conflict.');
  }else await fs.rm(resolved,{recursive:true,force:false});
}

const results=[];
try{
  for(const test of cases){
    const dir=path.join(scratch,test.id),input=path.join(dir,'fixture.html'),out=path.join(dir,'out');
    await fs.mkdir(dir);
    await fs.writeFile(input,test.html,'utf8');
    const before=await fs.readFile(input);
    try{
      const args=[helper,'--input',input,'--out',out,'--widths',String(test.viewportWidth??960),'--min-essential','16'];
      for(const key of ['module-dir','browser'])if(options[key])args.push('--'+key,options[key]);
      const executed=await run(args);
      assert.equal(executed.code,test.pass?0:1,executed.stderr||'Unexpected exit outcome.');
      const report=JSON.parse(await fs.readFile(path.join(out,'browser-export.json'),'utf8'));
      assert.equal(report.passed,test.pass,'Unexpected inspection outcome.');
      assert.equal(report.views.length,1);
      assert.equal(report.views[0].width,test.viewportWidth??960);
      assert.equal(report.source_sha256,sha(before));
      assert.deepEqual(await fs.readFile(input),before,'The source was altered.');
      assert.deepEqual(await fs.readFile(helper),helperBefore,'The helper changed during controls.');
      assert.deepEqual(await fs.readFile(testSource),testBefore,'The test source changed during controls.');
      const errors=[...report.errors,...report.views[0].errors];
      assert.equal(errors.length===0,test.pass,'The inspection and error state disagree.');
      const visible=report.views[0].essential_text.filter(text=>text.visible);
      if(test.smallFont)assert.ok(visible.some(text=>text.font_css_px<16),'Small displayed text was not measured.');
      if(test.text)assert.ok(visible.some(text=>text.text===test.text),'Required Vietnamese text was not present in the render.');
      if(test.pass)assert.ok(visible.every(text=>text.font_css_px>=16&&!text.clipped));
      if(test.blocked)assert.ok(report.views[0].blocked_request_count>0,'Remote asset was not blocked.');
      if(test.nameError)assert.ok(errors.some(error=>error.includes(test.nameError)),'The naming fault was not detected.');
      if(test.accessibleNames){
        assert.deepEqual(report.views[0].svg_names.map(svg=>svg.resolved_name),test.accessibleNames,'SVG names no longer identify their own chart.');
        assert.equal(report.views[0].accessibility_tree.available,true,'Actual browser accessibility-tree observation is unavailable.');
        assert.deepEqual(report.views[0].svg_names.map(svg=>svg.ax_name),test.accessibleNames,'Browser exposes a different chart name.');
        assert.ok(report.views[0].svg_names.every(svg=>svg.ax_observed&&svg.ax_exposed),'Named chart was not exposed in the browser accessibility tree.');
      }
      if(test.decorative){
        assert.ok(report.views[0].svg_names.every(svg=>svg.decorative&&!svg.ax_exposed),'Decorative SVG should not be exposed as a named chart.');
      }
      if(test.cellError)assert.ok(visible.some(text=>text.exceeds_table_cell),'The overflowing numeric value was not detected.');
      const pngs=report.files.filter(file=>file.kind==='PNG');
      assert.equal(pngs.length,1,'Whole view should produce one capture.');
      const png=await fs.readFile(path.join(out,pngs[0].path));
      assert.deepEqual(png.subarray(0,8),Buffer.from([137,80,78,71,13,10,26,10]));
      const width=png.readUInt32BE(16),height=png.readUInt32BE(20);
      assert.equal(width,(test.width??test.viewportWidth??960)*2,'Capture lost horizontal view content.');
      assert.equal(height,(test.height??600)*2,'Capture lost vertical view content.');
      results.push({id:test.id,passed:true,expected_export_pass:test.pass,png_width:width,png_height:height,
        source_unchanged:true,helper_unchanged:true,test_source_unchanged:true,
        measured_essential_px:visible.map(text=>text.font_css_px),
        accessibility_tree_available:report.views[0].accessibility_tree.available,
        observed_svg_names:report.views[0].svg_names.filter(svg=>svg.visible&&!svg.decorative&&svg.requires_name)
          .map(svg=>({declared:svg.resolved_name,observed:svg.ax_name,exposed:svg.ax_exposed})),
        table_cell_overflow_count:visible.filter(text=>text.exceeds_table_cell).length});
    }catch(error){
      results.push({id:test.id,passed:false,error:error.message});
    }
  }
}finally{
  // Every helper subprocess has exited and closed its browser before cleanup.
  await cleanScratch();
}
const passed=results.every(result=>result.passed);
assert.deepEqual(await fs.readFile(helper),helperBefore,'The helper changed during controls.');
assert.deepEqual(await fs.readFile(testSource),testBefore,'The test source changed during controls.');
console.log(JSON.stringify({schema:'browser-export-regression.v1',passed,helper_sha256:sha(helperBefore),test_sha256:sha(testBefore),cases:results,scratch_removed:true}));
if(!passed)process.exitCode=1;
