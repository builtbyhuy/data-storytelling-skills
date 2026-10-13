# From finding to explanation and action

Read this when the user asks why something happened, what it means, or what to do. Evidence can support a response before it fully identifies a cause, but the response must respect what is and is not known.

## Keep distinct claims distinct

| Claim | Appropriate form |
|---|---|
| Observation | A reproducible value, contrast, or pattern within a declared source and scope. |
| Explanation | A mechanism supported by relevant evidence, with the strength and limits of that support. |
| Hypothesis | A plausible mechanism the present data has not distinguished from alternatives. |
| Estimate | A quantity derived under stated assumptions or a model, with meaningful uncertainty or sensitivity. |
| Recommendation | A proposed response based on the evidence, constraints, and decision objective. |

Do not strengthen a hypothesis by polishing its wording. "After the change" does not mean "because of the change." A segmentation result can identify where a problem sits without proving why it arose. A conditional opportunity, expected recoverable amount, and observed outcome are different claims.

## Choose what the reader needs to understand

For a decision brief, write a provisional takeaway with its level of evidence, then choose the smallest adequate set of contrasts that supports it. Each selected finding should establish the problem, distinguish an explanation, or justify the response. An additional correct statistic belongs in supporting evidence when it does not alter one of those links. Revise the takeaway when counterevidence changes the choice; do not select evidence to protect the first wording.

A useful shape is: **observed difference → business consequence → supported choice**, with the important unresolved condition beside the link it limits. Use the audience's operating terms rather than exposing only statistical vocabulary. If a statistic describes a highly uneven distribution, explain which cases drive the total or burden and which summary answers the reader's question; do not turn skewness into a dramatic claim about all customers.

Make the decisive comparison inspectable. A short headline states the finding; adjacent values or a well-chosen graphic show the base, difference and scope. Supporting calculations can be separate. A reader should not have to combine several unexplained KPI cards or search an appendix to discover that the recommendation rests on incomplete coverage.

For example, if a closed ledger shows a contribution decline while revenue rises, the main explanation should reconcile the contribution change and identify the component relevant to the response. A detailed cost export with partial coverage can explain its matched portion, but cannot establish the cause of the full decline. A decision bound may support a pilot even while that attribution remains unresolved.

## Translate the technical finding

Build a short chain:

1. **Measured result:** What contrast was calculated, for whom, over which period, and against what base?
2. **Business meaning:** Which constraint, opportunity, cost, service obligation, or risk does that contrast affect?
3. **Response:** Which feasible decision follows, and what would change that choice?

Keep each link supported. If no action is warranted, explain which condition justifies maintaining the current course and which signal should trigger reconsideration. Avoid manufacturing an action simply because a metric changed.

Use the outcome the decision actually targets. Sales bookings, revenue recognition, collected cash, gross profit, contribution, and net profit are not interchangeable. Attributed revenue divided by advertising spend is not incremental profit ROI. Estimate a commercial consequence only under explicit cost, margin, timing, and capacity assumptions. Service, safety, access, or reliability stakes may be better expressed in their own units.

When a supported finding meets audience resistance, identify the disputed definition, explanation, or consequence. Make the evidence inspectable, acknowledge the audience's operating constraints, and connect the proposed response to a decision they can take. Use a shared comparison or a mechanism-specific test where it can resolve disagreement. Avoid blame, overstating certainty, or concealing an inconvenient result to win acceptance. A clear presentation does not establish that the audience accepted the conclusion or acted on it.

## Challenge the preferred explanation

Choose the alternatives that can materially change the response. For each relevant alternative, state:

- The mechanism it proposes.
- The pattern it would predict in available data or an obtainable check.
- Evidence for and against it.
- Whether the present evidence distinguishes it, and what next observation would do so.

Useful probes include:

| Possible error in reasoning | Discriminating check |
|---|---|
| A changed denominator or reporting rule looks like a business change | Recompute on comparable definitions and coverage; inspect counts and data lineage. |
| Recent or memorable events dominate the explanation | Inspect the relevant full horizon and comparable prior periods. |
| Only surviving customers, successful orders, or current locations appear | Seek the departed, failed, or excluded population when it affects the target question. |
| An aggregate conceals changed group composition | Compare group counts/exposure, within-group results, and the weighted aggregate. |
| A dramatic case is assumed to be typical | Check prevalence, concentration, and sensitivity to the case. |
| The action's benefit is treated as fully recoverable | Model the feasible counterfactual, affected exposure, margin, capacity, and implementation limits. |
| Evidence is selected to defend an early answer | Seek a result that would contradict that answer; retain material negative or null findings. |

A contradictory result is not clutter when it changes the decision. Explain its implication instead of hiding it in a footnote. Do not demand every bias check for an uncomplicated calculation.

## Prioritize without a novelty gate

BUS provides three audience-specific prompts: how consequential is this finding, which decision does it help, and what expectation does it revise? The third prompt is optional when the audience's beliefs are unknown or surprise is irrelevant.

Judge consequence using the real denominator, exposure, horizon, and reversibility. A small rate change can affect a large population; a large relative change on a tiny base can be immaterial. A rare high-severity event may outrank a common low-cost event. Do not impose a universal impact percentage, variability multiple, or numerical BUS score.

