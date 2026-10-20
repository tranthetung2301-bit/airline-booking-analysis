# Mẫu viết insight

**Yêu cầu:** tối thiểu **6 insight** từ **ít nhất 4 chủ đề khác nhau**; mỗi insight **80–120 từ**.
Chủ đề gợi ý: hãng hàng không · mùa vụ nhu cầu · lead time · quốc gia · phân khúc thị trường · chính sách giá vé · giá vé (giá vé bình quân) · thời gian chuyến đi · đổi hạng ghế · chất lượng dữ liệu.

---

## Bảng tổng hợp (điền trước khi viết)

| # | Chủ đề | Bằng chứng (Câu / Bảng / Hình) | Phát hiện chính (1 câu) |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |

---

## Insight 1 — [Tiêu đề ngắn nêu phát hiện]

- **Câu hỏi / chủ đề:**
- **Phát hiện chính:** (1 câu)
- **Số liệu, đơn vị và mẫu số:** … trên … đặt chỗ; điều kiện lọc: …; đã loại … đặt chỗ vì …
- **So sánh làm rõ phát hiện:** (chênh … điểm phần trăm / gấp … lần / so với hãng hàng không, tháng, nhóm …)
- **Ý nghĩa trong phạm vi dữ liệu:** (hai hãng hàng không, giai đoạn 2024–2026)
- **Giới hạn hoặc thông tin cần kiểm chứng:**
- **Bằng chứng:** Bảng `outputs/tables/…` · Hình `outputs/figures/…`

**Đoạn hoàn chỉnh (80–120 từ):**

> …

*Nhân bản cấu trúc này cho Insight 2 đến 6.*

---

## Ví dụ giả định (KHÔNG phải kết quả của bộ dữ liệu này)

> Trong 1.000 đặt chỗ có trạng thái của hãng hàng không A, 400 bị hủy (40%), cao hơn hãng hàng không B (25% trên 800 đặt chỗ) 15 điểm phần trăm. Khoảng cách xuất hiện ở hầu hết các tháng, nên không chỉ do một mùa cao điểm. Tuy nhiên, hai hãng hàng không khác loại hình và cơ cấu kênh bán; cần dữ liệu về lý do hủy và chính sách giá để giải thích chênh lệch. *(Nguồn: Bảng q02, Hình 1)*

| Cách viết | Đánh giá |
|---|---|
| “Hãng hàng không A bị hủy nhiều.” | Yếu — không số liệu, không mẫu số, không so sánh |
| “Hãng hàng không A nên bắt buộc chính sách giá vé để giảm hủy đặt chỗ.” | Vượt bằng chứng — dữ liệu không chứng minh quan hệ nhân quả |
| Đoạn ví dụ ở trên | Tốt — có số liệu, mẫu số, so sánh, ý nghĩa, giới hạn, nguồn |

---

## Tự kiểm tra từng insight

- [ ] Có số liệu **và** mẫu số; nêu rõ điều kiện lọc (ví dụ “chỉ đặt chỗ không hủy, avg_ticket_fare > 0”)
- [ ] Có ít nhất một phép so sánh (điểm phần trăm, số lần, giữa hãng hàng không/tháng/nhóm)
- [ ] Nêu ý nghĩa **trong phạm vi hai hãng hàng không của mẫu** (không suy rộng ra toàn ngành)
- [ ] Nêu ít nhất một giới hạn cụ thể
- [ ] Trỏ tới đúng tên bảng/hình
- [ ] Không dùng từ nhân quả (“khiến”, “dẫn đến”, “nhờ … nên”); không gọi `avg_ticket_fare`/`booking_value_est` là doanh thu thực tế
- [ ] Nêu cỡ mẫu khi so sánh nhóm nhỏ
- [ ] Không lặp lại cùng một thông tin với insight khác

**Nhắc lại:** Một tỷ lệ chỉ có ý nghĩa khi nêu đối tượng được tính và điều kiện lọc. Không điền số giả định vào báo cáo.
