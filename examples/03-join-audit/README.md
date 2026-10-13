# Revenue did not double. The join repeated it.

**$1,200 invoiced. $2,500 after the raw left join. $1,300 is duplication.**

![Invoice-level audit showing legitimate revenue, payment multiplicity, joined revenue and duplication, including the unpaid invoice](join.png)

A service business combines invoice lines with payment allocations to report revenue and collections. Both exports repeat `invoice_id` for legitimate reasons: one invoice has several services, and one customer pays in installments. Summing line amounts after the join repeats those amounts for each payment.

## Try this request

> I joined our invoice lines to payment allocations by invoice ID, and invoiced revenue jumped. Check the two CSVs, explain exactly where the extra money comes from, and give me a trustworthy revenue-and-collections reconciliation. Keep unpaid invoices visible. Give me a short explanation I can send to the team.

Use [invoice lines](inputs/invoice-lines.csv), [payment allocations](inputs/payment-allocations.csv), and the [source contract](inputs/source-notes.md). The sources and outcome are synthetic.

## A useful answer

[The team memo](memo.md) identifies the error, the amount, and the correction. [The invoice-level reconciliation](result/invoice-reconciliation.csv) preserves four invoices and separates billed revenue, received cash, and outstanding balance.

| Measure | Correct source value | After the raw left join |
|---|---:|---:|
| Invoiced revenue | $1,200 | $2,500 |
| Revenue duplication | $0 | $1,300 |
| Cash received | $1,050 | Not calculated from the raw join |
| Outstanding balance | $150 | Not calculated from the raw join |

The [executed join audit](result/report.json) predicts 13 left-join rows from seven invoice lines. Its [key evidence](result/key-audit.csv) locates $300 of duplication on INV-1001 and $1,000 on INV-1002. An inner join would instead report $2,350 and omit the unpaid $150 invoice, compounding two different errors.

**A cardinality pass is not a revenue pass.** `many-to-many` correctly describes the raw sources, so the helper exits successfully. That relationship still makes the revenue sum invalid. The correction is to aggregate each export at invoice grain before joining, rather than deleting legitimate lines or payments.

## Reproduce

From the repository root, with Python 3.10 or newer:

```sh
python examples/03-join-audit/rebuild.py --out ./scratch/join-example
```

Use a new output directory. The script invokes the bundled helper, verifies its amounts and row counts against an independently materialized nested-loop join, writes the corrected reconciliation, and confirms that both input hashes remain unchanged. It uses only the Python standard library.

To run only the audit:

```sh
python skills/business-insight-diagnosis/scripts/join_audit.py --left examples/03-join-audit/inputs/invoice-lines.csv --right examples/03-join-audit/inputs/payment-allocations.csv --left-key invoice_id --right-key invoice_id --expect many-to-many --left-measure net_amount_usd --out ./scratch/join-audit
```

The retained [verification receipt](result/verification.json) documents what was checked. This example proves this join failure and correction on these inputs. It does not establish a general quality or speed advantage over another method.

[Editable SVG](join.svg) · [PNG preview](join.png) · [Gallery and visual rebuild](../README.md)
