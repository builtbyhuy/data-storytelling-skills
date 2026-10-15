# UCI Wine Quality source provenance

Source acquisition and URL checks: 2026-10-15 UTC. This public file records provenance and schema only; observed answer statistics are reserved for the private oracle.

## Authoritative sources

- Dataset landing page: https://archive.ics.uci.edu/dataset/186/wine+quality
- Dataset DOI: https://doi.org/10.24432/C56S3T
- Official archive downloaded: https://archive.ics.uci.edu/static/public/186/wine%2Bquality.zip
- Original red CSV URL (HTTP 200 checked): https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv
- Original white CSV URL (HTTP 200 checked): https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv
- Original dictionary URL (HTTP 200 checked): https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality.names
- License declaration: the UCI dataset page links CC BY 4.0.
- License URL: https://creativecommons.org/licenses/by/4.0/
- Downloaded legal text: https://creativecommons.org/licenses/by/4.0/legalcode.txt

The three original data/dictionary files below were extracted unchanged from the official archive. The legacy individual URLs were checked for availability; the retained file hashes refer to the archive members.

## Retained bytes

All files are under `input/source/`. SHA-256 is computed over the retained original bytes.

| File | Bytes | SHA-256 |
|---|---:|---|
| wine+quality.zip | 91353 | 3ed56667f4b828242bd732d7d1dd7f2861e54432239d7fa63877014cbb0304d4 |
| winequality-red.csv | 84199 | 4a402cf041b025d4566d954c3b9ba8635a3a8a01e039005d97d6a710278cf05e |
| winequality-white.csv | 264426 | 76c3f809815c17c07212622f776311faeb31e87610d52c26d87d6e361b169836 |
| winequality.names | 3305 | 15d215e73b39105952380fd487e4ce1bf5a6b83a425abb285c2ec55193d3ca92 |
| LICENSE-CC-BY-4.0.txt | 18657 | 9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411 |

## Source schema

Both CSVs have the same header and use the semicolon (`;`) separator, double-quoted field names, and a period for the decimal mark. The CSVs do not contain a wine-type column; red/white provenance comes from the source filename.

```text
"fixed acidity";"volatile acidity";"citric acid";"residual sugar";"chlorides";"free sulfur dioxide";"total sulfur dioxide";"density";"pH";"sulphates";"alcohol";"quality"
```

The first eleven columns describe physicochemical tests. `quality` is an ordered sensory score on the documented scale from 0 through 10. The original dictionary describes it as the median of at least three expert evaluations. Units are not supplied in the CSV header; do not invent them. The dataset concerns red and white Portuguese Vinho Verde samples. It does not supply brand, grape variety, or selling price.

No source column supplies a unique physical sample/bottle identifier. A derived `source_file` plus one-based `data_row` identifies a row of the retained file, with the header excluded; it does not establish a unique physical bottle. No duplicate rows have been removed or source bytes edited.

## Credit and reuse

Dataset credit: Cortez, P., Cerdeira, A., Almeida, F., Matos, T., and Reis, J. (2009). *Wine Quality* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56S3T.

The original dictionary requests citation of: P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis, *Modeling wine preferences by data mining from physicochemical properties*, Decision Support Systems 47(4), 547-553 (2009), https://doi.org/10.1016/j.dss.2009.05.016.

Reuse is under CC BY 4.0 as declared on the current UCI landing page. Retain attribution, source and license links, and identify any derived analysis or alterations. The retained CSVs are unmodified. A later brief or chart is derived analysis, not an endorsement by the dataset creators.
