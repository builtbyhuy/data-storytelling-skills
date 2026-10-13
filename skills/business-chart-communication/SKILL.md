---
name: business-chart-communication
description: Create or repair decision-focused business charts, dashboard panels, and slide visuals from data or a bounded existing graphic. Deliver an editable chart source and an inspected export with faithful values, scales, labels, and context.
license: MIT
metadata:
  version: "3.1.2"
---

# Business chart communication

Deliver the requested chart, editable source and export inspected at its intended viewing size. A specification or critique alone does not complete a chart-making request. Work directly from a table, accepted facts or an existing graphic plus its sources; the full story suite need not run first.

## Establish what the chart can say

Reuse an established [evidence contract](references/evidence-contract.md), or consult relevant parts for unresolved metric meaning or authority. Carry forward sufficient supplied facts and preserve their source snapshot, definition, unit, denominator, population, filters and period.

Set the reader, question/decision, decisive comparison, metric/unit, scope/period and destination size/format. Specify what the reader should be able to compare or conclude. Use a table for precise lookup. Choose a supported finding headline; a question or descriptive title is appropriate when no stronger takeaway is established.

Separate input states:

- **Data or verified facts available:** reconcile plotted values and preserve rebuild transformations.
- **Only a screenshot/PDF graphic available:** use exact visible labels with their scope. Do not derive exact values from unlabelled marks or invent hidden rows. Identify partial coverage; unseen values are unknown, not zero or absent.
- **Required values unavailable:** make a useful annotated redesign or editable layout with unknowns visible, and name the smallest missing input. Label requested illustrative numbers beside the chart. A layout is not a verified reconstruction.

## Build the comparison

Use [chart choices and rendering checks](references/chart-method.md) when choosing an encoding or repairing scales, color, layout, or accessibility.

Choose encoding before styling. If unclear, compare plausible encodings using actual values: which exposes the decisive relationship with less decoding? Prefer shared position/length for precise comparisons; a reconciliation may need a bridge. Preserve natural time/stage/ordinal order; sort for ranking. Keep a working chart type rather than replacing it for a template or novelty.

Treat the mark's meaning as the baseline rule:

- Magnitude bars and filled areas start from zero; signed values extend on the correct side.
- Range/floating bars preserve both endpoints and label their meaning; a zero origin changes that question.
- Waterfalls distinguish totals from changes and reconcile each start/end level and the complete bridge.
- Lines/scatterplots may use a disclosed focused range; keep enough context and avoid exaggerating differences through aspect ratio or title.

Distinguish missing, zero, excluded, estimated, forecast, target and observed values. Use shared scales for comparable panels, scale bubble quantities by area, and display uncertainty only with supplied or validly calculated meaning and values.

For a chart that places several series on shared category positions, establish the full ordered category domain before adding any series. Align every series to that domain, preserving missing positions as missing. A shorter first series must not truncate the categories of a longer series. Continuous-coordinate charts retain actual coordinates and intervals. Check both the saved chart data and the target application's actual display; see [the category-domain procedure](references/chart-method.md#preserve-the-category-domain).

## Make the reading path intentional

Compose an explanatory view around its principal comparison: headline states the finding, plot demonstrates it, direct labels locate decisive values, and nearby context qualifies it. Equally prominent KPI figures, accent panels and repeated callouts can obscure that relationship. Put other questions or detailed calculations in adjacent prose or another view. Multi-purpose dashboards still need readable tasks and routes to detail.

Use position, color, size or line weight to emphasize relevant evidence while preserving readable alternatives and counterevidence. Apply useful Gestalt cues such as proximity, similarity, grouping and whitespace; the reference gives concrete applications. Connections must represent real relationships. No color quota, scan path or claimed perception time is a quality gate.

Keep color meaning stable across views: category, ordered magnitude, meaningful midpoint or explained status. Within a view, a title, mark and legend using the same color should not encode different dimensions. Use neutral panel titles or a different cue when panel identity and plotted series need different distinctions. Red is not automatically bad. Pair consequential distinctions with text, shapes, patterns or line styles.

Titles/labels/visible notes identify metric, unit, period, population, comparison and material limitation in each delivered artifact. A measurement distinction or assumption that changes the decision belongs beside the evidence or recommendation at readable size; speaker notes and a companion workbook cannot supply it for a standalone PDF. Keep number formatting consistent. Preserve exact-value access where useful. Dashboards retain selected filters, refresh/as-of state, source and meaningful controls.

Use aligned edges, consistent type roles and spacing for finding, data reading and notes. Place labels near their marks; direct series labels can remove repeated legend lookups when they fit without ambiguity. Give the principal comparison the most room, keep the decisive caveat in its reading path, and use a compact table only for details the reader must look up. Reduce repeated prose or separate questions before shrinking essentials. A considered composition needs no fixed brand style, canvas or palette recipe.

## Produce and inspect the real files

Use available tools for the requested format. For native spreadsheet, presentation or document charts, consult the relevant artifact method and discover the actual application/runtime before choosing the creation and verification path. Retain editable native charts, text-based SVG, or an editable specification with data/rebuild source; a raster alone is insufficient. Keep labels editable. Export static/interactive results and a static fallback when use requires it.

Inspect the saved editable file and every delivered export at destination size: values/geometry, scales/spans, the full category domain, labels, order, clipping/overlap, type, context and panel consistency. When native application access is available, reopen the saved file there and inspect its display or an export made by that application. A separately drawn preview, embedded data, object count or chart cache cannot establish the native render. If native access is unavailable, name that unverified surface and inspect the usable export. Interactive charts also need relevant control/selection, hover/keyboard and static-export checks.

Build material values, labels, table entries and factual speaker notes from the same checked calculation results. Reconcile the delivered text as well as the plotted data against those results, including sample sizes, ranges, zeros and missingness statements. A correct workbook does not prove an independently typed note correct.

Measure contrast for essential text/marks, provide useful text alternatives and redundant color distinctions. A palette name or grayscale preview does not establish accessibility. Repair observed failures and reinspect affected output.

Review use separately from numeric/export checks. Can the reader identify the comparison, main pattern and decision-changing qualification without layout explanation? Does the first attracting mark/text serve that task? Repair competing emphasis, unclear grouping, unexplained terms or density. A render, contrast pass or internal rating does not certify taste or human understanding; distinguish reader feedback from model inspection.

## Compose only the missing capability

When useful and available, use `scientific-visualization` for demanding plotting, `statistical-analysis` for estimators/uncertainty, `reliable-delivery` for material numeric reconciliation and the artifact skill for the requested format. These are implementation aids, not prerequisites. Complete bounded work with available tools and report an actual limitation. Chart-only work does not add an unrelated business recommendation or organization audit.

## Handoff

Deliver editable source, inspected export, revisable values/scope/transformations and the supported comparison. Propagate checked fact corrections to affected claims. State checks and use-relevant unknowns; file creation does not prove understanding, adoption or business impact.
