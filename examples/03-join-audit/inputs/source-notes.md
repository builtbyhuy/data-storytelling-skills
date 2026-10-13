# Source contract

This is a small synthetic service-business example. It demonstrates an equality-join accounting error; it is not a real customer outcome.

- `invoice-lines.csv` contains one row per invoice line. `line_id` is unique. `net_amount_usd` is the billed amount after discounts, excluding tax, in USD. Sum these rows once to measure invoiced revenue for this closed example period. There are no refunds, voids, currency conversions, opening balances, or unlisted invoices.
- `payment-allocations.csv` contains one row per received payment allocation against an invoice. `allocation_id` is unique. `received_amount_usd` is allocated cash in USD. An invoice can have several allocations. This export contains all payments received against the four invoices by the common cut-off. An invoice absent here is unpaid, not missing from the revenue population.
- `invoice_id` is an exact, shared business key, but is not unique in either export. Multiple invoice lines and multiple payments are legitimate. Joining the raw exports on this key creates combinations of lines and payments.
- Invoiced revenue and cash received are separate measures. A payment does not recognize the invoice line a second time. To reconcile at invoice level, aggregate each export by `invoice_id`, then join those invoice-level tables and retain unpaid invoices.

The inputs are retained unchanged. The generated report records their SHA-256 hashes. Published source paths are normalized to portable repository-relative names; numerical helper output is unmodified.
