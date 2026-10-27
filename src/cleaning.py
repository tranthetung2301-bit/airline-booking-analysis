"""Module phụ trách khảo sát và làm sạch dữ liệu cho dự án Airline Booking Analytics.
Phụ trách chính: Thành viên 1 — Trần Thế Tùng (Kỹ sư Làm sạch Dữ liệu)

Giai đoạn A: Khảo sát dữ liệu gốc (24 cột, 10.325 dòng)
Giai đoạn B1–B5: Làm sạch bước đầu
    B1 — Chuẩn hóa khóa & loại bản ghi trùng tuyệt đối
    B2 — Chuyển ngày nằm nhầm cột
    B3 — Chuẩn hóa giá trị thiếu (NULL, NA, ?, -, unknown → pd.NA)
    B4 — Chuẩn hóa nhãn phân loại & đồng bộ is_cancelled
    B5 — Chuyển định dạng ngày tháng về datetime chuẩn
"""

import re
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Hằng số quy ước (Mục 5 đề bài)
# ---------------------------------------------------------------------------
MISSING_TOKENS = ['NULL', 'N/A', 'NA', '?', 'unknown', '-']

AIRLINES = ['Aurora Air', 'Horizon Wings']
MEALS = ['Standard', 'Vegetarian', 'Special', 'No Meal']
SEGMENTS = ['Direct', 'Online OTA', 'Offline Agent', 'Corporate',
            'Group', 'Package Tour', 'Loyalty']
CHANNELS = ['Website', 'Mobile App', 'Travel Agency', 'GDS/Corporate']
FARE_POLICIES = ['Flexible', 'Semi-Flexible', 'Non-Refundable']
TRAVELERS = ['Individual', 'Linked Booking', 'Corporate Contract', 'Group']
STATUSES = ['Flown', 'Cancelled', 'No-Show']
CABIN_CODES = ['E1', 'E2', 'E3', 'E4', 'P1', 'P2',
               'B1', 'B2', 'B3', 'F1', 'F2', 'F3']

DEPARTURE_MIN = pd.Timestamp('2024-07-01')
DEPARTURE_MAX = pd.Timestamp('2026-08-31')
STATUS_MIN = pd.Timestamp('2024-01-01')
STATUS_MAX = pd.Timestamp('2026-09-15')

DATE_FORMATS = [
    '%Y-%m-%d',    # 2024-11-06 (ISO)
    '%d/%m/%Y',    # 23/08/2025
    '%B %d, %Y',   # October 6, 2025
    '%d-%b-%Y',    # 30-Jun-2025
    '%d %b %Y',    # 15 Nov 2024
]

# Từ điển ánh xạ nhãn phân loại
AIRLINE_MAP = {
    'auroraair': 'Aurora Air', 'aurora': 'Aurora Air',
    'horizonwings': 'Horizon Wings', 'horizon': 'Horizon Wings',
}
MEAL_MAP = {
    'standard': 'Standard', 'vegetarian': 'Vegetarian',
    'special': 'Special', 'nomeal': 'No Meal',
    'undefined': 'No Meal', 'none': 'No Meal',
}
SEGMENT_MAP = {
    'direct': 'Direct', 'onlineota': 'Online OTA',
    'offlineagent': 'Offline Agent', 'corporate': 'Corporate',
    'group': 'Group', 'packagetour': 'Package Tour', 'loyalty': 'Loyalty',
}
CHANNEL_MAP = {
    'website': 'Website', 'mobileapp': 'Mobile App',
    'travelagency': 'Travel Agency', 'gdscorporate': 'GDS/Corporate',
    'gds': 'GDS/Corporate', 'corporate': 'GDS/Corporate',
}
FARE_POLICY_MAP = {
    'flexible': 'Flexible', 'semiflexible': 'Semi-Flexible',
    'nonrefundable': 'Non-Refundable',
}
TRAVELER_MAP = {
    'individual': 'Individual', 'linkedbooking': 'Linked Booking',
    'corporatecontract': 'Corporate Contract', 'group': 'Group',
}
STATUS_MAP = {
    'flown': 'Flown', 'completed': 'Flown',
    'cancelled': 'Cancelled', 'canceled': 'Cancelled',
    'noshow': 'No-Show',
}


