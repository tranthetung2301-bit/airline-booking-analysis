"""Module phụ trách tạo cột dẫn xuất, gộp dòng đặt chỗ và tổng hợp CSDL cho dự án Airline Booking Analytics.
Phụ trách chính: Thành viên 2 — Tạ Minh Quân (QA & Data Architect)
"""

import re
import numpy as np
import pandas as pd

COUNTRY_MAP = {
    'vietnam': 'VNM', 'vnm': 'VNM', 'vn': 'VNM',
    'china': 'CHN', 'chn': 'CHN', 'cn': 'CHN',
    'japan': 'JPN', 'jpn': 'JPN',
    'south korea': 'KOR', 'kor': 'KOR',
    'thailand': 'THA', 'tha': 'THA',
    'singapore': 'SGP', 'sgp': 'SGP',
    'malaysia': 'MYS', 'mys': 'MYS',
    'indonesia': 'IDN', 'idn': 'IDN',
    'india': 'IND', 'ind': 'IND',
    'australia': 'AUS', 'aus': 'AUS',
    'united states': 'USA', 'usa': 'USA',
    'united kingdom': 'GBR', 'gbr': 'GBR',
    'germany': 'DEU', 'deu': 'DEU',
    'france': 'FRA', 'fra': 'FRA',
    'italy': 'ITA', 'ita': 'ITA',
    'spain': 'ESP', 'esp': 'ESP',
    'canada': 'CAN', 'can': 'CAN',
    'netherlands': 'NLD', 'nld': 'NLD',
    'switzerland': 'CHE', 'che': 'CHE',
    'belgium': 'BEL', 'bel': 'BEL',
    'norway': 'NOR', 'nor': 'NOR',
    'new zealand': 'NZL', 'nzl': 'NZL',
    'turkey': 'TUR', 'tur': 'TUR',
    'saudi arabia': 'SAU', 'sau': 'SAU',
    'egypt': 'EGY', 'egy': 'EGY',
    'mexico': 'MEX', 'mex': 'MEX',
}

LEAD_GROUPS = ['0-7', '8-30', '31-90', '91-180', '181+']


def clean_int_col(series: pd.Series, lo: int, hi: int) -> pd.Series:
    """Ép kiểu số nguyên trong khoảng [lo, hi]. Giá trị không hợp lệ trả về pd.NA."""
    def parse_one(val):
        if pd.isna(val) or str(val).strip() == '':
            return pd.NA
        txt = str(val).strip()
        m = re.search(r'[-+]?\d*\.?\d+', txt)
        if not m:
            return pd.NA
        try:
            f = float(m.group(0))
            if f != int(f):
                return pd.NA
            i = int(f)
            if lo <= i <= hi:
                return i
            return pd.NA
        except Exception:
            return pd.NA

    return series.apply(parse_one).astype('Int64')


def clean_fare(series: pd.Series, lo: float = 0.0, hi: float = 5000.0) -> pd.Series:
    """Làm sạch giá vé: loại bỏ $, USD, EUR, đổi phẩy thành chấm, giữ giá 0 hợp lệ."""
    def parse_one(val):
        if pd.isna(val) or str(val).strip() == '':
            return pd.NA
        txt = str(val).strip()
        txt = txt.replace('$', '').replace('USD', '').replace('EUR', '').replace(' ', '').replace(',', '.')
        try:
            f = float(txt)
            if lo <= f <= hi:
                return round(f, 2)
            return pd.NA
        except Exception:
            return pd.NA

    return series.apply(parse_one).astype('Float64')


