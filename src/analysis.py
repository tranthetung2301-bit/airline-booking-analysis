"""
analysis.py  (Thành viên 3 - BI & Data Analyst)
================================================
Câu 2-10: bảng kết quả (outputs/tables) + 8 biểu đồ (outputs/figures).

Cách dùng trong notebook:
    from src.analysis import *
    df = load_clean()                      # tự tìm reservations_clean.csv trong repo
    monthly = load_monthly()               # tùy chọn, dùng để đối chiếu Câu 3
    res = run_all(df, monthly)             # chạy Câu 2-10, lưu bảng + hình, in số liệu chính
    # hoặc chạy từng câu:  t2 = cau2(df)

Quy ước (Mục 9 đề bài):
- Tỷ lệ hủy = số is_cancelled == 1 / số dòng có is_cancelled KHÔNG thiếu.
- Dòng thiếu ở cột đang phân tích bị loại khỏi câu đó và được báo riêng.
- Không kết luận nhân quả; chỉ mô tả mối liên hệ.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Hằng số
# ----------------------------------------------------------------------------
AIRLINE_COLORS = {"Aurora Air": "#2F4858", "Horizon Wings": "#E07A1F"}
STATUS_COLORS = {"Flown": "#4C9F70", "Cancelled": "#C8553D", "No-Show": "#8D8D8D"}
STATUS_ORDER = ["Flown", "Cancelled", "No-Show"]
POLICY_ORDER = ["Flexible", "Semi-Flexible", "Non-Refundable"]
LEAD_ORDER = ["0-7", "8-30", "31-90", "91-180", "181+"]
LEAD_BINS = [-1, 7, 30, 90, 180, 365]
NEUTRAL = "#2F4858"
HIGHLIGHT = "#E07A1F"
MIN_N_WARNING = 100          # nhóm có mẫu số nhỏ hơn ngưỡng này sẽ bị gắn cờ small_sample
DPI = 150

INT_COLS = ["is_cancelled", "booking_lead_days", "trip_weekend_days", "trip_weekdays",
            "adult_passengers", "child_passengers", "infant_passengers",
            "is_returning_customer", "special_service_requests",
            "departure_year", "departure_month", "total_trip_days", "total_passengers"]
REQUIRED_COLS = ["airline", "is_cancelled", "booking_lead_days", "passenger_country",
                 "market_segment", "fare_policy", "booking_status", "avg_ticket_fare",
                 "booked_cabin_code", "assigned_cabin_code"]


# ----------------------------------------------------------------------------
# Đường dẫn & đọc dữ liệu
# ----------------------------------------------------------------------------
def repo_root(start=None) -> Path:
    """Đi ngược từ thư mục hiện tại tới thư mục có cả data/ và src/."""
    p = Path(start or Path.cwd()).resolve()
    for q in [p, *p.parents]:
        if (q / "data").exists() and (q / "src").exists():
            return q
    return p


ROOT = repo_root()
TABLES_DIR = ROOT / "outputs" / "tables"
FIGURES_DIR = ROOT / "outputs" / "figures"


def find_file(name: str) -> Path:
    """Tìm tệp theo tên trong repo (bỏ qua data/raw)."""
    hits = [p for p in ROOT.rglob(name) if "raw" not in p.parts]
    if not hits:
        raise FileNotFoundError(
            f"Không thấy {name} trong {ROOT}. Truyền đường dẫn trực tiếp: load_clean('đường/dẫn.csv')")
    return hits[0]


def load_clean(path=None) -> pd.DataFrame:
    path = Path(path) if path else find_file("reservations_clean.csv")
    print(f"Đọc: {path}")
    return prepare(pd.read_csv(path))


def load_monthly(path=None):
    try:
        path = Path(path) if path else find_file("monthly_summary.csv")
    except FileNotFoundError:
        print("Không thấy monthly_summary.csv, bỏ qua bước đối chiếu Câu 3.")
        return None
    return pd.read_csv(path)


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Ép kiểu, tạo cột dẫn xuất nếu chưa có, kiểm tra cột bắt buộc.
    KHÔNG sửa giá trị dữ liệu (việc làm sạch là của TV1/TV2)."""
    df = df.copy()
    for col in INT_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    df["avg_ticket_fare"] = pd.to_numeric(df["avg_ticket_fare"], errors="coerce")

    # cột dẫn xuất (Mục 8.1) - chỉ tạo khi thiếu
    if "departure_year" not in df.columns or "departure_month" not in df.columns:
        dep = pd.to_datetime(df["departure_date"], errors="coerce")
        df["departure_year"] = dep.dt.year.astype("Int64")
        df["departure_month"] = dep.dt.month.astype("Int64")
    if "total_trip_days" not in df.columns:
        df["total_trip_days"] = df["trip_weekend_days"] + df["trip_weekdays"]
    if "reservation_id" not in df.columns:
        df["reservation_id"] = np.arange(len(df))

    lead = df["booking_lead_days"].astype("float")
    recomputed = pd.cut(lead, bins=LEAD_BINS, labels=LEAD_ORDER).astype(object)
    if "lead_time_group" not in df.columns:
        df["lead_time_group"] = recomputed
    elif not set(df["lead_time_group"].dropna().unique()) <= set(LEAD_ORDER):
        print("CẢNH BÁO: nhãn lead_time_group khác chuẩn 0-7/8-30/31-90/91-180/181+, "
              "tính lại từ booking_lead_days.")
        df["lead_time_group"] = recomputed

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise KeyError(f"Thiếu cột bắt buộc: {missing}. Kiểm tra lại tên cột với TV1/TV2.")
    return df