# ---------------------------------------------------------------------------
# Hàm tiện ích
# ---------------------------------------------------------------------------
def clean_key(x):
    """Chuẩn hóa chuỗi về chữ thường, chỉ giữ ký tự a-z để so khớp."""
    if pd.isna(x):
        return pd.NA
    return re.sub(r'[^a-z]', '', str(x).strip().lower())


def _apply_label_map(series: pd.Series, label_map: dict) -> pd.Series:
    """Ánh xạ nhãn phân loại qua từ điển. Giá trị không khớp → pd.NA."""
    key_series = series.apply(clean_key)
    mapped = key_series.map(label_map)
    result = mapped.where(series.notna(), other=pd.NA)
    return result


def _to_binary_int(series: pd.Series) -> pd.Series:
    """Chuyển giá trị yes/no/True/False/0.0/1.0 về Int64 0/1."""
    TRUE_VALS = {'1', '1.0', 'yes', 'true', 'Yes', 'True', 'YES', 'TRUE'}
    FALSE_VALS = {'0', '0.0', 'no', 'false', 'No', 'False', 'NO', 'FALSE'}

    def conv(x):
        if pd.isna(x):
            return pd.NA
        s = str(x).strip()
        if s in TRUE_VALS:
            return 1
        if s in FALSE_VALS:
            return 0
        try:
            v = float(s)
            if v == 1.0:
                return 1
            if v == 0.0:
                return 0
        except (ValueError, TypeError):
            pass
        return pd.NA

    return series.apply(conv).astype('Int64')


# ===========================================================================
# GIAI ĐOẠN A — Khảo sát dữ liệu gốc
# ===========================================================================

def survey_missing_values(raw_df: pd.DataFrame) -> pd.DataFrame:
    """A2 — Thống kê số lượng ô thiếu theo từng cột (24 cột).

    Đếm:
    - empty_count: ô rỗng (sau strip)
    - token_count: ô chứa ký hiệu thiếu (NULL, N/A, NA, ?, unknown, -)
    - missing_total: tổng empty + token
    - missing_pct: tỷ lệ phần trăm thiếu
    """
    tokens_lower = [t.lower() for t in MISSING_TOKENS]
    records = []
    for col in raw_df.columns:
        n_rows = len(raw_df)
        empty_count = (raw_df[col].str.strip() == '').sum()
        token_count = raw_df[col].str.lower().isin(tokens_lower).sum()
        missing_total = empty_count + token_count
        missing_pct = round(missing_total / n_rows * 100, 2)
        records.append({
            'column': col,
            'n_rows': n_rows,
            'empty_count': int(empty_count),
            'token_count': int(token_count),
            'missing_total': int(missing_total),
            'missing_pct': missing_pct,
        })
    return pd.DataFrame(records)


