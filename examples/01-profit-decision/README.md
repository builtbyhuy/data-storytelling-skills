# More sales. Less contribution.

**Use this when:** sales growth hides a decline in contribution, and the team needs to choose a bounded commercial action.

![June to July contribution bridge, B2B downside bound, missing freight coverage and a bounded price-test recommendation](decision.png)

The business's sales grew **VND44.10m**, while contribution fell **VND4.05m**. Gross profit rose, but freight grew faster. The useful decision is to keep B2B in the plan, reconcile the missing freight and test a smaller discount with demand and service guardrails.

## Read or try the example

- [Copyable request and source definitions](brief.md)
- [Decision memo](memo.md)
- [Proposed four-week test and mature readout](test-plan.md)
- [Exact analysis](analysis.json) · [compact evidence](evidence.csv)
- [Editable SVG](decision.svg) · [PNG](decision.png)

## What the methods contributed

`business-insight-diagnosis` reconciles the accounting bridge and bounds the missing freight instead of inventing its attribution. `evidence-to-narrative` puts the choice, strongest counterargument and price sensitivity together. `business-chart-communication` makes the bridge legible with exact values and the source-coverage limitation alongside it. `analytics-adoption` gives the proposed intervention an owner, guardrails and an outcome date that waits for mature evidence.

**The useful limit:** the VND6.20m price-restoration sensitivity holds sales and returned quantities fixed. It estimates a mechanical scenario, not demand response. The VND17.70m B2B contribution floor excludes overhead and assumes all VND3m missing freight belongs to B2B. Neither figure is an observed benefit of a test.

This is a synthetic, curated worked example with unchanged public source exports. No intervention has been executed. It demonstrates this analysis and communication, not a controlled advantage over an unassisted model.

## Rebuild

From the repository root:

```sh
python examples/01-profit-decision/rebuild.py
python examples/build_visuals.py
```

The calculation uses the Python standard library and the five files in `inputs/`. The original Vietnamese [source notes](inputs/source-notes.md) define grain, recognition dates, units and coverage; [the English brief](brief.md) summarizes their business meaning. See the [gallery](../README.md) for PNG export.
