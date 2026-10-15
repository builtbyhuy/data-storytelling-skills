# Forward evaluation 3.4.0 — useful evidence, failed polish target

Five fresh solo authors received the same new inputs, runtime and 60-minute cap. Their first complete handoffs were sealed: 571 files, zero owner edits to outputs or rebuild code. The candidate method was frozen before the revision owner saw new answer values. These are matched method activations on a shared model/runtime/catalog, not a fully isolated causal A/B experiment. Exact backend model ID and hidden sampling settings were unavailable.

## Original public benchmark, limited scope

[Microsoft VisEval](https://github.com/microsoft/VisEval), commit `55162fac5765d8873180d962cce7e20e75b2c092`, was run with its original deterministic `Evaluator(None, None)`. A metadata-selected 29-task diagnostic set has 59 original paraphrases across 24 databases, with no task/database/relevant CSV-byte overlap with the earlier 50-task run. It includes five Bar tasks and four of each other supported type; only four unused Grouping Line sources remained under the declared exclusions. This is not the full 1,150-task benchmark.

| Method | Task macro score | Fully passing tasks | Passing paraphrase replays |
|---|---:|---:|---:|
| Candidate 3.4.0 | 72.4% | 21/29 | 45/59 |
| Published 3.3 | 72.4% | 21/29 | 43/59 |
| Frontend + art direction | 72.4% | 21/29 | 46/59 |
| K-Dense | 55.2% | 16/29 | 37/59 |
| Visual Explainer | 58.6% | 17/29 | 38/59 |

All have zero invalid executions. **No demonstrated task-score gain over 3.3 or Frontend.** One generated program per task is replayed against its original paraphrases; these are not independent generations. Official vision/browser readability and quality components were not run: **unmeasured**, regardless of default zero fields in the scorer CSV. Original parser rejections remain unchanged. Do not compare this subset percentage with the older 50-task percentage as matched difficulty.

[Original programs, raw official records and selection metadata](forward-v3.4/) retain the evidence. [Practical checks](forward-v3.4/practical-results.json), [both-position visual votes](forward-v3.4/visual-results.json) and [focused quantity readbacks](forward-v3.4/focused-3.4.1-readbacks.json) are exact copies of the retained result receipts, not a restyled author handoff. Referenced full local originals remain sealed separately. The upstream code license is MIT; no benchmark gold or source databases are republished here. The same adapter was used for all conditions, SHA-256 `9ebe8b213af78563bab447132e528b17b8d7085f7e322afe08e5240ac0466e9e`.

## Separate practical test: UCI Bike Sharing

Original UCI Bike Sharing data, credited to Hadi Fanaee-T (2013), [DOI 10.24432/C5W894](https://doi.org/10.24432/C5W894), CC BY 4.0. Each author selected a three-hour window using 2011, froze it for 2012 and compared it with the same-date 10–12 baseline. Eligible dates have exactly one valid record for each hour 06–21; an incomplete date is excluded from both numerator and denominator, never zero-filled. The source designer explored 2012 before the final rule; the method-revision owner did not see new answer values before freezing the candidate. This limits a stronger pristine-holdout claim.

All five first handoffs passed the bounded independent source/visible-value checks. All five original recipes rebuilt selected facts/report/chart outputs byte-identically after relocation. Offline browser checks covered 960×900 and 390×844 CSS pixels, DPR 2, complete original page sections and original disclosures; the owner also exercised each original report's three synthetic operational cases. No artifact was edited for review. A successful render does not certify general accessibility or professional quality.

Ten fresh model readers, two per report, answered manager questions before receiving synthetic operator fixtures. Their manager answers were sealed before phase two. Independent grading recorded 74 correct manager assertions, six finer omissions and no wrong numerical value or operational decision. Some omissions demanded more detail than the question explicitly asked; preserve that alignment limit instead of treating them as six wrong business decisions. All 50 common and 30 scenario operator assertions passed; all 2,400 raw values in final CSVs were preserved, and 3,840 values in 48 saved CSVs were checked. Synthetic readiness never authorizes field deployment.

## Polish did not meet the target

Eight additional fresh model contexts judged original complete capture sets. Candidate-versus-each-rival comparisons were repeated with both positions swapped. Polish and readability were separate votes. A mapped disagreement resolves to tie; no overall score is invented.

| Candidate 3.4.0 versus | Polish after swapped comparison | Readability after swapped comparison |
|---|---|---|
| Published 3.3 | Tie | Tie |
| Frontend + art direction | Rival preferred | Tie |
| K-Dense | Rival preferred | Tie |
| Visual Explainer | Rival preferred | Tie |

**3.4.0 did not demonstrate the requested presentation improvement.** Concrete defects include horizontal mobile table lookups, overly wide technical-name columns, repeated comparison material and several operational rules packed into long paragraphs. These negative results initiated a method correction and another new-source trial; they were not erased or relabeled as a later version's results. These preferences are model proxies, not human taste certification.

## Additional semantic checks and focused 3.4.1 repair

A separately scoped inspection rendered 35 original public-task SVGs at 960 CSS pixels. Text was legible within that inspection, but two programs used joined-record rather than distinct-entity grain; one program had equal visual spacing for unequal year intervals despite its official pass. All five pie charts for one task showed percentages without the requested absolute counts/base. Official scores remain unchanged.

The actual skill was amended to require the asked quantity to be recoverable in the rendered chart. A frozen 3.4.1 candidate was then tried on two unused source databases with all five methods, fresh solo authors and equal 15-minute caps. All ten original SVGs/fact sets and all five relocated builds passed source/rebuild checks. Four image readers correctly recovered both identity/count sets; one K-Dense reader transcribed John Deloor as John Delor although the original SVG was correctly spelled. The reader error is preserved separately from artifact correctness. Changed output format, lighter workload, two cases and one model family preclude a causal or full-benchmark improvement claim.

## What changed next

The 3.5 method makes actual Frontend and artifact-art-direction activation part of substantial HTML work when those complements are available, keeps one primary expression of the decisive comparison, moves detailed reconciliation into accessible supporting material, and checks narrow-screen value identity, captions and individually findable action rules. The new Wine Quality practical test is separate. The historical records here remain 3.4.0 and focused 3.4.1, never a 3.5 benchmark result.

[Untouched 3.4.0 example and exact-file publication receipt](../examples/07-bike-sharing/PACKAGE.md). No human acceptance, live operational work, business outcome, statistical significance or general best-method claim follows from these bounded trials.