def catalog_issues(raw_df: pd.DataFrame) -> pd.DataFrame:
    """A6 — Tìm ≥ 10 nhóm vấn đề dữ liệu kèm ví dụ record_id.

    Trả về DataFrame gồm 12 nhóm vấn đề (I01–I12):
    I01: airline nhãn không chuẩn
    I02: ngày nằm nhầm cột booking_status
    I03: booking_status nhãn không chuẩn
    I04: is_cancelled giá trị không chuẩn
    I05: departure_date nhiều định dạng
    I06: avg_ticket_fare ký hiệu/bất hợp lý
    I07: passenger_country mã không chuẩn
    I08: bản ghi trùng tuyệt đối
    I09: meal_option nhãn không chuẩn
    I10: child_passengers thiếu
    I11: market_segment/sales_channel Undefined
    I12: is_cancelled mâu thuẫn booking_status
    """
    tokens_lower = [t.lower() for t in MISSING_TOKENS]

    def get_examples(mask, n=5):
        ids = raw_df[mask]['record_id'].head(n).tolist()
        return '; '.join(ids)

    issues = []

    # I01 · airline: nhãn không chuẩn
    airline_valid = raw_df['airline'].str.strip().isin(AIRLINES)
    i01_mask = ~airline_valid & (raw_df['airline'].str.strip() != '')
    issues.append({
        'issue_id': 'I01', 'field': 'airline',
        'issue': 'Nhãn airline không chuẩn (AURORA AIR, aurora air, Horizon, Aurora)',
        'detection_rule': 'airline.strip() không thuộc {Aurora Air, Horizon Wings}',
        'affected_rows': int(i01_mask.sum()),
        'example_record_ids': get_examples(i01_mask),
    })

    # I02 · booking_status: ngày nằm nhầm cột
    bs_is_date = raw_df['booking_status'].str.strip().str.fullmatch(r'\d{4}-\d{2}-\d{2}')
    bsd_empty = raw_df['booking_status_date'].str.strip() == ''
    i02_mask = bs_is_date & bsd_empty
    issues.append({
        'issue_id': 'I02', 'field': 'booking_status / booking_status_date',
        'issue': 'Ngày YYYY-MM-DD nằm nhầm ở booking_status thay vì booking_status_date',
        'detection_rule': 'booking_status fullmatch YYYY-MM-DD AND booking_status_date rỗng',
        'affected_rows': int(i02_mask.sum()),
        'example_record_ids': get_examples(i02_mask),
    })

    # I03 · booking_status: nhãn không chuẩn
    bs_valid = raw_df['booking_status'].str.strip().isin(STATUSES)
    bs_not_date = ~raw_df['booking_status'].str.strip().str.fullmatch(r'\d{4}-\d{2}-\d{2}')
    bs_not_empty = raw_df['booking_status'].str.strip() != ''
    i03_mask = ~bs_valid & bs_not_date & bs_not_empty
    issues.append({
        'issue_id': 'I03', 'field': 'booking_status',
        'issue': 'Nhãn trạng thái không chuẩn (flown, FLOWN, Completed, Canceled, CANCELLED)',
        'detection_rule': 'booking_status.strip() không thuộc {Flown, Cancelled, No-Show} và không phải ngày',
        'affected_rows': int(i03_mask.sum()),
        'example_record_ids': get_examples(i03_mask),
    })

    # I04 · is_cancelled: giá trị không chuẩn
    canc_valid = raw_df['is_cancelled'].str.strip().isin(['0', '1'])
    canc_not_empty = raw_df['is_cancelled'].str.strip() != ''
    i04_mask = ~canc_valid & canc_not_empty
    issues.append({
        'issue_id': 'I04', 'field': 'is_cancelled',
        'issue': 'Giá trị không chuẩn: yes/no/True/False/0.0/1.0',
        'detection_rule': 'is_cancelled.strip() không thuộc {0, 1}',
        'affected_rows': int(i04_mask.sum()),
        'example_record_ids': get_examples(i04_mask),
    })

    # I05 · departure_date: nhiều định dạng
    dep_noniso = ~raw_df['departure_date'].str.strip().str.fullmatch(r'\d{4}-\d{2}-\d{2}')
    dep_not_empty = raw_df['departure_date'].str.strip() != ''
    dep_not_token = ~raw_df['departure_date'].str.lower().isin(tokens_lower)
    i05_mask = dep_noniso & dep_not_empty & dep_not_token
    issues.append({
        'issue_id': 'I05', 'field': 'departure_date',
        'issue': 'Nhiều định dạng ngày: DD/MM/YYYY, DD-Mon-YYYY, Month DD, YYYY',
        'detection_rule': r'departure_date không khớp \d{4}-\d{2}-\d{2}',
        'affected_rows': int(i05_mask.sum()),
        'example_record_ids': get_examples(i05_mask),
    })

    # I06 · avg_ticket_fare: ký hiệu, thiếu, bất hợp lý
    fare_nonnum = pd.to_numeric(raw_df['avg_ticket_fare'], errors='coerce').isna()
    fare_not_empty = raw_df['avg_ticket_fare'].str.strip() != ''
    fare_not_token = ~raw_df['avg_ticket_fare'].str.lower().isin(tokens_lower)
    i06_mask = fare_nonnum & fare_not_empty & fare_not_token
    fare_num = pd.to_numeric(raw_df['avg_ticket_fare'], errors='coerce')
    fare_outrange = fare_num.notna() & (~fare_num.between(0, 5000))
    issues.append({
        'issue_id': 'I06', 'field': 'avg_ticket_fare',
        'issue': 'Ký hiệu thiếu (null/N/A/-), ký hiệu tiền tệ ($), giá bất hợp lý (9999)',
        'detection_rule': 'to_numeric fails OR value not in [0, 5000]',
        'affected_rows': int(i06_mask.sum() + fare_outrange.sum()),
        'example_record_ids': get_examples(i06_mask | fare_outrange),
    })

    # I07 · passenger_country: mã không chuẩn
    country_bad = ~raw_df['passenger_country'].str.strip().str.fullmatch(r'[A-Z]{3}')
    country_not_empty = raw_df['passenger_country'].str.strip() != ''
    country_not_token = ~raw_df['passenger_country'].str.lower().isin(tokens_lower)
    i07_mask = country_bad & country_not_empty & country_not_token
    issues.append({
        'issue_id': 'I07', 'field': 'passenger_country',
        'issue': 'Mã quốc gia không chuẩn: 2 chữ (CN→CHN), chữ thường, ký hiệu thiếu',
        'detection_rule': 'passenger_country không khớp [A-Z]{3}',
        'affected_rows': int(i07_mask.sum()),
        'example_record_ids': get_examples(i07_mask),
    })

    # I08 · Bản ghi trùng
    biz_cols = [c for c in raw_df.columns if c != 'record_id']
    dup_mask = raw_df.duplicated(subset=biz_cols, keep=False)
    issues.append({
        'issue_id': 'I08', 'field': 'ALL (23 cột nghiệp vụ)',
        'issue': 'Bản ghi trùng tuyệt đối trên 23 cột nghiệp vụ (không tính record_id)',
        'detection_rule': 'duplicated(subset=23_biz_cols, keep=False)',
        'affected_rows': int(dup_mask.sum()),
        'example_record_ids': get_examples(dup_mask),
    })

    # I09 · meal_option: nhãn không chuẩn và thiếu
    meal_valid = raw_df['meal_option'].str.strip().isin(MEALS)
    meal_not_empty = raw_df['meal_option'].str.strip() != ''
    meal_not_token = ~raw_df['meal_option'].str.lower().isin(tokens_lower)
    i09_mask = ~meal_valid & meal_not_empty & meal_not_token
    meal_token_mask = raw_df['meal_option'].str.lower().isin(tokens_lower)
    meal_empty_mask = raw_df['meal_option'].str.strip() == ''
    issues.append({
        'issue_id': 'I09', 'field': 'meal_option',
        'issue': 'Nhãn không chuẩn (Undefined→No Meal), ký hiệu thiếu, ô rỗng',
        'detection_rule': 'meal_option.strip() không thuộc MEALS hoặc là token/rỗng',
        'affected_rows': int(i09_mask.sum() + meal_token_mask.sum() + meal_empty_mask.sum()),
        'example_record_ids': get_examples(i09_mask | meal_token_mask | meal_empty_mask),
    })

    # I10 · child_passengers: thiếu
    child_token = raw_df['child_passengers'].str.lower().isin(tokens_lower)
    child_empty = raw_df['child_passengers'].str.strip() == ''
    i10_mask = child_token | child_empty
    issues.append({
        'issue_id': 'I10', 'field': 'child_passengers',
        'issue': 'Giá trị thiếu: ký hiệu NULL/NA/? hoặc ô rỗng',
        'detection_rule': 'child_passengers là MISSING_TOKEN hoặc rỗng',
        'affected_rows': int(i10_mask.sum()),
        'example_record_ids': get_examples(i10_mask),
    })

    # I11 · market_segment / sales_channel: Undefined
    seg_undef = raw_df['market_segment'].str.strip().str.lower() == 'undefined'
    ch_undef = raw_df['sales_channel'].str.strip().str.lower() == 'undefined'
    i11_mask = seg_undef | ch_undef
    issues.append({
        'issue_id': 'I11', 'field': 'market_segment / sales_channel',
        'issue': 'Nhãn Undefined = không xác định → cần đưa về NaN',
        'detection_rule': 'value.strip().lower() == "undefined"',
        'affected_rows': int(i11_mask.sum()),
        'example_record_ids': get_examples(i11_mask),
    })

    # I12 · is_cancelled mâu thuẫn với booking_status
    canc_0 = raw_df['is_cancelled'].str.strip().isin(['0'])
    canc_1 = raw_df['is_cancelled'].str.strip().isin(['1'])
    status_flown_r = raw_df['booking_status'].str.strip().str.lower() == 'flown'
    status_cancelled_r = raw_df['booking_status'].str.strip().str.lower().isin(
        ['cancelled', 'no-show']
    )
    i12_mask = (status_flown_r & canc_1) | (status_cancelled_r & canc_0)
    issues.append({
        'issue_id': 'I12', 'field': 'is_cancelled / booking_status',
        'issue': 'is_cancelled mâu thuẫn với booking_status (Flown↔1 hoặc Cancelled↔0)',
        'detection_rule': '(status==Flown AND is_cancelled==1) OR '
                          '(status==Cancelled/No-Show AND is_cancelled==0)',
        'affected_rows': int(i12_mask.sum()),
        'example_record_ids': get_examples(i12_mask),
    })

    return pd.DataFrame(issues)


