# Independent Wine Quality source audit

Completed: 2026-10-15T03:51:52.444379+00:00

Scope: original red/white CSV bytes and dictionary/SOURCE metadata, followed by the permitted private oracle comparison. No trial method, authored story/output, source-owner algorithm, prior case output, or child agent was used. Python standard library and in-memory SQLite were invoked only through the required Windows Python helper. The reliable-delivery numeric handoff guidance was applied.

The independent receipt was saved at 2026-10-15T03:49:10.296378+00:00, before this auditor read oracle content. Candidate freeze metadata records 2026-10-15T03:43:44.466752+00:00; this source audit occurred after that freeze. Freeze timing and owner answer visibility are recorded metadata, not independently proven by raw CSV bytes.

## Raw counts and thresholds

All raw rows are retained, excluding only the header. The `quality <= 5` threshold is the task's descriptive grouping of an ordered 0..10 sensory score.

| Source | Data rows | Fields | <=5 count | >5 count | <=5 / all rows |
|---|---:|---:|---:|---:|---:|
| red | 1,599 | 12 | 744 | 855 | 46.5290806754% |
| white | 4,898 | 12 | 1,640 | 3,258 | 33.4830543079% |
| Combined | 6,497 | 12 | 2,384 | 4,113 | 36.6938587040% |

These are ratio-of-sums values (`low count / raw row count`), never an unweighted mean of red and white percentages. Both files have the expected identical header, every row has 12 fields, no empty cells, no invalid/nonfinite numeric cells, and no quality value outside integer 0..10. All category counts and the threshold partition reconcile to row counts.

| Quality | Red | White |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 2 | 0 | 0 |
| 3 | 10 | 20 |
| 4 | 53 | 163 |
| 5 | 681 | 1457 |
| 6 | 638 | 2198 |
| 7 | 199 | 880 |
| 8 | 18 | 175 |
| 9 | 0 | 5 |
| 10 | 0 | 0 |

Observed categories: red 3,4,5,6,7,8; white 3,4,5,6,7,8,9. Zero-count documented categories remain explicit.

## Exact row-vector patterns

Equality means all 12 parsed CSV field strings are identical, without rounding or trimming numeric values. SQLite TEXT-column grouping supplies the independent calculation. `Beyond first` is sum(frequency−1); `all participating` is sum(frequency) over repeated patterns. Neither means confirmed accidental duplicate physical samples. No rows were dropped.

| Source | Repeated vector groups | Beyond first | All participating | Distinct vectors |
|---|---:|---:|---:|---:|
| red | 220 | 240 | 460 | 1359 |
| white | 772 | 937 | 1709 | 3961 |

Ignoring source type, there are 993 repeated vector groups, 1,179 occurrences beyond first and 2,172 participating rows; two exact vector patterns occur in both source files (five participating rows). Every detailed repeated vector and every one-based row address agrees with the oracle. The receipt also records numeric-normalized sensitivity separately from exact-string equality.

## Hypothetical 40-record desktop plan

Reviewer A can be assigned red data rows 1–20 and reviewer B white data rows 1–20, each with `source_file + data_row`; header excluded, physical lines 2–21. All 40 addresses resolve and are distinct row addresses, and their quality values agree with the oracle. Six repeated exact vectors appear in this subset (12 participating rows, six beyond first). This does not establish 40 unique physical samples or a representative/random sample.

The resource arithmetic is hypothetical: 2 reviewers × 20 records × 3 minutes = 120 staff minutes. With equal parallel workload and no overhead, elapsed time is 20 × 3 = 60 minutes (one parallel hour). No reviewer was scheduled and no desktop or physical audit was performed.

## Oracle and source provenance

Formal private-oracle comparison: **52 checks passed; zero mismatches**. Checks cover row counts, headers/width, missing/numeric/quality validation, all 0..10 counts, threshold counts and proportions, exact vector summaries and complete memberships, all 6,497 raw-line hashes/row identities, combined/cross-file patterns, the first 40 addresses/values and source/private snapshot stability. Floating ratios compare at 1e-12 tolerance; integer and membership checks are exact.

Three private files changed externally between schema inspection and formal comparison. This audit wrote only source-independent/. All private oracle files stayed unchanged within the formal comparison; source hashes stayed unchanged across the whole audit. The formal snapshot is the compared version.

| File | Source SHA-256 before = after |
|---|---|
| wine+quality.zip | `3ed56667f4b828242bd732d7d1dd7f2861e54432239d7fa63877014cbb0304d4` |
| winequality-red.csv | `4a402cf041b025d4566d954c3b9ba8635a3a8a01e039005d97d6a710278cf05e` |
| winequality-white.csv | `76c3f809815c17c07212622f776311faeb31e87610d52c26d87d6e361b169836` |
| winequality.names | `15d215e73b39105952380fd487e4ce1bf5a6b83a425abb285c2ec55193d3ca92` |
| LICENSE-CC-BY-4.0.txt | `9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411` |

Retained source byte sizes and hashes agree with SOURCE.md. Both CSVs and the dictionary equal their retained official archive members byte for byte.

| Private file | Initial schema-inspection SHA-256 | Formal comparison SHA-256 before = after |
|---|---|---|
| wine-source-oracle.json | `c87fc2edf3ae5b4497bcef9fb200dd1204ac467f960b9121c4b013fb0fb830e4` | `7af4fad1cac40b3734ff6c145fd187bba3bda74807bc67d0a4918a36e67335c3` |
| wine-source-checks.json | `795ce45409c7761c856edcbe4f5657d9cee8ee1892fd4a68e839091b535d72f5` | `b0277635f54f0a26b574e53608450f794e28230aba3a942f1e35ae79c3318cfb` |
| wine-powershell-crosscheck.json | `3c72eda299a3c9a33fb137102a78c7802a65fcca5176543a67e7067ce0ed64a4` | `24d79fb2c846515131ef36b7e871c344536257d671957c49dc966a6e0160977b` |
| wine-duplicate-patterns.json | `ae192203f54ea7d41a015c912b7af667a0d0057f359eda81046285c33c76212b` | `ae192203f54ea7d41a015c912b7af667a0d0057f359eda81046285c33c76212b` |
| wine-record-identity.json | `536a86e3ca011a775fea8b71affef3b389a6e99dfbb323ceffafe31937863e21` | `536a86e3ca011a775fea8b71affef3b389a6e99dfbb323ceffafe31937863e21` |

## Source novelty boundary

Source-only comparison covers 2 Bike CSVs, 1 Bank CSV and 46 table CSVs across 29 main29 case directories. No wine CSV SHA-256 equals any compared prior source SHA-256, and no compared prior header equals the 12-field wine header. Details are in `novelty-receipt.json`.

Wine's source geometry is two files sharing 12 numeric fields, with 1,599 and 4,898 rows, an ordered sensory score, filename-derived type, and no time or unique sample identifier in the headers. This supports byte/schema novelty only. It does not prove new reasoning capability, better rendering, business value, an actual audit, physical sample uniqueness, representativeness or present-day wine quality.

Usable audit files: `checker.py`, pre-oracle `receipt.json`, `compare_oracle.py`, `oracle-comparison.json`, `finish_report.py`, `novelty-receipt.json` and this `REPORT.md`. No files outside `source-independent/` were written.
