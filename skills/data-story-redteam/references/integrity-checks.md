# Targeted evidence checks and repairs

Select checks that can change the artifact's claim or the decision it supports. Do not report a risk as a proven defect, infer motives from an error, or impose a finding quota.

## Reconcile the evidence first

For a material assertion, compare the artifact's number to its source row/label and calculation, then compare the assertion's scope to the metric definition. Check units, signs, period boundaries, source snapshot, filters, and numerator/denominator. Compare repeated values across prose, tables, charts, notes, and summaries. Trace a benchmark or target to its source and date before treating it as a fact.

For an absence, null or zero assertion, check and name the relevant field and eligible population. Inspect components separately when the claim includes them: a positive total does not establish positive components. Preserve the distinction between an absent record, an unmeasured value and an observed zero.

For means, rates or coverage ranges, recover the exact eligibility used by the displayed calculation. Recompute its numerator and observed count/exposure together, then compare any note or caption's denominators with those same groups. Whole-source coverage and counts for a plotted subset can both be correct while answering different questions.

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

When a full eligible dataset is supplied, calculate important headline quantities on that scope rather than silently substituting a convenient subset. If a subset is the only available basis, expose its analyzed count and coverage beside the affected value, then recompute on the full scope if available, narrow the claim, or remove it. A general caveats slide cannot repair a population-wide headline read before the qualifier.

For an aggregate performance difference, examine material subgroup weights when mix could change the interpretation. Compute an overall rate from the summed numerators and denominators or valid exposure weights. Compare like populations and periods. A reversal across groups may be consistent with a composition effect, but do not call every subgroup difference a paradox or assume an omitted denominator can be recovered.

## Magnitude and claim strength

- **Absolute and relative change:** retain the starting base and use both forms when either alone could mislead. A large percentage from a tiny base may have small practical impact; a small percentage on a large base may matter.
- **Rates:** distinguish percentage-point differences from relative percentage changes. Check unequal sample sizes, exposure, denominator shifts, calendar effects, changing definitions and missingness before selecting a winner.
- **Averages:** confirm the estimand. Mean, median, totals and weighted rates answer different questions; a mean–median gap alone does not make the mean invalid.
- **Causation:** correlation, sequencing, segment contrasts and co-movement do not by themselves isolate a cause. Identify what design or assumptions would support the causal claim, reduce it to association when necessary, or propose a bounded experiment if the action depends on cause.
- **Financial impact:** separate unit change, revenue, contribution margin, profit and cash. Show conversion assumptions, relevant horizon, attributable benefit, incremental cost basis and uncertainty. Use ROI only with a defined benefit-and-cost formula; a revenue-to-cost multiple is not automatically net ROI. Do not invent costs or assume every churned account removes a full period of revenue.
- **Forecasts and estimates:** label their assumptions, horizon and uncertainty. Do not treat extra decimal places as accuracy or a scenario as a measured outcome.

For visual scale review, ask what the mark encodes. Magnitude bars require zero; endpoint ranges and floating intervals are judged by their endpoints/spans; waterfalls by their signed bridge and totals. Focused nonzero line/scatter ranges can be valid with adequate labels and context. Retain correct charts rather than forcing all plots to the same baseline.

## Inspect the conclusion created by the surface

Review the chart or brief as delivered, at its intended reading size. Source code, an author's narration and a high-resolution zoom can explain a result that the audience-facing surface does not communicate. Record what the surface allows a reader to answer, then trace that answer to the available evidence.

| What the reader needs | Observable failure | Effective repair |
|---|---|---|
| The finding and its scope | A title declares a cause or winner while the marks show only association, partial coverage or incompatible groups | Calibrate the title and place the decisive scope condition beside the comparison; reassess the action. |
| The base and difference | A prominent percentage has no original amount, exposure or comparable period | Show the relevant base and absolute or percentage-point change; retain enough context to judge consequence. |
| The evidence for the takeaway | Equally prominent KPI cards require the reader to infer the comparison, or a dramatic isolated case stands in for the population | Give the decisive contrast a clear reading path; label an illustration as such and add the supported population evidence. |
| The limits that control the choice | A coverage gap or counterexample is present only in tiny footer text while the main recommendation reads as unconditional | Move that condition to the claim or action it changes; revise an unconditional choice when needed. |
| What the measure and operating window mean | Repeated events read as unique entities, or exposure/time-bin assumptions appear only in a companion workbook or speaker notes | Put the essential unit, relevant exposure and consequential interval assumption beside the evidence or window in every standalone artifact. |
| What to do next | The ending requests action but gives no intervention, usable measure or decision condition | Replace it with a feasible proposed response or discriminating check, including the details required by this decision. |

