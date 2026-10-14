# Choose and check a business chart

Use the sections needed for the actual chart. This method supports visual comparison, not a fixed aesthetic or a chart-type prohibition list.

## Choose by the reader's task

| Reader's task | Practical choices | Preserve or disclose |
|---|---|---|
| Compare categories or rank them | Horizontal/vertical bars, dots; grouped bars for a small set of series | Common scale, category definitions, the important reference value; natural order when meaningful |
| Follow change over time | Lines; area when magnitude or composition is central | Real time spacing, missing intervals, comparable periods, observed/forecast boundary, relevant events |
| Compare ranges or changes | Range/floating bars, interval plot, waterfall | Interval endpoints and definitions; signed changes; bridge arithmetic; totals distinct from movements |
| Understand a distribution | Histogram, box plot, points; density view when its estimate is supported | Sample size, unit of observation, bin or density choices, outliers and missingness |
| Assess a relationship | Scatterplot, grouped relationship view | Actual observations, important groups, units; association language unless causal evidence exists |
| Read part-to-whole | Stacked or 100% stacked bars; a simple pie for a readily understood whole; treemap for approximate hierarchy | Whole and denominator, share versus absolute size; interior segments are difficult to compare exactly |
| Locate a spatial pattern | Map if location matters; otherwise a category comparison may suffice | Geographic coverage; counts versus normalized rates; a size or color legend; missing regions |
| Judge progress against a target | KPI plus target/comparable period and a short trend | Target source, unit, period, desirable direction, absolute gap and relevant relative change |
| Look up exact values | A well-formatted table, optionally alongside a chart | Definitions, precision, sorting/filter state and total reconciliation |

Use a map rate when region population or exposure would otherwise dominate a comparison; do not normalize away the count if the decision is about workload. A pie's suitability depends on the task and distinguishable slices, not a universal slice limit. If exact segment ranking matters, provide a common-baseline comparison rather than expecting a stacked interior or area to do that job.

Write the intended reading before choosing a chart: "compare these amounts," "find where this trend changes," "see whether the total is explained by these changes," or the actual equivalent. Then select marks that expose that relation. For example, two signed component changes in the same unit can be compared on one common axis; a waterfall is useful when the reader needs the full opening-to-closing reconciliation. A row of KPI cards would make the reader perform that comparison mentally. These are task-dependent choices, not preferred templates.

When several encodings are plausible, test their reading burden with the actual values, especially long labels, close differences, negative values and important exceptions. Choose the one whose visible marks answer the question without requiring several legend lookups or an unstated subtraction. Aesthetic interest may support attention, but does not justify weakening the comparison.

## Quantitative meaning before styling

Inspect the plotted table or specification independently of the picture. Confirm aggregation grain, signs, totals, denominator, ordering, and units. Rate totals need the appropriate summed numerators and denominators, not the simple average of category rates. State transformations such as normalization, logarithms, smoothing, or rebasing and keep a route to original values.

For a waterfall, recompute opening total plus signed changes equals closing total. Check each displayed start/end level and any intermediate totals. For an interval, verify both endpoints and whether the span is min–max, confidence interval, actual start–end, or another quantity. Do not apply magnitude-bar zero-baseline repairs to valid interval/change encodings.

Prefer aligned separate panels when unrelated units would otherwise require adjustable dual axes. If dual axes are necessary for the task, explain both scales and check that their ranges were not chosen to suggest an artificial relationship. Do not smooth away material volatility, connect across missing observations without an explicit interpolation treatment, or silently remove inconvenient categories.

Use absolute changes and relative changes together when either can materially alter interpretation. Distinguish percentage points from relative percentages and show the starting base. Do not claim a quantifiable perceptual exaggeration merely from a visual impression.

## Preserve the category domain

