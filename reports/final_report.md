# BÁO CÁO GIỮA KỲ: PHÂN TÍCH & LÀM SẠCH DỮ LIỆU ĐẶT VÉ MÁY BAY
**Dự án mô phỏng: Aurora Air & Horizon Wings (Giai đoạn 2024–2026)**
*Bộ môn: Phân tích Dữ liệu (Data Analytics) — Nhóm thực hiện: NhomXX*

---

## PHẦN 1. TỔNG QUAN, BỐI CẢNH & NGUỒN DỮ LIỆU
*(Thành viên 2 — Tạ Minh Quân phụ trách soạn thảo)*

### 1.1. Bối cảnh bài toán kinh doanh
Trong ngành hàng không dân dụng hiện đại, bộ phận **Quản trị Doanh thu (Revenue Management)** đóng vai trò sống còn trong việc tối ưu hóa hiệu suất ghế bay (load factor) và tối đa hóa doanh thu từ giá vé. Hai hãng hàng không mô phỏng trong dự án này bao gồm:
* **Aurora Air:** Hãng hàng không truyền thống với dịch vụ đầy đủ (Full-Service Carrier - FSC), khai thác các chuyến bay nội địa và quốc tế với nhiều hạng ghế từ Phổ thông (Economy), Phổ thông đặc biệt (Premium Economy), Thương gia (Business) đến Hạng nhất (First Class).
* **Horizon Wings:** Hãng hàng không thế hệ mới tập trung vào sự linh hoạt, phân khúc khách hàng đa dạng từ khách cá nhân, khách đoàn (Group) đến các hợp đồng đối tác doanh nghiệp (Corporate Contract).

Dữ liệu đặt chỗ vé máy bay là nguồn tài sản vô giá ghi nhận toàn bộ hành vi đặt chỗ, thời gian đặt trước (*lead time*), phân khúc thị trường, kênh bán hàng và trạng thái cuối cùng của vé (*Flown, Cancelled, No-Show*).

### 1.2. Mục tiêu nghiên cứu và giải quyết bài toán
Mục tiêu trung tâm của dự án là chuyển đổi bộ dữ liệu đặt vé thô còn nhiều lỗi kỹ thuật thành một cơ sở dữ liệu phân tích sạch đạt chuẩn, đồng thời giải quyết các câu hỏi nghiệp vụ quan trọng:
1. **Làm sạch khoa học & truy vết 100%:** Thiết lập quy trình làm sạch dữ liệu tự động bằng mã Python, loại bỏ các bản ghi trùng lặp tuyệt đối, xử lý dị thường số đo, chuẩn hóa mã quốc tế và lập bảng truy vết `row_lineage.csv` đủ 10.325 dòng gốc.
2. **Chuẩn hóa cơ sở dữ liệu:** Xây dựng bảng đặt chỗ sạch `reservations_clean.csv` (10.000 dòng đặt chỗ độc lập), bổ sung 7 cột dẫn xuất nghiệp vụ và tổng hợp bảng chỉ số vận hành theo tháng `monthly_summary.csv`.
3. **Phân tích hành vi & hỗ trợ ra quyết định:** Phân tích tỷ lệ hủy theo hãng bay, theo thời gian đặt trước (*lead time*), theo chính sách hoàn hủy (*fare policy*) và phân khúc thị trường; từ đó đúc kết 6 insight kinh doanh có bằng chứng số liệu thuyết phục.

### 1.3. Mô tả nguồn dữ liệu
* **Tệp dữ liệu đầu vào:** `data/airline_bookings_dirty.csv` gồm **10.325 dòng × 24 cột**, ghi nhận các giao dịch đặt vé từ tháng 07/2024 đến tháng 08/2026.
* **Thời điểm chốt sổ phân tích (*Snapshot Date*):** Ngày **15/09/2026**.
* **Đặc điểm cài đặt lỗi có chủ đích:**
  * Lỗi khóa và trùng lặp: Trùng tuyệt đối 23 cột (416 dòng liên quan) và nhiều dòng cùng chia sẻ chung mã `reservation_id` (117 dòng trùng mã).
  * Lỗi định dạng ngày tháng: Lẫn lộn 4 kiểu định dạng ngày khác nhau (ISO, DD/MM/YYYY, Month DD, YYYY, DD-Mon-YYYY).
  * Lỗi lệch cột: Ngày tháng bị điền nhầm vào cột trạng thái `booking_status`.
  * Lỗi số đo và giá vé: Số đo có gắn kèm đơn vị văn bản (*days, pax, requests*); giá vé lẫn ký hiệu tiền tệ (`$`, `USD`, `EUR`) và dấu phẩy thập phân.
  * Mâu thuẫn nghiệp vụ: 42 bản ghi có sự xung đột giữa cờ hủy `is_cancelled` và trạng thái `booking_status`.

