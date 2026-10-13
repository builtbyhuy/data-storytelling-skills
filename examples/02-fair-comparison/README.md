# Lead mix changes the ranking

**Use this when:** a sales report uses an aggregate win rate to justify a coaching rollout, but teams receive different lead populations.

![Both the overall and within-tier comparisons, with denominators and the limit on causal interpretation](comparison.png)

## Try it

> Our draft says “B's coaching improves conversion by 50%, so roll it out to A.” Review this conclusion against data.csv, repair the chart, and recommend the next decision. Keep the overall rates, show the denominators, and explain any comparison that changes the recommendation.

## The repaired decision

The overall rates are correct: A wins **24/80 (30%)** and B wins **36/80 (45%)**. B's rate is 50% higher relative to A's rate. The unsupported step is attributing that difference to coaching.

B receives **75% High-tier leads**, compared with **25% for A**. Within each supplied tier, A's observed rate is five percentage points higher: High **60% vs 55%**, Low **20% vs 15%**. Applying the same hypothetical 50/50 mix gives **40% for A and 35% for B**. This standardization describes the four supplied cells; it does not identify a coaching effect or prove future team performance.

**Decision:** review lead assignment before changing coaching. If a coaching comparison is needed, propose a test within each tier, with an agreed outcome window and decision threshold before launch. No coaching assignment, observation period or randomized test is supplied here.

## What the methods contributed

- `data-story-redteam` repairs the causal claim and changes the rollout decision.
- `business-chart-communication` preserves valid aggregate values, adds comparable within-tier rates, starts magnitude bars at zero and puts the sample counts beside the marks.
- `evidence-to-narrative` makes the decision and its qualification readable together.

This is a **synthetic, curated worked example**, derived from the suite's earlier team-comparison fixture. It demonstrates a completed repair, not a controlled proof that the suite beats an unassisted model. It contains no customer data.

## Inspect or rebuild

- [Source CSV](data.csv)
- [Exact calculations](calculations.json)
- [Editable SVG](comparison.svg)
- [PNG preview](comparison.png)

```sh
python examples/02-fair-comparison/rebuild.py
python examples/build_visuals.py
```

Run from the repository root. The first command recomputes the rates with exact fractions and records the derivation; the second regenerates the editable SVGs. PNG export is optional and described in the [example gallery](../README.md).
