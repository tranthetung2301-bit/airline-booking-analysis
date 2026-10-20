#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm tra cấu trúc bài nộp Phân tích đặt vé máy bay.

Cách dùng (máy cá nhân):   python tools/kiem_tra_nop_bai.py NhomXX_HangKhong
Cách dùng (Google Colab):  !python kiem_tra_nop_bai.py .

Công cụ chỉ kiểm tra cấu trúc, khóa, miền giá trị và tính nhất quán theo đề bài; không chứa đáp án.
"""
import pandas as pd

AIRLINES = ['Aurora Air', 'Horizon Wings']
MEALS = ['Standard', 'Vegetarian', 'Special', 'No Meal']
SEGMENTS = ['Direct', 'Online OTA', 'Offline Agent', 'Corporate', 'Group', 'Package Tour', 'Loyalty']
CHANNELS = ['Website', 'Mobile App', 'Travel Agency', 'GDS/Corporate']
FARE_POLICIES = ['Flexible', 'Semi-Flexible', 'Non-Refundable']
TRAVELERS = ['Individual', 'Linked Booking', 'Corporate Contract', 'Group']
STATUSES = ['Flown', 'Cancelled', 'No-Show']
CABIN_CODES = ['E1', 'E2', 'E3', 'E4', 'P1', 'P2', 'B1', 'B2', 'B3', 'F1', 'F2', 'F3']
LEAD_GROUPS = ['0-7', '8-30', '31-90', '91-180', '181+']
DEPARTURE_MIN, DEPARTURE_MAX = pd.Timestamp('2024-07-01'), pd.Timestamp('2026-08-31')
STATUS_MIN, STATUS_MAX = pd.Timestamp('2024-01-01'), pd.Timestamp('2026-09-15')
LEAD_MIN, LEAD_MAX = 0, 365
WEEKEND_MAX, WEEK_MAX = 20, 50
PASSENGER_MAX = 10
FARE_MIN, FARE_MAX = 0, 5000
REQ_MAX = 5
N_RAW_ROWS = 10325

CLEAN_REQUIRED = ['reservation_id', 'airline', 'is_cancelled', 'booking_lead_days', 'departure_date', 'trip_weekend_days',
                  'trip_weekdays', 'adult_passengers', 'child_passengers', 'infant_passengers', 'meal_option',
                  'passenger_country', 'market_segment', 'sales_channel', 'is_returning_customer', 'booked_cabin_code',
                  'assigned_cabin_code', 'fare_policy', 'traveler_type', 'avg_ticket_fare', 'special_service_requests',
                  'booking_status', 'booking_status_date', 'departure_year', 'departure_month', 'total_trip_days',
                  'total_passengers', 'lead_time_group', 'cabin_changed_flag', 'booking_value_est']
SUMMARY_COLUMNS = ['airline', 'departure_year', 'departure_month', 'n_reservations', 'n_cancelled',
                   'cancel_rate_pct', 'passengers_flown']
LOG_COLUMNS = ['step', 'field', 'issue', 'detection_rule', 'action', 'affected_rows', 'changed_cells', 'removed_rows',
               'example_record_ids', 'reason', 'check_after']
LINEAGE_COLUMNS = ['record_id', 'reservation_id', 'status']
LINEAGE_STATUS = ['kept', 'merged', 'dropped']
QUALITY_COLUMNS = ['column', 'stage', 'denominator_rows', 'missing_count', 'invalid_count', 'missing_pct']
CORE_FILES = ['reservations_clean.csv', 'monthly_summary.csv', 'cleaning_log.csv', 'row_lineage.csv', 'quality_report.csv']
FIGURE_FILES = ['fig01_airline_cancel.png', 'fig02_monthly_departures_2025.png', 'fig03_leadtime_cancel.png',
                'fig04_top10_country.png', 'fig05_segment_cancel.png', 'fig06_fare_policy_status.png',
                'fig07_fare_hist.png', 'fig08_trip_days.png']
TABLE_FILES = ['a_missing_survey.csv', 'a_issue_catalog.csv', 'q01_before_after.csv',
               'q02_airline_cancel.csv', 'q03_monthly_departures_2025.csv', 'q04_leadtime_stats.csv',
               'q04_leadtime_cancel.csv', 'q05_top10_country.csv', 'q06_segment_cancel.csv',
               'q07_fare_policy_status.csv', 'q08_fare_stats_by_airline.csv', 'q09_trip_days.csv',
               'q10_cabin_change_by_airline.csv', 'q10_cabin_change_by_booked_code.csv']

def _blank(s):
    """True khi ô thiếu: NaN/None/NA hoặc chuỗi rỗng sau khi bỏ khoảng trắng."""
    return s.isna() | s.astype('string').str.strip().fillna('').eq('')


def _num(s):
    return pd.to_numeric(s.where(~_blank(s)), errors='coerce')


def _int_ok(s, lo, hi):
    """Ô có dữ liệu phải là số nguyên trong [lo, hi]. Trả về (đạt?, số ô sai)."""
    present = ~_blank(s)
    v = _num(s)
    bad = present & (v.isna() | (v % 1 != 0) | (v < lo) | (v > hi))
    return int(bad.sum()) == 0, int(bad.sum())


def _bool(s):
    m = {'true': True, 'false': False, '1': True, '0': False, '1.0': True, '0.0': False}
    return s.astype('string').str.strip().str.lower().map(m)


def _date(s):
    txt = s.astype('string').str.strip()
    return pd.to_datetime(txt.where(~_blank(s)), format='%Y-%m-%d', errors='coerce')


def _cat_ok(s, allowed, allow_missing=True):
    present = ~_blank(s)
    bad = sorted(set(s[present].astype(str)) - set(allowed))
    miss = int((~present).sum())
    ok = not bad and (allow_missing or miss == 0)
    return ok, ('Nhãn lạ: ' + ', '.join(bad[:6]) if bad else '') + ('' if allow_missing or miss == 0 else f' {miss} ô thiếu')


def validate_outputs(clean, monthly, row_lineage, cleaning_log, quality_report, raw_record_ids=None):
    """Chạy toàn bộ kiểm tra. Trả về DataFrame: nhom, kiem_tra, ket_qua, chi_tiet."""
    res = []

    def add(group, name, ok, detail=''):
        res.append({'nhom': group, 'kiem_tra': name,
                    'ket_qua': 'ĐẠT' if ok else 'CHƯA ĐẠT', 'chi_tiet': detail})

    def safe(group, name, fn):
        try:
            ok, detail = fn()
        except Exception as e:  # thiếu cột, sai kiểu... -> báo lỗi thân thiện
            ok, detail = False, f'Lỗi khi kiểm tra: {type(e).__name__}: {e}'
        add(group, name, ok, detail)

    frames = {'reservations_clean': clean, 'monthly_summary': monthly, 'row_lineage': row_lineage,
              'cleaning_log': cleaning_log, 'quality_report': quality_report}
    for k, v in frames.items():
        add('0 Tồn tại', f'{k} đã được tạo', v is not None and len(v) > 0,
            '' if v is not None else 'Biến/tệp còn trống (None).')

    # ---------------- Bảng chính: khóa và nhãn ----------------
    if clean is not None:
        c = clean
        G = '1 Khóa & nhãn'
        safe(G, 'Đủ các cột bắt buộc',
             lambda: (not (miss := [x for x in CLEAN_REQUIRED if x not in c.columns]),
                      'Thiếu: ' + ', '.join(miss) if miss else f'{len(c.columns)} cột'))
        safe(G, 'reservation_id không thiếu, dạng AR + 6 chữ số',
             lambda: ((n := int((_blank(c['reservation_id']) | ~c['reservation_id'].astype('string').str.fullmatch(r'AR\d{6}').fillna(False)).sum())) == 0,
                      f'{n} ô thiếu hoặc sai dạng'))
        safe(G, 'reservation_id không trùng (1 dòng / đặt chỗ)',
             lambda: ((n := int(c['reservation_id'].duplicated().sum())) == 0, f'{n} reservation_id lặp'))
        safe(G, 'airline chỉ gồm Aurora Air, Horizon Wings (không thiếu)', lambda: _cat_ok(c['airline'], AIRLINES, False))
        for col, allowed in [('meal_option', MEALS), ('market_segment', SEGMENTS), ('sales_channel', CHANNELS),
                             ('fare_policy', FARE_POLICIES), ('traveler_type', TRAVELERS), ('booking_status', STATUSES),
                             ('booked_cabin_code', CABIN_CODES), ('assigned_cabin_code', CABIN_CODES)]:
            safe(G, f'{col} thuộc tập nhãn hợp lệ hoặc thiếu', lambda col=col, allowed=allowed: _cat_ok(c[col], allowed))
        safe(G, 'passenger_country là mã 2–3 chữ in hoa hoặc thiếu',
             lambda: ((n := int((~_blank(c['passenger_country']) & ~c['passenger_country'].astype('string').str.fullmatch(r'[A-Z]{2,3}').fillna(False)).sum())) == 0,
                      f'{n} ô sai dạng'))
        safe(G, 'is_cancelled, is_returning_customer chỉ là 0/1 hoặc thiếu',
             lambda: ((a := _int_ok(c['is_cancelled'], 0, 1))[0] and (b := _int_ok(c['is_returning_customer'], 0, 1))[0],
                      f'is_cancelled sai: {a[1]}; is_returning_customer sai: {b[1]}'))

        # ---------------- Số đo và ngày ----------------
        G = '2 Số & ngày'
        for col, lo, hi in [('booking_lead_days', LEAD_MIN, LEAD_MAX), ('trip_weekend_days', 0, WEEKEND_MAX),
                            ('trip_weekdays', 0, WEEK_MAX), ('adult_passengers', 0, PASSENGER_MAX), ('child_passengers', 0, PASSENGER_MAX),
                            ('infant_passengers', 0, PASSENGER_MAX), ('special_service_requests', 0, REQ_MAX)]:
            safe(G, f'{col} nguyên trong {lo}–{hi}', lambda col=col, lo=lo, hi=hi: ((r := _int_ok(c[col], lo, hi))[0], f'{r[1]} ô sai'))

        def _avg_ticket_fare():
            present = ~_blank(c['avg_ticket_fare'])
            v = _num(c['avg_ticket_fare'])
            bad = present & (v.isna() | (v < FARE_MIN) | (v > FARE_MAX))
            return int(bad.sum()) == 0, f'{int(bad.sum())} ô không phải số trong 0–5000'
        safe(G, 'avg_ticket_fare là số (USD) trong 0–5000 hoặc thiếu', _avg_ticket_fare)

        def _dates(col, lo, hi):
            s = c[col]
            present = ~_blank(s)
            fmt_bad = present & ~s.astype('string').str.strip().str.fullmatch(r'\d{4}-\d{2}-\d{2}').fillna(False)
            d = _date(s)
            rng_bad = present & (d.isna() | (d < lo) | (d > hi))
            n = int((fmt_bad | rng_bad).sum())
            return n == 0, f'{n} ô sai định dạng YYYY-MM-DD hoặc ngoài {lo:%Y-%m-%d}..{hi:%Y-%m-%d}'
        safe(G, 'departure_date dạng YYYY-MM-DD, trong 2024-07-01..2026-08-31',
             lambda: _dates('departure_date', DEPARTURE_MIN, DEPARTURE_MAX))
        safe(G, 'booking_status_date dạng YYYY-MM-DD, trong 2024-01-01..2026-09-15',
             lambda: _dates('booking_status_date', STATUS_MIN, STATUS_MAX))

        def _cons():
            st = c['booking_status'].astype('string')
            ic = _num(c['is_cancelled'])
            exp = st.map({'Flown': 0, 'Cancelled': 1, 'No-Show': 1})
            bad = exp.notna() & (ic.astype('Float64') != exp.astype('Float64')).fillna(True)
            return int(bad.sum()) == 0, f'{int(bad.sum())} dòng is_cancelled mâu thuẫn booking_status'
        safe(G, 'is_cancelled nhất quán với booking_status', _cons)

        # ---------------- Cột dẫn xuất ----------------
        G = '3 Cột dẫn xuất'

        def _ym():
            d = _date(c['departure_date'])
            bad = (d.dt.year.astype('Float64').fillna(-1) != _num(c['departure_year']).fillna(-1)) | \
                  (d.dt.month.astype('Float64').fillna(-1) != _num(c['departure_month']).fillna(-1))
            return int(bad.sum()) == 0, f'{int(bad.sum())} dòng không khớp departure_date'
        safe(G, 'departure_year, departure_month lấy từ departure_date', _ym)

        def _sum(target, parts):
            exp = sum(_num(c[p]) for p in parts)
            bad = exp.fillna(-999) != _num(c[target]).fillna(-999)
            return int(bad.sum()) == 0, f'{int(bad.sum())} dòng sai (thiếu một thành phần → kết quả thiếu)'
        safe(G, 'total_trip_days = trip_weekend_days + trip_weekdays', lambda: _sum('total_trip_days', ['trip_weekend_days', 'trip_weekdays']))
        safe(G, 'total_passengers = adult_passengers + child_passengers + infant_passengers', lambda: _sum('total_passengers', ['adult_passengers', 'child_passengers', 'infant_passengers']))

        def _lead():
            lt = _num(c['booking_lead_days'])
            exp = pd.cut(lt, bins=[-0.5, 7.5, 30.5, 90.5, 180.5, float('inf')], labels=LEAD_GROUPS).astype('string')
            got = c['lead_time_group'].astype('string').where(~_blank(c['lead_time_group']))
            bad = exp.fillna('∅') != got.fillna('∅')
            return int(bad.sum()) == 0, f'{int(bad.sum())} dòng sai nhóm (nhãn: {", ".join(LEAD_GROUPS)})'
        safe(G, 'lead_time_group đúng 5 nhóm quy ước', _lead)

        def _room():
            r, a = c['booked_cabin_code'], c['assigned_cabin_code']
            exp = (~_blank(r) & ~_blank(a) & (r.astype('string') != a.astype('string'))).fillna(False)
            got = _bool(c['cabin_changed_flag'])
            bad = got.isna() | (got.astype('boolean') != exp.astype('boolean'))
            return int(bad.sum()) == 0, f'{int(bad.sum())} dòng sai hoặc thiếu cờ (chỉ dùng True/False)'
        safe(G, 'cabin_changed_flag đúng quy tắc', _room)

        def _rev():
            fare, pax, ic = _num(c['avg_ticket_fare']), _num(c['total_passengers']), _num(c['is_cancelled'])
            exp = (fare * pax).where(ic == 0).round(2)
            got = _num(c['booking_value_est']).round(2)
            bad = ~((exp.isna() & got.isna()) | ((exp - got).abs() <= 0.011))
            return int(bad.sum()) == 0, f'{int(bad.sum())} dòng sai (chỉ tính khi is_cancelled = 0 và fare, total_passengers hợp lệ)'
        safe(G, 'booking_value_est = avg_ticket_fare × total_passengers (chỉ reservation không hủy)', _rev)

    # ---------------- Bảng tổng hợp theo tháng ----------------
    if monthly is not None:
        m = monthly
        G = '4 Bảng tháng'
        safe(G, 'monthly_summary đúng 7 cột',
             lambda: (list(m.columns) == SUMMARY_COLUMNS, f'Cột hiện có: {list(m.columns)}'))
        safe(G, 'Không trùng khóa (airline, departure_year, departure_month)',
             lambda: ((n := int(m.duplicated(['airline', 'departure_year', 'departure_month']).sum())) == 0, f'{n} khóa lặp'))
        if clean is not None:
            def _recompute():
                c = clean.copy()
                c['_y'], c['_m'] = _num(c['departure_year']), _num(c['departure_month'])
                c['_ic'], c['_pax'] = _num(c['is_cancelled']), _num(c['total_passengers'])
                c = c[c['_y'].notna()]
                g = c.groupby([c['airline'].astype(str), '_y', '_m'])
                exp = pd.DataFrame({'n_reservations': g.size(), 'n_cancelled': g['_ic'].apply(lambda s: (s == 1).sum()),
                                    'known': g['_ic'].apply(lambda s: s.notna().sum()),
                                    'passengers_flown': g.apply(lambda x: x.loc[x['_ic'] == 0, '_pax'].sum())}).reset_index()
                exp.columns = ['airline', 'departure_year', 'departure_month', 'n_reservations', 'n_cancelled', 'known', 'passengers_flown']
                exp['cancel_rate_pct'] = (exp['n_cancelled'] / exp['known'] * 100).round(2)
                got = m.copy()
                for col in ['departure_year', 'departure_month', 'n_reservations', 'n_cancelled', 'cancel_rate_pct', 'passengers_flown']:
                    got[col] = _num(got[col])
                got['airline'] = got['airline'].astype(str)
                j = exp.merge(got, on=['airline', 'departure_year', 'departure_month'], how='outer', suffixes=('_e', '_g'), indicator=True)
                miss = int((j['_merge'] != 'both').sum())
                b = j[j['_merge'] == 'both']
                bad = int(((b['n_reservations_e'] != b['n_reservations_g']) | (b['n_cancelled_e'] != b['n_cancelled_g']) |
                           ~(((b['cancel_rate_pct_e'] - b['cancel_rate_pct_g']).abs() <= 0.011) |
                             (b['cancel_rate_pct_e'].isna() & b['cancel_rate_pct_g'].isna())) |
                           ((b['passengers_flown_e'] - b['passengers_flown_g']).abs() > 0.5)).sum())
                return miss == 0 and bad == 0, f'{miss} tháng thiếu/thừa; {bad} tháng lệch số liệu so với bảng chính'
            safe(G, 'Số liệu khớp khi tính lại từ reservations_clean', _recompute)

    # ---------------- Truy vết ----------------
    if row_lineage is not None:
        rl = row_lineage
        G = '5 Truy vết'
        safe(G, 'row_lineage có cột record_id, reservation_id, status',
             lambda: (all(x in rl.columns for x in LINEAGE_COLUMNS), f'Cột hiện có: {list(rl.columns)}'))
        safe(G, 'Mỗi record_id xuất hiện đúng 1 lần',
             lambda: ((n := int(rl['record_id'].duplicated().sum())) == 0, f'{n} record_id lặp'))
        if raw_record_ids is not None:
            safe(G, f'Phủ đủ {N_RAW_ROWS} record_id gốc',
                 lambda: ((mm := len(set(raw_record_ids) - set(rl['record_id']))) == 0 and
                          (x := len(set(rl['record_id']) - set(raw_record_ids))) == 0,
                          f'Thiếu {mm} record_id gốc; thừa {x} record_id lạ'))
        safe(G, 'status thuộc kept / merged / dropped',
             lambda: (not (bad := sorted(set(rl['status'].astype(str)) - set(LINEAGE_STATUS))),
                      'Giá trị lạ: ' + ', '.join(bad[:5]) if bad else ''))
        if clean is not None:
            safe(G, 'Mỗi reservation_id trong bảng chính có đúng 1 dòng kept',
                 lambda: ((k := rl.loc[rl['status'] == 'kept', 'reservation_id']).is_unique and
                          set(k) == set(clean['reservation_id']),
                          f'{int(k.duplicated().sum())} reservation_id có >1 kept; '
                          f'{len(set(clean["reservation_id"]) - set(k))} reservation_id không có kept'))
            safe(G, 'Dòng kept/merged trỏ tới reservation_id có trong bảng chính',
                 lambda: ((n := int((rl['status'].isin(['kept', 'merged']) &
                                     ~rl['reservation_id'].isin(clean['reservation_id'])).sum())) == 0, f'{n} dòng trỏ sai'))

    # ---------------- Nhật ký & chất lượng ----------------
    G = '6 Nhật ký'
    if cleaning_log is not None:
        lg = cleaning_log
        safe(G, 'cleaning_log đúng 11 cột theo mẫu',
             lambda: (list(lg.columns) == LOG_COLUMNS, f'Cột hiện có: {list(lg.columns)}'))
        safe(G, 'Có ít nhất 10 quy tắc được ghi', lambda: (len(lg) >= 10, f'{len(lg)} dòng'))
        safe(G, 'affected_rows, changed_cells, removed_rows là số nguyên ≥ 0',
             lambda: (all(_int_ok(lg[x], 0, 10**7)[0] and (~_blank(lg[x])).all()
                          for x in ['affected_rows', 'changed_cells', 'removed_rows']), ''))
        safe(G, 'Mỗi quy tắc có lý do (reason) và kiểm tra sau (check_after)',
             lambda: ((n := int((_blank(lg['reason']) | _blank(lg['check_after'])).sum())) == 0, f'{n} dòng thiếu'))
    if quality_report is not None:
        q = quality_report
        safe(G, 'quality_report có các cột bắt buộc',
             lambda: (not (mm := [x for x in QUALITY_COLUMNS if x not in q.columns]), 'Thiếu: ' + ', '.join(mm) if mm else ''))
        safe(G, 'quality_report có cả before và after',
             lambda: ({'before', 'after'} <= set(q['stage'].astype(str)), f'stage: {sorted(set(q["stage"].astype(str)))}'))

    return pd.DataFrame(res)


def print_report(report):
    n_ok = int((report['ket_qua'] == 'ĐẠT').sum())
    for _, r in report.iterrows():
        mark = '✅' if r['ket_qua'] == 'ĐẠT' else '❌'
        extra = f'  — {r["chi_tiet"]}' if r['chi_tiet'] and r['ket_qua'] != 'ĐẠT' else ''
        print(f'{mark} [{r["nhom"]}] {r["kiem_tra"]}{extra}')
    print(f'\nTỔNG KẾT: {n_ok}/{len(report)} kiểm tra đạt.')
    return n_ok == len(report)
# =============================================================================================


# ===================== CHƯƠNG TRÌNH KIỂM TRA THƯ MỤC BÀI NỘP =====================
import json
import sys
from pathlib import Path


def _read(p):
    return pd.read_csv(p, dtype=str, keep_default_na=False, encoding='utf-8-sig') if p.exists() else None


def _find_outputs(root):
    for cand in [root / 'outputs', root]:
        if (cand / 'reservations_clean.csv').exists() or (cand / 'figures').exists():
            return cand
    return root / 'outputs'


def _find_raw(root):
    for cand in [root / 'data' / 'airline_bookings_dirty.csv', root / 'airline_bookings_dirty.csv',
                 root.parent / 'data' / 'airline_bookings_dirty.csv', root.parent / 'airline_bookings_dirty.csv']:
        if cand.exists():
            return cand
    return None


def check_package(root):
    rows = []

    def add(group, name, ok, detail='', warn=False):
        state = 'ĐẠT' if ok else ('CẢNH BÁO' if warn else 'CHƯA ĐẠT')
        rows.append({'nhom': group, 'kiem_tra': name, 'ket_qua': state, 'chi_tiet': detail})

    out = _find_outputs(root)
    print(f'Thư mục bài nộp : {root.resolve()}')
    print(f'Thư mục outputs : {out.resolve()}\n')

    # Hồ sơ nộp
    nb = root / 'airline_analysis.ipynb'
    add('7 Hồ sơ nộp', 'Có airline_analysis.ipynb', nb.exists(), 'Đổi tên notebook khung thành airline_analysis.ipynb')
    add('7 Hồ sơ nộp', 'Có README.md', (root / 'README.md').exists(), 'Dùng templates/README_nop_bai_template.md')
    rp = [p for p in [root / 'Bao_cao_Hang_khong.pdf', root / 'Bao_cao_Hang_khong.docx'] if p.exists()]
    add('7 Hồ sơ nộp', 'Có Bao_cao_Hang_khong.pdf hoặc .docx', bool(rp), 'Đặt báo cáo ở thư mục gốc bài nộp')
    if nb.exists():
        try:
            cells = [c for c in json.loads(nb.read_text(encoding='utf-8'))['cells'] if c['cell_type'] == 'code']
            todo = sum(''.join(c['source']).count('TODO') for c in cells)
            add('7 Hồ sơ nộp', 'Notebook không còn TODO', todo == 0, f'Còn {todo} chỗ TODO', warn=True)
            counts = [c.get('execution_count') for c in cells if ''.join(c['source']).strip()]
            seq = counts == list(range(1, len(counts) + 1))
            add('7 Hồ sơ nộp', 'Notebook đã chạy lại từ đầu, đúng thứ tự (1, 2, 3, ...)', seq,
                'Chọn Restart & Run all rồi lưu lại', warn=True)
        except Exception as e:
            add('7 Hồ sơ nộp', 'Đọc được notebook', False, str(e))

    # Tệp đầu ra
    for f in CORE_FILES:
        add('8 Tệp đầu ra', f'outputs/{f}', (out / f).exists(), 'Chưa xuất tệp')
    for f in TABLE_FILES:
        add('8 Tệp đầu ra', f'outputs/tables/{f}', (out / 'tables' / f).exists(), 'Chưa lưu bảng nguồn')
    for f in FIGURE_FILES:
        p = out / 'figures' / f
        add('8 Tệp đầu ra', f'outputs/figures/{f}', p.exists() and p.stat().st_size > 5000,
            'Thiếu hình hoặc tệp quá nhỏ (có thể là hình trống)')

    raw_path = _find_raw(root)
    raw_ids = None
    if raw_path is not None:
        raw_ids = pd.read_csv(raw_path, dtype=str, keep_default_na=False, encoding='utf-8-sig')['record_id']
    else:
        add('5 Truy vết', 'Tìm thấy airline_bookings_dirty.csv để đối chiếu record_id', False,
            'Đặt dữ liệu gốc tại data/airline_bookings_dirty.csv', warn=True)

    rep = validate_outputs(_read(out / 'reservations_clean.csv'),
                           _read(out / 'monthly_summary.csv'),
                           _read(out / 'row_lineage.csv'), _read(out / 'cleaning_log.csv'),
                           _read(out / 'quality_report.csv'), raw_ids)
    allrep = pd.concat([rep, pd.DataFrame(rows)], ignore_index=True).sort_values('nhom', kind='stable')
    return allrep


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    rep = check_package(root)
    icons = {'ĐẠT': '✅', 'CHƯA ĐẠT': '❌', 'CẢNH BÁO': '⚠️ '}
    for _, r in rep.iterrows():
        extra = f'  — {r["chi_tiet"]}' if r['chi_tiet'] and r['ket_qua'] != 'ĐẠT' else ''
        print(f'{icons[r["ket_qua"]]} [{r["nhom"]}] {r["kiem_tra"]}{extra}')
    n = rep['ket_qua'].value_counts()
    print('\n' + '=' * 70)
    print(f'TỔNG KẾT: {n.get("ĐẠT", 0)} đạt · {n.get("CHƯA ĐẠT", 0)} chưa đạt · {n.get("CẢNH BÁO", 0)} cảnh báo')
    print('Lưu ý: đạt hết kiểm tra cấu trúc KHÔNG có nghĩa là phân tích đúng; điểm vẫn chấm theo thang điểm.')
    sys.exit(0 if n.get('CHƯA ĐẠT', 0) == 0 else 1)


if __name__ == '__main__':
    main()
