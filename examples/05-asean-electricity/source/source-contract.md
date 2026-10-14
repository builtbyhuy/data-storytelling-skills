# Frozen source contract

Use `raw/ember-generation-five-countries-2015-2024.csv`: 200 untouched records, all original columns, five ISO codes, ten annual observations each, four source categories. Country labels are `Viet Nam`/VNM, `Thailand`/THA, `Malaysia`/MYS, `The Philippines`/PHL and `Indonesia`/IDN. Keep ISO keys when translating labels. The key is ISO code + year + electricity source.

`Generation (TWh)` is annual electricity produced. `Share of generation (%)` uses domestic generation as denominator; net imports are excluded. It is not consumption share or installed capacity. `Wind and solar` is an aggregate, overlapping its component rows: do not add all four rows together. Use the reported combined share as the canonical published measure; independently reconcile it with components and total generation. Published shares have three decimals, so minor rounding differences are expected. Compare changes in percentage points separately from relative percent change; a zero baseline cannot support a finite relative increase.

Ember's [methodology](https://files.ember-energy.org/public-downloads/ember_electricity_data_methodology.pdf), retained unchanged, aims for gross annual generation. It documents captive/distributed-generation coverage limits. Annual sources include EI and national reporting, with EIA for Philippines. Indonesia's captive production includes Ember estimates. The Vietnam pre-2022 wind warning concerns the monthly EVN series; do not silently transfer it to every annual observation.

The CSV snapshot was last modified 6 October 2026, downloaded 14 October 2026. Data after 2024 is outside this brief. These five countries do not constitute all ASEAN. No causal, grid-reliability, tariff or investment data is supplied.

[Ember Yearly Electricity Data](https://ember-energy.org/data/yearly-electricity-data/) is [CC BY 4.0](https://ember-energy.org/creative-commons/). Attribute Ember, identify filtering and your own analysis/presentation, and avoid implying endorsement. No Ember logo is supplied. Full retrieval hashes, exact source-line selection and replay instructions are in `provenance.json`.
