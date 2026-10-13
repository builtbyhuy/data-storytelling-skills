# Worked examples

Three complete examples of turning a business question into a usable decision. Each includes a normal-language request, synthetic inputs, inspectable calculations and an editable visual. These are curated instructional examples, not customer outcomes or controlled claims of superiority.

| Business task | Useful result | Open the example |
|---|---|---|
| Sales rise while contribution falls | A reconciled bridge, a conservative B2B bound and a proposed price test with an honest readout date | [01 — Profit decision](01-profit-decision/README.md) |
| A headline rate is used to justify coaching | Preserve the aggregate rates, expose different lead mix and replace the unsupported rollout with a within-tier test | [02 — Fair comparison](02-fair-comparison/README.md) |
| A join inflates reported revenue | Locate the repeated money and reconcile invoices, payments and unpaid balances at the right grain | [03 — Join audit](03-join-audit/README.md) |

## Use the files

Open an example's README, copy its request and supply its inputs to your assistant. Read the memo or repaired decision before the implementation notes. SVGs retain editable text and vector marks; PNGs provide convenient previews. CSV/JSON files keep exact values available without reading them off a picture.

The profit example combines diagnosis, narrative, chart communication and a proposed adoption plan. The comparison example uses redteam and chart repair. The join example actually executes the bundled audit helper and checks it with a separately materialized join. All three carry uncertainty where it changes the decision.

## Rebuild

From the repository root, with Python 3.10 or newer:

```sh
python examples/01-profit-decision/rebuild.py
python examples/02-fair-comparison/rebuild.py
python examples/03-join-audit/rebuild.py --out ./scratch/join-example
python examples/build_visuals.py
```

The join output path must be new. It preserves the supplied inputs and refuses to overwrite existing results. Its published `result/` is the original checked example; rebuild outputs are separate. The SVG builder reads the retained analysis and join audit values and uses a layout designed for these fixtures. If you change the business data, reconsider the conclusion, scale and layout too.

PNG exports were rendered from the SVGs using `sharp`. If that package is available in your Node environment, run:

```sh
node examples/render_previews.cjs
```

No Python dependencies, server, account or paid API is required to recompute the examples or view the SVGs. Font appearance can vary across systems; exported PNGs retain the inspected appearance.

## Provenance

The profit fixture reuses the independently authored public June/July source exports from the local raw-data comparison. Its new memo, plan and visual are curated illustrations; the comparison's timed-out runs remain timed out. The team fixture reuses the earlier four-cell synthetic comparison. The join fixture was authored for this gallery, run through the helper and checked against an independent nested-loop join. No private original ebook, hidden fixture allocation or customer data is included.

The original package's [evaluation record](../evals/README.md) describes a different question: how candidate and baseline sessions performed. A polished example and a verified calculation do not establish a general quality, speed or business-impact advantage.
