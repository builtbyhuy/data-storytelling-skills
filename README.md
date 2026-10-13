# Data Storytelling Skills · 3.0

Turn business data into a choice someone can understand, check and act on. Six complementary Codex skills cover diagnosis, narrative, charts, evidence repair and recurring measurement. English instructions support Vietnamese and English requests.

The 3.0 revision follows a complete reread of the supplied 89-page MDA guide. It changes the actual methods: decision-relevant contrasts, evidence sequencing, reader/grain/channel choices, visible qualifications, chart composition and practical action handoffs. [See the source-to-execution map](shared/source-method-map.md).

## See the work

### 01 — Doanh thu tăng, đóng góp giảm: nên đổi gì?

A meeting memo reconciles the change, exposes unallocated freight and proposes a bounded delivery test. Its workbook, plan and populated decision record separate checked facts from an unexecuted proposal.

![One-page Vietnamese decision memo: contribution falls from 35.00 to 30.95m VND; 3m unallocated freight limits the B2B conclusion; proposed delivery pilot has explicit prerequisites and decision rules](examples/01-profit-decision/brief.png)

[Open the one-page PDF](examples/01-profit-decision/brief.pdf) · [Editable SVG](examples/01-profit-decision/brief.svg) · [Workbook](examples/01-profit-decision/analysis.xlsx) · [Request, source, plan and rebuild](examples/01-profit-decision/README.md)

### 02 — “Tăng 50%” chưa chứng minh coaching có hiệu quả

The corrected report preserves the true overall rates, shows the different lead populations and keeps the causal limit beside the conclusion. The proposed next decision follows from that evidence.

![One-page Vietnamese sales review comparing observed overall rates with common-mix rates, retaining tier denominators and the missing coaching-assignment and observation-period limit](examples/02-fair-comparison/brief.png)

[Open the one-page PDF](examples/02-fair-comparison/brief.pdf) · [Editable SVG](examples/02-fair-comparison/brief.svg) · [Ready-to-use repaired claim](examples/02-fair-comparison/memo.md) · [Request and source](examples/02-fair-comparison/README.md)

### 03 — Tiền bị tính lặp ở đâu khi ghép bảng?

A six-cell invoice example shows the repetition. The accounting table retains all four invoices, separates billed revenue from cash and preserves the unpaid balance. The executed audit is checked against literal joins.

![One-page Vietnamese join explanation and four-invoice reconciliation:1,200 USD billed, 1,050 USD collected,150 USD unpaid; raw joins duplicate both revenue and cash](examples/03-join-audit/brief.png)

[Open the one-page PDF](examples/03-join-audit/brief.pdf) · [Editable SVG](examples/03-join-audit/brief.svg) · [Accounting CSV](examples/03-join-audit/invoice-reconciliation.csv) · [Request, audit and rebuild](examples/03-join-audit/README.md)

These synthetic examples began as fresh independent executions of the revised skills using raw inputs and realistic briefs, without old outputs or intended answers. The published copies incorporate reader-review and portability edits. They are curated handoffs, not untouched trials, customer outcomes or aesthetic certification. [Gallery and use instructions](examples/README.md) · [3.0 checks and limits](evals/book-aligned-v3.md).

## Choose the job

| Skill | Job |
|---|---|
| `data-storytelling` | Select and combine the work needed for a multi-output request |
| `business-insight-diagnosis` | Explain changes, prioritize findings and choose a supported action/test |
| `evidence-to-narrative` | Write a reader-ready memo, email draft or slide argument |
| `business-chart-communication` | Produce or repair an editable communication chart |
| `data-story-redteam` | Challenge and repair misleading claims, charts and recommendations |
| `analytics-adoption` | Plan recurring metric stewardship, decisions and outcome learning |

All six skills are version 3.0.0. A narrow KPI question stays short; a decision memo does not require all six methods.

## Give a normal request

> Từ dữ liệu này, giải thích biến động, chọn việc nên làm, tạo biểu đồ và viết memo ngắn cho giám đốc. Kiểm số liệu và giữ rõ các giới hạn kết luận.

> Repair this chart and its conclusion. Preserve the source, show relevant denominators, and deliver an editable chart plus a concise decision-ready explanation.

The assistant can select complementary methods for one prompt. Direct invocation such as `$data-storytelling` is also available. Descriptions support discovery; they are not an autonomous scheduler or a guarantee that every client selects correctly.

## Install

Copy the six folders under `skills/` into your client's discoverable skill directory, commonly `~/.codex/skills`. Each folder includes its references. Automatic invocation is enabled.

```text
python tools/install.py --dest ~/.codex/skills
python tools/install.py --dest ~/.codex/skills --apply --replace --backup-dir ./private-backups
```

The first command previews. Replacement requires a backup directory and preserves unlisted existing resources. The skill package and optional CSV audit require no dependency download, server, credential or MCP setup. Use an available Python runtime. Refresh stale client metadata or start a fresh chat when needed. Example PDF/workbook rebuilding has separate optional local rendering dependencies; viewing the delivered files needs no rebuild.

## Complement the existing stack

Use available statistical methods for inference, economics for cost/capacity/scenarios, figure tools for demanding charts, native Office/PDF methods for actual formats and verification methods for numeric handoffs. Those capabilities are referenced, not bundled or required under a particular brand. The suite creates no tools, accounts or permissions.

Canonical shared references live under `shared/`; `python tools/sync_shared.py` updates independently installable copies. `python tools/validate.py` checks package structure, links, source boundaries and copies. These checks do not establish output quality.

The optional [CSV join audit](skills/business-insight-diagnosis/references/join-audit.md) predicts row multiplication and repeated additive amounts with exact keys/decimals, source hashes and key-level evidence. It does not infer source authority, business key or eligible population. [Independent black-box tests](tools/test_join_audit.py) previously passed 13 groups / 48 invocations; the new invoice example also runs the unchanged helper against materialized joins.

## Source and evidence

This independently authored suite adapts useful ideas from the user's MDA guide using original wording and qualified scopes. It is not an MDA or OpenAI product. [Coverage and operational qualifications](shared/source-method-map.md) include source advertising, unverified business cases and rigid heuristics. The original ebook and page images remain private. Only newly authored example PDFs are distributed. [Attribution](NOTICE.md).

The 3.0 checks cover actual artifacts, source calculations, narrow controls and model reader inspection. No human comprehension, accepted taste, beneficial adoption or real intervention outcome has been measured. The profit workbook's cached values and formula presence were checked; an Excel recalculation engine was not run.

Earlier matched evaluations remain in [the historical record](evals/README.md): quality ties and candidate completion-limit failures are retained. The suite has no demonstrated overall quality, speed or completion advantage over an unassisted model. The new runs use different output requirements and no matched baseline, so they do not change that conclusion.

## License

[MIT](LICENSE) covers this project's original instructions, tools and synthetic examples. The source ebook and complementary third-party skills are not relicensed or redistributed.
