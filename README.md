# ✈️ Airline Booking Analysis

> **Bài Tập Lớn Giữa Kỳ — Phân Tích & Làm Sạch Dữ Liệu Đặt Vé Máy Bay**  
> *Dự án mô phỏng: Aurora Air & Horizon Wings — Giai đoạn 2024–2026*

---

## 📌 Giới thiệu

Dự án phân tích và làm sạch bộ dữ liệu đặt vé máy bay gồm **10.325 dòng × 24 cột**, thực hiện bằng Python (pandas, matplotlib, seaborn) trong Jupyter Notebook.

**Mục tiêu:**
- Làm sạch dữ liệu và lập bảng truy vết 100% dòng dữ liệu gốc
- Tạo 5 tệp dữ liệu sạch chuẩn và 14 bảng phân tích
- Trả lời 10 câu hỏi nghiệp vụ và vẽ 8 biểu đồ trực quan hóa
- Đúc kết 6 insight kinh doanh có bằng chứng

---

## 👥 Thành viên nhóm

| Thành viên | MSSV | Vai trò |
|---|---|---|
| Thành viên 1 | — | Data Cleaning Specialist (Giai đoạn A, B1–B5) |
| Thành viên 2 | — | QA & Data Architect (B6–C4, Câu 1) |
| Thành viên 3 | — | BI & Data Analyst (Câu 2–10, 8 biểu đồ) |

---

## 📂 Cấu trúc thư mục

```
airline-booking-analysis/
├── data/raw/                  # Dữ liệu gốc 10.325 dòng (không sửa)
├── notebooks/                 # Jupyter Notebook chính
├── src/                       # Mã nguồn Python
│   ├── cleaning.py            # Hàm làm sạch (TV1)
│   ├── feature_engineering.py # Hàm tạo cột dẫn xuất (TV2)
│   └── analysis.py            # Hàm phân tích & vẽ biểu đồ (TV3)
├── outputs/
│   ├── tables/                # 14 bảng CSV kết quả
│   └── figures/               # 8 biểu đồ PNG
├── reports/                   # Báo cáo
└── tests/                     # Kiểm thử tự động
```

---

## 🛠️ Thư viện sử dụng

```bash
pip install -r requirements.txt
```

- `pandas` — Xử lý và làm sạch dữ liệu
- `numpy` — Tính toán số học
- `matplotlib` — Vẽ biểu đồ
- `seaborn` — Trực quan hóa nâng cao
- `jupyter` — Môi trường Notebook

---

## 🚀 Cách chạy

```bash
# 1. Clone repo
git clone https://github.com/tranthetung2301-bit/airline-booking-analysis.git
cd airline-booking-analysis

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Mở notebook
jupyter notebook notebooks/airline_analysis.ipynb
```

---

## 📖 Hướng dẫn Git cho thành viên

Xem file [`HUONG_DAN_GIT_CHO_NHOM.md`](./HUONG_DAN_GIT_CHO_NHOM.md) để biết cách:
- Cài đặt & cấu hình Git
- Clone repo và quy trình làm việc hàng ngày
- Phân công file theo từng thành viên

---

## ⚠️ Quy tắc quan trọng

- **Không sửa** `data/raw/airline_bookings_dirty.csv` — dữ liệu gốc
- **Không điền mò** dữ liệu thiếu (mean/median/mode)
- Mọi thao tác làm sạch **phải thực hiện bằng code Python**
- **Không kết luận nhân quả** từ dữ liệu tương quan