For charts that place series on shared category positions, derive one complete ordered domain from the intended comparison, then align each series by category key. Preserve natural time or ordinal order; include eligible categories with no observation when their absence matters. Each series uses the same domain positions, including missing values at the beginning, interior or end. A union of observed categories is enough only when the intended comparison has no additional expected categories. Missing values remain native blanks/nulls or the format's supported missing representation, rather than zero, an empty string interpreted as zero, or a shortened array that shifts later values. Continuous-coordinate charts retain each actual coordinate and missing interval; do not pad them to invented categorical positions.

Native chart applications may choose category labels from one series. When that series has less coverage than others, valid longer-series values can appear with absent or displaced labels. Give the chart an explicit complete domain and align all category/value ranges and caches with it. For categorical charts, check the category label at every plotted position; for continuous time, check real coordinates, visible extent and missing intervals. Label excluded points or coverage limits without discarding the domain needed to interpret the remaining data. Axis tick thinning for readability is different from losing categories or plotting values against the wrong labels.

Verify the saved native file in the application that will display it whenever access exists: reopen it, inspect the chart and an export made from that file, and compare category identities and series endpoints with the checked plot table. Inspect each delivered export separately; a PDF produced by a different drawing path can be correct while the editable chart is wrong. XML, caches, embedded workbooks, shape counts and a successful open are useful source checks, but do not show what the application renders. Repair generation/data alignment, save again and repeat the affected display checks. Report unavailable native verification accurately rather than substituting a metadata pass.

## Attention and grouping

Keep the complete plotted data/domain while choosing a readable cadence for displayed ticks. Data completeness does not require printing every time label. Use natural interval labels and visible endpoints that let the reader locate the period, then verify the unchanged native category/value positions. For a decision about particular peaks, exceptions or changes, mark and label those actual observations on the chart; prose below an unmarked overview makes the reader hunt for the evidence twice.

Give explanatory series a clear hierarchy. Use direct labels or markers for the decisive series/points, readable supporting context for other material groups, or aligned panels when crossings make the comparison hard. Test whether the intended comparison can be located without repeatedly moving between a legend and the plot. Keep color assignments understandable across the whole handoff; reusing a prominent hue for a year in one view and a group in another requires unnecessary relearning when the views tell one story. Prefer a stable semantic role, with position, line pattern or explicit panel labeling for the other dimension. Do not remove counterevidence to make the picture cleaner.

In decomposition tables, name columns as contributions/components in the displayed output unit; retain the raw driver units separately if needed. Check a column heading and one cell together: would someone mistake a currency contribution for a price or quantity? A mathematically correct subtitle or footnote does not excuse an ambiguous header.

For an explanatory visual, name its principal question and finding before arranging the page. Read the finding headline together with the strongest mark: they should point to the same comparison. A descriptive chart label can remain as a unit/scope label; it should not replace a supported finding headline. Put supplementary business decisions and detailed sensitivity work in adjacent prose or a separate view when large KPI figures or callout boxes would compete with that comparison. Do not fill a repeated page template merely because it has empty regions.

Start with a useful reading sequence: supported takeaway, principal comparison, nearby qualification, then supporting detail or next choice. A decision artifact can place its proposed choice first when that helps the reader, then show evidence and the consequential tradeoff. These are composition options, not mandatory screen scan paths. Use position and alignment to make relationships visible before adding decoration. Select the grouping lenses that serve the actual comparison; do not force every lens into one chart.

| Gestalt lens | Useful chart application | Meaning to protect |
|---|---|---|
| Proximity | Keep direct labels near their marks; place a panel's title, unit and caveat next to that panel | Nearby items should belong together, rather than implying a relationship between separate series |
| Similarity | Give the same series the same color, shape and line treatment across views | Similar styling should denote the same category or role; distinguish actuals from forecasts |
| Enclosure | Use a light boundary or background to group a related set of panels or a selected region | An enclosure should identify a real grouping, not arbitrarily separate inconvenient evidence |
| Closure | Use a restrained partial outline or frame when the reader can still recognize the grouped region | Incomplete framing can reduce clutter; never use closure to imply missing observations or a completed trajectory |
| Continuity | Align comparable panels and preserve natural time progression so the eye can follow a series | A smooth path must not bridge missing data or imply interpolation without disclosure |
| Connection | Connect paired observations, waterfall steps, or an explicitly related transition | Connected items must have that relationship; a causal-looking arrow needs causal support |
| Figure/ground | Give the focal marks clear separation from their background and supporting context | Background evidence must remain legible and material contrary evidence must remain visible |
| Whitespace | Leave space between unrelated groups, around labels and between plot and notes | Spacing should clarify hierarchy without hiding sources, qualifications or comparison values |