Simplicity means removing irrelevant competition while keeping evidence needed to evaluate the claim. It does not mean making a small effect look large, hiding a denominator, or dropping a contradictory group. Avoid treating a preferred palette, fixed chart count, decorative style or an internal aesthetic rating as an integrity rule. When design quality is within scope, assess concrete hierarchy, alignment, spacing, readable labels and consistency against the intended medium and audience.

For a launch proposal, test whether every critical prerequisite has an observable completed state, including approved resource availability for the selected work/window. A capacity ceiling, proposed measurement method or readiness-to-submit label does not establish assigned staff, equipment or partner time. Check the gate's actual meaning and any editable status logic; it may explicitly include resource approval within an existing condition. Distinguish this completeness gap from evidence that resources are actually unavailable.

Map a material completeness finding to the user's requested decision and deliverables. Verify that all used aggregates and methods are inspectable; do not require an additional national total, chart or operational record merely because it could be helpful. Label extra suggestions as optional. A real unmet prerequisite can remain material even when today's safe decision is to defer.

For a consequential chart repair, a reader or an independent reviewer can state the finding, identify its evidence and name the limitation or choice without being given the intended answer. Compare those answers with the checked source. Keep numerical accuracy, rendered legibility, model comprehension proxies and observed human feedback distinct; passing one does not establish the others.

## Check editable and exported formats

For a multi-format handoff, check the saved native file and every required export as separate artifacts. Discover connected application sessions, supported tools or bundled runtimes and attempt the needed open/render operation before reporting a capability gap. Record which renderer and format were actually inspected; a library's presence or a successful file write does not establish a native render.

For PPTX/XLSX, the optional [Office handoff checker](../scripts/check_office_handoff.py) checks OOXML category-domain/cache structure, summarizes editable objects and notes, and flags cached spreadsheet errors. Read its usage before running it with the available Python runtime. A pass covers its structural assertions only; verify source facts, factual notes and actual native rendering separately.

When a native chart has an embedded workbook or caches, compare its categories and series with the computed facts, including missing positions. For series sharing a categorical axis, check the full ordered category domain independently of any shortened series, and verify that each nonmissing value remains paired with its intended label. A missing end of one series must remain an explicit gap in that series while other measured categories remain available. Inspect both stored data and the application's visible axis: matching values alone can miss a lost or shifted label.

When stale calculations or chart caches are implicated, refresh/recalculate an authorized working copy, save it, then render the native file and regenerate its exports. Compare category sequence, labels, endpoint visibility, values and essential qualifications at the intended reading size. Keep legitimate blanks distinct from stale caches and zeros. If native rendering remains unavailable, complete source/data and available-renderer checks and name the unverified format behavior; an accurate PDF cannot certify the editable file's appearance.

## Narrative and action checks

Recover the operator as well as the population behind each growth statement: sum/value, quantity, row count and distinct count need their own calculation. A correct percentage attached only to a population noun can imply the wrong measure. Narrow that wording without alleging incorrect arithmetic when the calculation itself is sound. For a web visual, inspect table values and each exposed chart name at the required widths; hidden variant IDs and unmarked tables remain part of the delivered document.

Read derived table headings as if the cell were detached from its footnote: do name and unit identify a contribution, raw driver or rate correctly? Name the reference for each more/less/increase/decrease statement. A correct numerical decomposition can coexist with a misleading driver label or a sentence using a different unstated comparator.

Check visual effort even when the reader repeats the conclusion correctly. Ask them to locate the decisive point/series and the condition governing the next action. Flag unnecessary legend hopping, crowded or unnecessary every-point tick labels, equally prominent crossing series, paragraph tables and action blocks whose conditions are buried. Preserve the complete data/domain when simplifying visible ticks or emphasis. An understood but burdensome surface can still need repair.

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
