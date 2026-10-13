# More sales. Less contribution.

**Use this when:** sales growth hides a decline in contribution, and the team needs to choose a bounded commercial action.

![June to July2026 contribution:35.00m VND plus2.80m gross-profit gain minus6.85m freight growth equals30.95m; freight is the focused comparison](decision.png)

The chart answers one question: which accounting change consumed the gross-profit gain? The memo below gives the separate B2B bound and price sensitivity behind the proposed action; those supporting figures are not additional focal points in the chart.

The business's sales grew **VND44.10m**, while contribution fell **VND4.05m**. Gross profit rose, but freight grew faster. The useful decision is to keep B2B in the plan, reconcile the missing freight and test a smaller discount with demand and service guardrails.

## Read or try the example

- [Copyable request and source definitions](brief.md)
- [Decision memo](memo.md)
- [Proposed four-week test and mature readout](test-plan.md)
- [Exact analysis](analysis.json) · [compact evidence](evidence.csv)
- [Editable SVG](decision.svg) · [PNG](decision.png)

## What the methods contributed

`business-insight-diagnosis` reconciles the accounting bridge and bounds the missing freight instead of inventing its attribution. `evidence-to-narrative` puts the choice, strongest counterargument and price sensitivity together. `business-chart-communication` isolates the decisive gross-profit/freight contrast with a finding headline, neutral context and one highlighted change. `analytics-adoption` gives the proposed intervention an owner, guardrails and an outcome date that waits for mature evidence.

**The useful limit:** the VND6.20m price-restoration sensitivity holds sales and returned quantities fixed. It estimates a mechanical scenario, not demand response. The VND17.70m B2B contribution floor excludes overhead and assumes all VND3m missing freight belongs to B2B. Neither figure is an observed benefit of a test.

This is a synthetic, curated worked example with unchanged public source exports. No intervention has been executed. It demonstrates this analysis and communication, not a controlled advantage over an unassisted model.

## Rebuild

From the repository root:

```sh
python examples/01-profit-decision/rebuild.py
python examples/build_visuals.py
```

The calculation uses the Python standard library and the five files in `inputs/`. The original Vietnamese [source notes](inputs/source-notes.md) define grain, recognition dates, units and coverage; [the English brief](brief.md) summarizes their business meaning. See the [gallery](../README.md) for PNG export.
