MSSV: 202603012

# Lab 11 · Scenario Forge — báo cáo

Mỗi câu: trả lời ngắn, **trích số từ `evidence/`** (ghi tên file và trường, ví dụ `mc.json: crashes = 4`). Grader chạy lại với MSSV của bạn; số không khớp `evidence/` thì mất điểm phần D (RUBRIC), và câu dựa trên số sai khó được điểm đầy đủ. Không cần văn hay: một bảng nhỏ và hai, ba câu giải thích là đủ.

Thị trấn của bạn (`meta.json: _run.town`): D

## 1. Phát lại log có trung thực không? (bước A)

Trong `replay.json`: bao nhiêu kịch bản bị bỏ vì người lái gây va chạm, bao nhiêu va chạm khi planner chạy trên log phát lại, bao nhiêu trong thế giới phản ứng, theo từng loại tiếp xúc. Giải thích vì sao phần lớn va chạm của "phát lại" là `rear`, và vì sao đó là va chạm **giả**. Chọn một kịch bản trong `replay_only` và nói chuyện gì đã xảy ra.

`replay.json`: bỏ 1 log, dùng 399/400; phát lại có 95 va chạm (rear 85, side 9, front 1), thế giới phản ứng 0 và va chạm cả hai 0. Xe sau trong log giữ quỹ đạo/tốc độ cũ, không phản ứng với planner phanh sớm, nên phần lớn rear là giả trong thế giới phản ứng. Ví dụ `replay_only[0]` (scenario 0) là rear; bản reactive có TTC tối thiểu 7.46 s nhưng xe bám đuôi không thích nghi khi ego đổi tốc độ (`replay.json: replay, reactive, replay_only[0]`).

## 2. Kịch bản bất khả thi (bước B)

Liệt kê các luật trong `is_feasible` và căn cứ vật lý của từng luật (ma sát, gia tốc, tốc độ người). Trong `hunt.json`, cuộc săn nào sinh nhiều kịch bản bất khả thi nhất, và vì sao CEM lại bị kéo về phía đó? Điều gì xảy ra với ước lượng nếu bạn **đếm** chúng là va chạm?

Loại nếu chuyển làn 3.5 m cần gia tốc ngang `(π/cutDur)²·3.5/2 > μg`, phanh sau nhập làn `cutBrake > μg`, người đi bộ vượt 2.5 m/s, hoặc `cutV` ngoài `(0,22]` (`lab11/feasible.py`). Hunt bỏ bất khả thi: bus 6, cut-in 4, crosswalk 23, rear 6; nhiều nhất là crosswalk. CEM tối đa hóa điểm nguy hiểm nên dồn vào đuôi phân phối cực đoan; đếm các mẫu bị loại như va chạm sẽ thổi phồng xác suất bằng những tình huống vi phạm vật lý (`hunt.json: *.infeasible`).

## 3. Monte Carlo cho bạn biết gì (bước C1)

`mc.json`: k, n, p̂ và khoảng Wilson 95 %. Với p̂ đó, cần bao nhiêu lần chạy để khoảng tin cậy hẹp lại còn ±20 % của p? Có kiểu thất bại nào **chưa hề xuất hiện** trong 3 000 lần chạy không? Con số đúng cần báo cho kiểu đó là gì?

`mc.json`: k=4, n=3000, p̂=0.001333, Wilson 95% [0.000519, 0.003424]; 96/p̂ ≈ 72,000 lượt để nhắm sai số tương đối ±20%. Chỉ thấy 4 bus_bypass; cut_in, crosswalk_block, rear_ended và other đều 0 hit. Không kết luận xác suất bằng 0: Wilson upper mỗi mode 0 hit là 0.001279 (`mc.json: per_mode.*.hi`).

## 4. Importance sampling, ESS và độ suy biến (bước C3)

Bảng: với từng kiểu và từng seed trong `estimate.json`, ghi `p`, `hits`, `ess`, `top_share`. Ba seed có đồng ý với nhau không, và có đồng ý với Monte Carlo không? Ở đâu `top_share` lớn (> 0,5), và vì sao khi đó con số thực ra chỉ là trọng số của một mẫu? So ngân sách (`budget`) với số lần chạy Monte Carlo cần để có cùng độ chính xác. Phần `other` trong tổng lấy từ đâu, và vì sao không săn nó?

`estimate.json` (p; hits; ESS; top_share):

| Mode | Seed 0 | Seed 1 | Seed 2 |
|---|---|---|---|
| bus_bypass | 2.01e-4; 27; 132; .229 | 1.60e-3; 31; 131; .703 | 1.85e-4; 26; 130; .196 |
| cut_in | 0; 0; 116; 0 | 0; 0; 118; 0 | 0; 0; 109; 0 |
| crosswalk_block | 3.71e-6; 116; 128; .693 | 3.72e-7; 115; 119; .392 | 2.71e-7; 121; 125; .285 |
| rear_ended | 0; 0; 124; 0 | 0; 0; 115; 0 | 0; 0; 116; 0 |

Ba seed không ổn định hoàn toàn; bus seed 1 và crosswalk seed 0 có `top_share > .5`, nghĩa là một mẫu chi phối trọng số. Các số bus bao quanh MC 1.33e-3 nhưng dao động mạnh; IS không đồng thuận về crosswalk. Mode không hit có `upper_zero_hits=3/(0.2·600)=.025`, không phải xác suất bằng 0. Ngân sách IS 16,800 mẫu, gấp 5.6 lần MC 3,000; `other` lấy từ MC (0 hit/3000, upper .001279), không săn riêng vì lab chỉ nhắm bốn kiểu có score chuyên biệt (`estimate.json: seeds, budget, other`).

