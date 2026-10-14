# Visual delivery repair — 3.2.0

The user's 4K preview experience remained unsatisfactory. An independent inspection found crisp local source edges and vector/text in the existing PDF, but did not measure the chat viewer. A fixed slide shown 600px wide reduced its 18.75pt table text to about 11.7px, irrespective of 3840px raster dimensions. The repair addresses source/export quality, actual reading size and delivery routes separately; it does not claim to have diagnosed viewer compression.

## Actual method and tool changes

The composing, chart, narrative and redteam entrypoints now select [visual delivery](../shared/visual-delivery.md). All six folders carry the qualified reference and version 3.2.0; diagnosis/adoption logic is preserved. The supplement specifies reader surface/size, a practical text budget, space for the comparison, direct labels, narrow-width reflow, a suitable editable/vector path and distinct source/render/hosted inspection. It preserves requested native Office formats.

[Selective primary repository research](../shared/repository-methods.md) examined original Plot, Vega-Lite, Matplotlib, reveal.js and Marp methods, licenses and maintenance metadata. Three specific browser-rendered examples were viewed. Their libraries/themes were not installed, vendored or claimed as locally executed. Regular Marp image-based PPTX is explicitly distinguished from editable charts/text.

The original optional browser helper exports the actual authored HTML, records font sizes/bounds at declared display widths and fails missing required assets. Independent synthetic controls found four false passes during development: vertically crushed SVG text, missing SVG images, omitted text beside inline bold children, and HTML ancestor scaling. Those were repaired in the tool. [Portable regression controls](../tools/test_browser_export.mjs) then passed 10/10 on helper SHA256 `34c97412ab72856cc199466b02af793e6a569506159925a9699c1103c2e9f6a8`; another independent mixed-text positive also passed. These are mechanical controls, not an aesthetic score.

## Unfamiliar-source forward execution

A fresh-context author received the ordinary [editorial brief](../examples/05-asean-electricity/source/brief.vi.md), frozen Ember source and candidate skills, with no old example, desired answer or layout. An early executor was interrupted before creating any work files while controls ran. The final author continued calculation/creation while remaining mechanical controls were completed; the final 66-file candidate was frozen before its browser export and first complete handoff. This timing is recorded rather than described as a strict pre-first-read benchmark.

The raw snapshot has 200 original rows: five countries, 2015–2024 and four overlapping electricity source categories. The canonical measure is reported wind+solar share of domestic generation. Imports, consumption, installed capacity and all-ASEAN rankings are outside that measure. Source definitions and selected rows remain unchanged.

The first completed output was sealed before owner artifact inspection. It includes a self-contained four-page HTML report, four-page PDF, six text-based SVGs, calculations, a full source archive and relocatable recipe. **Owner output/rebuild-code edits:0.** The public subset preserves 25 original files byte-for-byte, with new packaging documentation/manifest. Source method PDF, original full ZIP and selfcheck receipts remain archival omissions, documented in the wrapper. No original report, SVG, calculation, code or recipe guide was altered for publication.

## Checks and their boundaries

- Independent source oracle recomputes all 50 country-years, all 200 source-share reconciliations, endpoint comparisons, percentage-point changes, generation growth and annual declines using Decimal from the frozen raw CSV. Material claims and plotted data are compared with that oracle separately from author selfchecks.
- Independent PDF-object checks find four A4 pages with searchable text/vector operators and 0 images; six SVGs have editable `text` and 0 `image` elements. Root views every complete PDF page and all four 375px browser views, plus the requested desktop views. Browser helper passes at 960/1280/375; author also inspected 360/390. Local in-app browser shows the actual HTML reading page, independently of PNG preview scaling.
- A separate reader receives completed artifacts without source, skill, intended answer or other reviews. It assesses recovered angle/comparison, metric/period/country scope, consequential limits and practical two-day follow-up. This is a model readback and visual proxy.
- The exact public subset recipe runs after relocation, offline with existing runtimes. Ten deterministic HTML/SVG/calculation files match byte-for-byte; all four PDF pages match text, dimensions and rendered pixels. PDF timestamp bytes are not a deterministic rebuild criterion.

Final scoped gate outcomes and any secondary observations are recorded in the example's [publication manifest](../examples/05-asean-electricity/PUBLICATION.json). Original selfcheck claims are not substituted for these independent checks. The suite's structural checks, six official skill frontmatter checks and installation byte checks are package evidence, not professional quality certification.

Human taste/comprehension, reading speed, broad accessibility, actual editorial assignment/publication and business outcomes are unmeasured. The original chat PNG surface remains unobserved. This new run has no matched baseline and does not reverse earlier ties/completion failures; [historical evaluations](README.md) and [untouched 3.1 trials](forward-v3.1.md) remain intact.