# ----------------------------------------------------------------------------
# Hàm dùng chung
# ----------------------------------------------------------------------------
def cancel_summary(df: pd.DataFrame, by) -> pd.DataFrame:
    """n_reservations, n_cancelled, n_known (mẫu số), cancel_rate_pct theo nhóm `by`."""
    d = df.assign(
        _c=df["is_cancelled"].eq(1).fillna(False).astype(int),
        _k=df["is_cancelled"].notna().astype(int),
    )
    out = d.groupby(by, observed=True).agg(
        n_reservations=("_c", "size"), n_cancelled=("_c", "sum"), n_known=("_k", "sum"))
    out["cancel_rate_pct"] = (out["n_cancelled"] / out["n_known"].replace(0, np.nan) * 100).round(2)
    return out


def _quantiles(s: pd.Series) -> dict:
    return {"n": int(s.count()), "mean": round(s.mean(), 2), "median": round(s.median(), 2),
            "q1": round(s.quantile(0.25), 2), "q3": round(s.quantile(0.75), 2),
            "max": round(s.max(), 2)}


def _airlines(df):
    return sorted(df["airline"].dropna().unique())


def _color(airline):
    return AIRLINE_COLORS.get(airline, "#888888")


def save_table(t: pd.DataFrame, name: str) -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    t.to_csv(TABLES_DIR / f"{name}.csv", index=False, encoding="utf-8-sig")


def _style(ax, title, xlabel=None, ylabel=None, grid_axis="y"):
    ax.set_title(title, fontsize=13, fontweight="bold", loc="left")
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis=grid_axis, alpha=0.25)
    ax.set_axisbelow(True)