Pre-attentive cues can make a focal item stand out: a darker line, accent fill, distinct shape, size, or position. Use them for the decision-relevant evidence and keep other material evidence readable. Emphasis should not make an uncertain or weakly supported result look settled.

Use a qualitative palette for categories, a sequential palette for ordered values, and a diverging palette when a meaningful reference divides two directions. Keep assignments stable across views and across titles, marks and legends within a view. If panels identify one dimension while lines distinguish another, use neutral panel titles and let color serve the lines, or separate the dimensions with another clear cue. Avoid an ordered rainbow whose hue changes do not convey ordered magnitude reliably. Remove 3D perspective, heavy grids, redundant borders, and decorative effects when they interfere with measurement; retain meaningful baselines, targets, interval marks, and reference lines.

## Compose a considered visual

Make the hierarchy visible through relative emphasis, not through a checklist of decorative objects. Begin with the space needed to read the data and labels; arrange the finding and qualification around it. A large headline is useful only if it leaves the comparison legible. Strong emphasis should select the decision-relevant relationship, not every interesting number.

- **Type has a role.** Distinguish finding, unit/scope, data labels and notes by size/weight/placement. Keep repeated roles consistent. Choose fonts that render the language correctly in the actual export. A named font, seven-level type ladder or tiny footnote convention is not a universal requirement.
- **Space expresses grouping.** Align comparable marks and labels; use consistent gaps for comparable items and a clearer separation between unrelated groups. Whitespace around a note is useful when it keeps the note attached to its claim. Empty space is not a prompt to add another card.
- **Color has a job.** Start with readable neutral context when that suits the task, then add emphasis or category meaning. If everything is accented, decide what must attract attention first and quiet the rest without making it disappear. Do not impose a fixed color count or 60-30-10 area ratio.
- **Labels reduce work.** Put decisive values and explanations beside the relevant marks; keep scope/units close to the plot. Use rounding that preserves the decision and a consistent locale. Remove redundant labels when the axis already supports the task. Explain a specialist term briefly when the intended reader would otherwise misread it.
- **Restraint protects information.** Avoid ornamental separators, decorative badges, shadowed cards or illustrations that add no meaning to this comparison. Keep boundaries when they group real content, and keep sources, uncertainty and exceptions readable. A restrained dark theme can work if contrast and hierarchy do; background color alone does not establish quality.

Give the visual one clear center of attention, enough space to compare its marks and a short visible statement of the limit that controls the conclusion. For several lines, try adjacent endpoint or inline series labels before adding a distant legend; move or separate labels if crossings or close endpoints make identity ambiguous. Show only the ticks needed to orient the reader while keeping decisive positions and exact-value access. Essential limitations need ordinary reading size and contrast, rather than a bottom footnote that requires zooming.

Use tables for exact retrieval or an operational schedule. Keep each column tied to a reader question, align numeric values, make units and any parenthetical denominator explicit, and group comparable rows. Move repeated explanations into a short shared caption, or use a separate comparison view for reasons and tradeoffs when they make the table dense. In a presentation, surface the decisive comparison above or beside the table instead of expecting the audience to parse every cell. Preserve lookup detail in an accessible table when simplifying the main view.

View the result in its destination rather than only as a full-resolution image. For an embedded chart, inspect the expected displayed width. For presentation or print, inspect the actual page/slide scale. If labels cannot be read, reorganize content, reduce nonessential text, use a more suitable aspect ratio or separate questions. Shrinking all typography usually preserves the file while losing its use.

