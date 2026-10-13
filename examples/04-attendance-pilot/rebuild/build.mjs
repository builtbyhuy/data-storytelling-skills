import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile,Workbook,SpreadsheetFile} from '@oai/artifact-tool';

const arg=(k,d)=>{const i=process.argv.indexOf('--'+k);return i<0?d:process.argv[i+1]};
const build=path.resolve(arg('build-dir','build'));
const out=path.resolve(arg('output-dir','outputs'));
const skill=path.resolve(arg('presentation-skill',''));
const python=arg('python-exe','');
await fs.mkdir(build,{recursive:true});await fs.mkdir(out,{recursive:true});
const f=JSON.parse(await fs.readFile(path.join(build,'facts.json'),'utf8'));
if(f.periods.join(',')!=='202425,202526')throw new Error('New periods require source, method, labels and narrative review before building.');
const P='State-funded primary',S='State-funded secondary';
const vn=x=>x.toLocaleString('vi-VN');
const pct=x=>(x*100).toFixed(2).replace('.',',')+'%';
const pp=x=>(x>=0?'+':'')+(x*100).toFixed(2).replace('.',',');
const nat=(phase,t)=>f.national.find(r=>r.phase===phase&&r.period===t);
const shortNames=['Knowsley','North East Lincolnshire','Blackburn with Darwen'];
const selected=shortNames.map(name=>f.local.find(r=>r.phase===S&&r.name===name));
const sec=f.local.filter(r=>r.phase===S);
const rank=(r,metric)=>1+sec.filter(x=>(metric==='rise'?x.delta.pa:x.new.pa)>(metric==='rise'?r.delta.pa:r.new.pa)).length;
if(rank(selected[0],'level')!==1||rank(selected[1],'level')!==2||rank(selected[2],'rise')!==1)throw new Error('The source revision changed the selection evidence. Review and update the narrative before building.');
const source='Nguồn: DfE, Autumn term 2025/26. Công bố 6/8/2026, bản tải 13/10/2026. Phép tính từ toàn bộ phạm vi hai nhóm trường.';
const sourceURL='https://explore-education-statistics.service.gov.uk/data-catalogue/data-set/407a4c0a-260f-4bd0-8b6d-0f49febb207c';
const methodology='https://explore-education-statistics.service.gov.uk/methodology/pupil-absence-statistics-methodology';
const presentation=Presentation.create({slideSize:{width:1280,height:720}});
presentation.theme.defaultFont='Arial';
const ink='#162B35',muted='#485F68',accent='#1B6273',old='#788991',paper='#FFFFFF';
let notes=[];
function txt(s,text,x,y,w,h,size=28,color=ink,bold=false){
  const sh=s.shapes.add({geometry:'textbox',name:text.slice(0,55),position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  sh.text=text;sh.text.style={fontSize:size,typeface:'Arial',color,bold,wrap:'square',autoFit:'none',insets:0};return sh;
}
function slide(title,note=''){
  const s=presentation.slides.add();s.background.fill=paper;
  txt(s,title,64,44,1152,110,44,ink,true);
  const index=presentation.slides.items.length;
  txt(s,String(index).padStart(2,'0'),1180,676,34,22,18,muted);
  notes.push({slide:index,text:note});s.speakerNotes.text=note+'\n'+source+'\n'+sourceURL+'\n'+methodology;return s;
}
function foot(s,text){txt(s,text,64,630,1120,44,21,muted);}
const chartFont={fontSize:24,fill:ink};
function bar(s,cats,series,where,max,fmt='0.00%'){
 const c=s.charts.add('bar',{position:where,categories:cats,series:series.map((a,i)=>({name:a.name,values:a.values.map(v=>Number(v.toFixed(6))),fill:i===0?old:accent,valuesFormatCode:fmt})),hasLegend:true,legend:{position:'bottom',textStyle:chartFont},barOptions:{direction:'column',grouping:'clustered',gapWidth:130},xAxis:{textStyle:chartFont,majorGridlines:null,line:{fill:'#CAD3D6',width:1}},yAxis:{min:0,max,numberFormatCode:fmt,majorGridlines:{fill:'#DFE6E8',width:1},textStyle:chartFont},dataLabels:{showValue:true,position:'outEnd',numberFormatCode:fmt,numberFormatSourceLinked:false,textStyle:{fontSize:25,fill:ink,bold:true}},chartFill:'none',plotAreaFill:'none'});
 return c;
}
function table(s,values,x,y,w,h,widths,font=25){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,columnWidths:widths,values});
 t.styleOptions={headerRow:false,bandedRows:false};
 t.cells.block({row:0,column:0,rowCount:values.length,columnCount:values[0].length}).assign({fill:paper,textStyle:{fontSize:font,typeface:'Arial',color:ink},margins:{left:12,right:12,top:10,bottom:10}});
 for(let r=0;r<values.length;r++){t.rows[r].height=h/values.length;for(let c=0;c<values[0].length;c++){let cell=t.getCell(r,c);cell.text.style={fontSize:font,typeface:'Arial',color:r===0?paper:ink,bold:r===0};if(r===0)cell.fill=ink;}}
 t.borders.assign({fill:'#DDE4E7',width:0.5});return t;
}

