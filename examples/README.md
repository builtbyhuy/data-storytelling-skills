# Worked examples

Five untouched runs on real source data and three curated synthetic scenarios. Example 08 uses a new Wine Quality source with version 3.5, combining Frontend and art direction; the [comparison record](../evals/forward-v3.5.md) separates numerical checks, comprehension reviews, work recording, and aesthetics. Each example includes a request, sources, usable files, and rebuild instructions, with its verification scope stated separately.

The historical reports and artifacts retain the Vietnamese requested for those runs. They are examples, not a language restriction. New work follows the intended audience and requested language, format, and domain.

| Task | Deliverables | Open the example |
|---|---|---|
| Read rates and the full distribution without treating source rows as bottle counts; prepare a provenance review | Original HTML text/charts, a work-recording form, a list of 40 HOLD rows, sources, and a Python recipe requiring no additional libraries | [08 — Wine Quality, untouched version 3.5](08-wine-quality/PACKAGE.md) |
| Select time windows to investigate in bike rental data, keeping selection and confirmation periods separate | Untouched 3.4 package, SVG, calculations, and a conditional 8-day check; the weaker aesthetic result is retained | [07 — Bike Sharing](07-bike-sharing/PACKAGE.md) |
| Read historical campaign data and propose a diagnostic before a new contact campaign | Offline HTML for desktop/mobile, a four-page PDF, four SVGs, calculations, and a conditional review of 60 records | [06 — Fresh solo run, untouched](06-bank-marketing/PACKAGE.md) |
| Choose a newsletter angle from electricity generation data while retaining exceptions and denominators | Desktop/mobile HTML, vector PDF/SVG, calculations, and a two-day review task | [05 — Fresh run, untouched](05-asean-electricity/README.md) |
| Prioritize attendance support while local resources remain unverified | 9-page PowerPoint/PDF, an Excel workbook with formulas, launch/hold conditions, and the original recipe | [04 — Real-data run, untouched](04-attendance-pilot/README.md) |
| Revenue rises while contribution falls | Meeting memo, Excel workbook, delivery trial plan, and a completed decision record | [01 — Profit decision](01-profit-decision/README.md) |
| An aggregate rate is used to claim that coaching works | Corrected report, comparison at a common lead mix, and ready-to-use conclusion wording | [02 — Sales comparison](02-fair-comparison/README.md) |
| A table join inflates money totals | Illustration of repeated amounts, reconciliation for each invoice, and an executed audit | [03 — Invoice reconciliation](03-join-audit/README.md) |

## Use the files

Example 08 preserves all 16 author files unchanged. Open `report.html` to read offline; `work-form.html` downloads a JSON record and does not send a real task; `review-40.csv` retains HOLD status. Keep the whole directory and run `python build.py` to rebuild if needed. The main chart retains every point, count, and rate on mobile; the expanded exact-value table still requires horizontal scrolling. The [five complete comparison packages](../evals/practical-v3.5/README.md) also preserve original bytes and recipes; a preferred image has not been substituted for the output.

Example 07 retains all 19 practical files in its ZIP; the [wrapper](07-bike-sharing/PACKAGE.md) distinguishes a recipe dependent on the original environment from rebuild inputs. This is version 3.4 output and has not been relabeled as 3.5.

Example 06 preserves all 22 author files unchanged: HTML/PDF, four SVGs, five source files, JSON/four calculation CSVs, a README, and five recipe files. The [packaging wrapper](06-bank-marketing/PACKAGE.md) states the UCI/CC BY 4.0 source, excluded private receipts, and verification scope; the [author README](06-bank-marketing/README.md) remains byte-for-byte unchanged. The diagnostic proposed in the report is conditional and has not been carried out.

Example 04 preserves the PPTX/PDF/XLSX, build code, and README from the first handoff byte-for-byte. It uses real DfE data, while the service and budget are hypothetical; the proposal has not been approved or implemented. Open the three files to read, discuss, or reconcile them without rebuilding. [Sources and OGL](04-attendance-pilot/SOURCES.md).

Open PDFs to read or print; SVGs retain editable text and vector graphics. Markdown memos provide copyable text. CSV/JSON files retain exact values. Example 1 includes a workbook with data, formulas, and cached values; those values were reconciled to the sources but have not been recalculated in Excel.

To use the skills with your data, copy a relevant example request and supply suitable source files. The gallery scripts reproduce these fixed snapshots; conclusions, proposed thresholds, and layouts need review when data changes. An example decision should not be applied automatically to another business.

## Rebuild

Example 06 uses the exact [author README and recipe](06-bank-marketing/README.md), the existing Windows runtime, and a fresh output directory. The recipe creates the browser/check receipts it needs while building; the separately stored author receipts are not inputs. After relocation, the original rebuild matched 10 deterministic files and the text, dimensions, and 96dpi pixels of all four PDF pages; that scope does not guarantee identical rendering on another runtime.

Example 04 needs the Windows/Office runtime described in its [recipe](04-attendance-pilot/rebuild/README.md). Move the whole `rebuild` directory, open PowerShell there, and run `pwsh -NoProfile -File ./Build.ps1 -SourceDir ./source -BuildDir ./build-06 -OutputDir ./generated-06` into a fresh output directory. The chart snapshot and source period have stated freshness limits.

With Python and the appropriate installed libraries:

```text
python examples/01-profit-decision/rebuild.py --output ./scratch/profit-v3
python examples/02-fair-comparison/rebuild.py --output ./scratch/comparison-v3
python examples/03-join-audit/rebuild.py --output ./scratch/join-v3
```

Use separate output directories. The scripts preserve sources and rebuild calculations, text, SVG, PDF, PNG, and the relevant workbook/reconciliation tables. They do not download libraries or call accounts/services.

Rebuild 1 requires `reportlab`, `xlsxwriter`, `pypdf`, and Poppler. Rebuild 2 requires `reportlab`, `pypdf`, and `pypdfium2`. Rebuild 3 requires `reportlab`, `pypdf`, `Pillow`, and Poppler; `--poppler` specifies the renderer location. The checked exports used Arial installed on Windows; font files are not distributed. The skills and join-audit tools remain usable independently of this PDF build setup.

## How the examples were made

Example 04 used separate roles for the source author, fresh executor, numerical oracle, and two independent readers. Sources, brief, and skill 3.1.2 were frozen before output; the owner did not view drafts, suggest content, or edit output/build code after handoff. Two earlier unsuccessful runs were retained; the skill was revised and the dataset changed. The third run passed five groups of checks; see the [full record of scope and limits](../evals/forward-v3.1.md). The publication wrapper explains which private HTML/receipts were excluded without changing the delivered files.

For curated examples 01–03, three fresh agents ran the frozen skill version from sources and briefs without receiving earlier visuals or answers. The data came from existing synthetic fixtures: these were independent reruns of the same inputs, not new holdouts or baseline comparisons. The owner separately recalculated the sources, inspected exports, and asked a reviewer to read only the pixels. The published versions add edits to terminology, decision conditions, total tables, and portable paths.

Model reading reviews help identify ambiguity; they do not prove improved human comprehension or human acceptance of the aesthetics. There are no customer outcomes, approved/executed trials, or demonstrated business benefits. [Version 3.0 checks and limits](../evals/book-aligned-v3.md). [Earlier comparison results](../evals/README.md) remain unchanged.