## Accessible reading at the actual destination

An inline chart needs a name that remains correct after composition. Give title/description IDs a document-unique chart prefix, including desktop/phone variants, and resolve each ARIA reference. Inspect the actual exposed browser name of every visible chart; matching visible labels do not prove matching accessibility names. A native SVG title or `aria-label` can provide the name, and a deliberate external caption can be referenced. Do not reuse another chart's title/description by accident. Hide genuinely decorative SVGs; naming/reference checks do not establish full accessibility conformance.

Choose type size, line thickness, and spacing for the expected slide, screen, page, or print size. Read the exported output at that size; font substitutions and rasterization can change readability. Check source notes and limitations as well as the headline.

Provide redundant distinctions using direct text, markers, line patterns, or panel separation. Check important foreground/background combinations individually. A grayscale preview helps reveal lost separation but does not test every color-vision condition or accessibility need. Alt text should describe the question, main pattern, material qualification, and where exact values are available. Complex charts may also need a longer description or accessible table.

For web charts, WCAG 2.2 provides scoped checks: normal text uses at least 4.5:1 contrast; large text uses at least 3:1; graphical parts necessary to understand the chart generally use at least 3:1 against adjacent colors, subject to the criterion's exceptions. Large text means the standard's defined size/weight, not merely the biggest text on the chart. Measure underlying colors without rounding a failing ratio up to a pass. Text and marks that meet these checks do not establish full conformance; relevant semantics, keyboard access, interaction states, and content alternatives still matter.

Primary guidance checked 2026-10-12: [WCAG 2.2 contrast minimum](https://www.w3.org/TR/WCAG22/#contrast-minimum), [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), and [use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html). Recheck applicable guidance when the target or requirements change.

## Final surface review

First reconcile the saved data and material claims with one checked calculation result. Use that result to populate chart points, rounded labels, tables, callouts and factual notes; if a format needs separate authoring, compare its extracted content to the result. Verify statements about sample sizes, ranges, zero values, coverage and eligibility against the exact variables and scope they describe. Check what is present in each output, including speaker notes when delivered, rather than assuming one correct chart makes every statement correct.

Then inspect the chart inside its destination as well as on its own. Verify that:

- The title and the visible values support the same claim and scope.
- Marks, labels, totals, endpoint spans, percentages and units agree with the accepted facts.
- The chart shows material context and counterevidence; any hidden detail has an explicit route.
- Limits, ticks, ordering, aspect ratio and selected filters support a faithful comparison.
- All series retain the intended category positions and missingness; native display and delivered exports have been checked separately.
- No important label, note, interval, mark or control is clipped, overlapped or unreadable.
- The delivered source can actually be edited or rebuilt; the export opens and retains the intended size and appearance.

Read each portable artifact independently, including a PDF that omits speaker notes and workbook context. The reader must be able to identify what is counted, the unit and denominator, the relevant period/population, and any assumption or coverage limit that changes the choice from visible content in that file. Distinguish events from unique entities, observed history from a forecast, and a source's time-bin label from an operational start/end time when those meanings matter. Retain detailed methods elsewhere, but place the decision-changing definition or assumption beside its claim. Links and companion files support deeper checking; they do not repair a misleading visible label.

A brief reader check can help reveal a confusing comparison. Show the chart without the explanation used to create it, and ask what is measured, which comparison supports the main finding, and what qualification changes its interpretation. If the answer depends on a long verbal rescue, inspect encoding, wording, grouping or density and repair the cause. A model readback is a useful ambiguity check; report it as such. Report human feedback only when it was actually observed. A timed heuristic, internal score, or completed render is not evidence of measured comprehension or business success.

Separate two review questions: whether the values, geometry and labels are correct, and whether the reading hierarchy helps someone answer the business question. A clipped-text check, contrast ratio or numeric pass cannot establish effective composition or accepted taste. Inspect the visual at its actual destination width; if several large figures, accent colors or boxed explanations compete for attention, revise the emphasis and recheck the reading task.
