"""Build focused, editable worked-example SVGs from retained calculations.

Python standard library only. These layouts serve the fixed example questions;
changed inputs need a fresh conclusion/layout review, not an automatic template fill.
"""
from html import escape
import csv
from decimal import Decimal
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INK, MUTED, BLUE = '#17252E', '#5B6874', '#245AE7'
CONTEXT, GRID, PAPER = '#758594', '#DFE5EA', '#FFFFFF'

class Sheet:
    def __init__(self, number, title, description):
        self.parts = [
            '<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="900" viewBox="0 0 1440 900" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
            '<style>text{font-family:"Segoe UI",Arial,sans-serif;font-variant-numeric:tabular-nums}.heading{font-family:Georgia,"Times New Roman",serif}</style>',
            '<rect width="1440" height="900" fill="#FFFFFF"/>',
        ]
        self.text(70, 46, number, 15, BLUE, 600)
        self.text(106, 46, 'WORKED EXAMPLE', 13, MUTED, 600, spacing=1.4)
        self.text(1370, 46, 'SYNTHETIC DATA', 13, MUTED, anchor='end', spacing=1.2)
        self.line(70, 68, 1370, 68)
        self.text(70, 132, title, 42, INK, 400, family='heading')
    def text(self, x, y, value, size=20, fill=INK, weight=400, anchor='start', spacing=None, family=None):
        extra = f' letter-spacing="{spacing}"' if spacing is not None else ''
        cls = f' class="{family}"' if family else ''
        self.parts.append(f'<text{cls} x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{extra}>{escape(str(value))}</text>')
    def lines(self, x, y, values, size=20, gap=29, fill=INK, weight=400):
        for i,value in enumerate(values): self.text(x,y+i*gap,value,size,fill,weight)
    def rect(self, x, y, width, height, fill=PAPER, stroke=None, radius=0):
        edge = f' stroke="{stroke}"' if stroke else ''
        self.parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}"{edge}/>')
    def line(self, x1,y1,x2,y2,color=GRID,width=1,dash=None):
        pattern=f' stroke-dasharray="{dash}"' if dash else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{pattern}/>')
    def footer(self, first, second):
        self.line(70, 817, 1370, 817)
        self.text(70, 850, first, 16, MUTED)
        self.text(70, 875, second, 16, MUTED)
    def write(self,path):
        path.write_text('\n'.join(self.parts+['</svg>'])+'\n',encoding='utf-8',newline='\n')

def profit():
    folder=ROOT/'01-profit-decision'
    data=json.loads((folder/'analysis.json').read_text(encoding='utf-8'))
    june,july=data['monthly']
    opening=Decimal(june['contribution_vnd'])/1_000_000
    closing=Decimal(july['contribution_vnd'])/1_000_000
    gross=Decimal(july['gross_profit_vnd']-june['gross_profit_vnd'])/1_000_000
    freight=-Decimal(july['outbound_freight_vnd']-june['outbound_freight_vnd'])/1_000_000
    assert opening+gross+freight==closing
    assert (opening,gross,freight,closing)==(Decimal('35'),Decimal('2.8'),Decimal('-6.85'),Decimal('30.95'))
    b=Sheet('01','Freight growth erased the gain in gross profit.',
        'June to July 2026: gross profit rose 2.80 million VND and freight rose 6.85 million VND. Contribution fell 4.05 million, from 35.00 to 30.95. Closed-ledger freight is authoritative; 3.00 million is unattributed.')
    b.text(70,176,'Contribution fell 4.05m VND from June to July 2026, despite higher sales.',21,MUTED)
    b.text(70,239,'Contribution',18,INK,600)
    b.text(1370,239,'million VND  ·  excludes overhead',17,MUTED,anchor='end')
    bottom,scale=652,8.4
    for tick in (0,10,20,30,40):
        y=bottom-tick*scale
        b.line(112,y,1338,y)
        b.text(95,y+6,tick,17,MUTED,anchor='end')
    entries=[('June',opening),('Gross-profit gain',gross),('Freight growth',freight),('July',closing)]
    running=opening
    for i,(label,value) in enumerate(entries):
        x=162+i*314
        if i in (0,3): low,high=Decimal(0),value
        else:
            before=running; running+=value; low,high=sorted((before,running))
        color=BLUE if i==2 else CONTEXT
        b.rect(x,bottom-float(high)*scale,170,float(high-low)*scale,color)
        amount=f'{value:.2f}' if i in (0,3) else f'{value:+.2f}'.replace('-','−')
        b.text(x+85,bottom-float(high)*scale-17,amount,28,BLUE if i==2 else INK,600,'middle')
        b.text(x+85,687,label,22,BLUE if i==2 else INK,600 if i==2 else 400,'middle')
        if i<3:
            level=opening if i==0 else running
            b.line(x+170,bottom-float(level)*scale,x+314,bottom-float(level)*scale,CONTEXT,1,'4 5')
    b.line(70,724,1370,724)
    b.text(70,760,'DECISION',13,MUTED,600,spacing=1.2)
    b.text(70,791,'Full memo: keep B2B; propose a bounded price test.',21)
    b.text(798,760,'LIMIT THAT MATTERS',13,MUTED,600,spacing=1.2)
    b.text(798,791,'3.00m freight is in the ledger but unattributed.',20)
    b.footer('Source: June/July invoice, credit and finance exports. July ledger freight 15.70m; carrier detail 12.70m.',
             'Proposed commercial-lead pilot: four-week execution review; expansion waits for complete return and freight evidence.')
    b.write(folder/'decision.svg')