## 5. Các kiểu thất bại (bước C2 + 3D)

Mỗi kiểu bạn tìm thấy: một ảnh chụp trình xem 3D (chương 9) ở đúng lúc va chạm, và một câu mô tả chuỗi sự kiện (ai thấy gì, ai chờ gì). Kiểu nào cuộc săn **không** tìm thấy, và bạn tin điều đó ở mức nào? Nếu chỉ chạy **một** cuộc săn chung cho mọi kiểu thì điều gì xảy ra (gợi ý: `hunt.json: found` của từng cuộc săn)?

## 6. Sửa planner (bước E + 3D)

`fix.json`: policy được chọn, `fail` và `fail_hi` trên TRAIN, trên TEST (`fail_hi_seen` và `fail_hi`), và của policy gốc trên TEST; vì sao `fail_hi` của bản sửa có thể lớn hơn `fail` của policy gốc dù bản sửa tốt hơn thật? quãng đường và số lần phanh gấp. Một ảnh chụp 3D có **bóng mờ** (policy gốc) cho một kịch bản mà bản sửa tránh được. Có núm chỉnh nào "nghe thì an toàn hơn" nhưng thực tế làm tăng thất bại? Giải thích bằng cách thế giới phản ứng lại.

## 7. Từ mô phỏng ra đường thật

Phân phối tự nhiên trong `space.py` là giả định. Chọn **ba** giả định ảnh hưởng nhiều nhất đến con số của bạn (ví dụ khe chấp nhận của xe chuyển làn, tỉ lệ người đi bộ ngó qua xe buýt, ma sát đường ướt). Với mỗi cái: dữ liệu thật nào sẽ thay nó, lấy từ đâu, và nếu nó sai thì con số của bạn sai theo hướng nào?

`space.py` cho thị trấn D: (1) khe nhập làn `cutGap` lognormal, median 14 m; thay bằng quỹ đạo xe từ camera tại đoạn tương tự, đối chiếu thêm [NGSIM I‑80](https://highways.dot.gov/media/6016) (dữ liệu freeway nên chỉ tham khảo). Nếu khe thật nhỏ hơn, planner gặp xe nhập gần hơn và lỗi mô phỏng có thể bị đánh giá thấp. (2) `pedLook=1` xác suất 0.90; đếm video người đi bộ nhìn qua xe buýt tại điểm qua đường, theo loại dữ liệu exposure/crossing counts nêu trong [FHWA pedestrian data guide](https://www.fhwa.dot.gov/publications/research/safety/17106/004.cfm). Nếu tỷ lệ nhìn thật thấp hơn, người đi bộ ít nhường hơn và rủi ro mô phỏng thấp hơn thực tế. (3) mưa/đường ướt xác suất 0.15; thay bằng đo ma sát tại tuyến và thời tiết ghép theo thời gian, dùng cách đo liên tục như [FHWA CPFM](https://infomaterials.fhwa.dot.gov/data). Nếu đường ướt thường hơn, giới hạn phanh thấp hơn và xác suất lỗi sẽ bị đánh giá thấp (`space.py: VARIANTS, CONT, BIN`). Đây là kế hoạch thu dữ liệu thay giả định, không phải các ước lượng thực địa của lab.

## 8. Giới hạn

Ba điều mà xác suất bạn báo **không** nói, ví dụ: thế giới chỉ có một con phố; người lái chỉ là IDM; cảm biến hoàn hảo trừ phần bị xe buýt che. Nếu được thêm một tuần, bạn sẽ đo gì tiếp?

Con số này chỉ áp dụng cho một hình học phố và xe buýt cố định; các xe khác dùng IDM với vài tham số ngẫu nhiên chứ không mô hình hành vi đa dạng; cảm biến không có lỗi phân loại/vật cản ngoài đường nhìn bị xe che. Một tuần tiếp theo, tôi sẽ gắn camera để đếm người băng ngang và mức nhìn qua xe buýt, trích quỹ đạo/gap khi xe nhập làn, và ghép mưa với phép đo ma sát tại cùng tuyến (`avsim/core.py`, `avsim/space.py`).

## 9. Rắc rối của bạn (bước G + chương 10)

- **Rắc rối:** bạn dựng gì, và ngoài đời nó giống tình huống nào.
- **Căn cứ:** vì sao bạn nghĩ planner sẽ xử lý kém.
- **Giả định:** `space` và `exposure` lấy từ đâu (`hazard.json: why`).
- **Kết quả**, theo `mine.json`:
  - số va chạm `avoidable` (tránh được bằng phanh hết cỡ, biết trước), `unavoidable`, `unattributed`, và `low_speed`, với policy gốc và với policy bạn chọn; `accepted` (bao nhiêu phần `space` của bạn là khả thi);
  - P(lỗi planner | rắc rối) kèm khoảng Wilson;
  - tần suất mỗi chuyến, đặt cạnh tần suất lách xe buýt của bạn.
- **Hình:** một ảnh chương 9 hoặc 10 ở lúc va chạm.
- **Bạn tự lái thì sao:** nếu bạn đã thử lái, bạn tránh được không, và bạn làm gì khác planner?
- **Cách sửa:** núm chỉnh nào sửa được rắc rối này? Nếu không núm nào sửa được, planner cần thêm **logic gì** (mô tả, không cần code)?
