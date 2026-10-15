# PRIVATE — synthetic recipient task and expected mechanics

Freeze before authors. These four records are **entirely synthetic evaluator fixtures**, not observations from UCI, real employees, completed audits, approvals or wine-quality findings. The integers in their row-position fields illustrate identifiers only. Do not mix them into source facts or charts. Empty CSV cells, `unknown` and `not done` are deliberate raw values and must survive the task unchanged. A derived status or note goes into a separate field.

## Exact task supplied to each fresh reader after the manager questions

> Dùng biểu mẫu và hướng dẫn bàn giao của trang để xử lý bốn phiếu SYN được cung cấp. Giữ nguyên các giá trị gốc, kể cả ô trống, `unknown` và `not done`. Ghi trạng thái cùng lý do còn thiếu của từng phiếu. Sau đó tạo **một dòng việc mới** cho SYN-C: giao việc xác nhận cho **SYN Coordinator**, yêu cầu xác nhận người kiểm tra và thời gian người đó có thể làm; không tự điền người kiểm tra còn trống hoặc biến `unknown` thành đã xác nhận. Dòng việc mới giữ liên kết với SYN-C và cặp tệp/vị trí gốc. Trả lại biểu mẫu đã điền hoặc các dòng CSV có thể dán vào biểu mẫu. Không bắt đầu kiểm tra và không gửi việc thật cho ai.

The task adds a coordinator for the new follow-up action; it does not appoint an available reviewer to the original audit record. All fixture confirmation words are simulated. No real authorization results.

## Expected mechanics, fixed before author results

| Fixture | Required derived status | Required preserved evidence / explanation |
|---|---|---|
| SYN-A | `READY FOR REVIEW` only | All simulated prerequisites confirmed; simulated record check done. No conversion to approved, started, passed wine quality or completed real audit. |
| SYN-B | `HOLD` | Source snapshot stays empty; provenance stays `unknown`; record check stays `not done`. Ask for confirmation/completion; do not silently fill raw fields. |
| SYN-C | `HOLD` | Assigned reviewer stays empty; availability stays `unknown`. New follow-up assigned to SYN Coordinator requests these confirmations, preserving original evidence. |
| SYN-D | `HOLD` | Scope stays `unknown`; permission stays `not done`. No invented permission or release to start. |

For the newly created action row, require: link to SYN-C; `SYN-red.csv` + data-row position `2`; action to confirm the reviewer and availability; action owner `SYN Coordinator`; original missing reviewer and `unknown` availability preserved directly or by a clear reference to the unchanged fixture; `HOLD` until confirmation; short reason. Do not require an invented deadline, email address, real name, extra source value, tasting result or software validator.

Accept equivalent Vietnamese labels if they preserve meaning. A human-readable CSV/template is enough. Do not penalize a different column order, visual design or a clear long-form representation. If the supplied template lacks raw fields, a linked unchanged input card plus separate derived row can satisfy preservation. An empty raw cell must not be replaced by the literal word `unknown`; they are distinct input states.

## Recipient scoring ledger

Record four status decisions separately, then these practical checks:

- Correct HOLD reasons and preserved raw inputs for all four fixtures.
- READY FOR REVIEW is never called approval to begin.
- One usable new action exists with the requested coordinator, task and original identity.
- The new coordinator assignment is distinct from the still-missing reviewer.
- A recipient can use the supplied template/instructions without inventing a missing rule or requiring a new application.

Mark each check `pass / fail / unclear`, quote the actual output and note any absent template field/instruction. Do not repair the author's package or the reader's answer before scoring. Keep source accuracy, recipient mechanics and visual preference as separate outcomes.