def comparison():
    folder=ROOT/'02-fair-comparison'
    data=json.loads((folder/'calculations.json').read_text(encoding='utf-8'))
    with (folder/'data.csv').open(encoding='utf-8',newline='') as file: cells=list(csv.DictReader(file))
    assert data['team_totals']['A']['rate']==.30 and data['team_totals']['B']['rate']==.45
    b=Sheet('02','Different lead mix reverses the team ranking.',
        'Overall B wins 45% versus A 30%; in High and Low tiers A leads by 5 percentage points. B receives 75% High-tier leads versus A 25%. No coaching effect or future superiority is established.')
    b.text(70,176,'B leads overall. A leads within both supplied tiers. Coaching is not identified as the cause.',21,MUTED)
    b.text(70,241,'Overall',25,INK,600)
    b.text(70,273,'80 leads per team',18,MUTED)
    b.text(765,241,'Within the same lead tier',25,INK,600)
    b.text(765,273,'Win rate · same 0–70% scale',18,MUTED)
    def axis(x,width,top,bottom):
        for tick in (0,20,40,60,70):
            xx=x+width*tick/70
            b.line(xx,top,xx,bottom)
            b.text(xx,bottom+28,f'{tick}%',16,MUTED,anchor='middle')
    axis(155,410,303,584)
    axis(876,410,303,584)
    b.text(1370,301,'wins / leads',14,MUTED,anchor='end')
    for i,team in enumerate(('A','B')):
        y=330+i*129; d=data['team_totals'][team]; rate=d['rate']*100; color=BLUE if team=='A' else CONTEXT
        b.text(99,y+28,team,21,INK,600)
        b.rect(155,y,410*rate/70,38,color)
        b.text(155+410*rate/70+15,y+28,f'{rate:.0f}%',26,INK,600)
        b.text(155,y+67,f"{d['wins']} wins / {d['eligible_leads']} leads",18,MUTED)
    for tier,team,y in [('High','A',323),('High','B',373),('Low','A',482),('Low','B',532)]:
        cell=next(r for r in cells if r['team']==team and r['lead_tier']==tier)
        rate=int(cell['wins'])/int(cell['eligible_leads'])*100
        color=BLUE if team=='A' else CONTEXT
        if team=='A': b.text(765,y+24,tier,20,INK,600)
        b.text(844,y+24,team,18,INK,600)
        b.rect(876,y,410*rate/70,30,color)
        b.text(876+410*rate/70+12,y+24,f'{rate:g}%',23,INK,600)
        b.text(1370,y+24,f"{cell['wins']} / {cell['eligible_leads']}",17,MUTED,anchor='end')
    b.text(70,657,'High-tier share of assigned leads',19,MUTED)
    b.text(432,657,'A 25%  /  B 75%',21,INK,600)
    b.line(70,724,1370,724)
    b.text(70,760,'DECISION',13,MUTED,600,spacing=1.2)
    b.text(70,791,'Review lead assignment before changing coaching.',21)
    b.footer('Source: four synthetic team × tier cells. Observation period and coaching assignment are not supplied.',
             'A hypothetical 50/50 lead mix gives A 40% and B 35%. Descriptive standardization; no causal coaching effect.')
    b.write(folder/'comparison.svg')

