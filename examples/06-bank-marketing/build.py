"""Build an offline decision report from the frozen source; paths are arguments."""
from pathlib import Path
import argparse, json, html, shutil
from calculate import calculate

def number(n): return f'{n:,}'.replace(',','.')
def pct(n, d=1): return f'{n:.{d}f}'.replace('.',',')+'%'
def text(s): return html.escape(str(s))

def svg_chart(rows, prefix, title, desc, maximum, baseline, mobile=False):
    width=340 if mobile else 940
    left=18 if mobile else 245; right=65 if mobile else 105
    top=58 if mobile else 52; gap=100 if mobile else 66
    height=top+gap*len(rows)+58
    plot=width-left-right
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="{prefix}-title {prefix}-desc"><title id="{prefix}-title">{text(title)}</title><desc id="{prefix}-desc">{text(desc)}</desc><style>text{{font-family:Segoe UI,Arial,sans-serif;fill:#243c45;font-size:{17 if mobile else 23}px}}.small{{font-size:{15 if mobile else 19}px;fill:#546870}}.tick{{font-size:{15 if mobile else 19}px;fill:#546870}}</style>']
    for tick in range(0,maximum+1,10 if maximum>20 else 5):
        x=left+tick/maximum*plot
        out += [f'<line x1="{x}" x2="{x}" y1="{top-16}" y2="{height-58}" stroke="#d7e0e1"/>',f'<text class="tick" x="{x}" y="{height-27}" text-anchor="middle">{tick}%</text>']
    bx=left+baseline/maximum*plot
    out.append(f'<line x1="{bx}" x2="{bx}" y1="{top-16}" y2="{height-58}" stroke="#546870" stroke-width="2" stroke-dasharray="5 5"/>')
    for i,r in enumerate(rows):
        y=top+i*gap
        col='#006b61' if i==0 else '#5e7985'
        if mobile:
            out.append(f'<rect x="16" y="{y-24}" width="{width-24}" height="25" fill="#fffdf9"/>')
            out.append(f'<text x="18" y="{y-4}">{text(r["label"])}</text>'); by=y+8
        else:
            out.append(f'<text x="{left-22}" y="{y+17}" text-anchor="end">{text(r["label"])}</text>');by=y
        bar=r['rate_pct']/maximum*plot
        out.append(f'<rect x="{left}" y="{by}" width="{bar}" height="{24 if mobile else 27}" rx="2" fill="{col}"/>')
        out.append(f'<text x="{left+bar+9}" y="{by+20}" font-weight="650">{pct(r["rate_pct"])}</text>')
        out.append(f'<rect x="{left-2}" y="{by+31}" width="{plot+right-6}" height="25" fill="#fffdf9"/>')
        out.append(f'<text class="small" x="{left}" y="{by+48}">{number(r["yes"])} yes / {number(r["records"])} hồ sơ</text>')
    out.append('</svg>');return ''.join(out)

def table(rows, caption, head='Nhóm kết quả trước', identifier='lookup'):
    h=f'<div class="table-scroll" role="region" aria-label="{text(caption)} - cuộn ngang nếu cần" tabindex="0"><table id="{identifier}" style="table-layout:fixed"><caption>{text(caption)}</caption><colgroup><col style="width:180px"><col style="width:110px"><col style="width:110px"><col style="width:110px"><col style="width:110px"></colgroup><thead><tr><th scope="col">{head}</th><th scope="col">Hồ sơ (n)</th><th scope="col">y = yes</th><th scope="col">y = no</th><th scope="col">Tỷ lệ yes</th></tr></thead><tbody>'
    for r in rows:
        h+=f'<tr data-key="{text(r["key"])}"><th scope="row">{text(r["label"])}</th><td>{number(r["records"])}</td><td>{number(r["yes"])}</td><td>{number(r["no"])}</td><td>{pct(r["rate_pct"],2)}</td></tr>'
    return h+'</tbody></table></div>'

def build(source,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    e=calculate(source,out/'evidence');(out/'charts').mkdir(exist_ok=True)
    h=e['history'];a=e['attempts'];base=e['rate_pct']
    charts={}
    specs=[('history',h,'Tỷ lệ đăng ký theo kết quả chiến dịch trước','Nhóm thành công trước: 978 trên 1.511 hồ sơ, 64,7%; không rõ kết quả: 3.386 trên 36.959, 9,2%. Tỷ lệ chung 11,7%. Đây là liên hệ lịch sử, không phải tác động của việc ưu tiên danh sách.',70),('attempts',a,'Tỷ lệ đăng ký theo số lần liên lạc trong chiến dịch','1 lần: 14,6%; 2 đến 3 lần: 11,2%; 4 đến 6 lần: 8,3%; từ 7 lần: 5,3%. Không thể suy ra gọi thêm làm giảm đăng ký vì số lần được ghi khi chiến dịch đã diễn ra.',20)]
    for k,rows,title,desc,maxv in specs:
        for mobile in [False,True]:
            suffix='phone' if mobile else 'desktop';svg=svg_chart(rows,f'{k}-{suffix}',title,desc,maxv,base,mobile)
            (out/'charts'/f'{k}-{suffix}.svg').write_text(svg,encoding='utf-8');charts[f'{k}-{suffix}']=svg
    def figure(k):
        return f'<figure><div class="chart-desktop">{charts[k+"-desktop"]}</div><div class="chart-phone">{charts[k+"-phone"]}</div><figcaption>Nét đứt: toàn tệp {pct(base)}. Tỷ lệ = số hồ sơ y = yes / số hồ sơ trong từng nhóm. Mẫu số khác nhau; xem bảng số chính xác.</figcaption></figure>'
    share=pct(e['success_share_records_pct']);ys=pct(e['success_share_yes_pct'])
    contact='<div class="table-scroll" role="region" aria-label="Đối chiếu theo loại liên lạc cuối - cuộn ngang nếu cần" tabindex="0"><table id="contact-check"><caption>Đối chiếu: chênh lệch vẫn hiện diện trong từng loại liên lạc cuối</caption><thead><tr><th scope="col">contact</th><th scope="col">Thành công trước<br>yes / n</th><th scope="col">Thành công trước<br>Tỷ lệ yes</th><th scope="col">Kết quả còn lại<br>yes / n</th><th scope="col">Kết quả còn lại<br>Tỷ lệ yes</th></tr></thead><tbody>'
    for i in range(0,len(e['contact_strata']),2):
        x,y=e['contact_strata'][i:i+2]
        contact+=f'<tr><th scope="row">{x["contact"]}</th><td>{number(x["yes"])} / {number(x["records"])}</td><td>{pct(x["rate_pct"],2)}</td><td>{number(y["yes"])} / {number(y["records"])}</td><td>{pct(y["rate_pct"],2)}</td></tr>'
    contact+='</tbody></table></div>'
    css='''
    :root{--ink:#243c45;--muted:#546870;--accent:#006b61;--paper:#fffdf9;--line:#d7e0e1;--soft:#edf5f2}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#e8edeb;color:var(--ink);font:18px/1.55 "Segoe UI",Arial,sans-serif}a{color:var(--accent);text-underline-offset:3px}a:focus-visible,.table-scroll:focus-visible{outline:3px solid #006b61;outline-offset:4px}
    .topnav{max-width:1160px;margin:0 auto;padding:20px 32px;display:flex;gap:24px;flex-wrap:wrap;font-size:16px}.topnav a{font-weight:600}.page{max-width:1160px;margin:0 auto 24px;background:var(--paper);padding:44px 64px 35px;position:relative}.eyebrow{font-size:15px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:0 0 18px}.page-header{display:flex;justify-content:space-between;gap:10px;font-size:15px;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:15px;margin-bottom:26px}.pageno{font-variant-numeric:tabular-nums;white-space:nowrap}h1{font-size:44px;line-height:1.14;letter-spacing:-.035em;max-width:850px;margin:0 0 20px}h2{font-size:34px;line-height:1.2;letter-spacing:-.025em;margin:0 0 20px}h3{font-size:22px;line-height:1.35;margin:22px 0 9px}p{margin:0 0 15px}.lead{font-size:21px;line-height:1.55;max-width:940px}.choice{border-left:5px solid var(--accent);padding:12px 0 12px 23px;margin:26px 0;color:var(--ink)}.choice strong{color:var(--accent)}.scope{font-size:16px;color:var(--muted);margin-bottom:20px}.chart-phone{display:none}figure{margin:22px 0 16px}svg{display:block;width:100%;height:auto}figcaption{font-size:16px;color:var(--muted);line-height:1.45;padding-top:8px}.split{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:20px}.split p{margin-bottom:0}.fact{font-size:21px;line-height:1.4;margin-bottom:6px!important}.fact strong{font-size:30px;color:var(--accent)}.note{font-size:17px}.limit{background:var(--soft);padding:18px 22px;border-radius:2px;margin:22px 0}.limit p:last-child{margin-bottom:0}.footer{border-top:1px solid var(--line);padding-top:13px;margin-top:28px;font-size:15px;color:var(--muted)}.table-scroll{overflow-x:auto;margin:20px 0;scrollbar-color:var(--accent) var(--soft)}table{width:100%;min-width:620px;border-collapse:collapse;font-variant-numeric:tabular-nums;font-size:16px;line-height:1.4}caption{text-align:left;font-weight:650;color:var(--ink);font-size:17px;margin-bottom:10px}th,td{padding:10px 8px;border-bottom:1px solid var(--line);text-align:right;vertical-align:top}th:first-child{text-align:left}thead th{font-size:14px;color:var(--muted);border-top:1px solid var(--line)}tbody th{font-weight:500}td{white-space:nowrap}.steps{list-style:none;padding:0;margin:20px 0}.steps li{display:grid;grid-template-columns:110px 1fr;gap:20px;border-top:1px solid var(--line);padding:17px 0}.steps .time{font-size:16px;color:var(--accent);font-weight:650}.steps p{margin:6px 0 0}.hours{font-size:16px;color:var(--muted)}.decision{border:1px solid var(--accent);padding:22px;margin-top:22px}.decision h3{margin-top:0;color:var(--accent)}ul{padding-left:22px}li{margin:6px 0}.source{font-size:15px;line-height:1.5}.hash{font-size:12px;overflow-wrap:anywhere;font-family:Consolas,monospace}.sources{border-top:1px solid var(--line);padding-top:15px;margin-top:20px}.definition-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}.definition-grid p{font-size:16px}.minor{color:var(--muted)}.download{display:inline-block;margin-right:18px}.print-only{display:none}
    @media(max-width:650px){body{font-size:17px;line-height:1.55}.topnav{padding:18px 22px;gap:13px 20px;font-size:15px}.page{padding:29px 24px 28px;margin-bottom:12px}.page-header{font-size:13px;align-items:flex-start;gap:12px;margin-bottom:24px}.eyebrow{font-size:13px;letter-spacing:.06em}h1{font-size:34px;line-height:1.17}h2{font-size:29px;line-height:1.2}h3{font-size:21px}.lead{font-size:19px}.scope,figcaption{font-size:15px}.choice{padding-left:18px;margin:22px 0}.chart-desktop{display:none}.chart-phone{display:block}.split,.definition-grid{display:block}.split>div{margin-bottom:20px}.fact{font-size:19px}.fact strong{font-size:27px}.limit{padding:16px 18px}.steps li{grid-template-columns:1fr;gap:5px}.steps .time{font-size:16px}.table-scroll{margin-right:-8px;padding-bottom:5px}table{font-size:16px;min-width:620px}caption{font-size:16px}th,td{padding:10px}.decision{padding:18px}.footer{font-size:14px}.source{font-size:14px}.hash{font-size:11px}.download{display:block;margin-bottom:12px}}
    @page{size:A4;margin:10mm 16mm}
    @media print{html{scroll-behavior:auto}body{background:white;font-size:10.6pt;line-height:1.40;print-color-adjust:exact;-webkit-print-color-adjust:exact}.topnav,.screen-only{display:none}.page{max-width:none;width:178mm;padding:0;margin:0;min-height:269mm;break-after:page}.page:last-child{break-after:auto;min-height:0}.page-header{font-size:9pt;padding-bottom:3mm;margin-bottom:6mm}.eyebrow{font-size:9pt;margin-bottom:3mm}h1{font-size:26pt;line-height:1.16;margin-bottom:4mm}h2{font-size:23pt;line-height:1.18;margin-bottom:4mm}h3{font-size:12.3pt;margin:4mm 0 2mm}p{margin-bottom:3mm}.lead{font-size:12.2pt;line-height:1.43}.scope{font-size:9.5pt;margin-bottom:3mm}.choice{padding:2mm 0 2mm 5mm;margin:5mm 0;border-left-width:1.2mm}.chart-desktop{display:block}.chart-phone{display:none}figure{margin:4mm 0 3mm}figcaption{font-size:9.3pt;padding-top:2mm}.split{gap:6mm;margin-top:4mm}.fact{font-size:12pt}.fact strong{font-size:20pt}.note{font-size:10.3pt}.limit{padding:3.7mm 4mm;margin:4mm 0}.footer{font-size:8.8pt;margin-top:5mm;padding-top:3mm}.table-scroll{overflow:visible;margin:4mm 0}table{min-width:0;font-size:9.3pt;line-height:1.34}caption{font-size:10pt;margin-bottom:2mm}th,td{padding:1.5mm 1.7mm}thead th{font-size:8.4pt}.steps{margin:4mm 0}.steps li{grid-template-columns:23mm 1fr;gap:4mm;padding:3mm 0}.steps .time,.hours{font-size:9.5pt}.steps p{margin-top:1mm}.decision{padding:4mm;margin-top:4mm}.source{font-size:8.6pt}.hash{font-size:7.1pt}.definition-grid{gap:5mm}.definition-grid p{font-size:9.5pt}.sources{padding-top:3mm;margin-top:4mm}.print-only{display:block}a{color:inherit;text-decoration:none}ul{margin:2mm 0;padding-left:5mm}li{margin:1.2mm 0}}
    '''
    body=f'''<nav class="topnav" aria-label="Mục lục"><a href="#choice">Kết luận</a><a href="#contacts">Số lần liên lạc</a><a href="#action">Bước tiếp theo</a><a href="#exact">Số chính xác &amp; nguồn</a></nav>
    <main>
    <section class="page" id="choice" aria-labelledby="main-title"><header class="page-header"><span>VẬN HÀNH TIẾP THỊ · BÁO CÁO HỒI CỨU</span><span class="pageno">01 / 04</span></header>
    <p class="eyebrow">Cuộc họp giả lập · 14.10.2026</p><h1 id="main-title">Lịch sử thành công là tín hiệu mạnh, nhưng có độ phủ hẹp</h1>
    <p class="lead">Đề xuất kiểm tra khả năng dùng lịch sử chiến dịch để phân nhóm danh sách. Chưa dùng kết quả này để dự báo khách hàng hiện nay hoặc giới hạn số lần liên lạc.</p>
    <div class="choice"><strong>Chọn ngay:</strong> một đợt chẩn đoán trong 10 ngày làm việc, tối đa 16 giờ phân tích và 2 giờ quản lý. Kiểm tra lịch sử có đúng người, đúng thời điểm và dùng được trước khi liên lạc hay không.</div>
    <p class="scope">Toàn bộ 45.211 hồ sơ của ngân hàng Bồ Đào Nha, 05/2008–11/2010 theo tài liệu nguồn. y = yes: đăng ký tiền gửi có kỳ hạn. Không có mã để xác định khách hàng duy nhất.</p>
    <h3>Tỷ lệ đăng ký cao hơn ở nhóm “thành công trước”</h3>{figure('history')}
    <div class="split"><div><p class="fact"><strong>{share}</strong> hồ sơ có lịch sử thành công</p><p class="note">1.511 / 45.211 hồ sơ. Nhóm này chứa {ys} số hồ sơ y = yes: 978 / 5.289.</p></div><div><p class="fact"><strong>{number(e['rest_yes'])}</strong> hồ sơ yes nằm ngoài nhóm</p><p class="note">Chỉ chọn nhóm thành công trước sẽ bỏ qua phần lớn kết quả yes đã ghi nhận. Nhóm không rõ kết quả cũng không đồng nghĩa với thất bại.</p></div></div>
    <div class="limit"><p><strong>Giới hạn làm đổi quyết định:</strong> đây là liên hệ quan sát. Nhu cầu sẵn có, cách chọn danh sách và thời kỳ chiến dịch có thể cùng tạo ra chênh lệch; chưa đo được lợi ích của việc ưu tiên nhóm này.</p></div>
    <footer class="footer">Nguồn: UCI Bank Marketing, bank-full.csv, toàn tệp nguyên bản. Phép tính và định nghĩa: trang 4. Đề xuất chưa được phê duyệt hoặc thực hiện.</footer></section>

    <section class="page" id="contacts" aria-labelledby="contact-title"><header class="page-header"><span>BẰNG CHỨNG &amp; CÁCH DIỄN GIẢI</span><span class="pageno">02 / 04</span></header>
    <h2 id="contact-title">Liên lạc nhiều lần đi cùng tỷ lệ thấp hơn; chưa có căn cứ đặt trần cuộc gọi</h2>
    <p class="lead">Tỷ lệ yes giảm từ {pct(a[0]['rate_pct'])} ở nhóm 1 lần xuống {pct(a[-1]['rate_pct'])} ở nhóm từ 7 lần. Nhưng chiến dịch có thể phải tiếp tục liên lạc vì chưa nhận được phản hồi thuận lợi.</p>
    <p class="scope">Toàn tệp 45.211 hồ sơ. campaign đếm số lần liên lạc trong chiến dịch hiện tại, gồm lần cuối; không phải nhật ký từng cuộc gọi. Các nhóm 1 / 2–3 / 4–6 / ≥7 do báo cáo chọn, không phải chính sách nguồn.</p>{figure('attempts')}
    <div class="limit"><p><strong>Hai cách giải thích vẫn mở:</strong> liên lạc lặp lại có thể ít hiệu quả; hoặc những trường hợp khó chuyển đổi được liên lạc thêm. CSV không cho biết phản hồi sau từng lần, khoảng cách các lần hay lý do tiếp tục, nên không phân biệt được hai cách giải thích.</p></div>
    <h3>Kiểm tra một khả năng gây nhiễu: loại liên lạc cuối</h3>{contact}
    <p class="note">Kết quả còn lại gồm failure, other và unknown. Chênh lệch lịch sử thành công vẫn có trong cellular và telephone; vì vậy khác biệt về loại liên lạc cuối chưa giải thích hết liên hệ. Tuy nhiên đây cũng là thông tin của lần cuối, không chứng minh lịch sử gây ra đăng ký. Nhóm success + contact unknown chỉ có 12 hồ sơ.</p>
    <footer class="footer">duration chỉ biết sau cuộc gọi; không dùng để chọn danh sách trước gọi. Không có năm trong CSV để phân tích lịch đầy đủ. Nguồn và tỷ lệ chính xác ở trang 4.</footer></section>

    <section class="page" id="action" aria-labelledby="action-title"><header class="page-header"><span>ĐỀ XUẤT CHẨN ĐOÁN · CHƯA THỐNG NHẤT</span><span class="pageno">03 / 04</span></header>
    <h2 id="action-title">Dùng 10 ngày để quyết định tín hiệu có dùng được hay không</h2>
    <p class="lead">Kiểm tra tín hiệu trước khi chọn danh sách hoặc đổi số lần liên lạc. Đợt chẩn đoán không gồm liên lạc khách hàng.</p>
    <ol class="steps"><li><div class="time">Ngày 1–2<br><span class="hours">3h phân tích<br>0,5h quản lý</span></div><div><strong>Xác nhận quyền truy cập và bản ghi đối chiếu.</strong><p>Người phân tích và quản lý đề xuất xin chủ nguồn liên kết dòng CSV với bản ghi gốc, mã khách hàng, thời điểm, lịch sử và quy tắc cập nhật. Chỉ nhận khi có quyền; dừng sau ngày 2 nếu không có quyền hoặc không khôi phục được liên kết.</p></div></li>
    <li><div class="time">Ngày 3–6<br><span class="hours">8h phân tích<br>0,5h quản lý</span></div><div><strong>Đối chiếu ngẫu nhiên 60 hồ sơ có liên kết.</strong><p>Đề xuất 30 success và 30 unknown; lấy mẫu với hạt cố định, giữ danh sách dòng. Kiểm tra đúng khách hàng, kết quả trước và bằng chứng thông tin đã có trước liên lạc hiện tại. Tối đa 8 phút/hồ sơ; ghi rõ trường hợp chưa xác minh, không đổi sang hồ sơ dễ kiểm tra.</p></div></li>
    <li><div class="time">Ngày 7–9<br><span class="hours">4h phân tích<br>0,5h quản lý</span></div><div><strong>Giải thích sai lệch và chuẩn bị điều kiện thử.</strong><p>Ghi số xác minh được / 30 mỗi nhóm và lý do thiếu. Nếu được cấp nhật ký gọi, kiểm tra phản hồi, thời điểm và lý do gọi tiếp để tách hai giả thuyết ở trang 2. Không có nhật ký: câu hỏi số lần gọi vẫn chưa giải quyết.</p></div></li>
    <li><div class="time">Ngày 10<br><span class="hours">1h phân tích<br>0,5h quản lý</span></div><div><strong>Quản lý đọc kết quả và quyết định bước tiếp.</strong><p>Bàn giao sổ đối chiếu, tỷ lệ xác minh và lỗi có thể đổi danh sách. Tổng đề xuất: 16 giờ phân tích + 2 giờ quản lý; xác nhận người thực hiện và thời gian sẵn có trước khi bắt đầu.</p></div></li></ol>
    <div class="decision"><h3>Cách đọc kết quả ngày 10</h3><p><strong>Tiếp tục chuẩn bị thử</strong> chỉ khi liên kết, định nghĩa lịch sử và thời điểm có thông tin đã được xác minh cho cả 60 hồ sơ. Cổng kiểm tra này là đề xuất; mẫu nhỏ không bảo đảm toàn bộ danh sách đúng.</p><p><strong>Thiếu bất kỳ điều kiện nào:</strong> sửa nguồn/định nghĩa hoặc thu hẹp câu hỏi; chưa dùng poutcome để ưu tiên. Không lấy được hồ sơ ngày 2: kết thúc bằng giới hạn đã ghi nhận và phép tính CSV đã đối chiếu.</p></div>
    <p class="note" style="margin-top:16px">Thử liên lạc sau này cần phê duyệt riêng về danh sách hiện hành đủ điều kiện, người gọi, khung giờ, ngân sách và cửa sổ đo đăng ký. Trần giả định là 200 lượt; báo cáo này chưa đề nghị triển khai thử.</p>
    <footer class="footer">Thước đo của đợt chẩn đoán là khả năng xác minh thông tin và giải quyết lỗi, không phải tăng tỷ lệ đăng ký. Mọi vai trò, phân bổ giờ, ngày và cổng kiểm tra trên là đề xuất.</footer></section>

    <section class="page" id="exact" aria-labelledby="exact-title"><header class="page-header"><span>TRA CỨU · ĐỊNH NGHĨA · NGUỒN</span><span class="pageno">04 / 04</span></header>
    <h2 id="exact-title">Đối chiếu từng số về cùng một tệp gốc</h2>
    <p class="note">Không lọc dòng, không loại unknown, không bỏ giá trị pdays = −1 và không gộp “khách hàng duy nhất”. Tất cả tỷ lệ trong báo cáo là mô tả hồ sơ quan sát, không phải dự báo.</p>
    {table(h,'Bảng 1 · Kết quả chiến dịch trước (poutcome)',identifier='history-table')}
    {table(a,'Bảng 2 · Số lần liên lạc trong chiến dịch (campaign)','Nhóm số lần liên lạc','attempts-table')}
    <p class="note"><strong>Đối chiếu tổng:</strong> cả hai bảng cộng thành 45.211 hồ sơ = 5.289 yes + 39.922 no. Tỷ lệ chung = 5.289 / 45.211 = {pct(base,2)}. Tỷ lệ nhóm = yes / n × 100; làm tròn 1 chữ số trên biểu đồ, 2 chữ số ở bảng. Tính từ số nguyên trước khi làm tròn.</p>
    <div class="definition-grid"><div><h3>Ý nghĩa và thời điểm</h3><p><strong>poutcome:</strong> kết quả chiến dịch trước. unknown là một nhóm nguồn, không phải ô trống hay thất bại; có 36.959 hồ sơ.<br><strong>pdays = −1:</strong> không liên lạc ở chiến dịch trước, 36.954 hồ sơ. Hai khái niệm không đồng nhất.<br><strong>campaign:</strong> từ 1 đến 63; đã gồm lần cuối.</p></div><div><h3>Điều chưa thể kết luận</h3><p>Không có mã khách hàng, năm/ngày giờ đầy đủ, nhật ký từng lần, chi phí gọi hay giá trị tiền gửi. Không suy ra nhân quả, lợi nhuận, khung giờ gọi, mức gọi tối ưu hoặc kết quả khách hàng hiện nay. Thời điểm có các thuộc tính khách hàng chưa được tài liệu xác định.</p></div></div>
    <div class="sources"><p class="source"><strong>Nguồn &amp; quyền sử dụng.</strong> Moro, S., Rita, P., &amp; Cortez, P. (2014). <em>Bank Marketing</em> [Dataset]. UCI Machine Learning Repository. <a href="https://doi.org/10.24432/C5K306">doi.org/10.24432/C5K306</a>. <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Trích dẫn gốc theo từ điển: Moro, Laureano &amp; Cortez (2011), <em>Using Data Mining for Bank Direct Marketing: An Application of the CRISP-DM Methodology</em>, ESM’2011, tr. 117–121.</p><p class="source">Bản nguồn bank-full.csv và bank-names.txt được giữ nguyên; metadata nguồn được xác minh ngày 14.10.2026. Báo cáo thêm các tổng hợp và nhóm campaign nêu trên. Từ điển gốc và source-contract.json quyết định ý nghĩa trường. Nội dung có thể đọc offline; liên kết nguồn cần mạng khi mở.</p><p class="hash">SHA-256 CSV: {e['source_sha256']}</p></div>
    <p class="source screen-only"><a class="download" href="report.pdf">Mở PDF 4 trang</a><a class="download" href="evidence/calculations.json">Các phép tính</a><a class="download" href="README.md">Hướng dẫn dựng lại</a></p>
    <footer class="footer">Các biểu đồ SVG giữ chữ chỉnh được; số liệu CSV/JSON và mã dựng kèm gói để kiểm tra. Trình tự gốc không dùng làm mốc năm; không lấy thêm bộ dữ liệu.</footer></section></main>'''
    doc=f'<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><title>Lịch sử thành công và bước chẩn đoán trước đợt liên lạc | Bank Marketing</title><style>{css}</style></head><body>{body}</body></html>'
    doc=doc.replace('<div class="table-scroll"','<p class="scroll-hint screen-only">Bảng có thêm cột: vuốt ngang hoặc dùng phím mũi tên khi chọn bảng.</p><div class="table-scroll"')
    doc=doc.replace('</style>','.scroll-hint{display:none}@media(max-width:650px){.scroll-hint{display:block;font-size:14px;color:var(--muted);margin:18px 0 -10px}.table-scroll th:first-child{position:sticky;left:0;z-index:2;background:var(--paper)}caption{max-width:calc(100vw - 48px);white-space:normal;position:sticky;left:0}}@media print{.scroll-hint{display:none}col{width:auto!important}}</style>')
    (out/'report.html').write_text(doc,encoding='utf-8')
    # Keep only source metadata; the unchanged raw CSV remains a caller-supplied input.
    provenance=out/'source';provenance.mkdir(exist_ok=True)
    for name in ['bank-full.csv','source-contract.json','bank-names.txt','PROVENANCE.md','brief.vi.md']:
        src=Path(source).parent/name
        if src.resolve()!=(provenance/name).resolve():shutil.copyfile(src,provenance/name)
    return e

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    e=build(a.source,a.out);print(json.dumps({'built':str(Path(a.out).resolve()),'rows':e['rows'],'yes':e['yes']},ensure_ascii=False))