# ===========================================================================
# GIAI ĐOẠN B — Làm sạch dữ liệu
# ===========================================================================

def clean_b1_duplicates(df: pd.DataFrame):
    """B1 — Chuẩn hóa reservation_id (strip+upper) và loại bản ghi trùng tuyệt đối.

    Returns:
        df_clean: DataFrame sau khi loại trùng
        dropped_record_ids: danh sách record_id bị loại (dùng cho row_lineage)
    """
    df = df.copy()

    # Chuẩn hóa reservation_id
    df['reservation_id'] = df['reservation_id'].str.strip().str.upper()

    # Loại bản ghi trùng tuyệt đối trên 23 cột nghiệp vụ
    biz_cols = [c for c in df.columns if c != 'record_id']
    dup_to_drop = df.duplicated(subset=biz_cols, keep='first')
    dropped_record_ids = df[dup_to_drop]['record_id'].tolist()
    df = df[~dup_to_drop].copy().reset_index(drop=True)

    return df, dropped_record_ids


def clean_b2_misplaced_dates(df: pd.DataFrame) -> pd.DataFrame:
    """B2 — Chuyển ngày YYYY-MM-DD nằm nhầm ở booking_status sang booking_status_date."""
    df = df.copy()

    bs_is_date = df['booking_status'].str.strip().str.fullmatch(r'\d{4}-\d{2}-\d{2}')
    bsd_empty = df['booking_status_date'].str.strip() == ''
    swap_mask = bs_is_date & bsd_empty

    if swap_mask.sum() > 0:
        df.loc[swap_mask, 'booking_status_date'] = df.loc[swap_mask, 'booking_status'].str.strip()
        df.loc[swap_mask, 'booking_status'] = ''

    return df


