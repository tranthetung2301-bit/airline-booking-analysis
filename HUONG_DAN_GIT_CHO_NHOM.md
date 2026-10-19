# 📘 HƯỚNG DẪN SỬ DỤNG GIT & GITHUB CHO NHÓM

> **Dự án:** Phân Tích & Làm Sạch Dữ Liệu Đặt Vé Máy Bay  
> **Repo:** [https://github.com/tranthetung2301-bit/airline-booking-analysis](https://github.com/tranthetung2301-bit/airline-booking-analysis)

---

## 📑 MỤC LỤC

1. [Cài đặt Git](#-1-cài-đặt-git)
2. [Thiết lập ban đầu (làm 1 lần duy nhất)](#-2-thiết-lập-ban-đầu-làm-1-lần-duy-nhất)
3. [Clone repo về máy](#-3-clone-repo-về-máy)
4. [Quy trình làm việc hàng ngày](#-4-quy-trình-làm-việc-hàng-ngày)
5. [Xử lý xung đột (Conflict)](#-5-xử-lý-xung-đột-conflict)
6. [Các lệnh Git thường dùng](#-6-các-lệnh-git-thường-dùng)
7. [Cấu trúc thư mục dự án](#-7-cấu-trúc-thư-mục-dự-án)
8. [Phân công file theo thành viên](#-8-phân-công-file-theo-thành-viên)
9. [Quy tắc làm việc nhóm trên Git](#-9-quy-tắc-làm-việc-nhóm-trên-git)
10. [FAQ — Câu hỏi thường gặp](#-10-faq--câu-hỏi-thường-gặp)

---

## 🔧 1. Cài đặt Git

### Windows
1. Tải Git tại: [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Chạy file `.exe`, nhấn **Next** liên tục (giữ mặc định)
3. Kiểm tra cài đặt thành công:
   ```bash
   git --version
   ```
   ✅ Kết quả mong đợi: `git version 2.x.x`

### macOS
```bash
brew install git
```

---

## ⚙️ 2. Thiết lập ban đầu (làm 1 lần duy nhất)

Mở **Terminal** (macOS) hoặc **Git Bash / PowerShell** (Windows) và chạy:

```bash
# Đặt tên hiển thị (thay bằng tên thật của bạn)
git config --global user.name "Nguyen Van A"

# Đặt email (dùng email GitHub của bạn)
git config --global user.email "nguyenvana@email.com"
```

> 💡 **Mẹo:** Tên và email này sẽ hiển thị trên mỗi commit, giúp biết ai đã sửa gì.

---

## 📥 3. Clone repo về máy

```bash
# Di chuyển đến thư mục bạn muốn chứa dự án
cd Desktop

# Clone repo
git clone https://github.com/tranthetung2301-bit/airline-booking-analysis.git

# Vào thư mục dự án
cd airline-booking-analysis
```

Sau khi clone xong, bạn sẽ thấy toàn bộ cấu trúc thư mục trên máy.

---

## 🔄 4. Quy trình làm việc hàng ngày

> ⚠️ **QUAN TRỌNG:** Luôn **pull trước khi code** và **pull trước khi push** để tránh xung đột!

### Bước 1: Cập nhật code mới nhất từ GitHub
```bash
git pull origin master
```

### Bước 2: Code bình thường trên máy
- Mở file, sửa code, lưu lại

### Bước 3: Kiểm tra những gì đã thay đổi
```bash
git status
```
- 🔴 File đỏ = chưa được thêm vào staging
- 🟢 File xanh = đã sẵn sàng commit

### Bước 4: Thêm file vào staging
```bash
# Thêm một file cụ thể
git add src/cleaning.py

# Hoặc thêm TẤT CẢ file đã thay đổi
git add .
```

### Bước 5: Commit (lưu thay đổi vào lịch sử)
```bash
git commit -m "Mô tả ngắn gọn việc bạn đã làm"
```

**Ví dụ commit message tốt:**
```bash
git commit -m "TV1: Hoàn thành B1 - xử lý trùng lặp reservation_id"
git commit -m "TV3: Thêm fig01_airline_cancel.png"
git commit -m "TV2: Tạo cột dẫn xuất C1"
```

### Bước 6: Đẩy code lên GitHub
```bash
git push origin master
```

### 📋 Tóm tắt nhanh (copy & paste):
```bash
git pull origin master       # 1. Lấy code mới nhất
# ... code xong ...
git add .                    # 2. Thêm tất cả thay đổi
git commit -m "Mô tả..."    # 3. Commit
git pull origin master       # 4. Lấy code mới lần nữa (phòng conflict)
git push origin master       # 5. Đẩy lên GitHub
```

---

## ⚔️ 5. Xử lý xung đột (Conflict)

Xung đột xảy ra khi **2 người sửa cùng 1 file ở cùng 1 dòng**. Git sẽ báo lỗi khi pull:

```
CONFLICT (content): Merge conflict in src/cleaning.py
```

### Cách xử lý:

1. Mở file bị xung đột, bạn sẽ thấy:
   ```
   <<<<<<< HEAD
   Đây là code của bạn (trên máy bạn)
   =======
   Đây là code của người khác (trên GitHub)
   >>>>>>> origin/master
   ```

2. **Chọn giữ phần nào** (hoặc gộp cả hai), xóa các dòng `<<<`, `===`, `>>>`

3. Lưu file, rồi:
   ```bash
   git add .
   git commit -m "Resolve conflict trong file cleaning.py"
   git push origin master
   ```

> 💡 **Mẹo tránh conflict:** Mỗi người làm **file riêng** theo phân công bên dưới. Tránh 2 người sửa cùng 1 file cùng lúc.

---

## 📖 6. Các lệnh Git thường dùng

| Lệnh | Chức năng |
|-------|-----------|
| `git clone <url>` | Tải repo về máy lần đầu |
| `git pull origin master` | Cập nhật code mới nhất từ GitHub |
| `git status` | Xem file nào đã thay đổi |
| `git add .` | Thêm tất cả file đã sửa vào staging |
| `git add <file>` | Thêm một file cụ thể |
| `git commit -m "..."` | Lưu thay đổi kèm mô tả |
| `git push origin master` | Đẩy code lên GitHub |
| `git log --oneline -10` | Xem 10 commit gần nhất |
| `git diff` | Xem chi tiết những gì đã sửa |
| `git restore <file>` | Hủy thay đổi chưa commit, quay về bản cũ |

---

## 📂 7. Cấu trúc thư mục dự án

```
airline-booking-analysis/
│
├── README.md                          # 📄 Mô tả dự án (TV2 phụ trách)
├── requirements.txt                   # 📦 Danh sách thư viện Python cần cài
├── .gitignore                         # 🚫 File/thư mục Git bỏ qua
│
├── data/                              # 📊 THƯ MỤC DỮ LIỆU
│   ├── raw/
│   │   └── airline_bookings_dirty.csv # Dữ liệu gốc 10.325 dòng (KHÔNG ĐƯỢC SỬA)
│   └── processed/                     # Dữ liệu trung gian (nếu cần)
│
├── notebooks/                         # 📓 JUPYTER NOTEBOOK
│   └── airline_analysis.ipynb         # Notebook chính (CẢ NHÓM làm chung)
│
├── src/                               # 🐍 MÃ NGUỒN PYTHON
│   ├── cleaning.py                    # Hàm làm sạch dữ liệu (TV1)
│   ├── feature_engineering.py         # Hàm tạo cột dẫn xuất (TV2)
│   └── analysis.py                    # Hàm phân tích & vẽ biểu đồ (TV3)
│
├── outputs/                           # 📤 KẾT QUẢ ĐẦU RA
│   ├── tables/                        # 14 bảng CSV (q01 → q10, a_*)
│   └── figures/                       # 8 biểu đồ PNG (fig01 → fig08)
│
├── reports/                           # 📝 BÁO CÁO
│   └── final_report.md               # Bản nháp báo cáo
│
└── tests/                             # ✅ KIỂM THỬ
    └── test_cleaning.py               # Unit test cho hàm làm sạch
```

### Giải thích từng thư mục:

| Thư mục/File | Mục đích | Ai dùng? |
|---|---|---|
| `data/raw/` | Chứa file CSV gốc. **TUYỆT ĐỐI KHÔNG SỬA FILE NÀY** | Cả nhóm (chỉ đọc) |
| `data/processed/` | Lưu dữ liệu trung gian trong quá trình xử lý | TV1, TV2 |
| `notebooks/` | Notebook chính để trình bày toàn bộ bài | Cả nhóm |
| `src/cleaning.py` | Chứa các hàm Python làm sạch dữ liệu (B1–B5) | **TV1** viết, cả nhóm import |
| `src/feature_engineering.py` | Chứa hàm tạo cột dẫn xuất, bảng tháng (B6–C4) | **TV2** viết, cả nhóm import |
| `src/analysis.py` | Chứa hàm phân tích, vẽ biểu đồ (Câu 2–10) | **TV3** viết, cả nhóm import |
| `outputs/tables/` | Chứa 14 file CSV kết quả + 5 file CSV cốt lõi | TV1, TV2, TV3 xuất vào đây |
| `outputs/figures/` | Chứa 8 file PNG biểu đồ | **TV3** xuất vào đây |
| `reports/` | Bản nháp nội dung báo cáo | Cả nhóm |
| `tests/` | Unit test kiểm tra hàm | TV2 chạy kiểm tra |

---

## 👤 8. Phân công file theo thành viên

### 🟦 Thành viên 1 — Kỹ sư Làm sạch Dữ liệu

**File chính bạn code:**
- `src/cleaning.py` — Viết các hàm làm sạch (B1–B5)

**File bạn tạo ra (xuất vào `outputs/tables/`):**
- `a_missing_survey.csv` — Khảo sát ô thiếu 24 cột
- `a_issue_catalog.csv` — Danh mục ≥ 10 vấn đề dữ liệu

**File bạn đóng góp:**
- `notebooks/airline_analysis.ipynb` — Viết code Giai đoạn A → B5
- `reports/final_report.md` — Viết nháp **Phần 2** báo cáo

**Lệnh commit mẫu:**
```bash
git add src/cleaning.py outputs/tables/a_missing_survey.csv outputs/tables/a_issue_catalog.csv
git commit -m "TV1: Hoàn thành khảo sát dữ liệu giai đoạn A"
```

---

### 🟩 Thành viên 2 — Quản trị CSDL & Kiểm soát Chất lượng

**File chính bạn code:**
- `src/feature_engineering.py` — Viết hàm xử lý B6–B8, tạo cột dẫn xuất C1–C4

**File bạn tạo ra (xuất vào `outputs/`):**
- `reservations_clean.csv` — Bảng chính đã làm sạch (~10.000 dòng)
- `monthly_summary.csv` — Bảng tổng hợp theo tháng
- `cleaning_log.csv` — Nhật ký ≥ 10 quy tắc
- `row_lineage.csv` — Truy vết 10.325 dòng gốc
- `quality_report.csv` — Báo cáo chất lượng Before/After
- `outputs/tables/q01_before_after.csv` — Kết quả Câu 1

**File bạn đóng góp:**
- `notebooks/airline_analysis.ipynb` — Viết code B6 → C4, Câu 1
- `README.md` — Hoàn thiện mô tả dự án
- `tests/test_cleaning.py` — Chạy kiểm thử tự động

**Lệnh commit mẫu:**
```bash
git add src/feature_engineering.py outputs/reservations_clean.csv outputs/row_lineage.csv
git commit -m "TV2: Hoàn thành B8 - gộp reservation_id và tạo row_lineage"
```

---

### 🟧 Thành viên 3 — Chuyên viên Phân tích & Trực quan hóa

**File chính bạn code:**
- `src/analysis.py` — Viết hàm phân tích & vẽ biểu đồ (Câu 2–10)

**File bạn tạo ra (xuất vào `outputs/tables/`):**
- `q02_airline_cancel.csv`
- `q03_monthly_departures_2025.csv`
- `q04_leadtime_stats.csv`, `q04_leadtime_cancel.csv`
- `q05_top10_country.csv`
- `q06_segment_cancel.csv`
- `q07_fare_policy_status.csv`
- `q08_fare_stats_by_airline.csv`
- `q09_trip_days.csv`
- `q10_cabin_change_by_airline.csv`, `q10_cabin_change_by_booked_code.csv`

**File bạn tạo ra (xuất vào `outputs/figures/`):**
- `fig01_airline_cancel.png`
- `fig02_monthly_departures_2025.png`
- `fig03_leadtime_cancel.png`
- `fig04_top10_country.png`
- `fig05_segment_cancel.png`
- `fig06_fare_policy_status.png`
- `fig07_fare_hist.png`
- `fig08_trip_days.png`

**File bạn đóng góp:**
- `notebooks/airline_analysis.ipynb` — Viết code Câu 2 → Câu 10
- `reports/final_report.md` — Viết nháp **Phần 3** + 6 insight

**Lệnh commit mẫu:**
```bash
git add src/analysis.py outputs/tables/q02_airline_cancel.csv outputs/figures/fig01_airline_cancel.png
git commit -m "TV3: Hoàn thành Câu 2 - tỷ lệ hủy theo hãng + biểu đồ fig01"
```

---

## 📏 9. Quy tắc làm việc nhóm trên Git

### ✅ NÊN làm:
1. **Pull trước khi bắt đầu code** mỗi ngày/buổi
2. **Commit thường xuyên** với message rõ ràng (ghi tên TV + mô tả)
3. **Mỗi người làm file riêng** theo phân công để tránh conflict
4. **Thông báo nhóm trước khi sửa file chung** (notebook, README)
5. **Push ngay sau khi commit** để mọi người cập nhật

### ❌ KHÔNG NÊN làm:
1. ❌ **Không sửa file `data/raw/airline_bookings_dirty.csv`** — đây là dữ liệu gốc
2. ❌ **Không commit file rác** (.pyc, __pycache__, .ipynb_checkpoints)
3. ❌ **Không force push** (`git push -f`) — sẽ xóa code của người khác
4. ❌ **Không code quá lâu không push** — push thường xuyên để đồng bộ
5. ❌ **Không sửa file của người khác** mà không thông báo trước

### 📝 Quy ước đặt tên commit message:
```
<TV số> : <Mô tả ngắn>
```
Ví dụ:
- `TV1: Hoàn thành B3 - xử lý ký hiệu rác NULL, NA, ?`
- `TV2: Xuất cleaning_log.csv với 12 quy tắc`
- `TV3: Vẽ xong fig05_segment_cancel.png`
- `NHOM: Merge và rà soát notebook lần cuối`

---

## ❓ 10. FAQ — Câu hỏi thường gặp

### Q: Tôi quên pull trước khi code, giờ push bị lỗi?
```bash
git pull origin master    # Pull trước
# Nếu có conflict → xử lý theo Mục 5
git push origin master    # Push lại
```

### Q: Tôi muốn xem ai đã sửa gì?
```bash
git log --oneline -20                    # Xem 20 commit gần nhất
git log --oneline --author="Nguyen"      # Xem commit của 1 người
```

### Q: Tôi lỡ sửa sai file, muốn quay lại bản cũ?
```bash
# Hủy thay đổi CHƯA commit
git restore src/cleaning.py

# Quay về 1 commit trước (CẨN THẬN)
git revert HEAD
```

### Q: Tôi không biết mình đang ở branch nào?
```bash
git branch          # Xem branch hiện tại (có dấu * ở trước)
```
> Nhóm mình chỉ dùng branch `master`, không cần tạo branch mới.

### Q: Push bị yêu cầu đăng nhập?
Lần đầu push, GitHub có thể yêu cầu xác thực. Có 2 cách:
1. **HTTPS + Token:** Vào GitHub → Settings → Developer Settings → Personal Access Tokens → Generate. Dùng token thay mật khẩu.
2. **SSH Key:** Tạo SSH key và thêm vào GitHub (hỏi nhóm trưởng hướng dẫn).

### Q: File notebook (.ipynb) hay bị conflict?
Đúng, file notebook rất dễ conflict. **Giải pháp:**
- Chỉ **1 người sửa notebook tại 1 thời điểm**
- Nhắn nhóm chat trước: "Mình đang sửa notebook nhé"
- Push xong thì nhắn: "Mình push xong rồi, các bạn pull đi"

---

## 🚀 BẮT ĐẦU NHANH (cho thành viên mới clone)

```bash
# 1. Clone repo
git clone https://github.com/tranthetung2301-bit/airline-booking-analysis.git
cd airline-booking-analysis

# 2. Cài thư viện (sau khi requirements.txt được cập nhật)
pip install -r requirements.txt

# 3. Mở notebook
jupyter notebook notebooks/airline_analysis.ipynb

# 4. Bắt đầu code theo phân công ở Mục 8!
```

---

> 📞 **Gặp vấn đề với Git?** Nhắn ngay vào group chat nhóm, đừng tự ý xóa hay force push!  
> 📅 **Cập nhật lần cuối:** 19/10/2026
