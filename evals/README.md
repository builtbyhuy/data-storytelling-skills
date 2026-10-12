# Evaluation protocol

These are synthetic acceptance exercises, not production work or a certification benchmark.

## Inputs and cases

`briefs.json` contains normal-language user requests. Each case lists only the inputs under `inputs/` that its agent may read. A tests joined transaction/refund/ad grains and a combined diagnosis, budget choice, chart, memo and evidence repair. B tests aggregate/subgroup performance and repair of a misleading draft. C1 tests endpoint-range encoding. C2 tests screenshot-only redesign without invented values. D tests a feasible team practice at stated capacity. C1 and C2 are separate subcases.

For screenshot-only C2, give the agent `screenshot.png`, not the companion fixture-generation SVG. Do not supply grader answers, prior runs, reviewer conclusions or source-book case remedies.

## Conditions

Baseline completes the same briefs with ordinary Codex tools and available complementary methods, explicitly omitting the six suite instructions and the suite-specific router amendment. Candidate selects relevant installed methods from the requests; it is not given a required specialist sequence. Both get the same raw files, tools, model settings, artifact requirements and no-subagent/no-external-action boundaries. Preserve input and treatment hashes.

The local pilot uses one fresh no-history agent session per condition, with cases A, B, C1, C2, D in the same order. Methods/context can carry within each condition; these are five subcases, not five independently sampled sessions. The available client does not expose a fully isolated common-global-instruction snapshot or usage accounting, so this is a descriptive diagnostic comparison. Missing token usage stays unknown. Do not infer a pure causal effect, speed advantage or general reliability rate.

## Checks

Compute ground truth separately from the raw inputs. Reconcile decisive calculations, source counts and definitions; inspect the actual SVG/PNG pair and the recommendation/message; require concrete outputs and feasible action/state. Discovery evidence distinguishes metadata candidates from methods actually selected/read and their contribution. False candidates are recorded instead of silently calling retrieval perfect.

For repeated comparisons, use fresh sessions per case and matched configurations/budgets, preserve failures, and review artifacts with condition labels hidden. Keep expected answers outside agent-readable inputs. A numeric checker or reviewer alone cannot establish rendered craft, audience comprehension or business effect.

## Observed results — 2026-10-12

Both conditions passed the direct acceptance checks for A, B, C1, C2 and D. Independent source calculations and range-to-mark checks passed 180 numeric assertions. All eight final PNGs were inspected directly by the trial authors, the primary evaluator and a reviewer who received X/Y artifact copies without condition identity. The blind review found no material arithmetic, geometry, causal-claim or brief defect within its scope. This is a diagnostic pilot, not proof that the suite is better than baseline.

Separate fresh-session controls E/F passed: E returned a single correct KPI sentence without chart/plan; F selected the narrative method from supplied reconciled facts and produced an unsent 179-word email without CSV reanalysis. These controls did not have their own baseline pair.

The compound A request selected and read the composing, diagnosis, economics, chart, narrative, redteam and numeric-verification methods; D selected adoption directly. Retrieved candidates and actual selected methods are distinct. Raw retrieval still produces extraneous results, including an adoption candidate for a simple KPI lookup; the E agent correctly skipped broad retrieval. F selected the appropriate narrative candidate at position seven after rejecting unrelated email workflows. These observations demonstrate scoped method selection, not a guaranteed automatic hook in every client/session.

See [structured results](results.json), [baseline artifacts](examples/baseline/) and [candidate artifacts](examples/candidate/). Controls are in [E](examples/controls/E/) and [F](examples/controls/F/); their exact prompts are in [control briefs](control-briefs.json).

Limits worth retaining: A's execution-level experiment pacing, sample adequacy and uncertainty threshold require a real plan before launch; advertising incrementality and other costs are unknown. B cannot prove coaching or team superiority. C1 does not identify the statistical meaning of the intervals. C2 has no exact bar values. D is a proposed pilot with no case data, approval or measured outcome. The baseline C2 approximate prototype satisfies the explicit labelled-prototype allowance but retains numeric-readback risk; the candidate uses unencoded unknown-value fields. No actual audience comprehension, adoption or business improvement was measured.
