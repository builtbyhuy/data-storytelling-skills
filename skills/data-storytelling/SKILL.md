---
name: data-storytelling
description: Compose data analysis, charts and audience-ready communication when a request spans several outputs, across languages and subject areas; explain findings and deliver the requested evidence-based memo, report or presentation. Route chart-only, audit-only and team-practice jobs to their specialists; simple KPI answers stay short.
metadata:
  version: "3.5.1"
---

# Data stories: compose the requested work

Use the requested artifact language and locale; otherwise follow the user's language, with English as the fallback. Adapt to the actual audience, subject and medium; historical examples do not set language or scenario defaults.

Start with the question and its intended use. A current-state question may need one sourced KPI; monitoring needs a condition, threshold and response; an explanation or choice needs evidence and a supported recommendation. A report supports detail/reconciliation, a dashboard supports monitoring/exploration, and a story supports understanding/decision. Choose or combine these roles from the request rather than turning every answer into a narrative.

Read [the shared evidence contract](references/evidence-contract.md) for material facts reused across outputs. Use [the decision workflow](references/decision-workflow.md) when the job spans analysis, communication and an action handoff; it provides a compact brief and a record that specialists can share. [Source coverage](references/source-method-map.md) and [terminology](references/terminology.md) are available when relevant.

## Select one or several methods

| Actual job | Suite specialist | Deliverable |
|---|---|---|
| Diagnose a change or choose useful insights | `business-insight-diagnosis` | Reconciled findings, competing explanations, a concrete choice/test |
| Turn sufficient evidence into a memo/email/deck/story | `evidence-to-narrative` | Reader-ready argument and usable requested medium |
| Create or improve a communication chart | `business-chart-communication` | Editable chart, requested export and render checks |
| Challenge and repair a misleading story/chart | `data-story-redteam` | Corrected artifact and affected decision |
| Establish recurring reporting-to-decision practice | `analytics-adoption` | Feasible pilot, metric ownership and outcome learning |

Read each selected actual `SKILL.md` and only relevant references. In a local installation, discover those names through the client catalog or installed skill lookup; in this repository they live in sibling folders. If a specialist is absent, complete the authorized work using available tools and explain the limitation. Do not require the entire suite for a narrow job.

A prompt can request several jobs. For “explain the change, choose an action, make a chart and write a memo,” select diagnosis, relevant economics, chart communication and narrative; apply proportionate checks and add redteam when a challenge is requested or consequential claims warrant independent scrutiny. Conversely, do not force a chart, audit, deck or rollout into a simple factual question. No one-skill-per-prompt limit, mandatory agent team, new router service or count quota applies.

## Keep a coherent chain

Frame the work in terms of the decision or use, reader, problem, success measure and window, constraints, affected roles and prior attempts. TOSCAR is a prompt for missing context, not a compulsory questionnaire: infer settled details and clarify only gaps that change correctness or a consequential choice. An expected finding remains a hypothesis; do not decide the Aha before inspecting evidence.

Connect the process or subject being studied to its records: which event creates a row, which source governs the metric, who resolves conflicting definitions, and when data becomes usable. Then analyze only unresolved decision-relevant questions. Reuse sufficient supplied analysis rather than repeating EDA. Keep one checked set of computed facts, units, denominators and claim limitations for all outputs; use it to populate charts, labels, tables and factual notes. Independent drafting can run in parallel once those facts are settled; reconcile the combined artifact afterward.

Before designing the artifact, write its evidence-to-choice sentence: what the evidence establishes, why it matters for this reader, which choice it supports, and what it leaves unresolved. Select the evidence needed to support that sentence, including material counterevidence. A chart, headline and recommendation must agree on both the main point and claim strength. Put detailed derivations in accessible supporting evidence; do not narrate the order in which analysis was performed.

Produce the requested editable artifact and inspect its final render. For visual work, establish the actual display size and required medium using [visual delivery](references/visual-delivery.md). Prefer a suitable text/vector master and provide a full-size reading route beside raster previews; retain requested native formats. Use a clear decision/evidence/tradeoff/next-step sequence suited to the medium: give the main comparison room, attach direct labels and the controlling qualification, and keep exact lookup detail accessible. Essential units, denominators, definitions and decision-changing limits must be visible in each portable artifact; notes or a companion workbook cannot carry them for a standalone PDF. The [decision workflow](references/decision-workflow.md#make-each-artifact-work-alone) gives the independent-file check.

Link the recommendation to the problem, desired outcome, feasible action and measurement. With unresolved causes, choose an exact diagnostic or reversible experiment when appropriate. Its measure must be one the action can still change, with a usable evidence window and stop/continue rule. Give that readout enough visible prominence that the reader can act on it.

For a substantial visual artifact, establish a short [content-specific direction](references/visual-delivery.md#commit-to-a-direction-then-exercise-it), then render and exercise a difficult representative view before repeating its composition. A consistent visual system should make this evidence easier to use; it need not look like every previous report.

## Reuse the installed stack

Use `statistical-analysis` for actual inference/assumptions/uncertainty, `business-economics` for unit economics/capacity/scenarios and `reliable-delivery` for material numeric/multiple-output verification when available. `scientific-visualization` contributes figure mechanics and research plots; native spreadsheet, presentation, document and PDF methods produce the requested formats. Read the relevant actual method instead of copying it into this suite. These are optional complements, not bundled dependencies or verified account entitlements.

For a substantial reader-facing HTML artifact, select available `artifact-art-direction` and `frontend-design` as complementary methods and read their actual instructions. Establish the content hierarchy and recipient task with art direction, realize it with frontend craft, and reconcile every visible claim with the shared facts. Keep supporting audits accessible without turning the main reading path into an equally weighted list of checks. Preserve the requested brand and medium; this combination is optional when unavailable and does not replace native document or presentation mechanics.

Select the existing skill router only when choices are unclear or span domains; it retrieves candidates and the assistant decides. Natural-language discovery is supported by these descriptions, not guaranteed in every chat. Loading instructions adds no permission for external action.

## Finish with observable results

Recompute decisive values and reconcile all delivered factual surfaces against the checked results, including chart domains, labels, tables, captions and speaker notes. Inspect the saved editable file in its native application when available and each delivered export separately; a custom preview or object inventory does not verify native display. Read each portable file on its own at its intended size, then consider the strongest pertinent alternative explanation. Repair observed contradictions or reading failures and recheck the affected surfaces.

Deliver actual files or the requested answer, decisive sources/calculations, the supported choice and genuine limitations. For an action handoff, identify who checks the evidence, who can decide, who executes, what happens next and when the outcome can be revisited; use proposed roles when actual assignments are unknown. These responsibilities may be shared by a small team. State the actual checks and unavailable surfaces without turning a successful render into an acceptance claim.

Keep prepared, reviewed, approved, executed and measured outcome separate. A credible recommendation can be delivered before its action is authorized or its result observed. Do not equate an internal score, render success or persuasive wording with business impact.
