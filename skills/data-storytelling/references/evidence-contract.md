# Evidence shared across analysis and communication

Use one consistent source of facts when several methods contribute to a task. This can be a short note or a calculation file; a database, schema service and formal ID system are optional.

## Establish meaning before comparing

Record the authoritative input/snapshot and which source wins a conflict. For each consequential metric establish grain/key, eligible population, period/timezone, unit/currency, definition, filters, exclusions and denominator. Distinguish booked, recognized and net revenue; returns, gross profit, contribution, cash and attributed advertising return. Inspect duplicate keys, joins and missingness where they could change the answer. Reconcile headline totals and their components. A screenshot provides only values actually visible; absent values remain unknown.

Keep an unspecified currency, timezone or accounting basis explicitly unspecified; a familiar symbol or plausible default is not a confirmed definition. Use a labeled assumption only when needed to proceed, and show whether it changes the decision.

Profile missing, zero and invalid values by field and eligible population. A zero in one component is compatible with a positive total; an absent row is a different state. Attach a claim such as "no zeros" or a sample-size range to its actual field, filters and period, using the computed result rather than a recollection of the analysis.

When a source correction or coverage change affects a trend, separate that measurement change from the like-for-like business comparison. Identify the common population/window, show the old-to-corrected bridge where available, and avoid applying a correction calculated on a different cohort. If those records are unavailable, bound or narrow the affected claim.

## Pass facts and claims between methods

Every comparative phrase needs an identifiable reference: more than which group, higher than which period, or changed from what base? Name it in the sentence or an unmistakable adjacent label. A page can contain a cross-group comparison and a year-on-year comparison; sharing a page does not make their reference interchangeable. Label derived components by their meaning and displayed unit. A cost decomposition component associated with a price or usage change is a cost contribution, not the raw price or usage measurement.

If a sentence or note discusses several periods, attach each displayed value to its own period. A single current-period value beside “both years” can imply the value is identical in both; use the two values or an unambiguous statement about the pattern. Keep this check on factual speaker notes as well as visible text.

For multiple artifacts, stable identifiers make contradictions easier to detect:

| Item | Useful fields |
|---|---|
| Source | `source_id`, snapshot/file/query reference, authority and freshness |
| Metric | definition, grain/key, population, period, unit, filters, denominator |
| Fact | `fact_id`, value, source or reproducible calculation, scope |
| Claim | `claim_id`, text, supporting `fact_ids`, strength and limitations |
| Action | intervention and eligible scope, accountable role, comparison, mature window, measure, decision rule, status |

Claim strength distinguishes observation, hypothesis, estimate/scenario and recommendation. Keep consequential counterevidence and unknowns attached to the claim they affect. Formal IDs are unnecessary for a one-sentence KPI answer; meaning and source still matter.

Reuse sufficient supplied calculations and confirmed definitions. If a later method discovers an error, update the authoritative fact and every affected chart/title/message; do not silently replace just one number. Keep a compact replay record when useful: input snapshot, calculation/transform version, material checks and the resulting artifact. Evidence review checks truth and interpretation; a commit/release check concerns the actual action authority. Handoff includes the requested artifact, decisive facts, genuine unresolved issues and action state. Prepared, checked, approved, executed and observed outcome are separate states.

Pass the intended reader task alongside the facts: which comparison the reader needs, which choice it informs and which limit controls that choice. Select the explanatory evidence after analysis, including consequential counterevidence. Details may live in linked working evidence, but a qualifier that changes the main recommendation belongs beside that recommendation.

Give each independently consumed artifact its own minimum reading context: what is counted, eligible scope, comparison denominator or exposure, and the assumption or limit that changes the choice. Put these near the relevant evidence in visible content. Speaker notes and linked workbooks can add derivations; they do not supply a missing essential definition in a standalone PDF. Reuse computed facts for captions, table cells, notes and summaries, and check each factual surface, including explanatory prose.

## Check proportionately

Treat truth, comprehension and visual effort as separate checks. A reader may recover the right answer from dense prose or a complicated legend while still finding the artifact difficult to use. Observe how they locate the decisive mark, compare alternatives and find the action condition. Correct readback alone does not dismiss a concrete density, unit-label or scanning problem.

Recompute material numbers independently where feasible, match chart marks to values, inspect the actual rendered output and check the strongest relevant competing interpretation. Percent change uses its stated base; percentage-point differences subtract rates. Aggregate patterns can reverse within segments. Correlation and before/after comparisons alone do not establish an intervention's effect. Revenue/spend is not profit ROI.

For a visual or document handoff, also perform the actual reading task at the intended size: find the conclusion, read its decisive comparison, identify the important qualification and locate the proposed response. A successfully exported file or matching numeric labels cannot establish this on its own. Independent model review is a comprehension proxy; observed human feedback and business outcomes remain separate evidence.

For several requested formats, inspect the final bytes in each format's actual renderer when available. Compare visible category labels, missing-series behavior, units, notes, ranges and decisive values across the requested files; a shared generation object is not that comparison. Discover available application/export capabilities before declaring a format or check unavailable. When native rendering is unavailable, state the specific fidelity check that remains unknown and keep a derivative preview distinct from the requested artifact.

Choose a concrete supported recommendation when asked. With unresolved causation, a bounded diagnostic or reversible experiment can still be useful: specify what is done, which observation distinguishes alternatives, who can decide and the stop/continue rule. Do not invent a price, return, owner name or approval to make the ending decisive.

For an operational proposal, distinguish stated resource ceilings and a plan from confirmed ability to carry out the selected work. Where launch depends on assigned staff, equipment, partner time or access during the required window, make their availability and approval an observable prerequisite. It may be part of an existing budget/measurement gate rather than an extra checklist, but define what that confirmation covers. Missing critical resource evidence means defer or revise; do not invent quantities or impose an operational plan on a simple factual answer.

Use existing statistical, economics, spreadsheet/document/chart and verification methods when they contribute to the requested output and are available. These skill instructions grant no tool entitlement or additional permission to send, publish, spend or mutate external systems.
