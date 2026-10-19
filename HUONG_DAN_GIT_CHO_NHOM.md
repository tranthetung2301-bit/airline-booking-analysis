# 📘 HƯỚNG DẪN CHI TIẾT GIT & GITHUB CHO NHÓM
### Dự án: Phân Tích & Làm Sạch Dữ Liệu Đặt Vé Máy Bay (Aurora Air & Horizon Wings)

> 🔗 **Link Repo:** https://github.com/tranthetung2301-bit/airline-booking-analysis  
> 👤 **Chủ repo:** tranthetung2301-bit  
> 📅 **Cập nhật:** 19/10/2026

---

## 📑 MỤC LỤC

| # | Nội dung |
|---|---|
| 1 | [Tổng quan Git là gì?](#-1-tổng-quan-git-là-gì) |
| 2 | [Cài đặt Git trên máy](#-2-cài-đặt-git-trên-máy) |
| 3 | [Thiết lập ban đầu (làm 1 lần duy nhất)](#-3-thiết-lập-ban-đầu-làm-1-lần-duy-nhất) |
| 4 | [Clone repo về máy](#-4-clone-repo-về-máy) |
| 5 | [Quy trình làm việc hàng ngày](#-5-quy-trình-làm-việc-hàng-ngày-vòng-lặp-chuẩn) |
| 6 | [Xử lý xung đột (Conflict)](#-6-xử-lý-xung-đột-conflict) |
| 7 | [Cấu trúc thư mục dự án](#-7-cấu-trúc-thư-mục-dự-án) |
| 8 | [Phân công file cụ thể cho từng thành viên](#-8-phân-công-file-cụ-thể-cho-từng-thành-viên) |
| 9 | [Bảng lệnh Git hay dùng nhất](#-9-bảng-lệnh-git-hay-dùng-nhất) |
| 10 | [Quy tắc vàng làm việc nhóm](#-10-quy-tắc-vàng-làm-việc-nhóm) |
| 11 | [FAQ — Câu hỏi thường gặp & cách xử lý](#-11-faq--câu-hỏi-thường-gặp--cách-xử-lý) |
| 12 | [Bắt đầu nhanh (5 phút)](#-12-bắt-đầu-nhanh-5-phút) |

---

## 💡 1. Tổng quan Git là gì?

**Git** là công cụ giúp **theo dõi lịch sử thay đổi code** và **nhiều người cùng làm việc trên 1 dự án** mà không bị ghi đè lên nhau.

**GitHub** là trang web lưu trữ code trên Internet (như Google Drive nhưng dành cho code).

```
Máy bạn (Local)          Internet (GitHub)
─────────────────         ─────────────────
  [Thư mục code]  ──push──▶  [Repo GitHub]
                  ◀──pull──
```

### Các khái niệm cơ bản:

| Thuật ngữ | Giải thích đơn giản |
|---|---|
| **Repository (Repo)** | Thư mục dự án, có lịch sử mọi thay đổi |
| **Clone** | Tải repo từ GitHub về máy lần đầu |
| **Commit** | Lưu một "snapshot" thay đổi vào lịch sử |
| **Push** | Đẩy commit từ máy lên GitHub |
| **Pull** | Tải về các commit mới nhất từ GitHub |
| **Branch** | Nhánh làm việc (nhóm mình chỉ dùng `master`) |
| **Conflict** | Xung đột khi 2 người sửa cùng 1 chỗ |

---

## 🔧 2. Cài đặt Git trên máy

### 🪟 Windows

**Bước 1:** Vào trang [https://git-scm.com/download/win](https://git-scm.com/download/win)

**Bước 2:** Tải file `.exe` (64-bit) và chạy

**Bước 3:** Trong quá trình cài đặt, **giữ nguyên tất cả mặc định** và nhấn Next đến cuối

**Bước 4:** Sau khi cài xong, nhấn chuột phải vào Desktop → bạn sẽ thấy **"Git Bash Here"** hoặc **"Open Git Bash"** — đó là terminal để chạy lệnh Git

**Bước 5:** Kiểm tra cài thành công — mở **Git Bash** và chạy:
```bash
git --version
```
✅ Kết quả đúng: `git version 2.xx.x.windows.x`

> 💡 **Tip:** Trên Windows bạn có thể dùng **Git Bash**, **PowerShell**, hoặc **Command Prompt** đều được.

---

### 🍎 macOS

Mở **Terminal** và chạy:
```bash
# Cách 1: Dùng Homebrew (nếu đã cài)
brew install git

# Cách 2: Cài Xcode Command Line Tools (tự động cài Git)
xcode-select --install
```

Kiểm tra:
```bash
git --version
```

---

### 🐧 Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install git
git --version
```

---

## ⚙️ 3. Thiết lập ban đầu (làm 1 lần duy nhất)

> ⚠️ Bước này **bắt buộc** phải làm trước khi commit lần đầu tiên. Nếu bỏ qua, Git sẽ báo lỗi.

Mở **Git Bash** (Windows) hoặc **Terminal** (macOS/Linux):

```bash
# Đặt tên hiển thị trên mỗi commit (thay bằng tên thật của bạn)
git config --global user.name "Nguyen Van A"

# Đặt email (phải trùng với email tài khoản GitHub của bạn)
git config --global user.email "nguyenvana@gmail.com"

# Kiểm tra lại cấu hình
git config --list
```

✅ Kết quả mong đợi sau `git config --list`:
```
user.name=Nguyen Van A
user.email=nguyenvana@gmail.com
...
```

---

### Tạo tài khoản GitHub (nếu chưa có)

1. Vào [https://github.com](https://github.com) → Nhấn **Sign up**
2. Điền email, mật khẩu, username
3. Xác nhận email
4. **Nhắn username GitHub của bạn cho nhóm trưởng** để được thêm vào repo với quyền push

---

### Được thêm vào repo (Collaborator)

Nhóm trưởng sẽ vào GitHub repo → **Settings** → **Collaborators** → **Add people** → nhập username của bạn.

Bạn sẽ nhận email xác nhận → Nhấn **Accept invitation**.

---

## 📥 4. Clone repo về máy

> **Clone** = Tải toàn bộ repo về máy lần đầu tiên. Chỉ cần làm **1 lần duy nhất**.

**Bước 1:** Mở **Git Bash** hoặc **Terminal**

**Bước 2:** Di chuyển đến thư mục bạn muốn lưu dự án:
```bash
# Ví dụ: Lưu vào Desktop
cd Desktop

# Hoặc lưu vào thư mục Documents
cd Documents
```

**Bước 3:** Clone repo:
```bash
git clone https://github.com/tranthetung2301-bit/airline-booking-analysis.git
```

**Bước 4:** Vào thư mục dự án:
```bash
cd airline-booking-analysis
```

**Bước 5:** Kiểm tra đã clone thành công:
```bash
ls        # macOS/Linux
dir       # Windows CMD
```

✅ Bạn sẽ thấy các thư mục và file của dự án xuất hiện.

---

## 🔄 5. Quy trình làm việc hàng ngày (Vòng lặp chuẩn)

> ⚠️ **QUY TẮC SỐ 1:** Luôn **PULL TRƯỚC** khi bắt đầu code mỗi ngày!

```
┌─────────────────────────────────────────────┐
│         VÒNG LẶP LÀM VIỆC CHUẨN            │
│                                             │
│  1. git pull      ← Lấy code mới nhất      │
│          ↓                                  │
│  2. Code / Sửa file                         │
│          ↓                                  │
│  3. git add .     ← Đánh dấu thay đổi      │
│          ↓                                  │
│  4. git commit    ← Lưu vào lịch sử        │
│          ↓                                  │
│  5. git pull      ← Kiểm tra lần nữa       │
│          ↓                                  │
│  6. git push      ← Đẩy lên GitHub         │
└─────────────────────────────────────────────┘
```

---

### Bước 1: Pull — Lấy code mới nhất từ GitHub

```bash
git pull origin master
```

**Tại sao phải pull?** Bạn khác có thể đã push code mới lên. Nếu không pull trước, khi push sau bạn sẽ bị lỗi hoặc conflict.

✅ Kết quả khi không có gì mới:
```
Already up to date.
```

✅ Kết quả khi có code mới:
```
Updating 0c21278..cbe51f7
Fast-forward
 src/cleaning.py | 25 +++++++++++++++++++++++++
 1 file changed, 25 insertions(+)
```

---

### Bước 2: Code bình thường

- Mở file bằng VS Code, Jupyter, hoặc bất kỳ editor nào
- Sửa code, lưu file (Ctrl+S)
- Làm công việc theo phân công của bạn

---

### Bước 3: Kiểm tra những gì đã thay đổi

```bash
git status
```

**Đọc kết quả:**
```
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   src/cleaning.py       ← File đã sửa (hiện màu đỏ)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        outputs/tables/a_missing_survey.csv   ← File mới tạo (hiện màu đỏ)
```

---

### Bước 4: Thêm file vào staging (đánh dấu để commit)

```bash
# Thêm một file cụ thể (KHUYẾN NGHỊ - chắc chắn hơn)
git add src/cleaning.py
git add outputs/tables/a_missing_survey.csv

# Hoặc thêm TẤT CẢ file đã thay đổi trong thư mục hiện tại
git add .
```

Kiểm tra lại sau khi add:
```bash
git status
```

```
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   src/cleaning.py          ← Màu XANH = sẵn sàng commit ✅
        new file:   outputs/tables/a_missing_survey.csv
```

---

### Bước 5: Commit — Lưu thay đổi vào lịch sử

```bash
git commit -m "Mô tả ngắn gọn việc bạn đã làm"
```

**Quy ước đặt tên commit message** (bắt buộc theo cho nhóm):
```
TV<số>: <Động từ> - <Mô tả cụ thể>
```

**Ví dụ commit message tốt:**
```bash
git commit -m "TV1: Hoàn thành giai đoạn A - khảo sát 24 cột, tìm 12 nhóm vấn đề"
git commit -m "TV1: Hoàn thành B3 - xử lý ký hiệu rác NULL, NA, ?, -, unknown"
git commit -m "TV2: Xuất cleaning_log.csv với 11 quy tắc đã áp dụng"
git commit -m "TV2: Hoàn thành B8 - gộp reservation_id còn ~10000 dòng"
git commit -m "TV3: Vẽ xong fig01_airline_cancel.png - biểu đồ tỷ lệ hủy theo hãng"
git commit -m "TV3: Hoàn thành Câu 4 - phân tích lead time và tỷ lệ hủy"
git commit -m "NHOM: Rà soát lần cuối notebook trước khi nộp"
```

**Ví dụ commit message TỆ (tránh dùng):**
```bash
git commit -m "fix"          # Quá chung chung
git commit -m "update"       # Không biết update gì
git commit -m "test"         # Không có ý nghĩa
git commit -m "abc"          # Vô nghĩa hoàn toàn
```

---

### Bước 6: Pull lần nữa (phòng conflict)

```bash
git pull origin master
```

Nếu có người khác push lên trong lúc bạn code, bước này sẽ cập nhật và merge code của họ vào.

---

### Bước 7: Push — Đẩy lên GitHub

```bash
git push origin master
```

✅ Kết quả thành công:
```
To https://github.com/tranthetung2301-bit/airline-booking-analysis.git
   0c21278..cbe51f7  master -> master
```

❌ Kết quả lỗi (cần pull trước):
```
error: failed to push some refs to 'https://github.com/...'
hint: Updates were rejected because the remote contains work that you do not have locally.
```
→ **Giải pháp:** Chạy `git pull origin master` rồi push lại.

---

### 📋 Tóm tắt nhanh (Copy & Paste khi làm việc):

```bash
# === MỖI KHI BẮT ĐẦU LÀM VIỆC ===
git pull origin master

# === SAU KHI CODE XONG ===
git add .
git commit -m "TV?: Mô tả ngắn gọn"
git pull origin master
git push origin master
```

---

## ⚔️ 6. Xử lý xung đột (Conflict)

### Conflict xảy ra khi nào?

Khi **2 người sửa cùng 1 file ở cùng 1 đoạn code** và cả hai đều push lên. Người push sau sẽ bị báo conflict.

### Nhận biết conflict:

```bash
git pull origin master
```

```
CONFLICT (content): Merge conflict in notebooks/airline_analysis.ipynb
Automatic merge failed; fix conflicts and then commit the result.
```

### Cách xử lý từng bước:

**Bước 1:** Mở file bị conflict bằng VS Code (hoặc bất kỳ editor)

**Bước 2:** Tìm các dấu hiệu conflict trong file:
```python
<<<<<<< HEAD
# Đây là code của BẠN (trên máy bạn)
df = pd.read_csv('data/raw/airline_bookings_dirty.csv')
=======
# Đây là code của NGƯỜI KHÁC (trên GitHub)  
df = pd.read_csv('data/raw/airline_bookings_dirty.csv', encoding='utf-8')
>>>>>>> origin/master
```

**Bước 3:** Quyết định giữ phần nào:
- Giữ code của **bạn** → xóa từ `=======` đến `>>>>>>> origin/master` và xóa dòng `<<<<<<< HEAD`
- Giữ code của **người kia** → xóa từ `<<<<<<< HEAD` đến `=======` và xóa dòng `>>>>>>> origin/master`
- **Gộp cả hai** (trường hợp này nên giữ cả 2 phần logic)

**Bước 4:** Đảm bảo không còn dòng nào bắt đầu bằng `<<<<<<<`, `=======`, hoặc `>>>>>>>`

**Bước 5:** Lưu file, commit và push:
```bash
git add .
git commit -m "TV?: Resolve conflict trong file <tên file>"
git push origin master
```

### 💡 Cách TỐT NHẤT để tránh conflict:

1. **Mỗi người làm file riêng** theo phân công (xem Mục 8)
2. **Thông báo nhóm trước** khi sửa file chung (notebook)
3. **Pull trước, push ngay** sau khi xong — đừng để code trên máy quá lâu mà chưa push

---

## 📂 7. Cấu trúc thư mục dự án

```
airline-booking-analysis/               ← Thư mục gốc (Root)
│
├── 📄 README.md                        # Mô tả dự án nộp bài (TV2 phụ trách)
├── 📄 HUONG_DAN_GIT_CHO_NHOM.md       # File này — hướng dẫn Git
├── 📦 requirements.txt                 # Danh sách thư viện cần cài (pip install -r)
├── 🚫 .gitignore                       # File/thư mục mà Git bỏ qua
│
├── 📊 data/                            # DỮ LIỆU
│   ├── raw/
│   │   └── airline_bookings_dirty.csv  # ⛔ FILE GỐC — TUYỆT ĐỐI KHÔNG SỬA
│   └── processed/                      # Dữ liệu trung gian trong quá trình xử lý
│
├── 📓 notebooks/                       # JUPYTER NOTEBOOK CHÍNH
│   └── airline_analysis.ipynb          # Notebook trình bày toàn bộ bài (CẢ NHÓM)
│
├── 🐍 src/                             # MÃ NGUỒN PYTHON
│   ├── cleaning.py                     # Hàm làm sạch dữ liệu → TV1 viết
│   ├── feature_engineering.py          # Hàm tạo cột dẫn xuất, bảng tháng → TV2 viết
│   └── analysis.py                     # Hàm phân tích & vẽ biểu đồ → TV3 viết
│
├── 📤 outputs/                         # KẾT QUẢ ĐẦU RA (quan trọng nhất!)
│   ├── reservations_clean.csv          # Bảng chính đã làm sạch ~10.000 dòng
│   ├── monthly_summary.csv             # Bảng tổng hợp theo tháng
│   ├── cleaning_log.csv                # Nhật ký ≥ 10 quy tắc làm sạch
│   ├── row_lineage.csv                 # Truy vết 10.325 dòng gốc (kept/merged/dropped)
│   ├── quality_report.csv              # Báo cáo chất lượng Before/After
│   │
│   ├── tables/                         # 14 bảng CSV kết quả phân tích
│   │   ├── a_missing_survey.csv        # Khảo sát ô thiếu 24 cột (TV1)
│   │   ├── a_issue_catalog.csv         # Danh mục ≥ 10 vấn đề dữ liệu (TV1)
│   │   ├── q01_before_after.csv        # Câu 1: So sánh trước/sau (TV2)
│   │   ├── q02_airline_cancel.csv      # Câu 2: Tỷ lệ hủy theo hãng (TV3)
│   │   ├── q03_monthly_departures_2025.csv  # Câu 3: Mùa vụ 2025 (TV3)
│   │   ├── q04_leadtime_stats.csv      # Câu 4: Thống kê lead time (TV3)
│   │   ├── q04_leadtime_cancel.csv     # Câu 4: Lead time vs hủy (TV3)
│   │   ├── q05_top10_country.csv       # Câu 5: Top 10 quốc gia (TV3)
│   │   ├── q06_segment_cancel.csv      # Câu 6: Phân khúc thị trường (TV3)
│   │   ├── q07_fare_policy_status.csv  # Câu 7: Chính sách giá (TV3)
│   │   ├── q08_fare_stats_by_airline.csv  # Câu 8: Phân phối giá vé (TV3)
│   │   ├── q09_trip_days.csv           # Câu 9: Độ dài chuyến đi (TV3)
│   │   ├── q10_cabin_change_by_airline.csv     # Câu 10: Đổi cabin (TV3)
│   │   └── q10_cabin_change_by_booked_code.csv # Câu 10: Đổi cabin (TV3)
│   │
│   └── figures/                        # 8 biểu đồ PNG chuẩn kỹ thuật
│       ├── fig01_airline_cancel.png
│       ├── fig02_monthly_departures_2025.png
│       ├── fig03_leadtime_cancel.png
│       ├── fig04_top10_country.png
│       ├── fig05_segment_cancel.png
│       ├── fig06_fare_policy_status.png
│       ├── fig07_fare_hist.png
│       └── fig08_trip_days.png
│
├── 📝 reports/
│   └── final_report.md                 # Bản nháp báo cáo (cả nhóm đóng góp)
│
└── ✅ tests/
    └── test_cleaning.py                # Kiểm thử tự động (TV2 chạy)
```

---

## 👤 8. Phân công file cụ thể cho từng thành viên

---

### 🟦 THÀNH VIÊN 1 — Kỹ sư Làm sạch Dữ liệu

**Vai trò:** Data Cleaning Specialist

---

#### File bạn cần CODE:

| File | Nội dung cần viết |
|---|---|
| `src/cleaning.py` | Tất cả hàm làm sạch dữ liệu giai đoạn A + B1–B5 |
| `notebooks/airline_analysis.ipynb` | Các ô code từ **Giai đoạn A** đến **B5** |

---

#### Nội dung cụ thể cần làm trong `src/cleaning.py`:

```python
# Giai đoạn A: Hàm khảo sát
def survey_missing_values(df):
    """Thống kê số lượng ô thiếu 24 cột"""
    pass

def catalog_issues(df):
    """Tìm ≥ 10 nhóm vấn đề dữ liệu kèm ví dụ record_id"""
    pass

# Giai đoạn B1–B5: Hàm làm sạch
def clean_b1_duplicates(df):
    """Xử lý khoảng trắng reservation_id, loại bỏ bản ghi trùng lặp"""
    pass

def clean_b2_misplaced_dates(df):
    """Chuyển ngày nằm nhầm ở cột booking_status"""
    pass

def clean_b3_invalid_symbols(df):
    """Đưa NULL, NA, ?, -, unknown về NaN"""
    pass

def clean_b4_categorical_labels(df):
    """Chuẩn hóa nhãn danh mục, đồng bộ is_cancelled"""
    pass

def clean_b5_date_formats(df):
    """Chuyển 4 định dạng ngày về YYYY-MM-DD"""
    pass
```

---

#### File bạn tạo ra (xuất vào `outputs/tables/`):

| File | Nội dung |
|---|---|
| `outputs/tables/a_missing_survey.csv` | Thống kê ô thiếu từng cột |
| `outputs/tables/a_issue_catalog.csv` | Danh mục ≥ 10 vấn đề tìm được |

---

#### File bạn đóng góp vào báo cáo:

- `reports/final_report.md` → Viết nháp **Phần 2: Chất lượng dữ liệu và các quyết định xử lý**
  - Bảng trước/sau làm sạch
  - 3 quyết định tiêu biểu (kèm lý do)
  - Lý do giữ ô thiếu (không điền mean/mode)

---

#### Lệnh commit mẫu cho TV1:

```bash
# Sau khi hoàn thành Giai đoạn A
git add src/cleaning.py outputs/tables/a_missing_survey.csv outputs/tables/a_issue_catalog.csv
git commit -m "TV1: Hoàn thành Giai đoạn A - tìm được 12 nhóm vấn đề dữ liệu"

# Sau khi xong B1-B2
git add src/cleaning.py
git commit -m "TV1: Hoàn thành B1 (xóa trùng lặp) và B2 (ngày nhầm cột)"

# Sau khi xong B3-B5
git add src/cleaning.py
git commit -m "TV1: Hoàn thành B3-B5 - xử lý ký hiệu rác, nhãn danh mục, định dạng ngày"
```

---

### 🟩 THÀNH VIÊN 2 — Quản trị CSDL & Kiểm soát Chất lượng

**Vai trò:** QA & Data Architect

---

#### File bạn cần CODE:

| File | Nội dung cần viết |
|---|---|
| `src/feature_engineering.py` | Hàm xử lý B6–B8, tạo cột dẫn xuất C1–C4 |
| `notebooks/airline_analysis.ipynb` | Các ô code từ **B6** đến **C4** và **Câu 1** |
| `tests/test_cleaning.py` | Unit test kiểm tra tự động |
| `README.md` | Hoàn thiện mô tả dự án, danh sách thành viên, hướng dẫn chạy |

---

#### Nội dung cụ thể cần làm trong `src/feature_engineering.py`:

```python
# Giai đoạn B6: Xử lý số đo
def clean_b6_numeric_columns(df):
    """
    - lead_time, số ngày, số khách → kiểu Int64
    - avg_ticket_fare: bỏ $, EUR, đổi , thành ., giữ giá 0 hợp lệ
    """
    pass

# Giai đoạn B7: Mã quốc gia
def clean_b7_country_codes(df):
    """Chuẩn hóa passenger_country in hoa 2-3 chữ cái"""
    pass

# Giai đoạn B8: Gộp reservation_id
def merge_b8_reservations(df):
    """Gộp dòng cùng reservation_id, ~10.000 dòng sau gộp"""
    pass

def create_row_lineage(df_original, df_clean):
    """Lập bảng truy vết 10.325 dòng gốc (kept/merged/dropped)"""
    pass

# Giai đoạn C1-C4: Tạo cột dẫn xuất
def create_derived_columns(df):
    """
    Tạo: departure_year, departure_month, total_trip_days,
         total_passengers, lead_time_group,
         cabin_changed_flag, booking_value_est
    """
    pass

def create_monthly_summary(df):
    """Tạo bảng tổng hợp theo tháng (tỷ lệ hủy = tổng hủy / tổng có trạng thái)"""
    pass
```

---

#### File bạn tạo ra (xuất vào `outputs/`):

| File | Nội dung | Yêu cầu kỹ thuật |
|---|---|---|
| `outputs/reservations_clean.csv` | Bảng chính đã làm sạch | ~10.000 dòng |
| `outputs/monthly_summary.csv` | Bảng tổng hợp theo tháng | Đúng công thức tỷ lệ hủy |
| `outputs/cleaning_log.csv` | Nhật ký các bước làm sạch | ≥ 10 quy tắc |
| `outputs/row_lineage.csv` | Truy vết dòng gốc | Đủ 10.325 dòng, 3 nhãn: kept/merged/dropped |
| `outputs/quality_report.csv` | Báo cáo chất lượng | Before/After so sánh |
| `outputs/tables/q01_before_after.csv` | Kết quả Câu 1 | So sánh trước/sau làm sạch |

---

#### File bạn đóng góp vào báo cáo:

- `README.md` → Điền đầy đủ: tên thành viên, MSSV, thư viện dùng, thời gian chạy, quy tắc riêng
- `reports/final_report.md` → Viết nháp **Phần 1** (Mục tiêu & Nguồn) và **Phần 5** (Phân công)

---

#### Lệnh commit mẫu cho TV2:

```bash
# Sau khi xong B6-B7
git add src/feature_engineering.py
git commit -m "TV2: Hoàn thành B6 (xử lý số đo, giá vé) và B7 (mã quốc gia)"

# Sau khi xuất file CSV chính
git add outputs/reservations_clean.csv outputs/cleaning_log.csv outputs/row_lineage.csv
git commit -m "TV2: Xuất reservations_clean.csv (~10000 dòng) và row_lineage.csv (10325 dòng)"

# Sau khi hoàn thành C1-C4
git add src/feature_engineering.py outputs/monthly_summary.csv outputs/quality_report.csv
git commit -m "TV2: Hoàn thành C1-C4 - tạo cột dẫn xuất và vượt bộ kiểm tra C4"

# Sau khi hoàn thành README
git add README.md
git commit -m "TV2: Hoàn thiện README.md với đầy đủ thông tin nộp bài"
```

---

### 🟧 THÀNH VIÊN 3 — Chuyên viên Phân tích & Trực quan hóa

**Vai trò:** BI & Data Analyst

---

#### File bạn cần CODE:

| File | Nội dung cần viết |
|---|---|
| `src/analysis.py` | Hàm phân tích và vẽ biểu đồ cho Câu 2 đến Câu 10 |
| `notebooks/airline_analysis.ipynb` | Các ô code từ **Câu 2** đến **Câu 10** (kèm nhận xét 3–6 câu mỗi câu) |

---

#### Nội dung cụ thể cần làm trong `src/analysis.py`:

```python
def q02_airline_cancel_rate(df):
    """Tỷ lệ hủy theo hãng → xuất q02, vẽ fig01"""
    pass

def q03_monthly_departures_2025(df):
    """Mùa vụ đặt chỗ năm 2025 → xuất q03, vẽ fig02"""
    pass

def q04_leadtime_analysis(df):
    """Lead time và tỷ lệ hủy → xuất q04 (2 file), vẽ fig03"""
    pass

def q05_top10_countries(df):
    """Top 10 quốc gia → xuất q05, vẽ fig04"""
    pass

def q06_market_segment(df):
    """Phân khúc thị trường → xuất q06, vẽ fig05"""
    pass

def q07_fare_policy_status(df):
    """Chính sách giá và trạng thái → xuất q07, vẽ fig06"""
    pass

def q08_fare_distribution(df):
    """
    Phân phối giá vé (CHỈ vé không hủy, avg_ticket_fare > 0)
    → xuất q08, vẽ fig07
    """
    pass

def q09_trip_days_distribution(df):
    """Phân phối độ dài chuyến đi → xuất q09, vẽ fig08"""
    pass

def q10_cabin_change(df):
    """
    Tỷ lệ đổi cabin (CHỈ vé Flown)
    → xuất q10 (2 file)
    """
    pass
```

---

#### Yêu cầu kỹ thuật biểu đồ (fig01 → fig08):

| File | Tiêu chuẩn bắt buộc |
|---|---|
| Định dạng | `.png`, DPI ≥ 150 |
| Kích thước | Phù hợp (thường 10×6 inch) |
| Tiêu đề | Có `plt.title()` rõ ràng bằng tiếng Anh hoặc tiếng Việt |
| Nhãn trục | Có `xlabel()` và `ylabel()` |
| Chú giải | Có `plt.legend()` nếu có nhiều nhóm |
| Lưu file | `plt.savefig('outputs/figures/fig0X_...png', dpi=150, bbox_inches='tight')` |

---

#### File bạn tạo ra:

**12 bảng CSV → `outputs/tables/`:**

| File | Câu hỏi | Mẫu số |
|---|---|---|
| `q02_airline_cancel.csv` | Tỷ lệ hủy theo hãng | Vé có trạng thái xác định |
| `q03_monthly_departures_2025.csv` | Mùa vụ năm 2025 | Vé khởi hành trong 2025 |
| `q04_leadtime_stats.csv` | Thống kê lead time | Tất cả vé |
| `q04_leadtime_cancel.csv` | Lead time và tỷ lệ hủy | Vé có trạng thái xác định |
| `q05_top10_country.csv` | Top 10 quốc gia | Tất cả vé |
| `q06_segment_cancel.csv` | Phân khúc và tỷ lệ hủy | Vé có trạng thái xác định |
| `q07_fare_policy_status.csv` | Chính sách giá | Tất cả vé |
| `q08_fare_stats_by_airline.csv` | Phân phối giá vé | **Chỉ vé KHÔNG HỦY** (`is_cancelled == 0`) |
| `q09_trip_days.csv` | Độ dài chuyến đi | **Chỉ vé KHÔNG HỦY** (`is_cancelled == 0`) |
| `q10_cabin_change_by_airline.csv` | Đổi cabin theo hãng | **Chỉ vé FLOWN** (`booking_status == 'Flown'`) |
| `q10_cabin_change_by_booked_code.csv` | Đổi cabin theo hạng đặt | **Chỉ vé FLOWN** (`booking_status == 'Flown'`) |

**8 biểu đồ PNG → `outputs/figures/`:**

| File | Câu hỏi |
|---|---|
| `fig01_airline_cancel.png` | Câu 2: Tỷ lệ hủy theo hãng |
| `fig02_monthly_departures_2025.png` | Câu 3: Mùa vụ đặt chỗ năm 2025 |
| `fig03_leadtime_cancel.png` | Câu 4: Lead time và tỷ lệ hủy |
| `fig04_top10_country.png` | Câu 5: Top 10 quốc gia |
| `fig05_segment_cancel.png` | Câu 6: Phân khúc thị trường |
| `fig06_fare_policy_status.png` | Câu 7: Chính sách giá |
| `fig07_fare_hist.png` | Câu 8: Phân phối giá vé (vé không hủy) |
| `fig08_trip_days.png` | Câu 9: Phân phối độ dài chuyến đi |

---

#### Lệnh commit mẫu cho TV3:

```bash
# Sau khi xong Câu 2-3
git add src/analysis.py outputs/tables/q02_airline_cancel.csv outputs/figures/fig01_airline_cancel.png
git commit -m "TV3: Hoàn thành Câu 2 - tỷ lệ hủy theo hãng, vẽ fig01"

# Sau khi xong Câu 4-5
git add src/analysis.py outputs/tables/ outputs/figures/
git commit -m "TV3: Hoàn thành Câu 4 (lead time) và Câu 5 (top 10 quốc gia)"

# Sau khi xong tất cả câu hỏi
git add src/analysis.py outputs/tables/ outputs/figures/
git commit -m "TV3: Hoàn thành Câu 2-10, xuất đủ 12 bảng CSV và 8 biểu đồ PNG"
```

---

## 📖 9. Bảng lệnh Git hay dùng nhất

### Lệnh cơ bản hàng ngày:

| Lệnh | Chức năng |
|---|---|
| `git pull origin master` | Lấy code mới nhất từ GitHub |
| `git status` | Xem file nào thay đổi |
| `git add .` | Thêm tất cả thay đổi |
| `git add <tên-file>` | Thêm 1 file cụ thể |
| `git commit -m "..."` | Lưu thay đổi + mô tả |
| `git push origin master` | Đẩy code lên GitHub |

### Lệnh xem lịch sử:

| Lệnh | Chức năng |
|---|---|
| `git log --oneline -10` | Xem 10 commit gần nhất (ngắn gọn) |
| `git log --oneline --all` | Xem toàn bộ lịch sử |
| `git diff` | Xem chi tiết những gì đang thay đổi (chưa add) |
| `git diff --staged` | Xem thay đổi đã add nhưng chưa commit |

### Lệnh khẩn cấp (khi có sự cố):

| Lệnh | Chức năng | ⚠️ Cẩn thận |
|---|---|---|
| `git restore <file>` | Hủy thay đổi chưa add | Mất hết code chưa lưu! |
| `git restore --staged <file>` | Bỏ file ra khỏi staging | An toàn |
| `git revert HEAD` | Tạo commit đảo ngược commit cuối | An toàn |
| `git stash` | Tạm cất code đang làm dở | Dùng khi cần pull khẩn cấp |
| `git stash pop` | Lấy lại code đã cất | Dùng sau khi stash |

---

## 📏 10. Quy tắc vàng làm việc nhóm

### ✅ 5 việc NÊN làm:

1. **Pull ngay khi bắt đầu** mỗi buổi làm việc — dù chỉ nghỉ 1 tiếng
2. **Commit thường xuyên** (mỗi 30–45 phút hoặc sau mỗi tính năng nhỏ hoàn thành)
3. **Commit message rõ ràng** theo quy ước `TV1/TV2/TV3: Mô tả`
4. **Thông báo nhóm chat** trước khi sửa file chung (notebook, README)
5. **Push ngay sau commit** để mọi người cập nhật

### ❌ 5 việc KHÔNG được làm:

1. ❌ **Không sửa `data/raw/airline_bookings_dirty.csv`** — file gốc, không được đụng vào
2. ❌ **Không dùng `git push --force`** — sẽ xóa lịch sử commit của người khác
3. ❌ **Không commit file rác**: `.pyc`, `__pycache__/`, `.ipynb_checkpoints/`, `.DS_Store`
4. ❌ **Không để code trên máy >1 ngày mà chưa push** — dễ bị conflict lớn
5. ❌ **Không sửa file của người khác** mà không thông báo trước

### 📝 Quy ước commit message:

```
TV1: <Mô tả> — Thành viên 1 dùng
TV2: <Mô tả> — Thành viên 2 dùng
TV3: <Mô tả> — Thành viên 3 dùng
NHOM: <Mô tả> — Khi cả nhóm cùng rà soát
FIX: <Mô tả> — Khi sửa lỗi
```

---

## ❓ 11. FAQ — Câu hỏi thường gặp & cách xử lý

---

### ❓ Tôi quên pull trước, giờ push bị lỗi?

```
error: failed to push some refs...
hint: Updates were rejected because the remote contains work that you do not have locally.
```

**Giải pháp:**
```bash
git pull origin master    # Pull về trước
# Nếu có conflict → xem Mục 6
git push origin master    # Push lại
```

---

### ❓ Tôi muốn xem ai đã làm gì?

```bash
# Xem 10 commit gần nhất với tên người commit
git log --oneline -10

# Xem commit của một người cụ thể
git log --oneline --author="TV1"

# Xem lịch sử thay đổi của 1 file
git log --oneline src/cleaning.py
```

---

### ❓ Tôi lỡ sửa sai và muốn quay về bản trước?

```bash
# Xem lịch sử các commit
git log --oneline -5

# Cách 1: Hủy thay đổi CHƯA commit (CẨN THẬN - mất code!)
git restore src/cleaning.py

# Cách 2: Tạo commit đảo ngược (AN TOÀN hơn)
git revert HEAD
```

---

### ❓ Lỡ commit nhầm và chưa push, sửa lại được không?

```bash
# Sửa lại commit message cuối (chưa push)
git commit --amend -m "TV1: Mô tả đúng hơn"

# Bỏ commit cuối nhưng giữ code (chưa push)
git reset --soft HEAD~1
```

---

### ❓ Push bị yêu cầu đăng nhập / xác thực?

**Cách 1: Dùng Personal Access Token (PAT)**
1. Đăng nhập GitHub → Nhấn ảnh đại diện góc phải → **Settings**
2. Cuộn xuống → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Nhấn **Generate new token (classic)**
4. Đặt tên, chọn thời hạn, tick ô **repo** → **Generate token**
5. Copy token (chỉ hiện 1 lần!)
6. Khi Git hỏi password → Dán token vào thay vì mật khẩu GitHub

**Cách 2: Dùng GitHub CLI (gh) — đã cài sẵn**
```bash
gh auth login
```
→ Chọn **GitHub.com** → **HTTPS** → **Login with a web browser** → Làm theo hướng dẫn

---

### ❓ File notebook (.ipynb) bị conflict rất phức tạp?

File notebook là JSON phức tạp, conflict rất khó resolve thủ công. **Cách tốt nhất:**

1. **Chỉ 1 người sửa notebook tại 1 thời điểm**
2. Nhắn group chat: `"[TV1] Mình đang sửa notebook, chờ mình push xong"`
3. Sau khi push xong nhắn: `"[TV1] Push xong rồi, pull đi nhé"`

Nếu vẫn bị conflict notebook:
```bash
# Giải pháp đơn giản nhất: giữ bản trên GitHub
git checkout origin/master -- notebooks/airline_analysis.ipynb
# Sau đó thêm lại code của bạn bằng tay vào đúng chỗ
```

---

### ❓ Tôi cần cài thư viện gì?

```bash
# Cài tất cả thư viện theo requirements.txt
pip install -r requirements.txt

# Hoặc cài từng cái:
pip install pandas matplotlib seaborn jupyter openpyxl
```

---

## 🚀 12. Bắt đầu nhanh (5 phút)

Làm theo thứ tự từng bước — **không bỏ bước nào**:

```bash
# ── BƯỚC 1: Cài Git (nếu chưa có) ───────────────────────────
# Tải tại: https://git-scm.com/download/win

# ── BƯỚC 2: Thiết lập danh tính ─────────────────────────────
git config --global user.name "Tên Thật Của Bạn"
git config --global user.email "email_github_cua_ban@gmail.com"

# ── BƯỚC 3: Clone repo về máy ───────────────────────────────
cd Desktop
git clone https://github.com/tranthetung2301-bit/airline-booking-analysis.git
cd airline-booking-analysis

# ── BƯỚC 4: Cài thư viện Python ─────────────────────────────
pip install -r requirements.txt

# ── BƯỚC 5: Mở notebook ─────────────────────────────────────
jupyter notebook notebooks/airline_analysis.ipynb

# ── BƯỚC 6: Bắt đầu code theo phân công ở Mục 8! ───────────
```

---

### 🔁 Mỗi ngày làm việc, copy & chạy:

```bash
# === ĐẦU BUỔI: cập nhật code mới nhất ===
cd Desktop/airline-booking-analysis    # Windows
cd ~/Desktop/airline-booking-analysis  # macOS/Linux

git pull origin master

# === CUỐI BUỔI: lưu và đẩy code lên ===
git add .
git commit -m "TV?: Mô tả công việc hôm nay"
git pull origin master
git push origin master
```

---

> 📞 **Gặp vấn đề?** Nhắn ngay vào group chat nhóm, đừng tự ý xóa repo hay force push!  
> 🤝 **Nhớ:** Thông báo nhóm trước khi sửa file chung. Git theo dõi tất cả — không gì bị mất nếu bạn không force push.  
> 📅 **Cập nhật lần cuối:** 19/10/2026
