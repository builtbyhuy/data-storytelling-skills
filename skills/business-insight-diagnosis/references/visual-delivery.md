# Readable visual delivery

Use this method for a chart, visual memo or presentation whose viewing/export quality matters. It supplements evidence and channel choices; a text answer does not need it. Read [repository methods](repository-methods.md) only when choosing a renderer or learning from those examples.

## Specify the surface before composing

Record the intended display width, full-page versus embedded use, source canvas, required editable format and portable output. A 3840px PNG displayed at 600px has the same apparent typography as a 1600px PNG displayed at 600px. Pixel dimensions establish sampling, not readability. For a fixed canvas, apparent text size is source size multiplied by displayed width divided by source width; convert points to the same units before comparing.

Use a practical starting budget, then inspect the actual destination: around 18–22 CSS px for essential reading text and chart labels at desktop display size, 16px for secondary provenance. These are adjustable defaults for a screen reader page, not research claims or universal print/presentation rules. A projected slide may need substantially larger text. A consequential qualification is essential text. If it does not fit, shorten repeated prose, separate questions or choose a reading document; shrinking all typography defeats the purpose.

Write one principal reader question per view. Allocate space to the comparison before adding a headline or supporting detail. Use consistent type roles, shared alignment, quiet context and direct labels with room at endpoints. A large headline cannot compensate for a tiny plot. Tables support exact retrieval; a dense operations matrix often belongs in a separate reading page rather than projected full-screen. Keep necessary counterevidence and definitions alongside the claim. Taste follows coherent choices, not a fixed palette, cards, decoration or font brand.

For a responsive web artifact, reflow prose at narrow widths and retain readable chart text. Either redesign/facet the chart for that width, or offer a clearly labeled scrollable chart and accessible exact-value table. Do not shrink an entire desktop slide into a phone screen and call it responsive. Test the widths required by the request; do not infer mobile verification from a desktop render.

## Select a real production path

An exact-value table is part of the reading path when the decision depends on it, even if the author omitted a `data-essential` marker. Inspect its longest values at each promised width, including signs, decimal/grouping separators, units and the row/column identity that gives them meaning. Keep each amount recoverable as one value; avoid interleaved neighboring numbers or wrapping that makes a sign or digit look like another row. Use appropriate precision, more space, paired labeled rows or deliberate labeled scrolling according to the lookup task. Reducing font size or counting a non-clipping render alone does not resolve a crowded comparison.

For inline SVG, use document-unique identifiers for chart titles/descriptions, including hidden responsive variants. A standalone SVG's generic IDs can collide when several charts are in one HTML document. Use a stable chart prefix, update every reference together, and check that each visible chart's exposed browser name identifies that chart at the required breakpoints. Valid `aria-label`, native SVG `title`, and deliberate external captions are alternatives; decorative SVGs can be hidden from the accessibility tree. DOM reference checks and browser names cover a narrower scope than screen-reader or full accessibility testing. [SVG title/description semantics](https://www.w3.org/TR/SVG2/struct.html#DescriptionAndTitleElements) and [document IDs](https://html.spec.whatwg.org/multipage/dom.html#the-id-attribute) are the underlying constraints.

| Use | Suitable path | What to verify |
|---|---|---|
| Independent chart / editorial reading page | SVG with editable text, or HTML with inline SVG; print to vector PDF | Actual browser-rendered labels, scaling, font loading, page breaks, SVG/PDF content and exact-value access |
| Scientific figure / publication | Available plotting library exporting SVG/PDF plus editable code and data | Encoding, dimensions, text/font handling, clipping, units and style at publication size |
| Requested editable PowerPoint / Excel | Native text, tables and charts through the available Office method | Saved file reopened in its application and exports from that file; chart data/category identity checked independently |
| Raster thumbnail / attachment | Export the tested source directly at enough pixels for the intended display density | Same full content, correct dimensions, visible essentials at displayed size, no accidental crop or missing fonts |

Use available libraries rather than inventing a new chart renderer when they fit. Observable Plot and Vega-Lite have useful declarative SVG workflows; Matplotlib supports SVG/PDF. Browser presentation tools suit web-first slides, but a PPTX export made from page images does not satisfy editable native chart/text requirements. Respect the requested medium. A vector reading alternative can accompany a native deck; it cannot silently replace it.

Inspect SVG source for raster `<image>` content and PDF image/text/vector objects when sharpness is in question. SVG is a container and may still contain a screenshot. A PDF can similarly contain full-page images. Text converted to outlines remains vector but loses text editing/search; record that tradeoff. Retain text-based source when revision is required.

For authored local HTML, the optional [browser export helper](https://github.com/builtbyhuy/data-storytelling-skills/blob/main/skills/business-chart-communication/scripts/export_web.mjs) is in the repository chart skill. Installed standalone skills should locate `business-chart-communication/scripts/export_web.mjs` if that specialist is installed; otherwise use an available browser exporter. Its [usage reference](https://github.com/builtbyhuy/data-storytelling-skills/blob/main/skills/business-chart-communication/references/browser-export.md) describes setup and limits. This helper is optional, not a remote service or a prerequisite for non-web formats.

## Inspect three distinct layers

1. **Source and technical output:** checked values/definitions; text/vector content; source/export dimensions; fonts and required assets available; no hidden crop or omitted page. A successful renderer is evidence only for the operation it performed.
2. **Practical reading size:** inspect the entire final view at the promised width and browser zoom. Read the headline, decisive comparison, series identity, units, period and controlling qualification without opening another file or zooming in. Inspect PDF and browser output separately. A crop can diagnose edges but cannot establish whole-page readability.
3. **Actual delivery surface:** inspect the hosted page, embedded preview or native file if access exists. If the preview looks worse than the local file, compare measured display size/zoom and served bytes before naming compression or blaming the viewer. If this surface cannot be inspected, state that limitation and provide a clearly labeled vector/full-size alternative.

Record concrete failures instead of a generic aesthetic score: a 12px projected label, endpoints with colliding labels, a caveat that cannot be read at the stated size, an image-only PDF, conflicting colors, or the absence of a usable full-size path. Repair the generation method/content allocation, render again, and verify affected surfaces.

In a skill evaluation, seal the first completed output and its rebuild sources before review. If it fails, change the skill/tool and use an unfamiliar input for the next execution; preserve the failed output rather than owner-polishing it into a purported untouched pass. A model readback is a proxy, not measured human taste or comprehension. Vector export alone is not aesthetic acceptance.
