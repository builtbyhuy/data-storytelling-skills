# English-first repository and multilingual output — 3.5.1

Version 3.5.1 corrects repository language and scope. Maintained navigation, skill descriptions and UI names are English. All six skill entry points and the shared evidence contract say that the requested artifact language and locale take precedence over the conversation language. The methods adapt to the actual audience, subject and requested medium. Historical Vietnamese cases do not prescribe a language, market, currency, industry or output format.

The visual delivery method also requires checking actual glyphs, shaping, line breaks and text direction in the chosen renderer, including right-to-left or mixed scripts when relevant. That instruction is a requirement for future work, not a claim that every language or renderer has been tested.

## Two fresh text checks

Before execution, the [two prompts](language-scope-v3.5.1/prompts.json) and [66-file core method snapshot](language-scope-v3.5.1/methods-sha256.json) were saved. Separate fresh model agents read the repository's composing and narrative methods, with the shared evidence contract, and produced their first completed responses. They had no prior artifacts or expected answers. No optional design complements or comparative conditions were requested. The owner did not edit either response.

| Request | Untouched output | Owner's source and brief review |
|---|---|---|
| English research notebook paragraph and exact table; six synthetic instrument readings | [English research summary](language-scope-v3.5.1/english-research.md) | Means 12 and 15 mg/L, difference 3 mg/L / 25%, sample SD 1 mg/L in both groups; all six readings preserved. English, within 180 words, with causal and generalization limits. No added business workflow. |
| Spanish public-library explanation using es-ES conventions, despite an English prompt; four synthetic source rows | [Spanish library explanation](language-scope-v3.5.1/spanish-library.md) | Totals 20,500 to 23,400 visits, change 2,900 / 14.1% rounded; branch changes 20% and 5%. Spanish prose and number formatting, unchanged NORTH/SOUTH identifiers, repeated visits distinguished from distinct people. Within 180 words; no added operational plan. |

[Check receipt and output hashes](language-scope-v3.5.1/checks.json) record the narrow checks. These are small instruction-following smoke checks with synthetic inputs and owner review. They do not establish an improvement over baseline, human language quality, visual quality, all-language support, RTL rendering or real-world adoption. The latest full visual comparison remains the frozen [3.5.0 Wine trial](forward-v3.5.md), with its original mixed results.

## Historical evidence

The gallery index and three maintained curated-example guides are translated into English. Their linked original artifacts and all frozen real-data trial files remain unchanged. The 3.5.0 packaging reconstruction is explicitly tied to its publication commit, so its tested method hashes are not relabeled as 3.5.1.