def clean_b3_invalid_symbols(df: pd.DataFrame) -> pd.DataFrame:
    """B3 — Đưa NULL, NA, N/A, ?, -, unknown, ô rỗng và Undefined về pd.NA."""
    df = df.copy().astype(object)

    tokens_lower = [t.lower() for t in MISSING_TOKENS]
    skip_cols = {'record_id', 'reservation_id'}

    for col in df.columns:
        if col in skip_cols:
            continue

        # Ô rỗng → pd.NA
        empty_mask = df[col].astype(str).str.strip() == ''
        df.loc[empty_mask, col] = pd.NA

        # Ký hiệu thiếu → pd.NA
        token_mask = df[col].dropna().astype(str).str.lower().isin(tokens_lower)
        token_idx = df[col].dropna()[token_mask].index
        df.loc[token_idx, col] = pd.NA

    # Xử lý Undefined ở market_segment, sales_channel
    for col in ['market_segment', 'sales_channel']:
        undef_mask = df[col].dropna().astype(str).str.strip().str.lower() == 'undefined'
        undef_idx = df[col].dropna()[undef_mask].index
        df.loc[undef_idx, col] = pd.NA

    return df


def clean_b4_categorical_labels(df: pd.DataFrame) -> pd.DataFrame:
    """B4 — Chuẩn hóa nhãn phân loại, cabin code, cờ nhị phân, đồng bộ is_cancelled."""
    df = df.copy()

    # Strip + gom nhiều khoảng trắng
    for col in df.select_dtypes(include='object').columns:
        if col == 'record_id':
            continue
        df[col] = df[col].apply(
            lambda x: re.sub(r'\s+', ' ', str(x).strip()) if pd.notna(x) else x
        )

    # Áp dụng ánh xạ nhãn phân loại
    df['airline'] = _apply_label_map(df['airline'], AIRLINE_MAP)
    df['meal_option'] = _apply_label_map(df['meal_option'], MEAL_MAP)
    df['market_segment'] = _apply_label_map(df['market_segment'], SEGMENT_MAP)
    df['sales_channel'] = _apply_label_map(df['sales_channel'], CHANNEL_MAP)
    df['fare_policy'] = _apply_label_map(df['fare_policy'], FARE_POLICY_MAP)
    df['traveler_type'] = _apply_label_map(df['traveler_type'], TRAVELER_MAP)
    df['booking_status'] = _apply_label_map(df['booking_status'], STATUS_MAP)

    # Chuẩn hóa cabin code
    for cabin_col in ['booked_cabin_code', 'assigned_cabin_code']:
        df[cabin_col] = df[cabin_col].apply(
            lambda x: (str(x).strip().upper()
                        if pd.notna(x) and str(x).strip().upper() in CABIN_CODES
                        else pd.NA)
        )

    # Chuẩn hóa is_cancelled, is_returning_customer → Int64 0/1
    df['is_cancelled'] = _to_binary_int(df['is_cancelled'])
    df['is_returning_customer'] = _to_binary_int(df['is_returning_customer'])

    # Đồng bộ is_cancelled từ booking_status
    status_flown_mask = df['booking_status'] == 'Flown'
    status_cancel_mask = df['booking_status'].isin(['Cancelled', 'No-Show'])
    df.loc[status_flown_mask, 'is_cancelled'] = pd.array(
        [0] * status_flown_mask.sum(), dtype='Int64'
    )
    df.loc[status_cancel_mask, 'is_cancelled'] = pd.array(
        [1] * status_cancel_mask.sum(), dtype='Int64'
    )

    return df


