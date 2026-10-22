# ✈️ Airline Booking Analysis (Aurora Air & Horizon Wings)

> **BÀI TẬP LỚN GIỮA KỲ — PHÂN TÍCH & LÀM SẠCH DỮ LIỆU ĐẶT VÉ MÁY BAY**  
> *Dự án mô phỏng: Aurora Air & Horizon Wings — Giai đoạn 2024–2026*

---

## 👥 1. Thành viên và phân công

| Họ tên | MSSV | Vai trò chính | Phụ trách chi tiết | Có thể giải thích thêm |
|---|---|---|---|---|
| **Trần Thế Tùng** | *(Điền MSSV)* | Kỹ sư Làm sạch Dữ liệu (*Data Cleaning Specialist*) | Giai đoạn A (Khảo sát 24 cột, tìm 12 nhóm vấn đề), Giai đoạn B1–B5, Phần 2 Báo cáo | Quy tắc xử lý ký hiệu rác B3, chuẩn hóa nhãn phân loại B4, định dạng ngày tháng B5 |
| **Tạ Minh Quân** | *(Điền MSSV)* | Quản trị CSDL & Kiểm soát Chất lượng (*QA & Data Architect*) | Giai đoạn B6–B8, Giai đoạn C1–C4, Câu 1 (So sánh Before/After), xuất 5 tệp cốt lõi, kiểm thử tự động, README.md, Phần 1 & 5 Báo cáo | Chiến lược đồng thuận khi gộp reservation_id, cấu trúc row_lineage.csv, công thức mẫu số cancel_rate_pct |
| **Nguyễn Đình Phan Anh** | *(Điền MSSV)* | Chuyên viên Phân tích & Trực quan hóa (*BI & Data Analyst*) | Giai đoạn D (Câu 2 đến Câu 10), thiết kế 8 biểu đồ chuẩn kỹ thuật, bản nháp 6 Insight, Phần 3 Báo cáo | Cách tính mẫu số 9 câu nghiệp vụ, phân tích mùa vụ và chính sách giá |

---

## 🚀 2. Cách chạy lại dự án

1. Clone repo hoặc giải nén `NhomXX_HangKhong.zip`, giữ nguyên cấu trúc thư mục.
2. Cài đặt môi trường phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```
3. Mở notebook `airline_analysis.ipynb` hoặc `notebooks/airline_analysis.ipynb` và chọn **Kernel** $\rightarrow$ **Restart & Run all**.
4. Toàn bộ kết quả sẽ được tự động xuất ra thư mục `outputs/`:
   - 5 tệp dữ liệu cốt lõi: `reservations_clean.csv`, `monthly_summary.csv`, `cleaning_log.csv`, `row_lineage.csv`, `quality_report.csv`
   - Bảng phân tích nguồn: `outputs/tables/`
   - Biểu đồ trực quan hóa: `outputs/figures/`
5. Kiểm tra chất lượng và cấu trúc bằng công cụ tự động:
   ```bash
   python tools/kiem_tra_nop_bai.py .
   ```

*Thời gian chạy toàn bộ trên máy nhóm:* khoảng **5 – 8 giây**.

---

## 🛠️ 3. Môi trường và thư viện

| Thành phần | Phiên bản | Ghi chú |
|---|---|---|
| **Python** | `3.9+` | Môi trường Python chuẩn |
| **pandas** | `2.3.3` | Xử lý dữ liệu bảng, kiểu `Int64`, `Float64` |
| **numpy** | `2.0.2` | Tính toán số học và điều kiện `np.where` |
| **matplotlib** | `3.9.4` | Vẽ biểu đồ và lưu file ảnh PNG |
| **Môi trường** | VS Code / Jupyter Notebook / Terminal | |

---

## 📊 4. Nguồn dữ liệu

Bộ dữ liệu mô phỏng `airline_bookings_dirty.csv` gồm **10.325 dòng × 24 cột**, được xây dựng riêng cho bài thực hành Airline Booking Analytics. Hai hãng hàng không `Aurora Air` và `Horizon Wings` là tên giả định, không đại diện cho doanh nghiệp thực tế. Dữ liệu có lỗi và bản ghi trùng được cài đặt có chủ đích để thực hành làm sạch, truy vết và phân tích dữ liệu chuyên nghiệp.

---

## ⚖️ 5. Quy tắc riêng của nhóm (Đồng thuận kỹ thuật)

| # | Tình huống kỹ thuật | Quy tắc nhóm lựa chọn | Lý do nghiệp vụ | Ảnh hưởng đến kết quả |
|---|---|---|---|---|
| 1 | Xung đột giá trị khi gộp cùng `reservation_id` | Sắp xếp theo `record_id` nhỏ nhất, ưu tiên lấy giá trị hợp lệ đầu tiên (*first non-null*) | Giữ tính đại diện nhất quán và không làm mất dữ liệu hợp lệ nếu một dòng bị khuyết | Hợp nhất 117 dòng trùng mã thành công, không tạo thêm ô thiếu nhân tạo |
| 2 | Giá vé bằng 0 đồng (`avg_ticket_fare == 0`) | Giữ nguyên trong bảng sạch; không xóa, không biến thành NaN | Đây là vé thưởng (award tickets), vé khách mời hoặc vé nội bộ hợp lệ | Số lượng vé 0đ được giữ nguyên; tính đúng doanh thu ước tính và phân phối giá vé |
| 3 | Xử lý dữ liệu thiếu (*Missing Imputation*) | Tuyệt đối **không** điền mean, median hay mode vào các ô thiếu không có cơ sở xác thực | Tôn trọng nguyên tắc trung thực dữ liệu, tránh tạo ra bằng chứng giả | Mẫu số tính toán tỷ lệ hủy và các chỉ số ở Giai đoạn D đạt độ chính xác khách quan |
| 4 | Mẫu số tính tỷ lệ hủy | Tính trên tổng số đặt chỗ có trạng thái xác định (`is_cancelled` không rỗng) | Loại trừ các dòng thiếu trạng thái gây sai lệch mẫu số | Tỷ lệ hủy cả năm phản ánh đúng thực tế, không lấy trung bình cộng tỷ lệ các tháng |

---

## 📦 6. Danh mục tệp đầu ra đã hoàn thành (Thành viên 1 & 2)

- [x] `airline_analysis.ipynb` (Notebook đã chạy trơn tru từ đầu đến C4 và Câu 1)
- [x] `README.md` (Tệp tài liệu tổng quan hoàn chỉnh)
- [x] `data/airline_bookings_dirty.csv` (File gốc 10.325 dòng nguyên vẹn)
- [x] `outputs/reservations_clean.csv` (10.000 dòng sạch chuẩn)
- [x] `outputs/monthly_summary.csv` (52 tháng tổng hợp, không trùng khóa)
- [x] `outputs/cleaning_log.csv` (15 quy tắc xử lý chi tiết kèm reason & check)
- [x] `outputs/row_lineage.csv` (10.325 dòng truy vết: kept/merged/dropped)
- [x] `outputs/quality_report.csv` (Báo cáo chất lượng Before vs After)
- [x] `outputs/tables/a_missing_survey.csv` (Khảo sát ô thiếu 24 cột)
- [x] `outputs/tables/a_issue_catalog.csv` (12 nhóm vấn đề dữ liệu)
- [x] `outputs/tables/q01_before_after.csv` (So sánh chất lượng Before/After Câu 1)
- [x] *Giai đoạn D (Câu 2–10) & 8 biểu đồ:* Thành viên 3 đang tiến hành
