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
| 9: export | 7334405 |
| 10: báo cáo | 601e48d |

## Bằng chứng UI đã hoàn tất

- Chương 9: ảnh B-01 tại 12.75 s và C-01 tại 20.75 s.
- So policy trên cùng params B-01: `viewer_policy_compare.json`, xe chính là policy chọn, bóng mờ baseline; ảnh `policy_before_after.jpg`.
- Chương 10: nạp hazard hợp lệ và chụp tại 4.9 s; `hazard_ui.json` đồng nhất với file chính. Trace thử chế độ Bạn được lưu ở `hazard_drive.json`; đây là thao tác agent, chỉ kiểm tra phanh ngắn đầu lượt.
- `evidence/shots/manifest.json`: nguồn cảnh, mốc ảnh và SHA256. Không có case cut_in/rear_ended thật để chụp.
- Sửa căn cứ khoảng cách ban đầu thành 246 m; chạy lại `mine` ngân sách 1500 và `export`. Scene/ranges/exposure không đổi; không có lỗi ego quy cho hazard. Zero-hit bị giới hạn bởi hazard xảy ra sớm ở phía xa.

## Bước người dùng còn lại

Nộp `evidence/Day11_202603012_final.zip` theo cổng nộp của lớp; nếu lớp yêu cầu GitHub thì push các commit hiện tại. Chưa thực hiện gửi bài hoặc push. Tự lái đủ chuyến bằng người dùng là kiểm tra bổ sung, chưa được nhận là đã làm.

## Tự kiểm rubric

Đây là kiểm tra điều kiện, không phải điểm chấm chính thức: A có 31 public tests đạt; B có pipeline đầy đủ nhưng chưa đối chiếu lời giải giảng viên; C đủ câu trả lời và ảnh thật ở câu 5–6; G có schema/physics và accepted ≥50%, không thấy lỗi ego quy cho hazard, đã xác nhận UI/ảnh, cảnh có hạn chế về thời điểm gặp ego; D có kiểm toán provenance và đối chiếu kết quả chạy lại. Không thể tuyên bố đạt 100 điểm.

Các file simulator, runner, grading tests và policy candidates không được sửa. `.gitignore` có thay đổi từ trước, không đưa vào các commit của bài lab. Chưa push các commit lên remote.
