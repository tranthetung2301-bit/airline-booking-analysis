# ✈️ BẢNG TỔNG HỢP TOÀN BỘ YÊU CẦU ĐỀ BÀI & KẾT QUẢ THỰC HIỆN
**Học phần: Phân tích Dữ liệu (Data Analytics) — Đề tài: Dữ liệu Đặt vé Máy bay (Aurora Air & Horizon Wings)**  
*Tài liệu tổng hợp phục vụ nộp bài và bảo vệ trước Hội đồng chấm thi*

---

## 📌 I. THÔNG TIN CHUNG & HỒ SƠ BÀI NỘP

* **Tên đề tài:** Phân tích & Làm sạch Dữ liệu Đặt vé Máy bay (Giai đoạn 2024–2026).
* **Mô hình nghiên cứu:** Hai hãng hàng không giả định:
  * **Aurora Air:** Hãng hàng không truyền thống đầy đủ dịch vụ (Full-Service Carrier - FSC).
  * **Horizon Wings:** Hãng hàng không thế hệ mới, tối ưu hóa chi phí.
* **Quy mô dữ liệu thô:** 10.325 dòng $\times$ 24 cột (`data/airline_bookings_dirty.csv`).
* **Thời điểm chốt sổ phân tích (*Snapshot Date*):** Ngày **15/09/2026**.
* **Kết quả kiểm thử cấu trúc tự động:** **83/83 tiêu chí ĐẠT** (`python tools/kiem_tra_nop_bai.py .`).

---

## 📑 II. CHI TIẾT TỪNG GIAI ĐOẠN ĐỀ BÀI YÊU CẦU & KẾT QUẢ ĐẠT ĐƯỢC

### 1. Giai đoạn A — Khảo sát chất lượng dữ liệu ban đầu
* **Yêu cầu đề bài:**
  * Khảo sát tỷ lệ ô thiếu trên toàn bộ 24 cột (phân biệt giữa ô trống rỗng và ký hiệu rác).
  * Phát hiện và lập danh mục ít nhất 10 nhóm vấn đề chất lượng dữ liệu.
* **Kết quả thực hiện:**
  * Xuất bảng tỷ lệ ô thiếu `outputs/tables/a_missing_survey.csv` (24 trường).
  * Xác lập danh mục **12 nhóm lỗi cốt lõi** (`outputs/tables/a_issue_catalog.csv`):
    * `I01`: Trùng lặp khóa chính & 208 bản sao dư thừa trên 23 cột.
    * `I02`: Giá trị ngày tháng bị điền nhầm sang cột `booking_status` (18 dòng).
    * `I03`: Ký hiệu rác phi quy ước (`NULL`, `N/A`, `?`, `unknown`, `-`).
    * `I04`: Nhãn danh mục không đồng nhất về viết hoa/thường và khoảng trắng thừa.
    * `I05`: Trường ngày tháng bị phân mảnh dưới 4 định dạng khác nhau.
    * `I06`: Số đo bị dính hậu tố văn bản (`days`, `pax`, `requests`).
    * `I07`: Giá vé bị lẫn ký hiệu tiền tệ (`$`, `USD`, `EUR`) và dấu phẩy phân cách.
    * `I08`: Tồn tại 9 vé có giá bằng 0 đồng (vé thưởng/nội bộ hợp lệ cần bảo toàn).
    * `I09`: Mã quốc gia chưa chuẩn ISO (chứa tên tiếng Anh đầy đủ, viết thường).
    * `I10`: 42 bản ghi mâu thuẫn giữa `is_cancelled` và `booking_status`.
    * `I11`: Ngày trạng thái diễn ra sau ngày chốt sổ hoặc trước ngày đặt vé.
    * `I12`: Mã khoang cabin ngoài danh mục quy ước chuẩn.

---