---

## PHẦN 2. CHẤT LƯỢNG DỮ LIỆU & CÁC QUYẾT ĐỊNH XỬ LÝ
*(Thành viên 1 — Trần Thế Tùng phụ trách hoàn thiện)*

*Phần này do Thành viên 1 trình bày chi tiết về:*
* Bảng khảo sát ô thiếu và 12 nhóm vấn đề dữ liệu (Giai đoạn A).
* Quy tắc chuẩn hóa khóa `reservation_id`, loại bỏ 208 bản sao ở bước B1.
* Quy tắc chuyển đổi ngày tháng nhầm cột (B2) và chuẩn hóa ký hiệu rác về `pd.NA` (B3).
* Ánh xạ danh mục hợp lệ và đồng bộ tính nhất quán `is_cancelled` ở bước B4.
* Chuyển đổi định dạng ngày tháng sang `datetime` ở bước B5.

---

## PHẦN 3. PHÁT HIỆN TỪ DỮ LIỆU & TRỰC QUAN HÓA
*(Thành viên 3 — BI & Data Analyst phụ trách hoàn thiện)*

*Phần này do Thành viên 3 trình bày chi tiết về:*
* Kết quả tính toán từ Câu 2 đến Câu 10.
* 8 biểu đồ trực quan hóa chuẩn kỹ thuật (`fig01_airline_cancel.png` đến `fig08_trip_days.png`).
* Trình bày chi tiết 6 Insight kinh doanh then chốt theo mẫu chuẩn (Phát hiện chính, Bằng chứng số liệu, So sánh định lượng, Giới hạn dữ liệu).

---

## PHẦN 4. GIỚI HẠN DỮ LIỆU & ĐỀ XUẤT HÀNH ĐỘNG
*(Cả nhóm đồng thuận biên soạn)*

### 4.1. Giới hạn của bộ dữ liệu
1. **Tính chất dữ liệu mô phỏng:** Dữ liệu được thiết kế nhân tạo phục vụ học tập, các mối tương quan (ví dụ lead time và tỷ lệ hủy) phản ánh quy luật mô phỏng, không thể suy rộng nguyên nhân nhân quả tuyệt đối cho toàn ngành hàng không thực tế.
2. **Khung thời gian không đồng đều:** Trong giai đoạn khảo sát (07/2024 – 08/2026), chỉ riêng năm 2025 là có trọn vẹn 12 tháng dữ liệu. Năm 2024 chỉ có từ tháng 7 và năm 2026 chỉ có đến tháng 8; do đó phân tích mùa vụ (Câu 3) bắt buộc phải cô lập riêng trên năm 2025 để tránh sai lệch tổng thể.
3. **Thiếu biến chi phí và lợi nhuận biên:** Cột `avg_ticket_fare` chỉ đại diện cho giá vé cơ sở bình quân của mỗi hành khách, không phản ánh phụ phí (hành lý, suất ăn, chọn chỗ) hay chi phí vận hành chuyến bay (nhiên liệu, nhân công). Do đó, chỉ số `booking_value_est` chỉ là giá trị đặt chỗ danh nghĩa, không được đồng nhất với doanh thu thực nhận.

