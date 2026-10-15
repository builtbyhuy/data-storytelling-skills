# Revenue rises, contribution falls: what should change?

[One-page PDF](brief.pdf) · [Editable SVG](brief.svg) · [Excel workbook](analysis.xlsx) · [Full memo](memo.md)

![Meeting memo: contribution bridge, the limit caused by VND 3 million of unallocated freight, and a conditional delivery trial proposal](brief.png)

Revenue rose by VND 44.10 million, but contribution fell by VND 4.05 million. The VND 6.85 million freight increase exceeded the VND 2.80 million gross-profit increase. Freight detail is still missing for VND 3 million, so segment results cannot yet be fully determined.

**Proposed direction:** keep B2B within its current scope and prepare a standard-delivery trial for orders with suitable delivery deadlines. Launch only after reconciling unallocated freight and confirming commitments, pricing, staffing, and budget. The plan retains a current-practice group, tracks every assigned request, and separates the intake cutoff from the date when results are complete. The EXPRESS/STANDARD freight difference is not a guaranteed saving.

## Supply the request

Copy [brief.md](brief.md) together with the five files in [inputs/](inputs/). Source exports retain their original bytes; amounts are whole VND, excluding VAT, with credits assigned to the posting month and freight to the service month. Finance's month-end close is the official total; overhead has not been deducted.

## Operational handoff

- [Four-week trial plan](test-plan.md): launch conditions, assignment unit, capacity, limits, metrics, reading dates, and keep/stop rules.
- [Completed decision record](decision-record.csv): proposal, approval, execution, and outcome statuses are kept separate.
- [Calculations and sources](analysis.json): totals, segments, coverage, sensitivity, and SHA256.
- [Workbook](analysis.xlsx): source, summary, segment, price, and definition sheets. Formula caches were checked against the sources; the workbook has not been recalculated in Excel.

## Rebuild

```text
python examples/01-profit-decision/rebuild.py --output ./scratch/profit-v3
```

See the [gallery](../README.md) for dependencies and limits. The script is tied to this snapshot and rejects changed sources to avoid retaining outdated conclusions. The workbook is editable; memo content needs review when the numbers change.

The data and names are synthetic. This curated version began with an independent execution using six version 3.0 skills, then received edits based on page reading and source checks. The limits, 60 requests, VND 1 million, VND 5,000, and trial schedule are proposals requiring confirmation, not existing policies, predicted effects, or completed work. The original report and artifact files retain the Vietnamese requested for that run; they illustrate an example, not a language restriction. New work follows its intended audience and requested language, format, and domain.