def _finish(fig, name: str, footnote: str, show: bool = True):
    """Ghi chú dưới hình, lưu PNG 150 dpi vào outputs/figures."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.text(0.01, 0.01, footnote, fontsize=8, color="#555555", ha="left", va="bottom")
    fig.savefig(FIGURES_DIR / f"{name}.png", dpi=DPI, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# ----------------------------------------------------------------------------
# Câu 2 - Hãng nào chiếm nhiều đặt chỗ hơn và tỷ lệ hủy mỗi hãng?
# ----------------------------------------------------------------------------
def cau2(df, show=True):
    t = cancel_summary(df, "airline").reset_index()
    t["share_pct"] = (t["n_reservations"] / t["n_reservations"].sum() * 100).round(2)
    t = t[["airline", "n_reservations", "share_pct", "n_cancelled", "n_known", "cancel_rate_pct"]]
    save_table(t, "q02_airline_cancel")

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(t["airline"], t["cancel_rate_pct"], color=[_color(a) for a in t["airline"]], width=0.55)
    ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=11)
    ax.set_ylim(0, t["cancel_rate_pct"].max() * 1.3)
    _style(ax, "Tỷ lệ hủy đặt chỗ theo hãng", ylabel="Tỷ lệ hủy (%)")
    _finish(fig, "fig01_airline_cancel",
            f"n = {int(t['n_known'].sum()):,} đặt chỗ có trạng thái hủy xác định | "
            f"Nguồn: outputs/tables/q02_airline_cancel.csv", show)

    top = t.sort_values("n_reservations", ascending=False).iloc[0]
    ranked = t.sort_values("cancel_rate_pct", ascending=False)
    hi, lo = ranked.iloc[0], ranked.iloc[-1]
    print(f"[Câu 2] {top.airline} chiếm nhiều đặt chỗ nhất ({top.share_pct:.1f}%). "
          f"Tỷ lệ hủy: {hi.airline} {hi.cancel_rate_pct:.2f}% vs {lo.airline} {lo.cancel_rate_pct:.2f}% "
          f"-> chênh {hi.cancel_rate_pct - lo.cancel_rate_pct:.2f} điểm %.")
    return t


# ----------------------------------------------------------------------------
# Câu 3 - Số đặt chỗ theo tháng khởi hành trong 2025 (mùa vụ)
# ----------------------------------------------------------------------------
def cau3(df, monthly=None, show=True):
    d = df[df["departure_year"].eq(2025).fillna(False).astype(bool)].dropna(subset=["departure_month"])
    d = d.assign(departure_month=d["departure_month"].astype(int))
    airlines = _airlines(df)
    idx = pd.MultiIndex.from_product([airlines, range(1, 13)], names=["airline", "departure_month"])
    t = (d.groupby(["airline", "departure_month"]).size().rename("n_reservations")
         .reindex(idx, fill_value=0).reset_index())
    t["share_of_airline_2025_pct"] = (t["n_reservations"] / t.groupby("airline")["n_reservations"].transform("sum") * 100).round(2)
    save_table(t, "q03_monthly_departures_2025")

    if monthly is not None:   # đối chiếu với monthly_summary của TV2
        m = monthly[monthly["departure_year"] == 2025][["airline", "departure_month", "n_reservations"]]
        chk = t.merge(m, on=["airline", "departure_month"], how="outer", suffixes=("", "_monthly")).fillna(0)
        diff = (chk["n_reservations"] != chk["n_reservations_monthly"]).sum()
        print(f"[Câu 3] Đối chiếu monthly_summary: {'KHỚP' if diff == 0 else f'LỆCH {diff} dòng, kiểm tra lại'}")

    fig, ax = plt.subplots(figsize=(9, 5))
    for a in airlines:
        s = t[t["airline"] == a]
        ax.plot(s["departure_month"], s["n_reservations"], marker="o", lw=2, color=_color(a), label=a)
        pk = s.loc[s["n_reservations"].idxmax()]
        ax.annotate(f"{int(pk.n_reservations)}", (pk.departure_month, pk.n_reservations),
                    textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9, color=_color(a))
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([f"T{m}" for m in range(1, 13)])
    ax.set_ylim(bottom=0)
    ax.legend(frameon=False)
    _style(ax, "Số đặt chỗ theo tháng khởi hành, năm 2025", "Tháng khởi hành", "Số đặt chỗ")
    _finish(fig, "fig02_monthly_departures_2025",
            f"n = {len(d):,} đặt chỗ khởi hành năm 2025 (loại dòng thiếu ngày khởi hành) | "
            f"Nguồn: outputs/tables/q03_monthly_departures_2025.csv", show)

    for a in airlines:
        s = t[t["airline"] == a].sort_values("n_reservations", ascending=False)
        print(f"[Câu 3] {a}: đỉnh T{int(s.iloc[0].departure_month)} ({int(s.iloc[0].n_reservations)}), "
              f"thấp nhất T{int(s.iloc[-1].departure_month)} ({int(s.iloc[-1].n_reservations)}).")
    return t


# ----------------------------------------------------------------------------
# Câu 4 - Lead time (thống kê theo hãng) và tỷ lệ hủy theo nhóm lead time
# ----------------------------------------------------------------------------
def cau4(df, show=True):
    d = df.dropna(subset=["booking_lead_days"]).copy()
    d["booking_lead_days"] = d["booking_lead_days"].astype(float)
    stats = pd.DataFrame({a: _quantiles(s["booking_lead_days"]) for a, s in d.groupby("airline")}).T
    stats = stats.rename_axis("airline").reset_index()
    stats["n"] = stats["n"].astype(int)
    save_table(stats, "q04_leadtime_stats")

    g = d.dropna(subset=["lead_time_group"])
    t = cancel_summary(g, "lead_time_group").reindex(LEAD_ORDER)
    t[["n_reservations", "n_cancelled", "n_known"]] = t[["n_reservations", "n_cancelled", "n_known"]].fillna(0).astype(int)
    t = t.rename_axis("lead_time_group").reset_index()
    save_table(t, "q04_leadtime_cancel")

    overall = t["n_cancelled"].sum() / t["n_known"].sum() * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = [f"{r.lead_time_group}\n(n={r.n_known:,})" for r in t.itertuples()]
    bars = ax.bar(labels, t["cancel_rate_pct"], color=NEUTRAL, width=0.6)
    ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=10)
    ax.axhline(overall, color=HIGHLIGHT, ls="--", lw=1.3, label=f"Trung bình chung {overall:.1f}%")
    ax.set_ylim(0, np.nanmax(t["cancel_rate_pct"]) * 1.3)
    ax.legend(frameon=False)
    _style(ax, "Tỷ lệ hủy theo nhóm thời gian đặt trước (lead time)",
           "Số ngày đặt trước khi bay", "Tỷ lệ hủy (%)")
    _finish(fig, "fig03_leadtime_cancel",
            f"n = {int(t['n_known'].sum()):,} đặt chỗ có lead time và trạng thái hủy xác định | "
            f"Nguồn: outputs/tables/q04_leadtime_cancel.csv | Mô tả liên hệ, không phải quan hệ nhân quả", show)

    print("[Câu 4] Thống kê lead time (ngày):")
    print(stats.to_string(index=False))
    hi = t.loc[t["cancel_rate_pct"].idxmax()]
    lo = t.loc[t["cancel_rate_pct"].idxmin()]
    print(f"[Câu 4] Tỷ lệ hủy cao nhất ở nhóm {hi.lead_time_group} ({hi.cancel_rate_pct:.2f}%), "
          f"thấp nhất ở nhóm {lo.lead_time_group} ({lo.cancel_rate_pct:.2f}%).")
    return stats, t


# ----------------------------------------------------------------------------
# Câu 5 - Top 10 quốc gia của hành khách
# ----------------------------------------------------------------------------
def cau5(df, show=True):
    c = df["passenger_country"].dropna()
    n_missing = int(df["passenger_country"].isna().sum())
    t = (c.value_counts().rename_axis("passenger_country").reset_index(name="n_reservations")
         .sort_values(["n_reservations", "passenger_country"], ascending=[False, True]).head(10))
    t.insert(0, "rank", range(1, len(t) + 1))
    t["share_pct"] = (t["n_reservations"] / len(c) * 100).round(2)
    save_table(t, "q05_top10_country")

    fig, ax = plt.subplots(figsize=(8, 5.5))
    r = t.iloc[::-1]
    bars = ax.barh(r["passenger_country"], r["n_reservations"], color=NEUTRAL)
    ax.bar_label(bars, labels=[f"{n:,} ({p:.1f}%)" for n, p in zip(r["n_reservations"], r["share_pct"])],
                 padding=3, fontsize=9)
    ax.set_xlim(0, r["n_reservations"].max() * 1.2)
    _style(ax, "Top 10 quốc gia của hành khách theo số đặt chỗ", "Số đặt chỗ", grid_axis="x")
    _finish(fig, "fig04_top10_country",
            f"n = {len(c):,} đặt chỗ có quốc gia; loại {n_missing:,} dòng thiếu quốc gia | "
            f"Mã quốc gia giữ nguyên như dữ liệu sạch | Nguồn: outputs/tables/q05_top10_country.csv", show)

    print(f"[Câu 5] Top 3: " + ", ".join(f"{r.passenger_country} {r.share_pct:.1f}%" for r in t.head(3).itertuples())
          + f" | thiếu quốc gia: {n_missing:,} dòng. Kiểm tra: có mã trùng nghĩa (vd CN/CHN) trong top 10 không?")
    return t


# ----------------------------------------------------------------------------
# Câu 6 - Phân khúc thị trường: quy mô và tỷ lệ hủy
# ----------------------------------------------------------------------------
def cau6(df, show=True):
    d = df.dropna(subset=["market_segment"])
    n_missing = len(df) - len(d)
    t = cancel_summary(d, "market_segment").reset_index()
    t["share_pct"] = (t["n_reservations"] / t["n_reservations"].sum() * 100).round(2)
    t["small_sample"] = t["n_known"] < MIN_N_WARNING
    t = t[["market_segment", "n_reservations", "share_pct", "n_cancelled", "n_known",
           "cancel_rate_pct", "small_sample"]].sort_values("cancel_rate_pct", ascending=False)
    save_table(t, "q06_segment_cancel")

    r = t.sort_values("cancel_rate_pct")
    colors = [HIGHLIGHT if v == r["cancel_rate_pct"].max() else NEUTRAL for v in r["cancel_rate_pct"]]
    labels = [f"{s}{'*' if sm else ''} (n={n:,})" for s, sm, n in zip(r["market_segment"], r["small_sample"], r["n_known"])]
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    bars = ax.barh(labels, r["cancel_rate_pct"], color=colors)
    ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=10)
    ax.set_xlim(0, r["cancel_rate_pct"].max() * 1.2)
    _style(ax, "Tỷ lệ hủy theo phân khúc thị trường", "Tỷ lệ hủy (%)", grid_axis="x")
    _finish(fig, "fig05_segment_cancel",
            f"n = {int(t['n_known'].sum()):,}; loại {n_missing:,} dòng thiếu phân khúc | "
            f"* mẫu số < {MIN_N_WARNING}, cần thận trọng khi diễn giải | "
            f"Nguồn: outputs/tables/q06_segment_cancel.csv", show)

    big = t.sort_values("n_reservations", ascending=False).iloc[0]
    hi = t.iloc[0]
    print(f"[Câu 6] Phân khúc lớn nhất: {big.market_segment} ({big.share_pct:.1f}%). "
          f"Hủy cao nhất: {hi.market_segment} ({hi.cancel_rate_pct:.2f}%, n={hi.n_known:,})."
          + (" Lưu ý: nhóm này có mẫu nhỏ." if hi.small_sample else ""))
    return t


# ----------------------------------------------------------------------------
# Câu 7 - Chính sách giá vé (fare_policy) x trạng thái đặt chỗ
# ----------------------------------------------------------------------------
def cau7(df, show=True):
    d = df.dropna(subset=["fare_policy", "booking_status"])
    n_missing = len(df) - len(d)
    ct = pd.crosstab(d["fare_policy"], d["booking_status"])
    for s in STATUS_ORDER:
        if s not in ct.columns:
            ct[s] = 0
    ct = ct[STATUS_ORDER + [c for c in ct.columns if c not in STATUS_ORDER]]
    ct = ct.reindex([p for p in POLICY_ORDER if p in ct.index] + [p for p in ct.index if p not in POLICY_ORDER])
    pct = ct.div(ct.sum(axis=1), axis=0) * 100

    t = (ct.stack().rename("n_reservations").reset_index()
         .merge(pct.stack().rename("pct_within_policy").round(2).reset_index(),
                on=["fare_policy", "booking_status"]))
    save_table(t, "q07_fare_policy_status")

    fig, ax = plt.subplots(figsize=(9, 4.8))
    left = np.zeros(len(pct))
    ylabels = [f"{p} (n={int(ct.loc[p].sum()):,})" for p in pct.index]
    for s in pct.columns:
        vals = pct[s].to_numpy()
        ax.barh(ylabels, vals, left=left, color=STATUS_COLORS.get(s, "#BBBBBB"), label=s)
        for i, v in enumerate(vals):
            if v >= 4:
                ax.text(left[i] + v / 2, i, f"{v:.1f}%", ha="center", va="center", color="white", fontsize=9)
        left += vals
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.legend(ncol=3, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    _style(ax, "Cơ cấu trạng thái đặt chỗ theo chính sách giá vé", "Tỷ lệ trong từng chính sách (%)", grid_axis="x")
    _finish(fig, "fig06_fare_policy_status",
            f"n = {len(d):,}; loại {n_missing:,} dòng thiếu fare_policy hoặc booking_status | "
            f"No-Show tách riêng khỏi Cancelled | Nguồn: outputs/tables/q07_fare_policy_status.csv", show)

    canc = t[t["booking_status"] == "Cancelled"].sort_values("pct_within_policy", ascending=False)
    if len(canc):
        print(f"[Câu 7] Tỷ lệ 'Cancelled' cao nhất ở {canc.iloc[0].fare_policy} ({canc.iloc[0].pct_within_policy:.2f}%), "
              f"thấp nhất ở {canc.iloc[-1].fare_policy} ({canc.iloc[-1].pct_within_policy:.2f}%).")
    return t


# ----------------------------------------------------------------------------
# Câu 8 - Giá vé trung bình theo hãng (chỉ đặt chỗ không hủy, giá > 0)
# ----------------------------------------------------------------------------
def cau8(df, show=True):
    d = df[df["is_cancelled"].eq(0).fillna(False).astype(bool)]
    excl_missing = d["avg_ticket_fare"].isna().groupby(d["airline"]).sum()
    excl_zero = d["avg_ticket_fare"].eq(0).groupby(d["airline"]).sum()
    v = d[d["avg_ticket_fare"] > 0]
    rows = {}
    for a, s in v.groupby("airline")["avg_ticket_fare"]:
        q = _quantiles(s)
        rows[a] = {"n_valid": q["n"], "mean": q["mean"], "median": q["median"], "q1": q["q1"],
                   "q3": q["q3"], "min": round(s.min(), 2), "max": q["max"],
                   "n_zero_excluded": int(excl_zero.get(a, 0)), "n_missing_excluded": int(excl_missing.get(a, 0))}
    t = pd.DataFrame(rows).T.rename_axis("airline").reset_index()
    for c in ["n_valid", "n_zero_excluded", "n_missing_excluded"]:
        t[c] = t[c].astype(int)
    save_table(t, "q08_fare_stats_by_airline")

    cap = float(v["avg_ticket_fare"].quantile(0.99))       # cắt trục ở phân vị 99 vì phân phối lệch phải
    n_above = int((v["avg_ticket_fare"] > cap).sum())
    fig, ax = plt.subplots(figsize=(9, 5))
    bins = np.linspace(0, cap, 41)
    for a in _airlines(v):
        s = v.loc[v["airline"] == a, "avg_ticket_fare"]
        sc = s[s <= cap]
        ax.hist(sc, bins=bins, weights=np.full(len(sc), 100 / len(s)), alpha=0.6,
                color=_color(a), label=f"{a} (n={len(s):,})")
        ax.axvline(s.median(), color=_color(a), ls="--", lw=1.5)
    ax.set_xlim(0, cap)
    ax.legend(frameon=False, title="Đường nét đứt = trung vị")
    _style(ax, "Phân phối giá vé trung bình theo hãng (đặt chỗ không hủy)",
           "Giá vé trung bình", "Tỷ lệ trong hãng (%)")
    _finish(fig, "fig07_fare_hist",
            f"n = {len(v):,}; chỉ đặt chỗ không hủy, giá > 0 | loại {int(excl_zero.sum()):,} dòng giá = 0 "
            f"và {int(excl_missing.sum()):,} dòng thiếu giá | trục x cắt ở phân vị 99 ({cap:,.0f}), "
            f"{n_above} dòng cao hơn không hiển thị | Nguồn: q08_fare_stats_by_airline.csv", show)

    print("[Câu 8] Giá vé (không hủy, giá > 0):")
    print(t.to_string(index=False))
    return t


# ----------------------------------------------------------------------------
# Câu 9 - Độ dài chuyến đi (chỉ đặt chỗ không hủy)
# ----------------------------------------------------------------------------
TRIP_BINS = [-1, 0, 2, 4, 7, 14, np.inf]
TRIP_LABELS = ["0", "1-2", "3-4", "5-7", "8-14", "15+"]


def cau9(df, show=True):
    d = df[df["is_cancelled"].eq(0).fillna(False).astype(bool)]
    n_missing = int(d["total_trip_days"].isna().sum())
    d = d.dropna(subset=["total_trip_days"]).copy()
    d["total_trip_days"] = d["total_trip_days"].astype(float)

    rows = {}
    for a, s in d.groupby("airline")["total_trip_days"]:
        q = _quantiles(s)
        q["n_zero_kept"] = int((s == 0).sum())      # giữ giá trị 0 hợp lệ, chỉ báo số lượng
        rows[a] = q
    t = pd.DataFrame(rows).T.rename_axis("airline").reset_index()
    t["n"] = t["n"].astype(int)
    t["n_zero_kept"] = t["n_zero_kept"].astype(int)
    save_table(t, "q09_trip_days")

    d["bucket"] = pd.cut(d["total_trip_days"], bins=TRIP_BINS, labels=TRIP_LABELS)
    dist = (d.groupby(["airline", "bucket"], observed=False).size().unstack(fill_value=0)
            .reindex(columns=TRIP_LABELS, fill_value=0))
    dist_pct = dist.div(dist.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(9, 5))
    airlines = list(dist_pct.index)
    w = 0.8 / max(len(airlines), 1)
    x = np.arange(len(TRIP_LABELS))
    for i, a in enumerate(airlines):
        bars = ax.bar(x + (i - (len(airlines) - 1) / 2) * w, dist_pct.loc[a], width=w,
                      color=_color(a), label=f"{a} (n={int(dist.loc[a].sum()):,})")
        ax.bar_label(bars, fmt="%.1f", padding=2, fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(TRIP_LABELS)
    ax.legend(frameon=False)
    _style(ax, "Phân phối độ dài chuyến đi (đặt chỗ không hủy)", "Tổng số ngày chuyến đi",
           "Tỷ lệ trong hãng (%)")
    _finish(fig, "fig08_trip_days",
            f"n = {len(d):,}; chỉ đặt chỗ không hủy, loại {n_missing:,} dòng thiếu độ dài chuyến đi | "
            f"giữ nhóm 0 ngày | Nguồn: outputs/tables/q09_trip_days.csv", show)

    print("[Câu 9] Độ dài chuyến đi (ngày):")
    print(t.to_string(index=False))
    return t, dist


# ----------------------------------------------------------------------------
# Câu 10 - Đổi hạng cabin (booked != assigned)
# ----------------------------------------------------------------------------
def _cabin_change(d, by):
    d = d.assign(_chg=(d["booked_cabin_code"] != d["assigned_cabin_code"]).astype(int))
    out = d.groupby(by).agg(n_valid=("_chg", "size"), n_changed=("_chg", "sum"))
    out["changed_rate_pct"] = (out["n_changed"] / out["n_valid"] * 100).round(2)
    return out.reset_index()


def cau10(df):
    d = df.dropna(subset=["booked_cabin_code", "assigned_cabin_code"])
    n_missing = len(df) - len(d)
    t_air = _cabin_change(d, "airline")
    t_code = _cabin_change(d, "booked_cabin_code")
    t_code["small_sample"] = t_code["n_valid"] < MIN_N_WARNING
    save_table(t_air, "q10_cabin_change_by_airline")
    save_table(t_code, "q10_cabin_change_by_booked_code")

    print(f"[Câu 10] Mẫu số: {len(d):,} dòng có đủ 2 mã cabin (loại {n_missing:,} dòng thiếu).")
    print(t_air.to_string(index=False))
    hi = t_code.sort_values("changed_rate_pct", ascending=False).iloc[0]
    print(f"[Câu 10] Mã cabin đặt có tỷ lệ đổi cao nhất: {hi.booked_cabin_code} "
          f"({hi.changed_rate_pct:.2f}%, n={hi.n_valid:,}).")
    return t_air, t_code


# ----------------------------------------------------------------------------
# Chạy tất cả
# ----------------------------------------------------------------------------
def run_all(df=None, monthly=None, show=True) -> dict:
    df = load_clean() if df is None else df
    if monthly is None:
        monthly = load_monthly()
    print(f"Dữ liệu: {len(df):,} dòng, {df.shape[1]} cột\n")
    res = {"q02": cau2(df, show), "q03": cau3(df, monthly, show), "q04": cau4(df, show),
           "q05": cau5(df, show), "q06": cau6(df, show), "q07": cau7(df, show),
           "q08": cau8(df, show), "q09": cau9(df, show), "q10": cau10(df)}
    print(f"\nĐã lưu bảng vào {TABLES_DIR} và hình vào {FIGURES_DIR}")
    return res


if __name__ == "__main__":
    plt.switch_backend("Agg")
    run_all(show=False)