### 4.2. Khuyến nghị và hướng phân tích tiếp theo
* Áp dụng chính sách đặt cọc linh hoạt cho các đặt chỗ có thời gian đặt trước xa (> 90 ngày) nhằm giảm thiểu tỷ lệ hủy vé.
* Tối ưu hóa phân bổ hạng ghế và chính sách nâng hạng (*cabin upgrade*) cho phân khúc khách hàng thường xuyên (*returning customers*).
* Thu thập thêm dữ liệu về mức độ hài lòng của khách hàng và thời điểm hủy vé cụ thể để xây dựng mô hình dự báo rủi ro hủy vé trong tương lai.

---

## PHẦN 5. PHÂN CÔNG CÔNG VIỆC NHÓM & ĐÁNH GIÁ MỨC ĐỘ ĐÓNG GÓP
*(Thành viên 2 — Tạ Minh Quân phụ trách soạn thảo)*

Nhóm gồm 3 thành viên, phối hợp chặt chẽ qua hệ thống quản lý phiên bản Git/GitHub, tuân thủ nghiêm ngặt quy trình pull trước khi code, commit đúng quy ước và kiểm thử tự động chéo trước khi tích hợp.

| Thành viên | Vai trò chính | Nhiệm vụ đảm nhiệm cụ thể | Sản phẩm đầu ra nghiệm thu | Tỷ lệ đóng góp |
|---|---|---|---|:---:|
| **Trần Thế Tùng** | Kỹ sư Làm sạch Dữ liệu (*Data Cleaning Specialist*) | • Phụ trách Giai đoạn A: khảo sát ô thiếu, phân loại 12 nhóm vấn đề.<br>• Phụ trách Giai đoạn B1–B5: chuẩn hóa khóa, chuyển ngày nhầm cột, xử lý ký hiệu rác, chuẩn hóa nhãn phân loại, parse ngày tháng.<br>• Viết nội dung Phần 2 Báo cáo Word. | • `a_missing_survey.csv`<br>• `a_issue_catalog.csv`<br>• Code sạch từ Ô 0 đến B5 trong notebook<br>• Ghi nhật ký các bước B1–B5 | **100%** |
| **Tạ Minh Quân** | Quản trị CSDL & Kiểm soát Chất lượng (*QA & Data Architect*) | • Phụ trách Giai đoạn B6–B8: làm sạch số đo, xử lý giá vé (giữ vé 0đ), chuẩn hóa mã quốc gia, gộp 117 dòng trùng `reservation_id`, lập `row_lineage.csv` đủ 10.325 dòng.<br>• Phụ trách Giai đoạn C1–C4: tạo 7 cột dẫn xuất, tổng hợp `monthly_summary.csv`, xuất 5 tệp cốt lõi, chạy bộ kiểm thử C4 (51/51 test đạt ✅).<br>• Phụ trách Câu 1 (Before/After), viết `README.md`, soạn Phần 1 & 5 Báo cáo. | • `reservations_clean.csv`<br>• `monthly_summary.csv`<br>• `cleaning_log.csv` (15 quy tắc)<br>• `row_lineage.csv` (10.325 dòng)<br>• `quality_report.csv`<br>• `q01_before_after.csv`<br>• `src/feature_engineering.py`<br>• `tests/test_cleaning.py`<br>• Tệp `README.md` hoàn chỉnh | **100%** |
| **Thành viên 3** | Chuyên viên Phân tích & Trực quan hóa (*BI & Data Analyst*) | • Phụ trách Giai đoạn D: tính toán chính xác mẫu số cho 9 câu hỏi nghiệp vụ (Câu 2 đến 10).<br>• Thiết kế 8 biểu đồ chuẩn kỹ thuật (`fig01` đến `fig08`).<br>• Soạn thảo bản nháp 6 Insight kinh doanh và hoàn thiện Phần 3 Báo cáo. | • 11 bảng phân tích CSV (`q02` đến `q10`)<br>• 8 biểu đồ PNG đạt chuẩn<br>• 6 Insight kinh doanh có bằng chứng<br>• Nội dung Phần 3 Báo cáo | **100%** |

**Cam kết của nhóm:** Tất cả các thành viên đều tham gia tích cực, thảo luận đồng thuận về mọi quyết định làm sạch và tự tin giải thích toàn bộ quy trình cũng như kết quả phân tích trong buổi bảo vệ trước giảng viên.
