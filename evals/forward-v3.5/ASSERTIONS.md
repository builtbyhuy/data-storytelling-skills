# PRIVATE — assertion specification; no source answers

Evaluator only. Do not give this file, the oracle, or recipient fixtures to authors. This file specifies checks before author launch. It contains no observed counts, rates, distributions, duplicate totals, winner, or source-derived answer. The source owner computes and seals actual expected values independently, after method freeze and before inspecting author results. Do not fill values from an author's output.

## Oracle contract

Use the exact sealed source bytes and their manifest. Preserve both original files. A data row means a parsed CSV record after the header, indexed from one; it is not necessarily a physical line. Record the parser and original separator/header handling. Fail explicitly if the file cannot be parsed reliably; do not quietly skip malformed records.

For each original file `f`, compute privately:

| Key | Expected expression / independent evidence |
|---|---|
| `N_f` | Number of original parsed data records, including exact duplicates. |
| `QVALID_f` | Count whose quality is a finite integer in the stated ordinal range 0–10. Preserve raw text and document parsing. |
| `QBAD_f` | Original rows with missing, nonnumeric, out-of-range or noninteger quality; retain reason and row position. |
| `L_f` | Count of original records with valid quality and quality <= 5. |
| `P_f` | `L_f / N_f`; keep exact numerator/denominator and unrounded value. If `N_f` is zero, undefined, not zero. |
| `H_f(q)` | Count of original records at every integer quality `q` in 0–10, including zero-count bins. |
| `DUP_EXTRA_f` | Number of rows beyond the first instance of each exact complete-record duplicate within this file, using a declared field-wise equality rule. |
| `DUP_GROUPS_f` | Number of repeated complete-record groups; distinguish this from duplicate-extra-row count. |
| `DELTA_PP` | `100 * (P_red - P_white)` percentage points; direction and absolute size are source-valued answers. |
| `CASE_f(k)` | Original record at data-row position `k`, for the proposed first-20-per-file audit list if available. Row identity is file + position. |

Reconcile `QVALID_f + QBAD_f = N_f`, `sum_q H_f(q) = QVALID_f`, and `L_f = sum_(q<=5) H_f(q)`. Retaining original rows is required for the requested primary comparison. A separately labeled duplicate sensitivity analysis may supplement it, with its own denominator; it cannot replace it or establish which row is erroneous.

If bad quality exists, the primary reported fraction remains the observed valid-threshold numerator over all original rows. The report must reveal the bad/missing count and avoid treating unknown quality as demonstrated above-threshold quality. Evaluate whether any uncertainty could change the directional reading. Never invent missing time/winery/batch/price/cost fields.

## Artifact/source acceptance checks against the sealed oracle

Mark each `correct / incorrect / not ascertainable`, with the exact report location and source evidence. A plausible design or a successful build is not evidence of numerical truth.

| ID | Assertion to verify; no expected answer is disclosed here |
|---|---|
| M01 | Both original-file row counts are stated correctly, with the right grain. |
| M02 | Both threshold counts are correct, retain duplicates and use the provided <= 5 predicate. |
| M03 | Each displayed percentage uses the corresponding original-file denominator, correct arithmetic and honest rounding. |
| M04 | The direction of the between-file comparison and any stated percentage-point difference match the oracle. Percent and percentage points are distinguished. |
| M05 | The complete ordinal distribution is recoverable for each file; plotted marks and labels agree with facts and do not silently interpolate unsupported score values. |
| M06 | Any duplicate claim uses a defined duplicate measure, correct count and appropriate uncertainty about whether records are erroneous. |
| M07 | Any quality missing/invalid claim is correct; handling and denominator effects are visible. |
| M08 | The leading claim fairly reflects the distribution and any relevant counterevidence; it does not equate the threshold fraction alone with universal superiority. |
| M09 | The hypothetical triage rule is not presented as a scientific defect limit; rows are not presented as unique bottles or people. |
| M10 | No unsupported causal, current-market, tasting, manufacturing, price, cost or revenue claim appears. |
| M11 | Audit arithmetic is correct for the stated assumptions: 40 records, 20 per type, two reviewers with 20 each, 3 minutes each, 120 staff-minutes and one hour only under the declared parallel assumption. |
| M12 | Audit purpose, nonrandom selection, file+position identity and all HOLD gates are clear. No actual staff availability or approval is invented. |
| M13 | The facts file, HTML and retained inputs agree, and the unmodified recipe regenerates materially identical facts and report content. |
| M14 | Main claims, denominators, ordinal distribution, caveats and next step remain available/readable in the common desktop and mobile captures. |

Numerical tolerance: integer counts and row identity must match exactly. Displayed rates may differ only by the explicitly shown rounding precision; recomputing from displayed numerator/denominator must land in that rounding interval. Do not allow a large generic floating-point tolerance to excuse a wrong denominator. The source owner records expected intervals privately.

## Fixed fresh-reader questions

Administer in this order, without oracle access, peer outputs or method labels. First ask from the rendered report alone; record the answer and the exact place the reader used. Do not lead with a source-derived answer.

1. Theo trang này, tệp nào có tỷ lệ mẫu `quality <= 5` cao hơn, hay trang chưa đủ cơ sở xác định? Nêu tử số, mẫu số, tỷ lệ của cả hai và ý nghĩa của ngưỡng.
2. Phân bố điểm cho biết điều gì khiến kết luận mở đầu cần thận trọng? Nếu trang không thể hiện đủ để đọc, nói rõ điều thiếu; không tự đoán số.
3. Có thể kết luận rằng số dòng là số chai riêng biệt, một loại luôn tốt hơn, hoặc đặc tính hóa học gây ra điểm chất lượng không? Dựa vào đâu?
4. Việc gì được đề xuất tiếp theo, cần bao nhiêu công/thời gian theo giả định, và điều gì phải được xác nhận trước khi bắt đầu?

Then give the identical private recipient task and four synthetic fixture cards. Permit the supplied handoff package for that stage. Keep the manager stage answer unchanged after opening additional files.

Score manager task accuracy separately from visual preference. Record missing evidence, answer effort and uncertainty instead of awarding points for confident prose. Independent readers are fresh sessions of the same common model; this is not a human-comprehension or population study.

## Reader-only rubric, distinct from artifact checks

Only the four questions above create reader obligations. M01–M14 remain artifact/source/build checks, not fourteen reader-answer requirements. Score RM1–RM4 independently: correct, incorrect, missing, or justified abstention. Record extraction cause: faithful to source-correct report, faithful to source-wrong report, misread, absent evidence, or abstention. Do not silently repair either artifact or response.

| ID | Asked content only |
|---|---|
| RM1 | Higher observed threshold fraction; both numerators, denominators and rates; hypothetical threshold meaning; evidence location. No required exact percentage-point difference. Any volunteered difference must be correct. |
| RM2 | A supported distribution-based caution, or a specific justified account of unavailable/unreadable evidence. No required recital of every bin or one preselected numerical contrast. |
| RM3 | Address all three named inferences: unique bottles, universal superiority and chemical causation, with reasons supported by the report. No requirement to repeat all other unsupported categories. |
| RM4 | Proposed next work, staff effort/conditional elapsed time and relevant assumptions, plus pre-start confirmations, with evidence location. Do not separately fail unasked row identity, nonrandom-selection label or every allocation detail. Record minor omissions qualitatively. |

A correct source-grounded abstention is distinct from an incorrect guess and does not establish the artifact made the requested evidence accessible. Preserve both ledgers. The four bundled SYN cases do not exhaustively isolate every individual gate. Do not require 40 completed real audit rows.