### 2. Giai đoạn B — Chuỗi quy tắc làm sạch dữ liệu (B1 $\rightarrow$ B8)
* **Yêu cầu đề bài:**
  * Thiết lập pipeline làm sạch tự động bằng mã Python, ghi nhật ký ít nhất 10 quy tắc vào `cleaning_log.csv`.
  * Lập bảng truy vết đủ 10.325 dòng gốc (`row_lineage.csv`) với 3 trạng thái: `kept`, `merged`, `dropped`.
  * Đảm bảo bảng dữ liệu sau làm sạch còn đúng **10.000 dòng đặt chỗ độc lập**.
* **Kết quả thực hiện:**
  * **B1 (Chuẩn hóa khóa & Khử trùng lặp):** Viết hoa `reservation_id` (ARxxxxxx); loại bỏ đúng 208 dòng bản sao dư thừa trên 23 cột (gán `dropped` trong lineage).
  * **B2 (Sửa ngày lệch cột):** Chuyển 18 giá trị ngày tháng từ `booking_status` sang `booking_status_date` và gán lại `booking_status = pd.NA`.
  * **B3 (Quy chuẩn ô thiếu):** Đưa toàn bộ ký tự rác về `pd.NA`. **Tuyệt đối không điền khống (Zero-imputation)** vào các trường bị thiếu.
  * **B4 (Đồng bộ nhãn & cờ hủy):** Xử lý dứt điểm 42 dòng xung đột: nếu `Cancelled` $\rightarrow$ `is_cancelled = 1`; nếu `Flown`/`No-Show` $\rightarrow$ `is_cancelled = 0`.
  * **B5 (Parse ngày chuẩn ISO):** Chuẩn hóa toàn bộ ngày tháng về định dạng ISO `YYYY-MM-DD`.
  * **B6 (Làm sạch số đo & giá vé):** Tách bỏ ký tự text; chuẩn hóa `avg_ticket_fare` về `float64` (bảo toàn 9 vé 0 đồng hợp lệ).
  * **B7 (Chuẩn hóa mã quốc gia):** Ánh xạ sang mã quốc tế ISO Alpha-3 (`VNM`, `CHN`, `JPN`...).
  * **B8 (Hợp nhất 117 dòng trùng mã):** Chọn bản ghi ít ô thiếu nhất làm dòng chính (`kept`), bổ sung thông tin từ bản ghi phụ (`merged`). Bảng sạch đạt đúng chuẩn **10.000 dòng**.

---

### 3. Giai đoạn C — Cấu trúc dữ liệu sạch & Bộ kiểm thử tự động
* **Yêu cầu đề bài:**
  * Tạo đủ 7 cột dẫn xuất nghiệp vụ trong `reservations_clean.csv`.
  * Tổng hợp bảng theo dõi chu kỳ tháng `monthly_summary.csv` (không trùng khóa `airline - year - month`).
  * Xuất đủ 5 tệp dữ liệu cốt lõi và vượt qua bộ kiểm thử tự động.
* **Kết quả thực hiện:**
  * **7 Cột dẫn xuất:**
    1. `departure_year`: Năm khởi hành (lấy từ `departure_date`).
    2. `departure_month`: Tháng khởi hành (lấy từ `departure_date`).
    3. `total_trip_days`: Tổng số ngày lưu trú (`trip_weekend_days + trip_weekdays`).
    4. `total_passengers`: Tổng số hành khách (`adult + child + infant`).
    5. `lead_time_group`: 5 phân nhóm chuẩn (`0-7`, `8-30`, `31-90`, `91-180`, `181+`).
    6. `cabin_changed_flag`: Cờ đổi hạng khoang (`booked != assigned`).
    7. `booking_value_est`: Tổng giá trị vé ước tính (`avg_ticket_fare * total_passengers`, chỉ tính cho vé không hủy).
  * **5 Tệp đầu ra cốt lõi xuất tại `outputs/`:**
    * `reservations_clean.csv`: 10.000 dòng $\times$ 30 cột.
    * `monthly_summary.csv`: 52 tháng tổng hợp (26 tháng $\times$ 2 hãng), khớp 100% số liệu.
    * `cleaning_log.csv`: Ghi nhận 15 quy tắc chi tiết kèm lý do và phép kiểm tra sau.
    * `row_lineage.csv`: Đủ 10.325 dòng gốc (10.000 `kept`, 117 `merged`, 208 `dropped`).
    * `quality_report.csv`: So sánh chất lượng Before vs After của 24 trường dữ liệu.
  * **Bộ kiểm thử C4:** Đạt chuẩn **51/51 tests** trong `tests/test_cleaning.py`.