Select findings for expected decision value, evidence credibility, urgency, feasible response, and counterevidence. State the judgment behind the priority rather than presenting the rank as a measured truth. Include a stable aggregate or familiar issue when it answers the user's question. There is no required number of insights or minimum number of surprising findings.

## Select a response that the evidence can carry

| Situation | Response to consider |
|---|---|
| The descriptive failure is verified, and a low-risk mitigation addresses it regardless of cause | Recommend the mitigation with a check of the affected outcome. Continue diagnosis only where it changes subsequent action. |
| Cause is uncertain, and different explanations imply different costly actions | Choose the cheapest credible discriminating check or bounded experiment before committing. |
| Economics or capacity determine whether an opportunity is usable | Compare bounded scenarios and the input that flips the choice; do not treat demand potential as earned revenue. |
| The observed difference is small, imprecise, or operationally irrelevant | Maintain course or monitor a specified signal; explain the decision criterion. |
| Evidence is inadequate for the proposed high-impact intervention | Narrow the claim and select an informative, reversible response; expose the unresolved limitation. |

For a constrained allocation, compare the preferred feasible option with its strongest feasible alternative, including doing nothing when relevant. Show the incremental benefit, resource use and residual capacity, not only total returns or benefit-per-hour rankings. Respect indivisible bundles and interactions. Calculate the decision boundary in a consequential uncertain input or resource limit when the supplied facts support it; include any evidenced value of displaced work once, without double counting costs already deducted. A small reduction in capacity can invalidate an otherwise attractive bundle. Put the actionable tradeoff in the recommendation, leaving exhaustive options in supporting evidence.

An action should identify the responsible **role** when no owner is assigned, an appropriate timing or evaluation window, the outcome to watch, and the rule for continuing, changing, or stopping. Match the measure to what the action can change; recovery after a missed deadline cannot erase the original miss. Derive an outcome readout from cohort maturity, metric-period closure and source availability, not simply the end of the work sprint. Add a cost/risk limit or rollback condition when the response warrants it. Mark these as proposed details unless supplied or accepted by the user.

Write the requested choice in the main recommendation, with the tradeoff or unresolved condition that controls it. An owner/deadline/KPI list does not make an action practical if it omits the intervention, resource limit, comparison or authority required. When a headline metric cannot mature before the decision deadline, use a justified interim operating signal and state when the outcome can be read; do not promise a mature result early to make the proposal attractive.

A bounded experiment needs a stated intervention, eligible unit/population, meaningful comparison, outcome, evaluation window, and decision criterion. Avoid choosing a favorable endpoint after seeing results. Use an available statistical method when sampling uncertainty, power, clustering, or causal identification changes the decision; ordinary arithmetic does not require an experiment protocol.

## Diagnostic patterns to adapt

These are original task patterns, not claims about actual organizations or ready-made remedies. Obtain the evidence on the user's case.

| Observed pattern | Possible explanations to distinguish | Useful result |
|---|---|---|
| An unusually large account or location | Classification error, one-time event, concentration, or a distinct buyer process | Reconciled segment definition and a choice about classification, exposure management, or further evaluation. |
| Outcomes differ between groups around an operational change | Intervention effect, different exposure or case mix, concurrent changes, selection, or measurement | A comparison with counts, timing, eligible populations, and a mechanism-specific check; address disputed evidence and audience constraints without treating the group contrast as causal proof. |
| Healthy total conversion with a localized decline | Changed mix, tracking gap, or a device/funnel failure | Affected population and period, reproducible diagnostic evidence, and a scoped mitigation or test. |
| Growth concentrated in a product or channel | Availability, changed attribution, customer mix, genuine repeat demand, or temporary promotion | Contribution to growth with margin/capacity context and a choice about expansion, diversification, or a bounded test. |
| Units rise while revenue falls | Realized unit value, discounts, returns, product mix, or incompatible denominators | A reconciled value/volume/mix explanation with uncertain mechanisms identified. |
| A region × category view suggests substantial growth | Comparable observed demand, estimated market size, reachable buyers, competitive access, margin, delivery cost, or capacity | A reconciled view and scoped opportunity model that separates demand potential, reachable revenue, contribution, and profit. Check capacity, costs, and scenario uncertainty before recommending allocation; test the input that could reverse the choice. |
| Spend rises while profit falls | Saturation, delayed returns, cost changes, attribution, mix, or operational capacity | Comparable economics and a proposed allocation or experiment tied to contribution and risk. |

## Handoff and acceptance

Deliver the requested diagnosis rather than only a list of possible analyses. The decisive claims must be numerically correct, scoped to their evidence, and connected to a feasible choice. Use [the evidence and handoff contract](evidence-contract.md) when sharing facts with a chart, narrative, or other specialist.

If a key fact is missing, keep the useful result and state the conditional branches: which action follows under each plausible answer, and the concrete check needed to choose. A completed worksheet, internal score, polished headline, or successful render does not prove that a business action was taken or that its expected outcome occurred.
