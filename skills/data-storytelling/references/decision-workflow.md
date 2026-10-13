# From a question to a usable decision handoff

Use this reference for work that spans several artifacts or responsibilities. It connects the business brief, authoritative facts, reader-facing explanation and feasible next action. A settled KPI question can be answered directly without this record.

## Select the job before selecting the medium

| Intended use | Minimum useful result | What changes the work |
|---|---|---|
| Know the current state | Sourced value, definition, comparison if asked | Unclear metric meaning or incomplete coverage |
| Detect a condition and respond | Condition, evidence, threshold basis, affected scope and response owner | Freshness, false alarms, authority and a usable response window |
| Understand an explanation | Reconciled change, tested alternatives and calibrated interpretation | Grain, measurement changes, confounders and missing evidence |
| Choose an action | Options, decisive evidence, feasible recommendation and outcome test | Economics, capacity, guardrails and decision deadline |

These uses can overlap. A request to explain falling contribution and write a price-test memo needs diagnosis and communication; a request for this week's contribution needs its calculation and source. Monitoring does not authorize an alert or background job.

## Build a compact brief from the available context

Use TOSCAR to resolve the gaps that matter. The working brief can be a paragraph rather than a form.

| Context | Translate into something usable |
|---|---|
| Trouble | What is wrong or uncertain, compared with what, and why this matters now |
| Owner | Who uses the answer and can make the actual choice; separate an evidence steward from the decision owner |
| Success | Desired outcome, definition, applicable population and evidence window |
| Constraints | Deadline, capacity, budget, access, fixed rules and relevant tradeoffs |
| Actors | Who executes, reviews or is affected; use roles when names are unknown |
| Reference | Previous attempts, known alternatives and the comparison that would make this decision fair |

Record unknowns explicitly. Do not invent a budget, permission, actual owner or target to make the brief appear complete. A desired result is a target; an expected explanation is a hypothesis. Neither is an observed fact.

Connect this brief to the data-generating process. For a delivery question, a dispatch event, invoice row, carrier charge and closed finance total describe different things. Identify the authoritative source and grain for each decisive fact, the person or role who resolves definition conflicts, and the source's finalization time. A shared local file and agreed definitions may cover this responsibility; a new warehouse is not a prerequisite.

## Keep one evidence-to-choice record

The useful intermediate product is a small record that another method can consume without redoing analysis:

| Component | Example of what belongs here |
|---|---|
| Finding | The actual change, eligible population, unit and period |
| Explanation | Which mechanism is established, which is only plausible, and which alternative was ruled out |
| Decisive support | Source or calculation for each fact used in the headline and recommendation |
| Decision relevance | How the finding changes the available choice or exposes a relevant risk |
| Bound | Missing coverage, causal limit or scenario assumption that could change the choice |
| Response | Feasible action or diagnostic, accountable role and proposed/approved status |
| Readout | Outcome the action can change, comparison, mature evidence date and stop/continue rule |

Formal IDs are useful when multiple files reuse facts; they are optional for a short memo. Keep counterevidence with the affected claim rather than hiding it in an unrelated disclaimer.

Keep quantitative facts in one computed result or a verified supplied result, including the precise variable, eligible scope, denominator and display rounding. Use it to populate values repeated in charts, tables, callouts, captions and factual speaker notes. Derive sample-size ranges and coverage statements from that result rather than typing approximate ranges from memory. Qualitative claims such as "no zeros" also need an exact variable and scope: a statement verified for a total column does not extend to its component columns. Recompute the decisive facts independently where feasible, then check the resulting content across files; sharing a generation source prevents drift but does not prove its calculations correct.

Draft the main sentence after this record is credible. For example: “The closed ledger shows contribution fell as freight grew faster than gross profit; test the proposed price change on an eligible segment, while reconciling the unallocated freight before assigning blame.” The claim does not turn a finance bridge into a causal effect estimate. The actual test scope, figures, owner and rules come from the task's evidence.

## Hand off the right layer

When a rebuild/update handoff is requested, give a recipient an executable recipe: retained file structure, exact working directory and commands, required local capabilities/platform, how to find or configure their locations, and where fresh outputs go. Configuration-variable names and a dependency list alone do not establish a usable setup. Use relative input paths or documented configuration without personal machine paths. Exercise the supplied recipe in a separate working/output location when capabilities are available; preserve the delivered snapshot, report which steps actually ran and state any remaining setup limitation. Keep technical setup in the supporting handoff rather than cluttering the decision pages.

- The reader-facing artifact gives the supported takeaway, decisive comparison and requested choice in language suited to that reader.
- Supporting evidence makes source meaning, calculations, exceptions and uncertainty inspectable. It can be a short note, CSV or working file.
- The action record tells the authorized team who decides, who executes, which guardrails apply and when the result can be evaluated.

An executive may need the tradeoff and approval request; the operator needs eligible cases, concrete steps and exceptions. Both use the same definitions and claim bounds. A dramatic hook, an Aha, a slide deck and all five specialists are optional; the decision should remain understandable without them.

## Make each artifact work alone

Identify which files may be forwarded, projected or read independently. In each, put the information needed to interpret the decision in visible content: what the metric counts, unit, denominator/eligible population, period, observed-versus-proposed status, and the limitation or assumption that could change the choice. The level of detail follows the use. For example, repeated events are not unique entities, historical averages are not a forecast, and a recorded time-bin label needs an explicit mapping before it becomes an operational interval. Use the task's actual distinctions, not a universal disclaimer list.

Speaker notes, hidden sheets, a companion workbook and external links can carry derivations or deeper methods. They cannot supply a definition that makes an otherwise ambiguous visible claim correct. A PDF without notes still needs its own decisive context. Put a short qualifier beside the affected chart or recommendation at ordinary readable size; collect secondary provenance in a source section within the file. Repeating a short controlling qualifier is appropriate when an action page must stand alone.

Shape the reading around the choice: a supported takeaway or proposal, the evidence that changes it, the consequential tradeoff, and the next decision or test. Allocate the most space to the comparison, keep direct labels adjacent to evidence, use emphasis selectively, and give an essential caveat the same reading accessibility as the claim. A table supports lookup; remove redundant prose and nonessential columns from the main view, preserving needed detail elsewhere. A schedule may need a table, while a tradeoff may read better as an aligned comparison. Choose locally from the content rather than imposing a palette, slide count or card layout.

Separate preparation from the readout in an action handoff. Make the outcome measure, evidence date and stop/continue rule easy to find alongside prerequisites and proposed roles. A polished action list with an inconspicuous review rule leaves the decision loop incomplete.

Before handoff, inspect the saved editable artifact in its intended application when available, and inspect every delivered export independently. Compare the displayed chart categories and values with the checked result; separately extract/review material text, tables and factual notes. Application object counts, cached data and a successful export are source checks, not proof of visible correctness. At the expected viewing size, read each file without the author's explanation or companion outputs and recover the finding, evidence, controlling limit, tradeoff and next step. Repair ambiguity or unreadable essentials. Report model-only readback as a proxy and name any native surface that could not be checked.

Before handoff, check that the headline does not imply more than the evidence, the recommended action fits the constraint, the measure can still respond to the action and the proposed readout is within the relevant deadline. A supplied fixed decision deadline remains fixed even if the data matures later. Record execution and observed results separately from the prepared recommendation.