---

### 4. Giai đoạn D — Phân tích thực nghiệm (Câu 1 đến Câu 10) & 6 Insight

#### Bảng tóm tắt kết quả 10 câu hỏi nghiệp vụ:
| Câu | Bài toán phân tích | Mẫu số xác định ($N$) | Kết quả cốt lõi | Biểu đồ minh họa |
|:---:|---|:---:|---|---|
| **Câu 1** | Đối chiếu Trước & Sau làm sạch | 10.325 $\rightarrow$ 10.000 | Giảm 325 dòng dư/trùng, giữ nguyên 10.000 đặt chỗ độc lập, xóa sạch 42 dòng mâu thuẫn cờ hủy. | Bảng `q01_before_after.csv` |
| **Câu 2** | Thị phần & Tỷ lệ hủy theo hãng | 10.000 | **Aurora Air:** 6.522 vé (65,22%), hủy 27,11%.<br>**Horizon Wings:** 3.478 vé (34,78%), hủy 27,86%. | `fig01_airline_cancel.png` |
| **Câu 3** | Mùa vụ đặt chỗ năm 2025 | 5.753 (trọn 12 tháng) | Mô hình hai đỉnh: Đỉnh hè (Tháng 7-8 đạt ~10-11%) và Đỉnh cuối năm (Tháng 12 đạt ~10,4%). Đáy rơi vào Tháng 5 và Tháng 10. | `fig02_monthly_departures_2025.png` |
| **Câu 4** | Lead Time & Rủi ro hủy đặt chỗ | 9.978 | Trung vị lead time: 57 ngày (Aurora), 58 ngày (Horizon). Tỷ lệ hủy tăng phi tuyến từ 22,22% (0-7 ngày) lên **44,63%** (181+ ngày). | `fig03_leadtime_cancel.png` |
| **Câu 5** | Top 10 quốc gia hành khách | 9.895 | **Việt Nam dẫn đầu:** 2.080 vé (21,02%), gấp 2,3 lần Trung Quốc (906 vé, 9,16%), tiếp theo là Nhật Bản (6,70%), Hàn Quốc (5,32%). | `fig04_top10_country.png` |
| **Câu 6** | Phân khúc thị trường (Market Segment) | 9.968 | **Online OTA** lớn nhất (39,17%) nhưng hủy cao nhất (29,47%). **Corporate** ổn định nhất: hủy chỉ 21,45% (thấp hơn OTA 8,02 pp). | `fig05_segment_cancel.png` |
| **Câu 7** | Tác động của chính sách giá vé | 9.957 | **Non-Refundable:** tỷ lệ bay 77,26%, hủy 21,30%.<br>**Flexible:** tỷ lệ hủy lên tới 28,56%. Tỷ lệ No-Show rất thấp (1,4% - 1,6%). | `fig06_fare_policy_status.png` |
| **Câu 8** | Giá vé trung bình theo hãng | 7.224 (không hủy, giá > 0) | Phân phối lệch phải mạnh. **Trung vị Aurora Air ($149,54)** cao hơn **Horizon Wings ($135,26)** là $14,28 (+10,56%). | `fig07_fare_hist.png` |
| **Câu 9** | Độ dài chuyến đi (Total Trip Days) | 7.232 (không hủy) | Trung vị chuyến đi: 4 ngày. Nhóm **3–4 ngày chiếm ưu thế lớn nhất (31–32%)**, gần 80% khách đi từ 1 đến 7 ngày. | `fig08_trip_days.png` |
| **Câu 10** | Tỷ lệ đổi hạng cabin | 9.921 | Tỷ lệ đổi cabin bình quân toàn mạng bay ~11,5% (Aurora: 11,39%, Horizon: 11,74%). Khoang Thương gia đổi nhiều nhất (**B3 đạt 13,56%**). | `q10_cabin_change...` |

