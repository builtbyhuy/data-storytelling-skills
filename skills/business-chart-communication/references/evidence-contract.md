# Evidence shared across analysis and communication

Use one consistent source of facts when several methods contribute to a task. This can be a short note or a calculation file; a database, schema service and formal ID system are optional.

## Establish meaning before comparing

Record the authoritative input/snapshot and which source wins a conflict. For each consequential metric establish grain/key, eligible population, period/timezone, unit/currency, definition, filters, exclusions and denominator. Distinguish booked, recognized and net revenue; returns, gross profit, contribution, cash and attributed advertising return. Inspect duplicate keys, joins and missingness where they could change the answer. Reconcile headline totals and their components. A screenshot provides only values actually visible; absent values remain unknown.

Keep an unspecified currency, timezone or accounting basis explicitly unspecified; a familiar symbol or plausible default is not a confirmed definition. Use a labeled assumption only when needed to proceed, and show whether it changes the decision.

When a source correction or coverage change affects a trend, separate that measurement change from the like-for-like business comparison. Identify the common population/window, show the old-to-corrected bridge where available, and avoid applying a correction calculated on a different cohort. If those records are unavailable, bound or narrow the affected claim.

## Pass facts and claims between methods

For multiple artifacts, stable identifiers make contradictions easier to detect:

| Item | Useful fields |
|---|---|
| Source | `source_id`, snapshot/file/query reference, authority and freshness |
| Metric | definition, grain/key, population, period, unit, filters, denominator |
| Fact | `fact_id`, value, source or reproducible calculation, scope |
| Claim | `claim_id`, text, supporting `fact_ids`, strength and limitations |
| Action | proposal, accountable role, window, measure, decision rule, status |

Claim strength distinguishes observation, hypothesis, estimate/scenario and recommendation. Keep consequential counterevidence and unknowns attached to the claim they affect. Formal IDs are unnecessary for a one-sentence KPI answer; meaning and source still matter.

Reuse sufficient supplied calculations and confirmed definitions. If a later method discovers an error, update the authoritative fact and every affected chart/title/message; do not silently replace just one number. Keep a compact replay record when useful: input snapshot, calculation/transform version, material checks and the resulting artifact. Evidence review checks truth and interpretation; a commit/release check concerns the actual action authority. Handoff includes the requested artifact, decisive facts, genuine unresolved issues and action state. Prepared, checked, approved, executed and observed outcome are separate states.

## Check proportionately

Recompute material numbers independently where feasible, match chart marks to values, inspect the actual rendered output and check the strongest relevant competing interpretation. Percent change uses its stated base; percentage-point differences subtract rates. Aggregate patterns can reverse within segments. Correlation and before/after comparisons alone do not establish an intervention's effect. Revenue/spend is not profit ROI.

Choose a concrete supported recommendation when asked. With unresolved causation, a bounded diagnostic or reversible experiment can still be useful: specify what is done, which observation distinguishes alternatives, who can decide and the stop/continue rule. Do not invent a price, return, owner name or approval to make the ending decisive.

Use existing statistical, economics, spreadsheet/document/chart and verification methods when they contribute to the requested output and are available. These skill instructions grant no tool entitlement or additional permission to send, publish, spend or mutate external systems.