{
 const s=presentation.slides.add();s.background.fill=ink;
 txt(s,'Thử nghiệm chuyên cần\ncó điều kiện',64,94,1110,190,58,paper,true);
 txt(s,'Ưu tiên tìm đối tác ở ba địa bàn.\nChỉ mở một nhóm khi đủ điều kiện tại địa phương.',64,335,1070,130,34,paper);
 txt(s,'Đề xuất cho một học kỳ tại England\nDữ liệu DfE thật. Bối cảnh và giới hạn dịch vụ là giả lập.',64,557,1110,74,24,'#D2E0E5');
 s.speakerNotes.text='Quyết định đề xuất: chưa mở triển khai hôm nay. Cho phép nhóm hợp tác chuẩn bị hồ sơ khả thi ở tối đa ba địa bàn. Nếu đủ điều kiện, mở một nhóm tại một địa bàn với trần 70.000 GBP. Đây là đề xuất chưa được duyệt hoặc thực hiện.\n'+source+'\n'+sourceURL;
 notes.push({slide:1,text:s.speakerNotes.text});
}
{
 const s=slide('Vắng thường xuyên cao hơn ở trung học',`Tỷ lệ PA dùng enrolments, không dùng possible sessions. Primary: ${pct(nat(P,'202425').pa)} và ${pct(nat(P,'202526').pa)}. Secondary: ${pct(nat(S,'202425').pa)} và ${pct(nat(S,'202526').pa)}. ${f.summary[S].pa_rise}/152 địa bàn secondary có tỷ lệ tăng. Toàn bộ 304 cặp địa bàn-nhóm trường khớp qua hai kỳ.`);
 txt(s,'Lượt ghi danh vắng ≥10% số buổi của lượt đó / tổng lượt ghi danh',64,152,1150,50,26,muted);
 bar(s,['Tiểu học','Trung học'],[{name:'Thu 2024/25',values:[nat(P,'202425').pa,nat(S,'202425').pa]},{name:'Thu 2025/26',values:[nat(P,'202526').pa,nat(S,'202526').pa]}],{left:64,top:220,width:770,height:376},0.26);
 txt(s,`${f.summary[S].pa_rise}/152`,914,229,288,82,58,accent,true);
 txt(s,'địa bàn trung học\ncó tỷ lệ tăng',914,319,286,93,29);
 txt(s,'Ưu tiên kiểm tra nhu cầu\nhỗ trợ tại trung học.',914,459,286,100,27);
 foot(s,'England, trường nhà nước tài trợ. Lượt ghi danh có thể lặp khi trẻ chuyển trường. Nguồn: DfE, bản tải 13/10/2026.');
}
{
 const s=slide('Mức vắng nặng cho tín hiệu khác',`Severe absence ≥50% possible sessions theo enrolment, là tập con của PA. Primary ${pct(nat(P,'202425').severe)} sang ${pct(nat(P,'202526').severe)}. Secondary ${pct(nat(S,'202425').severe)} sang ${pct(nat(S,'202526').severe)}. Số địa bàn có tỷ lệ severe tăng: primary ${f.summary[P].severe_rise}/152, secondary ${f.summary[S].severe_rise}/152. Không dùng hai số PA và severe cộng làm caseload.`);
 bar(s,['Tiểu học','Trung học'],[{name:'Thu 2024/25',values:[nat(P,'202425').severe,nat(S,'202425').severe]},{name:'Thu 2025/26',values:[nat(P,'202526').severe,nat(S,'202526').severe]}],{left:64,top:215,width:770,height:373},0.04);
 txt(s,'Lượt ghi danh vắng ≥50% số buổi / tổng lượt ghi danh',64,152,1150,45,26,muted);
 txt(s,`${f.summary[P].severe_rise}/152 địa bàn\ntiểu học tăng mức vắng nặng`,908,229,301,103,30,accent,true);
 txt(s,'Tiểu học vẫn đáng theo dõi.\nGói đầu tiên cần giới hạn nhu cầu mà đội có khả năng xử lý và có tuyến chuyển tiếp.',908,371,301,194,27);
 foot(s,'Hai học kỳ là tín hiệu chỉ báo. Độ dài kỳ, lượt ghi danh và số buổi có thể khác nhau. Nguồn: DfE, phương pháp mục 1.8.');
}
{
 const s=slide('Ba địa bàn ưu tiên tìm đối tác',selected.map(r=>`${r.name}: PA ${pct(r.old.pa)} sang ${pct(r.new.pa)}, thay đổi ${pp(r.delta.pa)} điểm phần trăm. Rank PA hiện tại ${rank(r,'level')}/152, rank tăng ${rank(r,'rise')}/152. Severe hiện tại ${pct(r.new.severe)}. PA 10 đến dưới50% ${vn(r.new.pa_less_severe)} lượt ghi danh.`).join('\n'));
 txt(s,'Trung học, tỷ lệ lượt ghi danh vắng ≥10%. Lựa chọn theo mức cao và mức tăng trên toàn bộ 152 địa bàn.',64,154,1140,66,25,muted);
 bar(s,shortNames,[{name:'Thu 2024/25',values:selected.map(r=>r.old.pa)},{name:'Thu 2025/26',values:selected.map(r=>r.new.pa)}],{left:64,top:237,width:1146,height:278},0.38);
 txt(s,'PA cao nhất\n'+pp(selected[0].delta.pa)+' điểm phần trăm',91,529,350,81,25,accent,true);
 txt(s,'PA cao thứ hai\n'+pp(selected[1].delta.pa)+' điểm phần trăm',487,529,350,81,25,accent,true);
 txt(s,'PA tăng nhanh nhất\n'+pp(selected[2].delta.pa)+' điểm phần trăm',883,529,330,81,25,accent,true);
 foot(s,'Tìm đối tác theo danh sách này, sau đó chọn địa bàn đạt điều kiện trước. Tỷ lệ cao chưa xác nhận gia đình sẵn sàng tham gia.');
}
{
 const s=slide('Lý do vắng gợi ý câu hỏi cần kiểm chứng',selected.map(r=>`${r.name}: illness ${pct(r.new.illness)} possible sessions, other unauthorised ${pct(r.new.other_unauthorised)} possible sessions, severe ${pct(r.new.severe)}, 10 đến dưới50% ${vn(r.new.pa_less_severe)} enrolments, ${r.new.num_schools} source schools.`).join('\n')+'\nKý hiệu do trường ghi không chứng minh nguyên nhân của một gia đình hoặc hiệu quả dịch vụ.');
 txt(s,'Thu 2025/26, trung học. Tỷ lệ lý do tính trên số buổi có thể tham dự, mỗi buổi là nửa ngày.',64,152,1140,62,25,muted);
 table(s,[['Địa bàn','Ốm có phép','Không phép khác','Vắng ≥50%'],...selected.map(r=>[r.name,pct(r.new.illness),pct(r.new.other_unauthorised),pct(r.new.severe)]),['England',pct(nat(S,'202526').illness),pct(nat(S,'202526').other_unauthorised),pct(nat(S,'202526').severe)]],64,246,1146,239,[490,210,245,201],25);
 txt(s,'Knowsley: kiểm tra trở ngại đi học và giao tiếp với gia đình.\nHai địa bàn còn lại: kiểm tra cả nhu cầu sức khỏe và tuyến hỗ trợ phù hợp.',64,512,1140,90,28);
 foot(s,'Mã lý do là ghi nhận của trường. Cột vắng ≥50% dùng tổng lượt ghi danh làm mẫu số. Chưa biết nguyên nhân hay khả năng nhận hỗ trợ.');
}
{
 const s=slide('Một nhóm giữ lại nguồn lực cho quyết định sau','Giới hạn giả lập từ brief: 12 nhân sự, mỗi nhóm4, 15 gia đình đồng thời/nhân sự,4 trường tối đa/địa bàn,70.000GBP tối đa/địa bàn,210.000GBP toàn bộ. Trần1nhóm=4*15=60 gia đình đang hỗ trợ đồng thời. Ba nhóm=180. Không suy ra số gia đình cả học kỳ hoặc hiệu quả. Các enrolments10-<50% hiện tại ở3địa bàn được chọn là1665,2292,2332 nhưng không phải danh sáchgia đình.');
 table(s,[['Phạm vi giả lập','Nhân sự','Gia đình đồng thời tối đa','Trần GBP'],['Chưa mở','0','0','0'],['Một địa bàn','4','60','70.000'],['Ba địa bàn','12','180','210.000']],64,189,1146,219,[360,170,360,256],27);
 txt(s,'Đề xuất một nhóm tại một địa bàn trong một học kỳ.\nGiữ 8 nhân sự và 140.000 GBP chưa phân bổ.',64,445,1130,98,33,accent,true);
 txt(s,'Gói ban đầu: hỗ trợ gia đình có trẻ trung học vắng 10% đến dưới 50%, sau xác minh từng trẻ và nhu cầu. Có chuyển tiếp khi cần chuyên môn khác.',64,560,1140,63,26);
 foot(s,'Đây là trần lập kế hoạch, chưa phải chi phí đã chi hoặc số người đủ điều kiện. Giới hạn 60 là đồng thời, không phải tổng học kỳ.');
}
{
 const s=slide('Triển khai còn phụ thuộc bằng chứng địa phương','Tất cả các điều kiện là chưa xác minh theo brief. Vai trò kiểm tra đề xuất. Giám đốc dịch vụ duyệt launch khi hồ sơ hoàn tất. Thiếu bất kỳ điều kiện nào thì hoãn hoặc sửa phạm vi. Nhân sự4, điều kiện đi lại/làmviệc, quyền truy cập dữ liệu và thời gian đối tác phải xác nhận cho học kỳ. Không thể coi trần tài nguyên là xác nhận đã phân công.');
 txt(s,'Hiện chưa địa bàn nào có đủ điều kiện đã xác minh. Mỗi dòng cần bằng chứng hoàn tất trước khi duyệt mở.',64,152,1140,70,28,accent,true);
 table(s,[['Điều kiện cần hoàn tất','Người kiểm tra đề xuất'],['Trường đúng nhóm, tối đa 4, cam kết thời gian','Trưởng nhóm hợp tác trường'],['Đầu mối địa phương, tiếp nhận và bảo vệ trẻ em','Giám đốc dịch vụ'],['4 nhân sự sẵn sàng, đi lại, công cụ và ngân sách ≤70.000 GBP','Quản lý ngân sách và giám đốc'],['Gia đình đồng ý, danh sách đã khử trùng lặp, nhu cầu phù hợp','Trưởng nhóm hỗ trợ'],['Định nghĩa đo, dữ liệu trước/sau và nhóm so sánh phù hợp','Người phụ trách đo lường']],64,250,1146,309,[773,373],25);
 txt(s,'Thiếu bằng chứng thì hoãn. Có thể chọn địa bàn khác trong ba địa bàn hoặc giảm phạm vi.',64,614,1140,57,27);
}
{
 const s=slide('Kết quả học kỳ quyết định việc mở rộng','Thiết kế đo đề xuất, chưa phê duyệt: đóng intake cuối tuần2 sau khởi động. Baseline4tuần học trước nhận hỗ trợ và6tuần theo dõi mỗi trẻ. Cần trường xác nhận dữ liệu đủ và khả năng theo dõi nằm trong học kỳ, nếu không giảm intake hoặc hoãn. Outcome overall absence sessions/possible sessions của cohort toàn bộtrẻ đã nhận, so sánh cùng6tuần của nhómtrẻ tương tự ở trường phù hợp nếu có. Theo dõi mất dữ liệu, thời gian nhân sự, harm, referrals và ngân sách. Không dùng before/after tuyên bố nhânquả. Giám đốc với phụtrách đo chốt mức giảm tối thiểu có ý nghĩa trước launch. Không mở thêm nếu thiếu evidence mature, vượtbudget/capacity hoặc safety unresolved.');
 txt(s,'Cách đo đề xuất',64,161,415,48,30,accent,true);
 txt(s,'4 tuần học trước hỗ trợ và 6 tuần theo dõi. Đóng tiếp nhận cuối tuần 2 để mọi trẻ có đủ thời gian trong học kỳ.',64,218,513,145,28);
 txt(s,'Tỷ lệ buổi vắng = tổng buổi vắng / tổng buổi có thể tham dự của toàn bộ trẻ nhận hỗ trợ. Giữ rõ dữ liệu thiếu và đối chiếu nhóm tương tự nếu khả thi.',64,382,513,183,28);
 txt(s,'Quy tắc quyết định đề xuất',661,161,548,48,30,accent,true);
 txt(s,'Hằng tuần: dừng tiếp nhận ở trần 60 gia đình hoặc 15/người. Dừng khi chạm trần chi hoặc có rủi ro bảo vệ trẻ em chưa xử lý.',661,218,548,143,28);
 txt(s,'Cuối kỳ, sau khi trường xác nhận dữ liệu: chỉ đề xuất mở rộng khi đạt mức giảm tối thiểu đã chốt trước, nguồn lực phù hợp và không có vấn đề an toàn tồn đọng.',661,382,548,183,28);
 foot(s,'Giám đốc duyệt tiêu chí trước khi mở. Thiếu dữ liệu trưởng thành thì chưa kết luận. So sánh trước/sau chưa chứng minh tác động nhân quả.');
}
{
 const s=slide('Phạm vi nguồn và cách cập nhật','Nguồn cố định được bàn giao trong source/raw. 153LA,304phasepairs,608rowstwo autumns. Mỗi phase152records kỳ. Isles of Scilly absentprimary, City ofLondon absentsecondary không thêm0. NationalTotal chứaspecial không dùng. Tất cảheadline/tablescalculated từ counts và matching denominator. NativeWorkbookphasescope nguyên bản. Cần review DfErevision,status,mãLA,phase,definitions trước đổiperiod. Phương pháptermly indicative length variation. Contains public sector information licensed under OGLv3.0.');
 txt(s,'Toàn bộ 153 địa bàn, 304 cặp địa bàn và nhóm trường, 608 dòng cho hai học kỳ thu. Chỉ primary và secondary được nhà nước tài trợ. Chỉ tiêu áp dụng tuổi 5 đến 15 theo nguồn.',64,159,1140,105,28);
 txt(s,'Vắng thường xuyên ≥10% và vắng nặng ≥50% dùng lượt ghi danh. Tỷ lệ buổi vắng và lý do dùng số buổi có thể tham dự. Tỷ lệ tổng hợp = tổng tử số / tổng mẫu số.',64,277,1140,111,28);
 txt(s,'Isles of Scilly thiếu dòng primary. City of London thiếu dòng secondary. Giữ trạng thái không có dòng, không thêm số 0. Không dùng dòng Total có special.',64,418,1140,83,27);
 txt(s,'Khi DfE sửa dữ liệu hoặc đổi kỳ: kiểm tra snapshot, mã địa bàn, nhóm trường, mẫu số, định nghĩa và mã lý do. Chạy lại tổng hợp, xem lại đề xuất và xuất lại cả ba tệp.',64,531,1140,80,27);
 foot(s,'DfE, công bố 6/8/2026, bản tải 13/10/2026. Dữ liệu học kỳ là chỉ báo. Contains public sector information licensed under OGL v3.0.');
}

