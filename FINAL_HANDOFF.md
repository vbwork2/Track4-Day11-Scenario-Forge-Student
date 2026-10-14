# Bàn giao bản nộp Day 11

MSSV: 202603012. Thị trấn: D.

## Nội dung bản nộp

- `lab11/*.py`: đủ 10 TODO, public tests và parity chạy trong full suite.
- `REPORT.md`: đủ 9 câu tiếng Việt, giữ tiêu đề và câu hỏi gốc, dẫn số liệu thật.
- `hazard.json`: cảnh người băng ngang giữa đoạn, đúng schema studio; exposure là giả định được ghi rõ.
- `evidence/*.json`: kết quả mô phỏng bằng ngân sách mặc định.
- `evidence/final_tests.txt`, `evidence/final_audit.json`: log test và kiểm toán cuối.

## Checkpoint đã lưu

| Checkpoint | Commit |
|---|---|
| 0: khảo sát | Không commit rỗng |
| 1: TTC/contact | f99ee24 |
| 2: khả thi | 78c2083 |
| 3: Wilson | 3fbe909 |
| 4: CEM/mode | 02741e6 |
| 5: IS | e7cd26f |
| 6: progress/policy | e0577f9 |
| Vá lower bound Wilson | 849fdd5 |
| 7: pipeline | 5e4e4b3 |
| 8: hazard/mine | 18ac1fb |
| 9: export, ảnh còn thiếu | 7334405 |
| 10: báo cáo | 601e48d |

## Phần còn thiếu

Chưa có ảnh thật trong `evidence/shots/`, chưa thử tự lái và chưa kiểm tra mở hazard trong UI. Browser automation đã từ chối URL `file://`; phần này được ghi trong REPORT. Python đã kiểm tra schema và cảnh khả thi.

Mở thủ công `viewer/index.html` trong trình duyệt:

1. Chương 9: nạp `evidence/viewer.json`, chọn B-01 tại 12.75 s, C-01 tại 20.75 s. Chụp hai mode có ví dụ vào `evidence/shots/`.
2. B-01: bật bóng mờ để chụp base vs fix; policy chọn tránh được va chạm baseline.
3. Chương 10: nạp `hazard.json`, chụp tại 4.9 s (tiếp xúc W2b–H0; ego không va chạm).
4. Thêm đường dẫn ảnh ở câu 5, 6, 9, rồi commit báo cáo và ảnh. Không có ví dụ thật của cut_in/rear_ended để chụp.

## Tự kiểm rubric

Đây là kiểm tra điều kiện, không phải điểm chấm chính thức: A có 31 public tests đạt; B có pipeline đầy đủ nhưng chưa đối chiếu lời giải giảng viên; C đủ câu trả lời, còn thiếu ảnh ở câu 5–6; G có schema/physics và accepted ≥50%, không thấy lỗi ego quy cho hazard, còn thiếu xác nhận UI/ảnh; D có kiểm toán provenance và đối chiếu kết quả chạy lại. Không thể tuyên bố đạt 100 điểm.

Các file simulator, runner, grading tests và policy candidates không được sửa. `.gitignore` có thay đổi từ trước, không đưa vào các commit của bài lab. Chưa push các commit lên remote.
