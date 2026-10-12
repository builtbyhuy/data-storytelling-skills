# Targeted evidence checks and repairs

Select checks that can change the artifact's claim or the decision it supports. Do not report a risk as a proven defect, infer motives from an error, or impose a finding quota.

## Reconcile the evidence first

For a material assertion, compare the artifact's number to its source row/label and calculation, then compare the assertion's scope to the metric definition. Check units, signs, period boundaries, source snapshot, filters, and numerator/denominator. Compare repeated values across prose, tables, charts, and summaries. Trace a benchmark or target to its source and date before treating it as a fact.

When sources disagree, try to reconcile definitions, grain, timing, filters, rounding and refresh dates. Do not silently choose the source that makes the story stronger. If the difference remains unresolved, show both comparable states or narrow the assertion to the source that is actually established. Explain the decision consequence; unresolved disagreement need not stop unrelated supported parts of the artifact.

Do not turn absent raw data into a numeric allegation. Exact visible labels may be checked against a screenshot; unlabelled mark heights are not exact observations. Neither an editable reconstruction nor visual digitization restores hidden records or proves the original denominator.

## Bias and coverage checks

| Failure mode | Evidence worth checking | Repair if the issue is demonstrated |
|---|---|---|
| Window or segment cut | Whether the selected dates, filters and segment exclusions fit the question; whether a comparable surrounding window changes the claim | Show the scope, restore relevant context, or narrow the finding; avoid mixing incompatible historical regimes |
| Cherry-picking | Material unfavorable results and contrary observations in the relevant available evidence; reasons for exclusions | Include the counterevidence and reassess the action, rather than only adding an inconsequential note |
| Confirmation bias | A plausible alternative explanation or a disconfirming test for a claimed mechanism | Separate effect from explanation, reduce causal wording, or propose the discriminating test |
| Striking case as general proof | How an anecdote, extreme case or selected example was chosen; evidence that it represents the population | Label it as an illustration or replace generalization with a supported population claim |
| Survivorship | Failed, canceled, inactive, lost, attrited or otherwise missing outcomes that belong to the denominator | Include them if available, recompute, or bound/narrow the claim and expose the coverage gap |
| Anchoring | Origin of targets, forecasts, comparison values and precise estimates | Use a grounded base and justified range; keep an unverified target labelled as a target |
| Decorative distortion | Whether perspective, symbol size, aspect ratio, smoothing, adjustable dual axes or omitted context alters the represented comparison | Repair the marks/scales and retain meaningful uncertainty/reference lines |
| Color distortion | Whether status meaning is explained and whether contrary evidence remains readable; whether color alone carries a critical distinction | Use consistent semantics and a non-color cue; restore contrast and visibility |

A sample can legitimately answer a question. Check its selection method, analyzed N, relevant coverage and uncertainty. An undisclosed convenience sample cannot establish a population-wide claim; a documented sample is not automatically a failure. Population coverage also does not prove freedom from measurement error or confounding.

For an aggregate performance difference, examine material subgroup weights when mix could change the interpretation. Compute an overall rate from the summed numerators and denominators or valid exposure weights. Compare like populations and periods. A reversal across groups may be consistent with a composition effect, but do not call every subgroup difference a paradox or assume an omitted denominator can be recovered.

## Magnitude and claim strength

- **Absolute and relative change:** retain the starting base and use both forms when either alone could mislead. A large percentage from a tiny base may have small practical impact; a small percentage on a large base may matter.
- **Rates:** distinguish percentage-point differences from relative percentage changes. Check unequal sample sizes, exposure, denominator shifts, calendar effects, changing definitions and missingness before selecting a winner.
- **Averages:** confirm the estimand. Mean, median, totals and weighted rates answer different questions; a mean–median gap alone does not make the mean invalid.
- **Causation:** correlation, sequencing, segment contrasts and co-movement do not by themselves isolate a cause. Identify what design or assumptions would support the causal claim, reduce it to association when necessary, or propose a bounded experiment if the action depends on cause.
- **Financial impact:** separate unit change, revenue, contribution margin, profit and cash. Show conversion assumptions, relevant horizon, attributable benefit, incremental cost basis and uncertainty. Use ROI only with a defined benefit-and-cost formula; a revenue-to-cost multiple is not automatically net ROI. Do not invent costs or assume every churned account removes a full period of revenue.
- **Forecasts and estimates:** label their assumptions, horizon and uncertainty. Do not treat extra decimal places as accuracy or a scenario as a measured outcome.

For visual scale review, ask what the mark encodes. Magnitude bars require zero; endpoint ranges and floating intervals are judged by their endpoints/spans; waterfalls by their signed bridge and totals. Focused nonzero line/scatter ranges can be valid with adequate labels and context. Retain correct charts rather than forcing all plots to the same baseline.

## Narrative and action checks

Check whether the headline, sequence, evidence and recommendation tell the same supported story. Remove unjustified urgency, manufactured scarcity, unauthenticated attributed quotes, and a conclusion chosen before its evidence. Keep the principal decision clear while preserving necessary complexity. Fixed chart counts, dramatic openings and rehearsal or timing quotas are optional presentation choices, not integrity tests.

A material qualification belongs next to the claim it changes. Appendices can hold detail; they cannot conceal that the headline's conclusion depends on unresolved evidence. Analogies should preserve scale and scope rather than make a minor effect feel enormous.

Trace the proposed action to the repaired evidence. An informed decision to keep monitoring or make no change can be useful. When evidence supports only a test, specify the question, proposed owner, window, measure, and decision/stop rule without implying budget or execution approval. Do not claim a benefit that was not observed.

## Choose a repair that preserves useful work

| Review state | Artifact response | Decision response |
|---|---|---|
| Source and computation disagree with a material displayed value | Recompute, update all uses of the value, and render the changed surface | Reassess magnitude, ranking, threshold and action |
| Value is right but claim exceeds its scope or strength | Narrow population/period, calibrate observation versus hypothesis, and move the limitation beside the claim | Retain, qualify or replace the recommendation according to what remains supported |
| Valid comparison lacks context that affects interpretation | Restore relevant base, denominator, subgroup, period or counterevidence | Explain whether added context changes the choice |
| Exact inputs cannot be recovered | Remove unsupported precision; show a bounded/annotated artifact and name the needed input | Use a conditional decision or a specific verification step where necessary |
| Encoding is sound and checked claims are supported | Preserve the artifact; report no material issue in the completed scope | Retain the supported recommendation without claiming untested impact |

Keep the review trail compact enough to revise the artifact from it: affected claim; observed evidence or gap; correction; decision effect; remaining uncertainty. Separate completed numerical checks, rendered visual checks, and observed reader feedback. None alone certifies professional quality or subsequent business results.