def join():
    folder=ROOT/'03-join-audit'
    with (folder/'inputs/invoice-lines.csv').open(encoding='utf-8',newline='') as file: invoices=list(csv.DictReader(file))
    with (folder/'inputs/payment-allocations.csv').open(encoding='utf-8',newline='') as file: payments=list(csv.DictReader(file))
    invoice='INV-1002'
    lines=[r for r in invoices if r['invoice_id']==invoice]
    matches=[r for r in payments if r['invoice_id']==invoice]
    billed=sum(Decimal(r['net_amount_usd']) for r in lines)
    assert billed==500 and len(lines)==2 and len(matches)==3
    report=json.loads((folder/'result'/'report.json').read_text(encoding='utf-8'))
    assert report['left_measure']['duplication_excess']=='1300'
    b=Sheet('03','One invoice. Counted three times.',
        'Invoice INV-1002 has two legitimate lines totaling 500 USD and three payment allocations. A raw join carries the 500 revenue into each allocation, producing 1500 and 1000 duplication. Across all invoices duplication is 1300 USD.')
    b.text(70,176,'INV-1002 creates $1,000 of the $1,300 revenue overstatement.',21,MUTED)
    b.text(70,239,'Before the join',23,INK,600)
    b.text(520,239,'After matching each payment allocation',23,INK,600)
    # Enclosure groups actual row relationships. Copied amounts are shown explicitly.
    def invoice_card(x,y,width,tag,subtitle,color=INK):
        b.rect(x,y,width,261,PAPER,GRID,4)
        b.text(x+24,y+38,tag,17,MUTED,600)
        b.line(x+24,y+58,x+width-24,y+58)
        for i,row in enumerate(lines):
            yy=y+102+i*42
            b.text(x+24,yy,'Line '+str(i+1),18,MUTED)
            b.text(x+width-24,yy,'$'+format(Decimal(row['net_amount_usd']),',.0f'),22,INK,500,'end')
        b.line(x+24,y+163,x+width-24,y+163)
        b.text(x+24,y+197,'Revenue',17,MUTED)
        b.text(x+width-24,y+197,'$500',28,color,600,'end')
        b.text(x+24,y+234,subtitle,15,MUTED)
    invoice_card(70,285,320,invoice,'Two original invoice lines')
    b.line(390,415,452,415,CONTEXT,1.5)
    b.line(452,415,452,264,CONTEXT,1.5)
    b.line(452,264,1270,264,CONTEXT,1.5)
    for i,payment in enumerate(matches):
        x=520+i*285
        b.line(x+120,264,x+120,285,CONTEXT,1.5)
        invoice_card(x,285,240,'Allocation '+str(i+1),'Payment $'+format(Decimal(payment['received_amount_usd']),',.0f'))
    b.text(520,592,'$500  +  $500  +  $500  =  $1,500',30,INK,500)
    b.text(520,638,'$1,000 is the same revenue repeated.',29,BLUE,600)
    b.line(70,724,1370,724)
    b.text(70,760,'REPAIR',13,MUTED,600,spacing=1.2)
    b.text(70,791,'Aggregate invoices and payments separately, then join.',21)
    b.footer('All four invoices (USD): $1,200 billed · $1,050 received · $150 unpaid. Raw left-join revenue: $2,500.',
             'Source: executed synthetic join audit. Many-to-many cardinality passes; that does not make revenue additive.')
    b.write(folder/'join.svg')

if __name__=='__main__':
    profit(); comparison(); join()
    print('Built three focused editable SVGs.')
