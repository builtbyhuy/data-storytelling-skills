---
name: business-insight-diagnosis
description: Diagnose business performance and turn verified findings into a supported choice. Use when a user asks why a KPI changed, which customers/products/channels explain a result, whether an anomaly matters, or what action the evidence supports. Pure chart formatting, narrative polishing, and statistical test selection have separate methods.
license: MIT
metadata:
  version: "3.5.1"
---

# Business Insight Diagnosis

Use the requested artifact language and locale; otherwise follow the user's language, with English as the fallback. Adapt to the actual audience, subject and medium; historical examples do not set language or scenario defaults.

Connect a measured pattern to the business decision it changes. A useful diagnosis states what happened, distinguishes explanation from hypothesis, establishes why it matters, and selects a proportionate action. A familiar finding or justified decision to keep the current course can be valuable; do not invent surprise, urgency, or a causal story.

## Scope, inputs, and output

Work from supplied data, queries, metric extracts, or sufficiently verified prior analysis, together with the business question, relevant period, and available context. Infer routine definitions when their meaning is clear and state consequential assumptions. Ask for a missing input only when it changes a calculation or decision that cannot otherwise be bounded.

For a narrow KPI question, reuse adequate calculations and verify the decisive definitions. Do not force a new exploratory pipeline. For a fuller diagnosis, inspect the underlying data and produce the requested memo, finding table, analysis note, or decision brief. Include enough calculation evidence to check the decisive claims; a dashboard or slide deck is optional unless requested.

Identify the job of the deliverable before choosing its content. A report preserves useful detail; a dashboard monitors defined signals; a decision story helps a named reader choose a response now. For a requested decision brief, do not deliver a dashboard of equally prominent KPI cards. Establish the contrast that separates the feasible choices, then give that contrast the main explanation or visual. Keep reconciliation and secondary findings available as supporting evidence.

The result should contain, in the requested output language:

- A direct conclusion and the choice it supports.
- The relevant measured contrast, with its population, period, unit, denominator, and source.
- Supported explanations and competing hypotheses, with any missing evidence that separates them.
- The consequence for this decision, including material limits or counterevidence.
- A concrete action, bounded test, diagnostic check, or informed non-action; include a proposed responsible role, evaluation window, outcome measure, and decision rule where these are useful.

Do not label a recommendation as implemented or an estimated gain as achieved. Use [the evidence and handoff contract](references/evidence-contract.md) for consistent facts, claims, limitations, and action status. Compact prose is sufficient for a small task; introduce IDs when several artifacts need to share the same facts.

## Diagnose the result

1. **Frame the choice.** Identify the audience's decision authority, feasible alternatives, business objective, time horizon, and relevant constraints. Separate the metric the user reported from the outcome the decision is meant to improve.
2. **Establish the analytical basis.** Define the target quantity (estimand), row grain, keys, eligible population, period, units, filters, and denominators. Check material duplicate counting, field-specific missingness and zeros, join expansion, and coverage changes. Derive a reported quantity and its eligible count from the same records. For raw CSV joins, the optional [join audit](references/join-audit.md) predicts row multiplication and additive-measure distortion and saves key-level evidence without creating an expanded join. Reconcile the relevant totals. Use the finest available, permissible grain needed for this question; aggregated data does not justify claims about unavailable individual behavior.
3. **Choose the revealing contrast.** Ask which comparison could change the choice, not which technique could generate another chart. Compare, trace a trend, segment a change, inspect an influential case, or examine a relationship according to that question. An overall result may need a process-based split to reveal a failure or opportunity; a second dimension is useful when competing explanations predict different intersections. These are alternatives or complementary checks, not a mandatory sequence. Consult the relevant section of [analytical methods](references/analytical-methods.md) when measurement, completeness, transformation, weighting or distribution remains unresolved; familiar arithmetic does not require loading the full guide.
4. **Develop and challenge the explanation.** Translate the calculation into a business consequence without jumping from a contrast to a cause. Test the plausible alternative that could change the action. Consult [explanation and action](references/explanation-and-action.md) for an unresolved mechanism, prioritization or action-design question. Reuse guidance already loaded in this task; unchanged references do not need a second read.
5. **Select and verify the response.** Match the action's cost, reversibility, and risk to the evidence. If the data supports a bounded decision, make it. If cause remains unresolved, specify the most useful discriminating check or experiment rather than stopping at "more analysis needed." Check the decisive arithmetic wherever it appears, including factual notes, then check claim strength and feasibility before handoff.

Choose mean, median, quantiles, totals, or rates according to the estimand and distribution. A skewed distribution does not make an arithmetic mean false. A median does not answer expected cost or reconcile a total. Report uncertainty that matters to the choice; a business threshold and a statistical threshold answer different questions.

Before handoff, state the diagnosis in a plain sentence linking the observed contrast, its business consequence, and the supported response. If the mechanism is unresolved, make that visible in the sentence; a useful localized failure or decision bound does not need an invented root cause. Select the evidence that makes this sentence assessable. A technical statistic becomes useful when translated into the operating quantity it changes—for example, affected orders, hours, contribution, or service exposure—under explicit assumptions.

For a brief or chart, give the reader a clear path from the comparison to its implication. Place the relevant base, unit, period, population and consequential limitation where the comparison is read. Explain unfamiliar measures in reader language. A headline and decorative number cannot substitute for evidence of the contrast; excessive precision and repeated statistics can obscure the decision even when their arithmetic is correct.

## Prioritize in context

Use BUS as a conversation about **Big**, **Useful**, and **Surprising**:

- **Big:** consequence at the relevant scale, including rare but serious failures.
- **Useful:** which feasible decision the finding changes for this audience.
- **Surprising:** how it differs from the audience's expectations, if known.

BUS is a prioritization lens, not a validated score. Do not require novelty, a fixed percentage impact, a prescribed multiple of variation, or a quota of insights. Consider evidence credibility, urgency, exposure, feasible response, and contradictory findings. Preserve an important operational, safety, access, or compliance finding even when it is familiar or should not be reduced to money.

For a decision story, rank findings by what they do in the argument: establish the problem, distinguish a plausible explanation, or justify a feasible response. Promote the finding that changes the decision. Move a correct but non-decisive KPI to supporting detail rather than trying to make every finding a main insight. Keep any contrary finding that changes the choice visible in the main argument.

## Compose with available methods

Discover and read the actual installed method only when its capability is needed; preserve its execution and evidence rules. These complements are optional and are not bundled or required by this skill:

| Need | Available complement | Useful fallback when absent |
|---|---|---|
| Sampling uncertainty, hypothesis tests, regression, experiment design, or power | `statistical-analysis` | Produce defensible descriptives and specify the design, effect of interest, assumptions, and analysis still needed. Do not report an uncomputed test, interval, or causal estimate. |
| Margin, capacity, payback, break-even, or cash consequence | `business-economics` | Build a transparent bounded model from supplied inputs, units, periods, and scenarios. Separate revenue, contribution, profit, and cash; label unknown costs. |
| A material numeric handoff or several acceptance checks | `reliable-delivery` | Recompute the decisive quantities, reconcile totals, trace claims to sources, and check the delivered artifact against the request. |
| An integrated decision story or presentation | `data-storytelling` | Hand over verified facts, competing explanations, selected action, and limits for the requested narrative or visual format. |

No server, warehouse, external account, or complete suite is needed for a bounded local diagnosis. Follow the user's authorized scope; preparing an analysis does not authorize spending, changing operations, or contacting others.