def clean_b5_date_formats(df: pd.DataFrame) -> pd.DataFrame:
    """B5 — Chuyển departure_date (4 định dạng) và booking_status_date về datetime chuẩn."""
    df = df.copy()

    # --- Parse departure_date ---
    dep_str = df['departure_date'].copy()
    dep_parsed = pd.Series([pd.NaT] * len(df), index=df.index, dtype='datetime64[ns]')

    for fmt in DATE_FORMATS:
        remaining_mask = dep_parsed.isna() & dep_str.notna()
        if remaining_mask.sum() == 0:
            break
        parsed_attempt = pd.to_datetime(
            dep_str.where(remaining_mask, other=None),
            format=fmt, errors='coerce'
        )
        dep_parsed = dep_parsed.fillna(parsed_attempt)

    # Loại bỏ ngày ngoài miền
    out_of_range_dep = dep_parsed.notna() & ~dep_parsed.between(DEPARTURE_MIN, DEPARTURE_MAX)
    dep_parsed[out_of_range_dep] = pd.NaT
    df['departure_date'] = dep_parsed

    # --- Parse booking_status_date ---
    bsd_str = df['booking_status_date'].copy()
    bsd_parsed = pd.to_datetime(bsd_str, format='%Y-%m-%d', errors='coerce')

    out_of_range_bsd = bsd_parsed.notna() & ~bsd_parsed.between(STATUS_MIN, STATUS_MAX)
    bsd_parsed[out_of_range_bsd] = pd.NaT
    df['booking_status_date'] = bsd_parsed

    return df


# ===========================================================================
# HÀM TỔNG HỢP — Chạy toàn bộ pipeline A + B1–B5
# ===========================================================================

def run_phase_a(raw_df: pd.DataFrame):
    """Chạy toàn bộ Giai đoạn A: khảo sát dữ liệu gốc.

    Returns:
        missing_survey: DataFrame thống kê ô thiếu 24 cột
        issue_catalog: DataFrame 12 nhóm vấn đề dữ liệu
    """
    missing_survey = survey_missing_values(raw_df)
    issue_catalog = catalog_issues(raw_df)
    return missing_survey, issue_catalog


def run_phase_b(raw_df: pd.DataFrame):
    """Chạy toàn bộ Giai đoạn B1–B5: làm sạch bước đầu.

    Returns:
        df: DataFrame sau B5 (sẵn sàng cho B6 của TV2)
        dropped_record_ids_B1: danh sách record_id bị loại ở B1
    """
    # B1 — Chuẩn hóa khóa & loại trùng
    df, dropped_record_ids_B1 = clean_b1_duplicates(raw_df.copy())

    # B2 — Chuyển ngày nhầm cột
    df = clean_b2_misplaced_dates(df)

    # B3 — Chuẩn hóa giá trị thiếu
    df = clean_b3_invalid_symbols(df)

    # B4 — Chuẩn hóa nhãn phân loại
    df = clean_b4_categorical_labels(df)

    # B5 — Chuyển định dạng ngày
    df = clean_b5_date_formats(df)

    return df, dropped_record_ids_B1
