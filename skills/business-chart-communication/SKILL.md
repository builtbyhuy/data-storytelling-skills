---
name: business-chart-communication
description: Create or repair decision-focused business charts, dashboard panels, and slide visuals from data or a bounded existing graphic. Deliver an editable chart source and an inspected export with faithful values, scales, labels, and context.
license: MIT
metadata:
  version: "2.0.0-local"
---

# Business chart communication

Turn the user's comparison into a usable chart. The result is the chart itself, its editable source, and an export checked at the intended viewing size. A chart specification or design critique alone does not complete a request to make or improve a chart.

This specialist can work directly from a table, accepted facts, or an existing chart plus its sources. It does not require the composing skill or the other specialists to run first.

## Establish what the chart can say

Read the [evidence contract](references/evidence-contract.md). Carry forward sufficient supplied facts; do not repeat analysis merely because a new stage began. Keep the same source snapshot, metric definition, unit, denominator, population, filters, and period in the chart and its notes.

Set a compact chart brief: intended reader; question or decision; important comparison; metric and unit; scope and period; delivery format and expected size. Use a table when precise lookup is the main need. Choose a finding headline after examining the evidence; a clear question or descriptive title is appropriate when no stronger takeaway is supported.

Separate input states:

- **Underlying data or verified facts available:** reconcile the plotted values to those inputs and preserve transformations needed to rebuild the chart.
- **Only a screenshot or PDF graphic available:** copy exact visible labels with their scope. Do not derive exact values from unlabelled marks, invent hidden rows, or claim to have recovered the dataset. An exact-label-only redraw must identify its partial coverage and must not imply that unseen or unlabelled values are zero or absent.
- **Values required for a faithful redraw unavailable:** produce a useful annotated redesign or editable layout with unknowns visibly marked, then name the smallest missing input needed to finish the numeric chart. Label any requested illustrative numbers as illustrative beside the chart. A layout is not a verified reconstruction.

## Build the comparison

Use [chart choices and rendering checks](references/chart-method.md) when choosing an encoding or repairing scales, color, layout, or accessibility.

Choose the simplest encoding that makes the required comparison readable. Keep natural time, stage, and ordinal order; sort categories when ranking is the question. Prefer common-position or length encodings when small quantitative differences matter. Keep the existing chart type when it already works.

Treat the mark's meaning as the baseline rule:

- Ordinary bars and filled areas that encode magnitude start from zero. Signed values extend on the correct side of zero.
- Range or floating bars encode two endpoints. Preserve their actual spans and label the endpoints or interval meaning; a zero origin would change the question.
- Waterfalls encode a reconciled sequence of changes and totals. Distinguish subtotal/total bars from change bars and verify that each change bridges the correct starting and ending level.
- Lines and scatterplots may use a focused nonzero range when disclosed and useful. Preserve enough comparison context and avoid an aspect ratio or title that exaggerates a small difference.

Keep missing, zero, excluded, estimated, forecast, target, and observed values distinguishable. Use shared scales for panels intended to be compared. Scale a quantity encoded by bubble area by area. Show uncertainty only when its meaning and values are supplied or validly calculated.

## Make the reading path intentional

Use pre-attentive differences such as position, size, color, or line weight for a real focal point; preserve readable alternatives and counterevidence. Choose suitable Gestalt cues: proximity, similarity, enclosure, closure, continuity, connection, figure/ground, and whitespace. The reference gives concrete applications; a chart need not use every lens. Do not connect unrelated items just to create visual unity. No color quota, fixed scan path, or claimed perception time is a quality gate.

Use color semantics consistently across panels: categories, ordered magnitude, a meaningful midpoint, or an explained status. Red is not automatically bad. Pair color with labels, shapes, patterns, or line styles for consequential distinctions.

Make the title, subtitle, axis labels, and nearby notes jointly identify the metric, unit, period, population, comparison, and material limitation. Keep abbreviated numbers, decimal precision, locale, and currency consistent. Label decisive values directly when it improves reading; preserve exact-value access through a table where useful. For a dashboard, retain the selected filters, refresh/as-of state, source, and meaningful controls.

## Produce and inspect the real files

Use the requested format and the available chart, spreadsheet, presentation, or plotting tools. For standalone delivery, an editable native chart, text-based SVG, or editable chart specification plus its data and rebuild source can serve as the source; a raster image alone cannot. Keep labels editable where the format allows it. Export the requested static or interactive result, with a static fallback when the use needs one.

Open or render the delivered files at their actual size. Check the value-to-mark mapping, axis limits, endpoint spans, legend and direct labels, ordering, clipping, overlap, typography, visible context, and panel consistency. For interactive charts, also test the relevant controls, selected state, hover and keyboard behavior, and the static export rather than assuming they match.

Check specific text and essential marks for contrast, add a useful text alternative, and ensure color is not the only carrier of meaning. A palette name or grayscale preview does not establish accessibility. Repair observed failures and inspect the affected output again.

## Compose only the missing capability

When available, use `scientific-visualization` for demanding plotting, uncertainty displays, or publication figure mechanics; use `statistical-analysis` for a required estimator or uncertainty computation; and use `reliable-delivery` for material numeric reconciliation or several acceptance checks. Use the relevant artifact skill for the requested file type. These are optional implementation aids, not prerequisites or copied resources. If unavailable, complete the same bounded chart work with the tools on hand and state any actual limitation.

Do not rerun the full story suite for a chart-only job. The chart specialist owns encoding, reading hierarchy, and visual delivery; it does not add an unrelated business recommendation or an organization-wide audit.

## Handoff

Deliver the editable source and inspected export, the values/data scope and transformations needed to revise them, and a short explanation of the comparison the chart supports. Update shared facts or claims only when a checked correction changes them. State what was verified and any remaining unknown that affects use. A successful export establishes file creation; it does not prove audience understanding, adoption, or business impact.