---

### 5. Hệ thống 6 Insight kinh doanh then chốt (Key Business Insights)

1. **Insight 1 (Khoảng cách đặt vé):** Đặt vé trước càng xa, rủi ro hủy vé càng cao (đạt đỉnh 44,63% ở nhóm trên 6 tháng, gấp 2,01 lần nhóm đặt trong tuần bay).  
   $\rightarrow$ *Hành động:* Thu tiền cọc lũy tiến đối với các giao dịch đặt trước trên 90 ngày để sàng lọc đơn giữ chỗ ảo.
2. **Insight 2 (Chính sách giá vé):** Vé Non-Refundable có tỷ lệ bay thành công cao nhất (77,26%) và tỷ lệ hủy thấp nhất (21,30%) do chế tài tài chính mất 100% tiền vé.  
   $\rightarrow$ *Hành động:* Tối ưu hóa phân bổ vé Semi-Flexible để cân bằng giữa tính linh hoạt và tỷ lệ lấp đầy ghế.
3. **Insight 3 (Kênh Online OTA):** Kênh OTA đóng góp quy mô lớn nhất (39,17%) nhưng lại tiềm ẩn rủi ro hủy cao nhất mạng bay (29,47%).  
   $\rightarrow$ *Hành động:* Rút ngắn thời hạn thanh toán giữ vé của đối tác OTA xuống 24 giờ và đẩy mạnh kích cầu kênh trực tiếp Direct.
4. **Insight 4 (Chu kỳ mùa vụ hai đỉnh):** Nhu cầu bay biến động hai đỉnh đồng pha vào mùa hè (Tháng 7-8) và cuối năm (Tháng 12) giữa hai hãng.  
   $\rightarrow$ *Hành động:* Áp dụng định giá động (Dynamic Pricing) trong cao điểm; bảo dưỡng đội bay và tung gói Package Tour vào tháng thấp điểm (Tháng 5 và Tháng 10).
5. **Insight 5 (Định vị giá vé):** Giá vé có phân phối lệch phải mạnh do tác động của vé hạng sang. Trung vị giá vé Aurora Air cao hơn Horizon Wings 10,56%.  
   $\rightarrow$ *Hành động:* Horizon Wings cần mở rộng bán kèm các gói dịch vụ phụ trợ (hành lý, suất ăn) để nâng cao doanh thu trên mỗi ghế.
6. **Insight 6 (Điều phối cabin):** Hơn 88% khách bay đúng khoang đã đặt; biến động đổi cabin tập trung tại khoang Thương gia (B3 đạt 13,56%) do nghiệp vụ nâng hạng giải tỏa quá tải.  
   $\rightarrow$ *Hành động:* Chuẩn hóa quy chế nâng hạng thương quyền (Operational Upgrade) thành quyền lợi khách hàng thân thiết.

---

## 📂 III. CẤU TRÚC BỘ HỒ SƠ NỘP BÀI CHUẨN

Thư mục dự án đã được tinh gọn, loại bỏ toàn bộ các file văn bản nháp/dư thừa, sẵn sàng nộp bài:

