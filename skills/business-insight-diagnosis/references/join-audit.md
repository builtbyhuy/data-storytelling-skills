# Check a proposed CSV join

Use the bundled [join audit](../scripts/join_audit.py) when a raw-data task combines CSV exports and a repeated key could inflate an additive left-side measure or discard unmatched records. It does not replace choosing the right business keys, source authority, eligibility rules or grain. For a simple adequate summary, skip it.

Run with an available Python 3.10+ runtime; no packages or network are required:

```text
python scripts/join_audit.py --left orders.csv --right order_lines.csv --left-key order_id --right-key order_id --expect one-to-many --left-measure revenue --out work/order-line-audit
```

Use the actual script path under this skill. Repeat each key option in corresponding order for a composite key, such as tenant and order ID. `--expect` describes the intended relationship from left to right. Choose it from the source contract, not the observed duplicates. A lookup of many orders into one current customer row would be `many-to-one`; history often requires an effective-date match that this equality-only helper cannot select.

`--out` must be a new directory. Inputs are read only. UTF-8 CSV, including BOM, is supported. Keys remain exact strings, preserving zeros, case and surrounding spaces. Missing or whitespace-only keys, malformed rows, duplicate/blank headers and invalid numeric measures fail explicitly. A literal `NA` is a valid string key; translate source-specific null sentinels only when the source contract establishes them, retaining the source and transformation evidence. Measures must be plain decimal numbers without grouping commas, currency symbols, spaces or exponents, in one known unit. Do not fill missing money with zero to make an audit pass.

The outputs are:

- `report.json`: source hashes, source/key counts, expected relationship violations, predicted inner/left/full join sizes, unmatched counts, and optional exact left-measure totals before and after a hypothetical join. Amounts are decimal strings to preserve precision.
- `key-audit.csv`: one record per distinct key, with left/right multiplicities, predicted join rows and amounts, including unmatched keys. This supports finding the contributing keys without creating the expanded table. `key_json` encodes the composite key unambiguously.

Exit 0 means the declared cardinality holds. Exit 1 means it fails; the report and key evidence are still produced. Exit 2 means invalid input or an output error; do not treat partial output as a completed audit. None means the analysis is correct. Inspect unmatched records, population, units and measure grain even when cardinality holds.

For example, an order worth 100 joined to three lines yields 300 if its order-level revenue is summed. A valid one-to-many relationship does not make that sum valid. Aggregate at the original grain or use a documented allocation. Zero and offsetting positive/negative amounts can conceal fanout in totals, so check the row counts and repeated-key evidence too. When a relationship fails, determine whether the key is incomplete, rows are duplicate exports, or versions/events genuinely repeat; do not automatically drop duplicates or select the last row.

This tool audits equality joins only. It holds input content, key maps and evidence in memory; use database-side checks for sources that exceed local memory. It does not execute the join, clean data, infer a relationship, assign revenue to segments, reconcile snapshots, choose an as-of record, calculate business KPIs or establish causation. Keep its evidence in working files and put only decision-relevant consequences into the reader's memo.
