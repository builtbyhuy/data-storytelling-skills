# Frozen source package: UCI Bank Marketing, original full variant

This package preserves the official `bank-full.csv` as source input. It contains 45,211 data records and 17 original columns: 16 source inputs and the recorded outcome `y`. No subset, alternative dataset version, data cleaning, resampling, row reordering, recoding, or encoding conversion was performed. The metadata and checks are source preparation only.

The official [UCI ID 222 page](https://archive.ics.uci.edu/dataset/222/bank+marketing) was retrieved on 14 October 2026. Its download link supplies [the official combined archive](https://archive.ics.uci.edu/static/public/222/bank%2Bmarketing.zip). The inner `bank.zip`, `bank-full.csv`, and `bank-names.txt` were extracted byte for byte. The 10% `bank.csv` and the newer 41,188-row CSV were not extracted as input. Original archive order is preserved.

The current page identifies DOI [10.24432/C5K306](https://doi.org/10.24432/C5K306) and [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The DOI was independently resolved to the UCI ID 222 page. The downloaded page and Creative Commons deed/legal code are retained with retrieval receipts. The older embedded dictionary requests a 2011 paper citation; it does not override the current repository's explicit CC BY 4.0 license. Both the current dataset citation and requested original-paper citation are recorded in `source-contract.json`.

Use attribution: Moro, S., Rita, P., & Cortez, P. (2014). Bank Marketing [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306. Licensed under CC BY 4.0. Retained source bytes are unchanged. Indicate subsequent modifications when sharing modified material and retain the license link.

The original dictionary governs original field meanings, including `day` as day of month, the original education categories, and `pdays=-1` for no prior contact. The current page's variables table includes some newer-variant field names and categories, so it is not used as the selected CSV's schema. The original dictionary reports no missing attribute values; `unknown` is an explicit documented category rather than an empty field.

The original dictionary defines `duration` as realized last-call duration in seconds. For timing documentation only, the unchanged official `bank-additional-names.txt` is retained from the other inner archive; it explicitly says the same duration quantity is unavailable before the call. Its alternate CSVs are not used. This file is official source documentation; the neutral contract includes the timing fact without deriving an analytical result.

Raw CSV SHA-256: `d1513ec63b385506f7cfce9f2c5caa9fe99e7ba4e8c3fa264b3aaf0f849ed32d`.

Original inner archive SHA-256: `99d7e8eb12401ed278b793984423915411ea8df099e1795f9fefe254f513fe5e`.

Official combined archive SHA-256: `e0bf5f5de5b846e2f18e9d90606637267d46dfa260e0f17bb12e605db5efbeb4`.

`prepare_source.py` reproduces the byte-preserving download/extraction into a fresh directory and refuses to overwrite frozen files. `verify_source.py` independently opens both archive levels and checks CRC, byte size, hashes, exact original header, row widths, row count, strict UTF-8 compatibility, original LF line endings, documented categorical domains, integer parsing, and blank cells. `source-verification.json` contains the executed results. It proves source integrity and shape, not analytical correctness or professional quality of a later deliverable.

The source CSV is ASCII, which is a valid UTF-8 subset, with no BOM. It has no client identifier and no complete date/year field. The original documentation describes May 2008 to November 2010 and ordering by date; that chronology is retained, not reconstructed.

All retained source bytes and documentation were obtained from UCI or Creative Commons primary sources. `download-receipts.json` records URLs, timestamps, available HTTP headers, byte lengths, and SHA-256 values. HTTP content type/length were absent for the ZIP response; ZIP CRC, member signatures, byte identity, and independent parsing establish local format integrity instead.