const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
for(const s of presentation.slides.items)for(const c of s.charts.items)applyPresentationChartFont(c,{fontFamily:'Arial'});
const candidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(presentation)).save(candidate);
const final=path.join(out,'thu-nghiem-chuyen-can.pptx');
await finalizePresentation({workspaceDir:path.resolve(out,'..'),candidatePath:candidate,finalPath:final,pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...[5,6,7].flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:9,requiredNativeTableOwnerSlides:[5,6,7],requiredNativeChartOwnerSlides:[2,3,4],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath:path.join(build,'pptx-validation.json')});

const wb=Workbook.create();const main=wb.worksheets.add('Tong hop'),la=wb.worksheets.add('Dia ban'),input=wb.worksheets.add('Nguon');
for(const sh of [main,la,input]){sh.showGridLines=false;sh.getRange('A1:U330').format.font={name:'Arial',size:11,color:ink};sh.getRange('A1:U330').format.verticalAlignment='center';}
main.tabColor=ink;
function cell(sh,r,c,v,formula=false){const range=sh.getCell(r-1,c-1);if(formula)range.formulas=[[v]];else range.values=[[v]];}
function row(sh,r,values){sh.getRangeByIndexes(r-1,0,1,values.length).values=[values];}
function header(sh,r,values){row(sh,r,values);sh.getRangeByIndexes(r-1,0,1,values.length).format={fill:ink,font:{name:'Arial',size:11,bold:true,color:paper},horizontalAlignment:'center',rowHeight:34,wrapText:true};}
function title(sh,t){cell(sh,2,1,t);sh.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:ink};sh.getRange('A2:K2').format.borders={bottom:{style:'thin',color:ink}};}
title(main,'Chuyên cần và phạm vi thử nghiệm có điều kiện');
cell(main,3,1,'England. Thu 2024/25 so với thu 2025/26. Phạm vi primary và secondary. Đề xuất chưa triển khai.');
main.getRange('A3:L3').format.font={name:'Arial',size:11,italic:true,color:muted};
title(input,'Đầu vào đã tổng hợp từ nguồn DfE');
cell(input,3,1,'Nguồn: Department for Education, Autumn term 2025/26, công bố 6/8/2026, bản tải 13/10/2026. OGL v3.0.');
cell(input,4,1,sourceURL);cell(input,5,1,'304 cặp địa bàn–nhóm trường, ghép bằng mã mới. Số đếm giữ nguyên. Ký hiệu không có dòng được giữ ngoài bảng, không thay bằng 0.');
const hdr=['Mã LA','Nhóm nguồn','Địa bàn','Ghi danh 24/25','Ghi danh 25/26','PA 24/25','PA 25/26','SV 24/25','SV 25/26','Buổi có thể 24/25','Buổi có thể 25/26','Vắng 24/25','Vắng 25/26','Ốm 25/26','Không phép khác 25/26','Trường 25/26'];header(input,7,hdr);
const records=f.local.map(r=>[r.code,r.phase,r.name,r.old.enrolments,r.new.enrolments,r.old.enrolments_pa_10_exact,r.new.enrolments_pa_10_exact,r.old.enrolments_pa_50_exact,r.new.enrolments_pa_50_exact,r.old.sess_possible,r.new.sess_possible,r.old.sess_overall,r.new.sess_overall,r.new.sess_auth_illness,r.new.sess_unauth_other,r.new.num_schools]);
input.getRange(`A8:P${7+records.length}`).values=records;input.getRange(`D8:P${7+records.length}`).setNumberFormat('#,##0');input.freezePanes.freezeRows(7);input.freezePanes.freezeColumns(3);
title(la,'Tín hiệu tại toàn bộ địa bàn và hai nhóm trường');
cell(la,3,1,'PA ≥10% và SV ≥50% là tỷ lệ lượt ghi danh. Delta dùng điểm phần trăm. Lý do vắng dùng số buổi có thể tham dự.');
cell(la,4,1,'PA gồm SV. Cột 10–<50% = PA trừ SV, vẫn là lượt ghi danh, chưa phải trẻ hay gia đình duy nhất.');
header(la,6,['Mã LA','Nhóm','Địa bàn','PA 24/25','PA 25/26','Δ PA điểm %','SV 24/25','SV 25/26','Δ SV điểm %','PA 10–<50% 25/26','Ốm 25/26','Không phép khác 25/26']);
for(let i=0;i<f.local.length;i++){const r=i+7,s=i+8;row(la,r,[f.local[i].code,f.local[i].phase===P?'Tiểu học':'Trung học',f.local[i].name]);for(const[c,v]of [[4,`=Nguon!F${s}/Nguon!D${s}`],[5,`=Nguon!G${s}/Nguon!E${s}`],[6,`=(E${r}-D${r})*100`],[7,`=Nguon!H${s}/Nguon!D${s}`],[8,`=Nguon!I${s}/Nguon!E${s}`],[9,`=(H${r}-G${r})*100`],[10,`=Nguon!G${s}-Nguon!I${s}`],[11,`=Nguon!N${s}/Nguon!K${s}`],[12,`=Nguon!O${s}/Nguon!K${s}`]])cell(la,r,c,v,true);}
for(const col of ['D','E','G','H','K','L'])la.getRange(`${col}7:${col}310`).setNumberFormat('0.00%');for(const col of ['F','I'])la.getRange(`${col}7:${col}310`).setNumberFormat('+0.00;-0.00;0.00');la.getRange('J7:J310').setNumberFormat('#,##0');la.freezePanes.freezeRows(6);la.freezePanes.freezeColumns(3);
header(main,6,['Nhóm','Ghi danh 24/25','Ghi danh 25/26','PA 24/25','PA 25/26','Δ PA điểm %','SV 24/25','SV 25/26','Δ SV điểm %']);
const last=311;
for(let i=0;i<2;i++){let r=7+i,phase=[P,S][i];cell(main,r,1,i===0?'Tiểu học':'Trung học');for(const[c,sourceCol]of[[2,'D'],[3,'E']])cell(main,r,c,`=SUMIFS(Nguon!$${sourceCol}$8:$${sourceCol}$${last},Nguon!$B$8:$B$${last},"${phase}")`,true);for(const[c,col,den]of[[4,'F','B'],[5,'G','C'],[7,'H','B'],[8,'I','C']])cell(main,r,c,`=SUMIFS(Nguon!$${col}$8:$${col}$${last},Nguon!$B$8:$B$${last},"${phase}")/${den}${r}`,true);cell(main,r,6,`=(E${r}-D${r})*100`,true);cell(main,r,9,`=(H${r}-G${r})*100`,true);}
main.getRange('B7:C8').setNumberFormat('#,##0');for(const c of ['D','E','G','H'])main.getRange(`${c}7:${c}8`).setNumberFormat('0.00%');for(const c of['F','I'])main.getRange(`${c}7:${c}8`).setNumberFormat('+0.00;-0.00;0.00');
cell(main,10,1,'PA = lượt ghi danh vắng ≥10% / tổng lượt ghi danh. SV = vắng ≥50%, nằm trong PA.');
header(main,12,['Nhóm','Số địa bàn','PA tăng','SV tăng']);
for(let i=0;i<2;i++){let r=13+i,g=i===0?'Tiểu học':'Trung học';cell(main,r,1,g);cell(main,r,2,`=COUNTIFS('Dia ban'!$B$7:$B$310,A${r})`,true);cell(main,r,3,`=COUNTIFS('Dia ban'!$B$7:$B$310,A${r},'Dia ban'!$F$7:$F$310,">0")`,true);cell(main,r,4,`=COUNTIFS('Dia ban'!$B$7:$B$310,A${r},'Dia ban'!$I$7:$I$310,">0")`,true);}
header(main,17,['Địa bàn trung học','PA 24/25','PA 25/26','Δ PA điểm %','SV 25/26','10–<50% ghi danh','Ốm / buổi','Không phép khác / buổi','Trường nguồn']);
for(let i=0;i<selected.length;i++){let r=i+18,idx=f.local.indexOf(selected[i]),d=idx+7,n=idx+8;cell(main,r,1,selected[i].name);for(const[c,col]of[[2,'D'],[3,'E'],[4,'F'],[5,'H'],[6,'J'],[7,'K'],[8,'L']])cell(main,r,c,`='Dia ban'!${col}${d}`,true);cell(main,r,9,`=Nguon!P${n}`,true);}
cell(main,21,1,'England');for(const[c,col]of[[2,'D'],[3,'E'],[4,'F'],[5,'H']])cell(main,21,c,`=${col}8`,true);
cell(main,21,6,`=SUMIFS(Nguon!$G$8:$G$${last},Nguon!$B$8:$B$${last},"${S}")-SUMIFS(Nguon!$I$8:$I$${last},Nguon!$B$8:$B$${last},"${S}")`,true);
for(const[c,col]of[[7,'N'],[8,'O']])cell(main,21,c,`=SUMIFS(Nguon!$${col}$8:$${col}$${last},Nguon!$B$8:$B$${last},"${S}")/SUMIFS(Nguon!$K$8:$K$${last},Nguon!$B$8:$B$${last},"${S}")`,true);
cell(main,21,9,`=SUMIFS(Nguon!$P$8:$P$${last},Nguon!$B$8:$B$${last},"${S}")`,true);
for(const c of ['B','C','E','G','H'])main.getRange(`${c}18:${c}21`).setNumberFormat('0.00%');main.getRange('D18:D21').setNumberFormat('+0.00;-0.00;0.00');main.getRange('F18:F21').setNumberFormat('#,##0');
cell(main,22,1,'Chọn: PA cao nhất, cao thứ hai kèm tăng mạnh, và PA tăng nhanh nhất trong 152 địa bàn trung học.');
cell(main,23,1,'Ưu tiên tìm đối tác. Chỉ số nguồn và số trường nguồn chưa xác nhận khả năng hợp tác hoặc gia đình sẵn sàng.');
header(main,26,['Giới hạn giả lập','Giá trị','Đơn vị']);
const assumptions=[['Tổng nhân sự',12,'người'],['Nhân sự mỗi nhóm',4,'người'],['Gia đình đồng thời / nhân sự',15,'gia đình'],['Trường tối đa / địa bàn',4,'trường'],['Trần mỗi địa bàn',70000,'GBP'],['Ngân sách toàn bộ',210000,'GBP']];main.getRange('A27:C32').values=assumptions;main.getRange('B27:B32').format.fill='#FFF0CB';main.getRange('B27:B32').setNumberFormat('#,##0');
header(main,35,['Số nhóm giả lập','Nhân sự','Gia đình đồng thời tối đa','Trần chi GBP','Nhân sự còn lại','GBP chưa phân bổ']);
for(let i=0;i<3;i++){let r=36+i;cell(main,r,1,[0,1,3][i]);cell(main,r,2,`=A${r}*$B$28`,true);cell(main,r,3,`=B${r}*$B$29`,true);cell(main,r,4,`=A${r}*$B$31`,true);cell(main,r,5,`=$B$27-B${r}`,true);cell(main,r,6,`=$B$32-D${r}`,true);}main.getRange('B36:F38').setNumberFormat('#,##0');
cell(main,40,1,'Đề xuất: một nhóm tại một địa bàn sau khi đủ điều kiện. Cột gia đình là trần đồng thời, không phải tổng học kỳ.');
cell(main,42,1,'Cập nhật: xem README.md. Phải kiểm tra mã địa bàn, kỳ, định nghĩa và trạng thái nguồn trước khi chạy lại.');
cell(main,43,1,'Dữ liệu học kỳ chỉ là chỉ báo. Chưa xác minh đối tác, nhân sự được phân công, chi phí địa phương hoặc hiệu quả can thiệp.');
for(const sh of[main,la,input]){sh.getRange('A1:A330').format.columnWidth=24;sh.getRange('B1:B330').format.columnWidth=23;sh.getRange('C1:C330').format.columnWidth=31;sh.getRange('D1:P330').format.columnWidth=17;sh.getRange('A7:P330').format.rowHeight=26;}
main.getRange('A1:A45').format.columnWidth=34;main.getRange('B1:I45').format.columnWidth=19;main.getRange('A6:I6').format.rowHeight=40;main.getRange('A17:I17').format.rowHeight=42;main.getRange('A35:F35').format.rowHeight=43;main.getRange('A35:A38').format.columnWidth=34;
input.getRange('A7:P7').format.rowHeight=48;la.getRange('A6:L6').format.rowHeight=44;
wb.recalculate();
const mainInspect=await wb.inspect({kind:'table',range:'Tong hop!A6:I20',include:'values,formulas',tableMaxRows:15,tableMaxCols:9,maxChars:10000});
await fs.writeFile(path.join(build,'xlsx-inspection.ndjson'),mainInspect.ndjson);
const err=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},maxChars:3000});await fs.writeFile(path.join(build,'xlsx-errors.ndjson'),err.ndjson);
for(const[sh,range]of[[main,'A1:I23'],[main,'A25:I43'],[la,'A1:L15'],[input,'A1:P16']]){let name=sh.name+'-'+range.split(':')[0];const png=await wb.render({sheetName:sh.name,range,scale:1.5,format:'png'});await fs.writeFile(path.join(build,name+'.png'),new Uint8Array(await png.arrayBuffer()));}
await(await SpreadsheetFile.exportXlsx(wb)).save(path.join(out,'tong-hop-chuyen-can.xlsx'));
await fs.writeFile(path.join(build,'claim-record.json'),JSON.stringify({selected:selected.map(r=>({code:r.code,name:r.name,pa:r.new.pa,pa_delta:r.delta.pa,rank_level:rank(r,'level'),rank_rise:rank(r,'rise')})),source_sha256:f.checks.raw_sha256,chosen_action:'Proposal only: defer launch now, prepare partner evidence in three named authorities, one group at first qualifying authority',notes},null,2));
console.log(JSON.stringify({pptx:final,xlsx:path.join(out,'tong-hop-chuyen-can.xlsx'),slides:presentation.slides.items.length,selected:selected.map(r=>r.name)}));
