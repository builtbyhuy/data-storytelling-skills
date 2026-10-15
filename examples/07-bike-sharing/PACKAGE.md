# Original Bike Sharing observation-planning handoff

This example was independently authored using **3.4.0**, then sealed before owner review. It uses unfamiliar UCI Bike Sharing source files. The later 3.4.1 quantity-retrieval repair has a separate focused follow-up; this report is not relabelled as a 3.4.1 execution.

[Download the original offline bundle](untouched-practical.zip), extract it into a new folder and open `report.html`. The archive includes all 19 original practical files: HTML, two editable text SVGs, facts/schedule/readout CSVs, source files, original analysis/build/validator code and recipe. All bytes match the first complete handoff. The two SVGs beside this note are identical preview copies, not polished replacements. [Exact-file receipt](PUBLICATION.json).

The report chooses windows from 2011 and checks them, unchanged, against 2012. It proposes a four-week, eight-day, 64-staff-hour observation plan. It remains HOLD until a manager confirms site permission, matching scope, staffing and actual local hour/calendar meaning. Historical rentals do not establish unmet demand, causal benefit, current availability or suitability of a particular station.

Independent source, visible-value and schedule checks passed within their recorded scope. The unchanged rebuild was executed in another directory on the existing Windows runtime and reproduced 11 selected outputs byte for byte. Browser inspection covered 960px and 390px; some charts and tables deliberately scroll horizontally on a narrow screen. Human reading speed, human taste, field execution and beneficial business outcomes remain unmeasured. [Full comparison and qualifications](../../evals/forward-v3.4.md).

## Original recipe and environment

The archive preserves the **environment-specific** original `README.md` and `Rebuild.ps1`, including the author's existing Windows runner paths. They are historical execution receipts, not commands assumed to work on every recipient's machine. They were not redacted, rewritten or fixed after handoff.

The original `build.py` resolves its source files relative to itself and documents `--out`. With a suitable existing Python and pandas runtime, the corresponding direct interface from the extracted folder is:

```text
python -B build.py --out rebuilt
python -B validate_readout.py readout-example.csv --output readout-example-recheck.json
```

The verified environment was Python 3.12.14 and pandas 3.0.1. No installation or global setting change is required to view the delivered HTML/SVG/CSV. Other operating systems and dependency versions have not been executed for this example. Build into a new directory; rebuilding creates blank templates and is not a way to merge real readouts.

## Source and license

Hadi Fanaee-T (2013), [Bike Sharing, UCI Machine Learning Repository](https://doi.org/10.24432/C5W894), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit also Fanaee-T and Gama, [Event labeling combining ensemble detectors and background knowledge](https://doi.org/10.1007/s13748-013-0040-3). Original Capital Bikeshare hourly/daily aggregates cover 2011–2012; weather was joined from Freemeteo. Source attribution and limitations remain in the archive's original `source/SOURCE.md` and report.

Original explanation, code and layout are MIT. The data retains CC BY 4.0; it is not relicensed as MIT. The owner's packaging note and cryptographic receipt are separate from the unchanged author output.