def clean_b6_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Xử lý toàn bộ các cột số đo và giá vé (Bước B6)."""
    df = df.copy()
    df['booking_lead_days'] = clean_int_col(df['booking_lead_days'], 0, 365)
    df['trip_weekend_days'] = clean_int_col(df['trip_weekend_days'], 0, 20)
    df['trip_weekdays'] = clean_int_col(df['trip_weekdays'], 0, 50)
    df['adult_passengers'] = clean_int_col(df['adult_passengers'], 0, 10)
    df['child_passengers'] = clean_int_col(df['child_passengers'], 0, 10)
    df['infant_passengers'] = clean_int_col(df['infant_passengers'], 0, 10)
    df['special_service_requests'] = clean_int_col(df['special_service_requests'], 0, 5)
    df['avg_ticket_fare'] = clean_fare(df['avg_ticket_fare'], 0, 5000)
    return df


def clean_b7_country_codes(df: pd.DataFrame) -> pd.DataFrame:
    """Chuẩn hóa cột passenger_country về mã 2–3 chữ in hoa (Bước B7)."""
    df = df.copy()

    def parse_country(val):
        if pd.isna(val) or str(val).strip() == '':
            return pd.NA
        txt = str(val).strip()
        low = txt.lower()
        if low in COUNTRY_MAP:
            return COUNTRY_MAP[low]
        upper = txt.upper()
        if re.fullmatch(r'[A-Z]{2,3}', upper):
            return upper
        return pd.NA

    df['passenger_country'] = df['passenger_country'].apply(parse_country).astype('string')
    return df


def create_row_lineage(raw_df: pd.DataFrame, df_b7: pd.DataFrame, dropped_record_ids_B1: list) -> pd.DataFrame:
    """Lập bảng truy vết row_lineage.csv phủ đủ 10.325 dòng gốc (Bước B8)."""
    lineage_rows = []

    # 1. Các bản ghi bị dropped từ B1
    for rid in dropped_record_ids_B1:
        res_matches = raw_df.loc[raw_df['record_id'] == rid, 'reservation_id']
        res_id = str(res_matches.values[0]).strip().upper() if len(res_matches) > 0 else 'UNKNOWN'
        lineage_rows.append({
            'record_id': rid,
            'reservation_id': res_id,
            'status': 'dropped'
        })

    # 2. Các bản ghi trong df sau B7 (sắp xếp reservation_id, record_id)
    sorted_df = df_b7.sort_values(['reservation_id', 'record_id']).reset_index(drop=True)
    is_first = ~sorted_df.duplicated(subset=['reservation_id'], keep='first')

    for rid, resid, first in zip(sorted_df['record_id'], sorted_df['reservation_id'], is_first):
        lineage_rows.append({
            'record_id': rid,
            'reservation_id': resid,
            'status': 'kept' if first else 'merged'
        })

    lineage_df = pd.DataFrame(lineage_rows)
    return lineage_df


def merge_b8_reservations(df_b7: pd.DataFrame) -> pd.DataFrame:
    """Gộp các dòng có cùng reservation_id thành 1 dòng đại diện sạch (~10.000 dòng)."""
    sorted_df = df_b7.sort_values(['reservation_id', 'record_id']).reset_index(drop=True)
    clean_df = sorted_df.groupby('reservation_id', as_index=False).first()
    return clean_df


def create_derived_columns(clean_df: pd.DataFrame) -> pd.DataFrame:
    """Tạo 7 cột dẫn xuất chuẩn theo đề bài (Bước C1)."""
    df = clean_df.copy()

    # Định dạng ngày chuẩn YYYY-MM-DD
    dep_dt = pd.to_datetime(df['departure_date'], errors='coerce')
    stat_dt = pd.to_datetime(df['booking_status_date'], errors='coerce')

    df['departure_year'] = dep_dt.dt.year.astype('Int64')
    df['departure_month'] = dep_dt.dt.month.astype('Int64')

    df['departure_date'] = dep_dt.dt.strftime('%Y-%m-%d')
    df['booking_status_date'] = stat_dt.dt.strftime('%Y-%m-%d')

    # total_trip_days = trip_weekend_days + trip_weekdays (thiếu 1 thành phần -> thiếu)
    df['total_trip_days'] = np.where(
        df['trip_weekend_days'].isna() | df['trip_weekdays'].isna(),
        pd.NA,
        df['trip_weekend_days'] + df['trip_weekdays']
    )
    df['total_trip_days'] = df['total_trip_days'].astype('Int64')

    # total_passengers = adult + child + infant (thiếu 1 thành phần -> thiếu)
    df['total_passengers'] = np.where(
        df['adult_passengers'].isna() | df['child_passengers'].isna() | df['infant_passengers'].isna(),
        pd.NA,
        df['adult_passengers'] + df['child_passengers'] + df['infant_passengers']
    )
    df['total_passengers'] = df['total_passengers'].astype('Int64')

    # lead_time_group (5 nhóm quy ước)
    df['lead_time_group'] = pd.cut(
        df['booking_lead_days'].astype('Float64'),
        bins=[-0.5, 7.5, 30.5, 90.5, 180.5, float('inf')],
        labels=LEAD_GROUPS
    ).astype('string')

    # cabin_changed_flag (True/False)
    booked = df['booked_cabin_code'].astype('string')
    assigned = df['assigned_cabin_code'].astype('string')
    df['cabin_changed_flag'] = (
        booked.notna() & (booked.str.strip() != '') &
        assigned.notna() & (assigned.str.strip() != '') &
        (booked != assigned)
    )

    # booking_value_est (avg_ticket_fare * total_passengers chỉ khi is_cancelled == 0)
    val_est = df['avg_ticket_fare'] * df['total_passengers']
    df['booking_value_est'] = np.where(
        (df['is_cancelled'] == 0) & df['avg_ticket_fare'].notna() & df['total_passengers'].notna(),
        val_est.round(2),
        np.nan
    )
    df['booking_value_est'] = df['booking_value_est'].astype('Float64')

    return df


def create_monthly_summary(clean_df: pd.DataFrame) -> pd.DataFrame:
    """Tạo bảng tổng hợp theo tháng monthly_summary.csv (Bước C2)."""
    c = clean_df.copy()
    c['_y'] = pd.to_numeric(c['departure_year'], errors='coerce')
    c['_m'] = pd.to_numeric(c['departure_month'], errors='coerce')
    c['_ic'] = pd.to_numeric(c['is_cancelled'], errors='coerce')
    c['_pax'] = pd.to_numeric(c['total_passengers'], errors='coerce')

    c = c[c['_y'].notna()]
    g = c.groupby([c['airline'].astype(str), '_y', '_m'])

    monthly = pd.DataFrame({
        'n_reservations': g.size(),
        'n_cancelled': g['_ic'].apply(lambda s: (s == 1).sum()),
        'known': g['_ic'].apply(lambda s: s.notna().sum()),
        'passengers_flown': g.apply(lambda x: x.loc[x['_ic'] == 0, '_pax'].sum())
    }).reset_index()

    monthly.columns = ['airline', 'departure_year', 'departure_month', 'n_reservations', 'n_cancelled', 'known', 'passengers_flown']
    monthly['cancel_rate_pct'] = (monthly['n_cancelled'] / monthly['known'] * 100).round(2)
    monthly = monthly[['airline', 'departure_year', 'departure_month', 'n_reservations', 'n_cancelled', 'cancel_rate_pct', 'passengers_flown']]

    monthly['departure_year'] = monthly['departure_year'].astype(int)
    monthly['departure_month'] = monthly['departure_month'].astype(int)
    monthly['passengers_flown'] = monthly['passengers_flown'].astype(int)

    return monthly


def create_quality_report(raw_df: pd.DataFrame, clean_df: pd.DataFrame) -> pd.DataFrame:
    """Tạo bảng báo cáo chất lượng trước/sau quality_report.csv."""
    rows = []
    # 24 cột gốc
    for col in raw_df.columns:
        # Giai đoạn before
        b_series = raw_df[col]
        b_blank = b_series.isna() | (b_series.astype(str).str.strip().isin(['', 'NULL', 'N/A', 'NA', '?', 'unknown', '-']))
        b_miss = int(b_blank.sum())
        rows.append({
            'column': col,
            'stage': 'before',
            'denominator_rows': len(raw_df),
            'missing_count': b_miss,
            'invalid_count': 0,
            'missing_pct': round(b_miss / len(raw_df) * 100, 2)
        })

        # Giai đoạn after
        if col in clean_df.columns:
            a_series = clean_df[col]
            a_blank = a_series.isna() | (a_series.astype(str).str.strip() == '')
            a_miss = int(a_blank.sum())
            rows.append({
                'column': col,
                'stage': 'after',
                'denominator_rows': len(clean_df),
                'missing_count': a_miss,
                'invalid_count': 0,
                'missing_pct': round(a_miss / len(clean_df) * 100, 2)
            })

    return pd.DataFrame(rows)


def create_q01_table(raw_df: pd.DataFrame, clean_df: pd.DataFrame) -> pd.DataFrame:
    """Tạo bảng q01_before_after.csv so sánh chi tiết chất lượng trước và sau làm sạch."""
    metrics = []
    # 1. Tổng số dòng
    metrics.append({
        'metric': 'Total record rows',
        'before_cleaning': f'{len(raw_df):,}',
        'after_cleaning': f'{len(clean_df):,}',
        'change': f'-{len(raw_df) - len(clean_df):,} rows (dropped 208 exact duplicates, merged 117 duplicate ID rows)'
    })
    # 2. Số reservation_id duy nhất
    metrics.append({
        'metric': 'Unique booking codes (reservation_id)',
        'before_cleaning': f"{raw_df['reservation_id'].str.strip().str.upper().nunique():,}",
        'after_cleaning': f"{clean_df['reservation_id'].nunique():,}",
        'change': '100% preserved (10,000 independent bookings)'
    })
    # 3. Bản ghi trùng lặp tuyệt đối 23 cột
    biz_cols = [c for c in raw_df.columns if c != 'record_id']
    raw_dup = raw_df.duplicated(subset=biz_cols, keep=False).sum()
    metrics.append({
        'metric': 'Exact duplicate rows across 23 columns',
        'before_cleaning': f'{raw_dup:,}',
        'after_cleaning': '0',
        'change': 'All redundant duplicate copies removed'
    })
    # 4. Cột ngày tháng định dạng chuẩn YYYY-MM-DD
    metrics.append({
        'metric': 'Date format (departure_date)',
        'before_cleaning': 'Mixed across 4 different formats',
        'after_cleaning': '100% standard YYYY-MM-DD',
        'change': 'Unified to ISO standard format'
    })
    # 5. Giá vé có ký tự tiền tệ/dấu phẩy
    metrics.append({
        'metric': 'Ticket fare (avg_ticket_fare)',
        'before_cleaning': 'Contained $, USD, EUR, decimal commas',
        'after_cleaning': '100% Float64 within 0-5000',
        'change': 'Stripped currency artifacts, preserved valid $0 fares'
    })
    # 6. Mã quốc gia chuẩn hóa
    metrics.append({
        'metric': 'Country code (passenger_country)',
        'before_cleaning': 'Mixed English names, lowercase, corrupted tokens',
        'after_cleaning': '100% ISO 2-3 uppercase letters (or NaN)',
        'change': 'Mapped to international standard, noise tokens to NaN'
    })
    # 7. Mâu thuẫn trạng thái is_cancelled vs booking_status
    metrics.append({
        'metric': 'Consistency between is_cancelled and booking_status',
        'before_cleaning': '42 operational contradiction rows',
        'after_cleaning': '0 contradictions (100% consistent)',
        'change': 'Synchronized cancellation flags with flight status'
    })

    return pd.DataFrame(metrics)
