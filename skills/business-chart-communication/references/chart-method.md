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

## Quantitative meaning before styling

Inspect the plotted table or specification independently of the picture. Confirm aggregation grain, signs, totals, denominator, ordering, and units. Rate totals need the appropriate summed numerators and denominators, not the simple average of category rates. State transformations such as normalization, logarithms, smoothing, or rebasing and keep a route to original values.

For a waterfall, recompute opening total plus signed changes equals closing total. Check each displayed start/end level and any intermediate totals. For an interval, verify both endpoints and whether the span is min–max, confidence interval, actual start–end, or another quantity. Do not apply magnitude-bar zero-baseline repairs to valid interval/change encodings.

Prefer aligned separate panels when unrelated units would otherwise require adjustable dual axes. If dual axes are necessary for the task, explain both scales and check that their ranges were not chosen to suggest an artificial relationship. Do not smooth away material volatility, connect across missing observations without an explicit interpolation treatment, or silently remove inconvenient categories.

Use absolute changes and relative changes together when either can materially alter interpretation. Distinguish percentage points from relative percentages and show the starting base. Do not claim a quantifiable perceptual exaggeration merely from a visual impression.

## Attention and grouping

For an explanatory visual, name its principal question and finding before arranging the page. Read the finding headline together with the strongest mark: they should point to the same comparison. A descriptive chart label can remain as a unit/scope label; it should not replace a supported finding headline. Put supplementary business decisions and detailed sensitivity work in adjacent prose or a separate view when large KPI figures or callout boxes would compete with that comparison. Do not fill a repeated page template merely because it has empty regions.

Start with the reading order: headline, principal comparison, evidence/context, then supporting notes or exact values. Use position and alignment to make relationships visible before adding decoration. Select the grouping lenses that serve the actual comparison; do not force every lens into one chart.

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

Use a qualitative palette for categories, a sequential palette for ordered values, and a diverging palette when a meaningful reference divides two directions. Keep category assignments stable across views. Avoid an ordered rainbow whose hue changes do not convey ordered magnitude reliably. Remove 3D perspective, heavy grids, redundant borders, and decorative effects when they interfere with measurement; retain meaningful baselines, targets, interval marks, and reference lines.

## Accessible reading at the actual destination

Choose type size, line thickness, and spacing for the expected slide, screen, page, or print size. Read the exported output at that size; font substitutions and rasterization can change readability. Check source notes and limitations as well as the headline.

Provide redundant distinctions using direct text, markers, line patterns, or panel separation. Check important foreground/background combinations individually. A grayscale preview helps reveal lost separation but does not test every color-vision condition or accessibility need. Alt text should describe the question, main pattern, material qualification, and where exact values are available. Complex charts may also need a longer description or accessible table.

For web charts, WCAG 2.2 provides scoped checks: normal text uses at least 4.5:1 contrast; large text uses at least 3:1; graphical parts necessary to understand the chart generally use at least 3:1 against adjacent colors, subject to the criterion's exceptions. Large text means the standard's defined size/weight, not merely the biggest text on the chart. Measure underlying colors without rounding a failing ratio up to a pass. Text and marks that meet these checks do not establish full conformance; relevant semantics, keyboard access, interaction states, and content alternatives still matter.

Primary guidance checked 2026-10-12: [WCAG 2.2 contrast minimum](https://www.w3.org/TR/WCAG22/#contrast-minimum), [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), and [use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html). Recheck applicable guidance when the target or requirements change.

## Final surface review

Inspect the chart inside its destination as well as on its own. Verify that:

- The title and the visible values support the same claim and scope.
- Marks, labels, totals, endpoint spans, percentages and units agree with the accepted facts.
- The chart shows material context and counterevidence; any hidden detail has an explicit route.
- Limits, ticks, ordering, aspect ratio and selected filters support a faithful comparison.
- No important label, note, interval, mark or control is clipped, overlapped or unreadable.
- The delivered source can actually be edited or rebuilt; the export opens and retains the intended size and appearance.

A brief reader check can help reveal a confusing comparison: can the intended reader identify what is measured, the principal pattern, and its limitation? Report observed feedback only. A timed heuristic, internal score, or completed render is not evidence of measured comprehension or business success.

Separate two review questions: whether the values, geometry and labels are correct, and whether the reading hierarchy helps someone answer the business question. A clipped-text check, contrast ratio or numeric pass cannot establish effective composition or accepted taste. Inspect the visual at its actual destination width; if several large figures, accent colors or boxed explanations compete for attention, revise the emphasis and recheck the reading task.
