"""Build editable SVG decision notes from the worked-example calculation files.

Run from any directory with Python 3. No third-party packages are required.
PNG rendering is a separate optional step; the SVG is the editable source.
"""
from html import escape
import csv
from decimal import Decimal
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BG, INK, MUTED = '#F7F5F0', '#182D33', '#52636A'
TEAL, CLAY, GRID, PALE = '#08766A', '#B44F31', '#D7DEDA', '#E7EEE8'

class Board:
    def __init__(self, title, description, number):
        self.parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1080" viewBox="0 0 1400 1080" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
                      '<style>text{font-family:"Segoe UI",Arial,sans-serif} .number{font-variant-numeric:tabular-nums}</style>']
        self.rect(0, 0, 1400, 1080, BG)
        self.text(64, 66, 'DATA STORYTELLING', 20, TEAL, 700, spacing=2)
        self.text(1336, 66, f'DECISION NOTE {number}  /  SYNTHETIC EXAMPLE', 18, MUTED, anchor='end')
        self.line(64, 91, 1336, 91, GRID)
    def text(self, x, y, value, size=24, fill=INK, weight=400, anchor='start', spacing=None):
        extra = f' letter-spacing="{spacing}"' if spacing is not None else ''
        self.parts.append(f'<text class="number" x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{extra}>{escape(str(value))}</text>')
    def lines(self, x, y, lines, size=24, gap=33, fill=INK, weight=400):
        for i, value in enumerate(lines): self.text(x, y+i*gap, value, size, fill, weight)
    def rect(self, x, y, w, h, fill, rx=0, stroke=None):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" rx="{rx}"' + (f' stroke="{stroke}"' if stroke else '') + '/>')
    def line(self, x1, y1, x2, y2, color=GRID, width=1, dash=None):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    def footer(self, source):
        self.text(64, 1045, source, 18, MUTED)
        self.text(1336, 1045, 'EDITABLE SVG + SOURCE DATA', 17, MUTED, anchor='end')
    def write(self, path):
        path.write_text('\n'.join(self.parts + ['</svg>']) + '\n', encoding='utf-8')

def profit():
    d=json.loads((ROOT/'01-profit-decision'/'analysis.json').read_text(encoding='utf-8'))
    june,july=d['monthly']
    million=lambda v: v/1_000_000
    sales_change=million(july['net_sales_vnd']-june['net_sales_vnd'])
    contribution_change=million(july['contribution_vnd']-june['contribution_vnd'])
    bridge=d['bridge']
    assert bridge['unit_cost_at_july_quantities_vnd']==0, 'This four-factor layout needs a cost step for changed unit costs.'
    b = Board('More sales. Less contribution.', 'June to July contribution falls from 35.00 to 30.95 million VND. Volume and mix add 10.90; invoice prices reduce 6.40; posted credits reduce 1.70; freight reduces 6.85. Three million freight is not attributed by the connector.', '01')
    b.lines(64, 167, ['More sales.', 'Less contribution.'], 66, 76, weight=650)
    b.text(64, 292, 'Explain the decline before choosing the August move.', 28, MUTED)
    b.text(1004, 155, 'NET SALES CHANGE', 18, MUTED, 600, spacing=1)
    b.text(1004, 212, f'{sales_change:+.2f}m', 50, TEAL, 650)
    b.text(1004, 250, 'Contribution change', 19, MUTED)
    b.text(1004, 294, f'{contribution_change:+.2f}m VND'.replace('-', '−'), 35, CLAY, 650)
    b.text(64, 358, 'The contribution bridge', 27, weight=650)
    b.text(64, 388, 'June → July 2026 · million VND · contribution excludes overhead', 20, MUTED)
    top, bottom, scale = 425, 742, 6.34
    for tick in (0, 10, 20, 30, 40, 50):
        y=bottom-tick*scale
        b.line(106, y, 925, y)
        b.text(91, y+6, tick, 17, MUTED, anchor='end')
    values = [('June', million(june['contribution_vnd'])), ('Volume', million(bridge['volume_mix_at_june_unit_margin_vnd'])), ('Invoice', million(bridge['invoice_price_at_july_quantities_vnd'])), ('Posted', million(bridge['change_in_posted_credit_effect_vnd'])), ('Freight', million(bridge['change_in_freight_effect_vnd'])), ('July', million(july['contribution_vnd']))]
    running = values[0][1]
    for i,(name,v) in enumerate(values):
        x = 128 + i*136
        if i in (0,5): lo,hi,fill=0,v,INK
        else:
            before=running; running += v
            lo,hi=sorted((before,running)); fill=TEAL if v>0 else CLAY
        b.rect(x, bottom-hi*scale, 87, (hi-lo)*scale, fill)
        label = f'{v:.2f}' if i in (0,5) else f'{v:+.2f}'.replace('-', '−')
        b.text(x+43.5, bottom-hi*scale-14, label, 23, fill, 650, 'middle')
        if i<5:
            level = v if i==0 else running
            b.line(x+87, bottom-level*scale, x+136, bottom-level*scale, MUTED, 1, '4 4')
        b.text(x+43.5, 776, name, 20, anchor='middle')
        suffix={1:'& mix',2:'prices',3:'credits'}.get(i, '')
        if suffix: b.text(x+43.5, 803, suffix, 20, MUTED, anchor='middle')
    assert abs(running-values[-1][1])<1e-9
    assert max(v for _,v in values)<=50, 'Revise the chart scale for new data.'
    b.rect(990, 335, 346, 491, PALE, 10)
    b.text(1018, 377, 'Keep B2B in the plan.', 27, INK, 650)
    b.lines(1018, 421, ['Even assigning all missing', 'freight to B2B leaves'], 23, 31)
    b.text(1018, 522, f"{million(d['b2b_july']['contribution_floor_if_all_missing_freight_is_b2b_vnd']):.2f}m", 57, TEAL, 650)
    b.text(1018, 557, 'positive contribution.', 24)
    b.line(1018, 590, 1308, 590, '#C1CEC5')
    b.text(1018, 630, 'Coverage changes the story.', 23, weight=650)
    b.lines(1018, 670, [f"Carrier detail: {million(july['connected_freight_vnd']):.2f}m", f"Closed ledger: {million(july['outbound_freight_vnd']):.2f}m", f"The {million(july['unattributed_freight_vnd']):.2f}m gap is real;", 'its attribution is unknown.'], 22, 31)
    b.text(64, 850, f"Gross profit rose {million(july['gross_profit_vnd']-june['gross_profit_vnd']):.2f}m. Freight rose {-million(bridge['change_in_freight_effect_vnd']):.2f}m. The ledger sets the total.", 22, MUTED)
    b.rect(64, 885, 1272, 125, INK, 8)
    b.text(92, 931, 'Test a smaller discount. Keep B2B.', 34, '#FFFFFF', 650)
    b.lines(92, 965, ['Use comparable customers and measure contribution after credits and freight.', f"The {million(d['full_price_restoration_sensitivity']['net_contribution_effect_vnd']):.2f}m price-restoration scenario holds quantity fixed; it is not a demand forecast."], 22, 29, '#E8EFED')
    b.footer('Source: supplied June/July exports + closed ledger. Curated illustration; no action has been run.')
    b.write(ROOT/'01-profit-decision'/'decision.svg')

