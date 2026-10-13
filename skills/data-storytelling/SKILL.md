---
name: data-storytelling
description: Compose analysis, business charts and audience-ready communication from data when a request spans several outputs; explain KPI changes and deliver a supported decision memo or deck. Kể chuyện với dữ liệu, phân tích rồi vẽ biểu đồ và viết memo. Route chart-only, audit-only and team-practice jobs to their specialists; simple KPI answers stay short.
metadata:
  version: "3.0.0"
---

# Data stories: compose the requested work

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

Connect the business process to its records: which event creates a row, which source governs the metric, who resolves conflicting definitions, and when data becomes usable. Then analyze only unresolved decision-relevant questions. Reuse sufficient supplied analysis rather than repeating EDA. Keep shared facts, units, denominators and claim limitations stable across all outputs. Independent drafting can run in parallel once the authoritative facts are settled; reconcile the combined artifact afterward.

Before designing the artifact, write its evidence-to-choice sentence: what the evidence establishes, why it matters for this reader, which choice it supports, and what it leaves unresolved. Select the evidence needed to support that sentence, including material counterevidence. A chart, headline and recommendation must agree on both the main point and claim strength. Put detailed derivations in accessible supporting evidence; do not narrate the order in which analysis was performed.

Produce the requested editable artifact and inspect its final render. Link the recommendation to the problem, desired outcome, feasible action and measurement. With unresolved causes, choose an exact diagnostic or reversible experiment when appropriate. Its measure must be one the action can still change, with a usable evidence window and stop/continue rule.

## Reuse the installed stack

Use `statistical-analysis` for actual inference/assumptions/uncertainty, `business-economics` for unit economics/capacity/scenarios and `reliable-delivery` for material numeric/multiple-output verification when available. `scientific-visualization` contributes figure mechanics and research plots; native spreadsheet, presentation, document and PDF methods produce the requested formats. Read the relevant actual method instead of copying it into this suite. These are optional complements, not bundled dependencies or verified account entitlements.

Select the existing skill router only when choices are unclear or span domains; it retrieves candidates and the assistant decides. Natural-language discovery is supported by these descriptions, not guaranteed in every chat. Loading instructions adds no permission for external action.

## Finish with observable results

Recompute decisive values, reconcile chart and prose, inspect labels/layout and consider the strongest pertinent alternative explanation. Deliver actual files or the requested answer, decisive sources/calculations, the supported choice and genuine limitations. For an action handoff, identify who checks the evidence, who can decide, who executes, what happens next and when the outcome can be revisited; use proposed roles when actual assignments are unknown. These responsibilities may be shared by a small team.

Keep prepared, reviewed, approved, executed and measured outcome separate. A credible recommendation can be delivered before its action is authorized or its result observed. Do not equate an internal score, render success or persuasive wording with business impact.