```text
airline-booking-analysis/
├── airline_analysis.ipynb          # Notebook thực thi hoàn chỉnh từ đầu đến cuối
├── Bao_cao_Hang_khong.pdf          # Báo cáo PDF chính thức (biên dịch từ LaTeX Overleaf)
├── Bao_cao_Hang_khong.docx         # Báo cáo Word học thuật
├── README.md                       # Tài liệu tổng quan dự án và phân công nhóm
├── TONG_HOP_YEU_CAU_DE_BAI.md      # File tổng hợp toàn diện đề bài & số liệu (file này)
├── requirements.txt                # Thư viện môi trường (Python, pandas, matplotlib)
├── data/
│   └── airline_bookings_dirty.csv  # Tệp dữ liệu gốc (10.325 dòng nguyên vẹn)
├── outputs/
│   ├── reservations_clean.csv      # Bảng 10.000 đặt chỗ sạch tiêu chuẩn
│   ├── monthly_summary.csv         # Bảng tổng hợp chỉ số 52 tháng
│   ├── cleaning_log.csv            # Nhật ký 15 quy tắc làm sạch
│   ├── row_lineage.csv             # Truy vết 10.325 dòng (kept, merged, dropped)
│   ├── quality_report.csv          # Báo cáo đối chiếu chất lượng Before/After
│   ├── tables/                     # 14 bảng dữ liệu phân tích chi tiết (q01 -> q10)
│   └── figures/                    # 8 biểu đồ trực quan hóa chuẩn kỹ thuật (fig01 -> fig08)
├── reports/
│   ├── main.tex                    # Mã nguồn LaTeX tiếng Việt học thuật
│   ├── final_report_overleaf.zip   # Gói zip Overleaf chứa main.tex và toàn bộ ảnh
│   └── figures/                    # Toàn bộ file ảnh PNG phục vụ biên dịch
├── src/                            # Mã nguồn module hóa (cleaning, feature, analysis)
├── tests/                          # Bộ kiểm thử tự động (test_cleaning.py)
└── tools/                          # Công cụ kiểm tra nộp bài tự động (kiem_tra_nop_bai.py)
```

---

## 🎯 IV. BẢNG CHEAT SHEET CÁC CON SỐ TRỌNG YẾU ĐỂ BẢO VỆ

| Chỉ số / Bài toán | Con số chính xác cần nhớ khi giảng viên hỏi |
|---|---|
| **Số dòng làm sạch** | $10.325 \rightarrow 10.000$ (Bỏ 208 dòng bản sao, gộp 117 dòng trùng mã đặt chỗ) |
| **Xung đột logic cờ hủy** | Khử dứt điểm 42 dòng mâu thuẫn giữa `is_cancelled` và `booking_status` |
| **Thị phần đặt chỗ** | Aurora Air chiếm **65,22%** (6.522 vé) — Horizon Wings chiếm **34,78%** (3.478 vé) |
| **Tỷ lệ hủy vé theo hãng** | Aurora Air: **27,11%** — Horizon Wings: **27,86%** (Chênh lệch chỉ 0,75%) |
| **Trung vị Lead Time** | Aurora Air: **57 ngày** — Horizon Wings: **58 ngày** (Khoảng Q1-Q3 là 27–99 ngày) |
| **Tỷ lệ hủy theo Lead Time** | Nhóm 0–7 ngày: **22,22%** $\rightarrow$ Nhóm 181+ ngày: **44,63%** (Tăng gấp 2,01 lần) |
| **Thị trường lớn nhất** | **Việt Nam (VNM): 21,02%** (2.080 vé) — Trung Quốc (CHN): **9,16%** (906 vé) |
| **Kênh bán vé hủy cao nhất** | **Online OTA: 29,47%** (Kênh thấp nhất là **Corporate: 21,45%**) |
| **Chính sách giá vé bay cao nhất**| **Non-Refundable: 77,26%** bay (Hủy 21,30%; Flexible hủy 28,56%) |
| **Trung vị giá vé theo hãng** | Aurora Air: **149,54 USD** — Horizon Wings: **135,26 USD** (Cao hơn 10,56%) |
| **Thời gian chuyến đi phổ biến** | Trung vị **4 ngày**; nhóm **3–4 ngày chiếm 32%**, nhóm 1–2 ngày chiếm 20% |
| **Tỷ lệ đổi cabin** | Toàn mạng bay đạt **11,5%** (Aurora: 11,39%, Horizon: 11,74%; Mã B3 cao nhất 13,56%) |