def comparison():
    p=ROOT/'02-fair-comparison'
    d=json.loads((p/'calculations.json').read_text(encoding='utf-8'))
    b=Board('Lead mix changes the ranking.', 'B has the higher overall win rate, 45% versus 30%. A has a five percentage point higher rate in each supplied lead tier. Different lead mix explains the ranking reversal; no coaching effect is identified.', '02')
    b.text(64, 175, 'Lead mix changes the ranking.', 62, weight=650)
    b.lines(64, 230, ['The aggregate rates are correct. The coaching conclusion goes beyond the data.'], 27, 34, MUTED)
    b.rect(64, 275, 1272, 67, '#F0E6DE', 7)
    b.text(88, 316, 'DRAFT CLAIM', 18, '#98432C', 650, spacing=1)
    b.text(254, 317, '“B’s coaching improves conversion by 50%. Roll it out to A.”', 25)
    b.text(64, 399, 'Overall win rate', 28, weight=650)
    b.text(64, 435, 'The visible advantage', 22, MUTED)
    b.text(710, 399, 'Within the same lead tier', 28, weight=650)
    b.text(710, 435, 'The comparison that changes the decision', 22, MUTED)
    b.line(665, 378, 665, 824, GRID)
    def axis(x,y,width):
        for t in (0,20,40,60,70):
            xx=x+width*t/70
            b.line(xx,y-180,xx,y,GRID)
            b.text(xx,y+28,f'{t}%',17,MUTED,anchor='middle')
    axis(118,656,440)
    for i,team in enumerate(('A','B')):
        y=486+i*91; rate=d['team_totals'][team]['rate']*100; color=TEAL if team=='A' else INK
        b.text(83,y+32,team,25,color,650)
        b.rect(118,y,440*rate/70,44,color)
        b.text(118+440*rate/70+14,y+31,f'{rate:.0f}%',26,color,650)
        t=d['team_totals'][team]
        b.text(118,y+68,f"{t['wins']} wins / {t['eligible_leads']} leads",19,MUTED)
    b.text(64,734,'High-tier share of assigned leads',22,weight=600)
    b.text(64,778,'A  25%',23,TEAL,650); b.text(420,778,'B  75%',23,INK,650)
    b.text(64,816,'Different populations. Different headline.',21,MUTED)
    # Same 0–70% scale as the aggregate bars. Every denominator remains visible.
    x,width=805,365
    for tick in (0,20,40,60,70):
        xx=x+width*tick/70; b.line(xx,462,xx,750,GRID); b.text(xx,780,f'{tick}%',17,MUTED,anchor='middle')
    with (p/'data.csv').open(encoding='utf-8',newline='') as file: cells=list(csv.DictReader(file))
    rows=[]
    for tier,team,y in [('High','A',474),('High','B',532),('Low','A',636),('Low','B',694)]:
        cell=next(r for r in cells if r['team']==team and r['lead_tier']==tier)
        rows.append((tier,team,int(cell['wins'])/int(cell['eligible_leads'])*100,f"{cell['wins']} / {cell['eligible_leads']}",y))
    for tier,team,rate,count,y in rows:
        color=TEAL if team=='A' else INK
        if team=='A': b.text(710,y+27,tier,23,weight=600)
        b.text(776,y+27,team,20,color,650)
        b.rect(x,y,width*rate/70,36,color)
        b.text(x+width*rate/70+12,y+26,f'{rate:g}% · {count}',21,color,600)
    b.text(710,818,'Equal 50/50 mix: A 40% · B 35% (illustrative)',21,MUTED)
    b.rect(64,875,1272,135,INK,8)
    b.text(92,922,'Review lead assignment before changing coaching.',32,'#FFFFFF',650)
    b.lines(92,961,['Compare coaching within tier, with an agreed outcome window before launch.', 'These four cells do not identify a causal effect or establish future team performance.'],22,29,'#E8EFED')
    b.footer('Source: four synthetic team × tier cells. Period and coaching assignment are not supplied.')
    b.write(p/'comparison.svg')

