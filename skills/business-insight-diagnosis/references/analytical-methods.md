# Analytical methods for business diagnosis

Read the sections that answer the question. A correct comparison with relevant context can be enough; more techniques do not automatically produce more insight.

## Establish what the numbers describe

Write a short analytical basis before transforming data:

| Item | Question it resolves |
|---|---|
| Business process and grain | Is one row an order, order line, account, session, shipment, or period summary? |
| Keys and joins | What uniquely identifies the record, and can a join repeat a measure? |
| Target quantity | Are we estimating a total, typical record, rate, expected cost, tail risk, or difference? |
| Eligible population | Which records or exposures can appear in both numerator and denominator? |
| Period and calendar | Is this event time, cohort time, or recognition time? Is the window complete and comparable? |
| Definitions | Which refunds, discounts, tax, cancellations, missing records, or currency conversions affect the metric? |
| Source and snapshot | Which file, query, or source version supports the result, and when was it current? |

Scope these checks to what could change the conclusion. A supplied aggregate with clear definitions can support aggregate findings. It cannot reveal the distribution of its underlying records or effects within a missing segment.

Check uniqueness at the declared grain. Compare row counts and totals before and after a join. Joining orders to lines can validly increase rows while making a repeated order-level revenue field unsafe to sum. Aggregate the measure at its own grain or allocate it under an explicit rule before combining it. Retain the exclusions and reasons needed to reproduce material totals.

Align populations and periods before comparison. A new location, changed tracking rule, incomplete week, different attribution window, or switch from cohort retention to calendar retention can mimic performance change. If alignment is impossible, report the scoped contrast and its limitation rather than silently treating it as like-for-like.

## Select summaries by the decision

- Use a **total** when the decision concerns the amount of work, money, or exposure.
- Use a **mean** for an arithmetic expectation, resource planning, or an additive total divided by its relevant count.
- Use a **median** or other quantile for a typical record or a service threshold. Ties and even sample sizes mean the median need not be one observed record.
- Use **tail proportions or percentiles** when unusually costly, slow, or harmful cases drive the decision.
- Use a **rate** with the eligible exposure denominator when counts arise from different amounts of opportunity.

Inspect spread, shape, sample size, missingness, and relevant subgroups when the summary could conceal distinct experiences. A mean-median gap is a clue about shape, not a rule for discarding a mean. Multimodal data may need meaningful segmentation rather than a single "typical" value. A coefficient of variation is unstable near a zero mean and is not a universal alarm threshold.

## Transform only for a question

Preserve units, bases, and formulas in the working evidence:

| Quantity | Calculation and interpretation |
|---|---|
| Absolute change | Current minus baseline, in the original unit. |
| Relative change | `(current - baseline) / baseline`; zero is undefined and negative bases need domain-specific interpretation. Choose an absolute change or a justified alternative rather than reporting infinite growth. |
| Rate change | Current rate minus baseline rate in percentage points; relative rate change divides that difference by the baseline rate. Label both distinctly. |
| Aggregate rate | Sum of eligible numerators divided by sum of corresponding denominators. Averaging group rates without their exposure weights changes the target quantity. |
| Plan variance | Actual minus plan, with a direction label. Higher revenue and higher defect counts do not have the same business meaning. |
| Share or contribution | Segment amount divided by the applicable total, with non-overlapping segments when shares must reconcile. |
| Per-unit value | Relevant amount divided by orders, customers, units, hours, or another named denominator. Order value, customer value, and realized unit price are different quantities. |

Use unrounded values for computation and consistent displayed precision. Normalizing, indexing, taking a log, or smoothing may help a specific comparison; retain the original scale and make the transformation visible. Do not silently change the denominator or use smoothing to remove an inconvenient incident.

## Compare

Compare a result with a relevant prior period, control group, plan, operating requirement, or credible benchmark. Check equivalent definitions, eligible exposure, calendar, and measurement coverage. State why the comparator answers the business question. A convenient last period is not always a relevant counterfactual.

Separate **magnitude** from **precision**. Show the actual difference or ratio and the group sizes/exposures. If the available observations are a complete operational population for the stated period, distinguish that exact descriptive result from uncertainty about future performance or a broader population. Formal inference needs a design that addresses independence, clustering, selection, and the target effect; do not add a p-value simply to make a business contrast look authoritative.

## Trace a trend

Start with consistent intervals and a relevant horizon. Inspect partial periods, weekday/seasonal patterns, exposure, reporting delays, measurement changes, and unusual events. Put operational changes on the timeline as candidate explanations.

A coincident release, campaign, price change, or policy is evidence of timing, not proof of causation. Compare unaffected populations or longer history when those can discriminate mechanisms. Show the raw incident and the underlying pattern when smoothing is used. A forecast must state its model or scenario assumptions; an extrapolated short incident is not observed future loss.

## Segment and reconcile a change

Choose segments from the business process and decision, such as acquisition cohort, product, geography, customer type, or device. Use combinations when a single split could conceal a relevant interaction. Avoid an exhaustive search followed by selective reporting of only striking cells.

For additive totals, compute each segment's change and verify that the contributions sum to the total change within stated rounding or scope. Distinguish a segment's large share of the total from its share of the change. Check whether a group's movement reflects its own performance, its exposure, or a changed mix of groups.

For rates, retain numerator and denominator counts. Examine within-group rates and the weighted aggregate when group composition changes. A common-mix or matched-cohort comparison can answer a different, useful question; label that question and keep the observed aggregate. An aggregate reversal does not make either arithmetic result false.

For identities such as revenue = units × realized value per unit, choose and disclose a decomposition convention. Volume, price, discounts, returns, and mix can offset one another. Some bridges assign the interaction term differently; reconcile the chosen bridge and avoid implying that an arithmetic contribution is a causal effect. Do not double count overlapping slices in an impact total.

## Inspect outliers and influence

Determine whether an unusual record is an error, a rare valid event, or a repeated business pattern. Inspect source records, classification, concentration, timing, and relevant counterparts. An outlier may reveal a failure or opportunity; its unusual position alone does not establish either.

Keep valid observations in the primary descriptive result. Show sensitivity with and without an influential case when that changes the interpretation, and distinguish the sensitivity from a justified correction or exclusion. Document an error correction and its effect. Do not remove records because the desired claim becomes cleaner.

## Examine relationships

Plot or inspect the joint pattern before reducing it to a coefficient. Check scale, direction, nonlinearity, time alignment, influential observations, subgroup composition, and whether records are independent. Correlation measures association under a chosen definition; it is not a return-on-investment measure or a causal mechanism.

Consider reverse direction, common causes, selection, and shared denominators. A regression can adjust for measured variables without eliminating unmeasured confounding. When the decision requires an incremental causal effect, define the intervention and counterfactual and choose a justified design. If that design is unavailable, retain the association as a clue and choose a test or lower-risk response that does not rely on a causal promise.

## Keep the necessary evidence

Retain the formulas or query, source/snapshot, relevant counts, reconciliation, and sensitivity that support the decisive claims. Preserve consequential contrary results. The final diagnosis should expose the evidence needed to assess the choice, while detailed calculation notes can sit outside the main narrative.
