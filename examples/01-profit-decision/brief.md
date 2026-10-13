# Sales grew. Contribution fell.

**A practical example:** choose a reversible B2B price test without confusing sales growth, gross profit, delivery cost and net profit.

Copy this request into your agent with the five files in `inputs/`:

> I run an office-supply business. Sales grew from June to July, but contribution after delivery fell. Should we reduce B2B sales, change discounts, or change delivery? Use the attached invoice lines, credit notes, carrier charges and closed finance ledger. Give me a short decision memo, a reconciled calculation I can rebuild, and a four-week proposed test with an owner, guardrails and a clear readout. Keep accounting periods correct. Tell me what the data cannot establish.

## What to inspect

- [The decision memo](memo.md) makes the choice and retains the limits that matter.
- [The four-week plan](test-plan.md) distinguishes setup, action, early monitoring and a mature outcome.
- [The arithmetic](analysis.json) and [compact evidence](evidence.csv) reproduce the values.
- Run `python rebuild.py` with Python 3.9+ to rebuild from the public source files. Standard library only; run from any directory.

## Disclosure and source meaning

All business names, transactions and figures are **synthetic**. The source exports are copied unchanged from the independent instructional fixture, whose synthetic source snapshot is dated 7 August 2026. They demonstrate analysis and communication mechanics, not a client result, actual adoption, improved profit, or superiority over another model.

Amounts are integer VND, excluding VAT. Contribution means net sales minus net COGS minus **all recognized outbound freight**; overhead remains outside this metric. The closed management ledger supplies the monthly totals. The connected carrier export supplies shipment detail but omits VND3m of July freight. Its missing carrier, customer and reason cannot be recovered from these files. Credit notes stay in their posting month, including ten July lines referring to June invoices.

`source-notes.md` retains the original Vietnamese source definitions. No private fixture or hidden allocation is included or needed. `analysis.json` and `evidence.csv` are derived outputs; `memo.md` and `test-plan.md` are proposed examples, not executed actions.