def join():
    p=ROOT/'03-join-audit'
    report=json.loads((p/'result'/'report.json').read_text(encoding='utf-8'))
    measure=report['left_measure']
    money=lambda amount: '$'+format(Decimal(amount),',.0f')
    with (p/'result'/'key-audit.csv').open(encoding='utf-8',newline='') as file: keys=list(csv.DictReader(file))
    b=Board('A valid join can still double-count revenue.', 'Seven invoice lines joined to six payment allocations inflate source revenue from 1,200 to 2,500 dollars. Many-to-many is valid, but invoice revenue is repeated per allocation. Retain one invoice-level revenue value when reconciling payments.', '03')
    b.lines(64,166,['A valid join can still', 'double-count revenue.'],62,73,weight=650)
    b.text(64,290,'Reconcile at invoice grain before summing money.',28,MUTED)
    for x,label,value,color in [(64,'SOURCE REVENUE',money(measure['source_total']),TEAL),(505,'AFTER THE LEFT JOIN',money(measure['left_join_total']),CLAY),(946,'DUPLICATED AMOUNT','+'+money(measure['duplication_excess']),CLAY)]:
        b.text(x,373,label,18,MUTED,650,spacing=1)
        b.text(x,447,value,60,color,650)
    b.line(64,485,1336,485,GRID)
    b.text(64,530,'Where the extra money comes from',28,weight=650)
    b.text(64,565,'Actual helper output · USD · unpaid invoices retained by the left join',22,MUTED)
    b.rect(64,594,1272,49,INK,5)
    for x,s,anchor in [(88,'INVOICE','start'),(550,'SOURCE REVENUE','end'),(834,'PAYMENT ALLOCATIONS','end'),(1090,'JOINED REVENUE','end'),(1312,'EXCESS','end')]: b.text(x,626,s,18,'#FFFFFF',600,anchor)
    for i,row in enumerate(keys):
        invoice=json.loads(row['key_json'])[0]; amount=Decimal(row['left_source_amount'])
        allocations=int(row['right_rows']); mult=str(allocations) if allocations else '0 · unpaid'
        joined=amount*max(1,allocations); extra=joined-amount
        y=643+i*48
        b.rect(64,y,1272,48,PALE if i==1 else BG)
        b.text(88,y+32,invoice,23,weight=600)
        b.text(550,y+32,money(amount),23,anchor='end')
        b.text(834,y+32,mult,23,anchor='end')
        b.text(1090,y+32,money(joined),23,CLAY if extra else INK,600,'end')
        b.text(1312,y+32,'+'+money(extra) if extra else '—',23,CLAY if extra else MUTED,600,'end')
        b.line(64,y+48,1336,y+48,GRID)
    b.text(64,866,'Declared many-to-many cardinality passes. Revenue still repeats for each allocation.',22,MUTED)
    b.rect(64,881,1272,129,INK,8)
    b.text(92,927,'One revenue value per invoice. Sum payments separately.',31,'#FFFFFF',650)
    b.lines(92,964,['Correct reconciliation: $1,200 invoiced · $1,050 received · $150 unpaid.', 'Inner-join revenue is $2,350: it duplicates paid invoices and drops the unpaid invoice.'],22,29,'#E8EFED')
    b.footer('Source: synthetic invoice lines + payment allocations. Audit files preserve source hashes and key evidence.')
    b.write(p/'join.svg')

if __name__=='__main__':
    profit(); comparison(); join()
    print('Built three editable SVG decision notes.')
