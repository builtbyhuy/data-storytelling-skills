# Browser-rendered visual export

Use the optional `../scripts/export_web.mjs` for authored local HTML with inline/text SVG. It renders the actual source in Chromium, captures whole page sections at two display widths and 2x sampling, and can print that same document to PDF. It does not draw a separate preview or modify the source. Native Office requests still use the Office creation/verification path.

Requires an available Node runtime, Playwright module and Chromium executable. Discover existing workspace dependencies first. The package installer does not download these tools; no network or credential is required when they are already available. If they are absent, use the available format renderer or set up only the chosen optional capability with appropriate authorization. Do not claim installation from a documentation read.

```text
node /path/to/business-chart-communication/scripts/export_web.mjs --input report.html --out exports --module-dir /path/to/node_modules --widths 960,1280 --min-essential 16 --pdf report.pdf
```

If Playwright's Chromium is not installed, pass `--browser /path/to/chromium`. `--module-dir` is unnecessary when normal Node resolution finds Playwright. Run from the recipient's actual working directory and document the exact retained structure and invocation for rebuilds.

Author the page to load required assets locally, await fonts/data, and include `data-essential` on the headline, chart labels, unit/period, material caveat and next step. An ancestor may carry it. The default capture selector is `.page`; use `--selector` for another section class. Avoid duplicate nested capture roots. Set print styles, page dimensions and breaks deliberately; the helper honors CSS page size. Check the resulting PDF independently, including that one intended page did not split into two.

Include essential exact-value table headings/cells in the reading checks, especially long signed amounts. Use document-unique SVG IDs and correct title/description references, including hidden responsive copies. Inspect each visible chart's actual browser accessibility name; a correct visual label and an `aria-labelledby` attribute alone do not establish that it names the right chart. Record deliberate external captions or decorative SVGs. The helper's reference/name and cell-bound diagnostics are mechanical checks; they cannot certify screen-reader behavior, comfortable spacing or complete accessibility.

The helper blocks HTTP(S) asset requests unless `--allow-network` is explicitly chosen. Failed required asset requests (including SVG image URLs), HTTP errors, blocked requests, missing HTML images, page errors, horizontal overflow, too-small essential text and text outside its SVG/page bounds make its receipt fail. It checks actual text nodes, including a paragraph's text beside differently styled inline children. Fonts include SVG and ancestor CSS matrix scaling/zoom; the smaller singular value conservatively detects nonuniform crushing/shear. Unsupported independent CSS scale/rotate and 3D transforms fail conservatively. These heuristics do not check every decoding failure, overlap, contrast, data value, unmarked essential, or reading problem. Visually inspect every delivered page at its expected display size. The `verified_vector` PDF field is false until a separate PDF-object check establishes text/vector content; printing successfully does not establish it.

Deliver text-based SVG or HTML plus the requested portable output and rebuild data/code. PNG is a thumbnail/attachment; provide a labeled vector/full-size route beside it. Never describe a 4K image, a tool pass or a local render as verified sharpness in the unobserved hosted/chat surface.
