"""Unit test cho các hàm làm sạch dữ liệu (TV1: cleaning.py & TV2: feature_engineering.py)."""

import unittest
import numpy as np
import pandas as pd
from src.cleaning import (
    clean_key,
    _to_binary_int,
    clean_b1_duplicates,
    clean_b2_misplaced_dates,
    clean_b3_invalid_symbols,
    clean_b4_categorical_labels,
    clean_b5_date_formats,
    run_phase_b,
)
from src.feature_engineering import (
    clean_int_col,
    clean_fare,
    clean_b6_numeric_columns,
    clean_b7_country_codes,
    create_derived_columns,
    create_monthly_summary,
)


class TestCleaningTV1(unittest.TestCase):

    def test_clean_key(self):
        self.assertEqual(clean_key(" Aurora Air "), "auroraair")
        self.assertEqual(clean_key("Non-Refundable"), "nonrefundable")
        self.assertTrue(pd.isna(clean_key(None)))

    def test_to_binary_int(self):
        s = pd.Series(['yes', 'no', '1', '0', 'True', 'False', 'unknown', None])
        res = _to_binary_int(s)
        self.assertEqual(res[0], 1)
        self.assertEqual(res[1], 0)
        self.assertEqual(res[2], 1)
        self.assertEqual(res[3], 0)
        self.assertEqual(res[4], 1)
        self.assertEqual(res[5], 0)
        self.assertTrue(pd.isna(res[6]))
        self.assertTrue(pd.isna(res[7]))

    def test_clean_b1_duplicates(self):
        df = pd.DataFrame({
            'record_id': ['REC001', 'REC002', 'REC003'],
            'reservation_id': [' ar001 ', 'ar001', 'AR002'],
            'airline': ['Aurora Air', 'Aurora Air', 'Horizon Wings'],
        })
        res, dropped = clean_b1_duplicates(df)
        self.assertEqual(len(res), 2)
        self.assertEqual(dropped, ['REC002'])
        self.assertEqual(res['reservation_id'].iloc[0], 'AR001')

    def test_clean_b2_misplaced_dates(self):
        df = pd.DataFrame({
            'booking_status': ['2025-06-15', 'Flown'],
            'booking_status_date': ['', '2025-06-10']
        })
        res = clean_b2_misplaced_dates(df)
        self.assertEqual(res['booking_status_date'].iloc[0], '2025-06-15')
        self.assertEqual(res['booking_status'].iloc[0], '')
        self.assertEqual(res['booking_status'].iloc[1], 'Flown')

    def test_clean_b3_invalid_symbols(self):
        df = pd.DataFrame({
            'record_id': ['REC001'],
            'meal_option': ['?'],
            'market_segment': ['Undefined'],
            'sales_channel': ['NULL']
        })
        res = clean_b3_invalid_symbols(df)
        self.assertTrue(pd.isna(res['meal_option'].iloc[0]))
        self.assertTrue(pd.isna(res['market_segment'].iloc[0]))
        self.assertTrue(pd.isna(res['sales_channel'].iloc[0]))

    def test_clean_b4_categorical_labels(self):
        df = pd.DataFrame({
            'record_id': ['REC001', 'REC002'],
            'airline': ['aurora air', 'horizon'],
            'meal_option': ['standard', 'undefined'],
            'market_segment': ['direct', 'corporate'],
            'sales_channel': ['website', 'mobile app'],
            'fare_policy': ['flexible', 'nonrefundable'],
            'traveler_type': ['individual', 'group'],
            'booking_status': ['flown', 'cancelled'],
            'booked_cabin_code': ['e1', 'x9'],
            'assigned_cabin_code': ['E1', 'E2'],
            'is_cancelled': ['1', '0'],
            'is_returning_customer': ['no', 'yes']
        })
        res = clean_b4_categorical_labels(df)
        self.assertEqual(res['airline'].iloc[0], 'Aurora Air')
        self.assertEqual(res['airline'].iloc[1], 'Horizon Wings')
        self.assertEqual(res['meal_option'].iloc[1], 'No Meal')
        self.assertEqual(res['booked_cabin_code'].iloc[0], 'E1')
        self.assertTrue(pd.isna(res['booked_cabin_code'].iloc[1]))
        # is_cancelled must be synced with booking_status: Flown -> 0, Cancelled -> 1
        self.assertEqual(res['is_cancelled'].iloc[0], 0)
        self.assertEqual(res['is_cancelled'].iloc[1], 1)

    def test_clean_b5_date_formats(self):
        df = pd.DataFrame({
            'departure_date': ['2025-06-15', '23/08/2025', 'October 6, 2025', '15 Nov 2024'],
            'booking_status_date': ['2025-06-10', '2025-08-20', '2025-10-01', '2024-11-01']
        })
        res = clean_b5_date_formats(df)
        self.assertEqual(res['departure_date'].iloc[0], pd.Timestamp('2025-06-15'))
        self.assertEqual(res['departure_date'].iloc[1], pd.Timestamp('2025-08-23'))
        self.assertEqual(res['departure_date'].iloc[2], pd.Timestamp('2025-10-06'))
        self.assertEqual(res['departure_date'].iloc[3], pd.Timestamp('2024-11-15'))


class TestFeatureEngineering(unittest.TestCase):

    def test_clean_int_col(self):
        s = pd.Series(['10', ' 20 ', '2 days', '0.0', '-5', '999', 'N/A', None])
        res = clean_int_col(s, 0, 50)
        self.assertEqual(res[0], 10)
        self.assertEqual(res[1], 20)
        self.assertEqual(res[2], 2)
        self.assertEqual(res[3], 0)
        self.assertTrue(pd.isna(res[4]))  # -5 ngoài khoảng
        self.assertTrue(pd.isna(res[5]))  # 999 ngoài khoảng
        self.assertTrue(pd.isna(res[6]))
        self.assertTrue(pd.isna(res[7]))

    def test_clean_fare(self):
        s = pd.Series(['$125.50', 'USD 214.02', '115,64', '0.0', '0', '-25', '9999', 'N/A'])
        res = clean_fare(s, 0, 5000)
        self.assertEqual(res[0], 125.50)
        self.assertEqual(res[1], 214.02)
        self.assertEqual(res[2], 115.64)
        self.assertEqual(res[3], 0.0)  # vé 0 đồng hợp lệ
        self.assertEqual(res[4], 0.0)
        self.assertTrue(pd.isna(res[5]))  # -25
        self.assertTrue(pd.isna(res[6]))  # 9999
        self.assertTrue(pd.isna(res[7]))

    def test_clean_b7_country_codes(self):
        df = pd.DataFrame({'passenger_country': ['Vietnam', 'vnm', 'China', 'cn', 'USA', '12A', '??', None]})
        res = clean_b7_country_codes(df)['passenger_country']
        self.assertEqual(res[0], 'VNM')
        self.assertEqual(res[1], 'VNM')
        self.assertEqual(res[2], 'CHN')
        self.assertEqual(res[3], 'CHN')
        self.assertEqual(res[4], 'USA')
        self.assertTrue(pd.isna(res[5]))  # 12A
        self.assertTrue(pd.isna(res[6]))  # ??
        self.assertTrue(pd.isna(res[7]))

    def test_create_derived_columns(self):
        df = pd.DataFrame({
            'reservation_id': ['AR000001'],
            'departure_date': ['2025-06-15'],
            'booking_status_date': ['2025-06-10'],
            'booking_lead_days': [10],
            'trip_weekend_days': [2],
            'trip_weekdays': [5],
            'adult_passengers': [2],
            'child_passengers': [1],
            'infant_passengers': [0],
            'booked_cabin_code': ['E1'],
            'assigned_cabin_code': ['E2'],
            'avg_ticket_fare': [100.0],
            'is_cancelled': [0]
        })
        res = create_derived_columns(df)
        self.assertEqual(res['departure_year'].iloc[0], 2025)
        self.assertEqual(res['departure_month'].iloc[0], 6)
        self.assertEqual(res['total_trip_days'].iloc[0], 7)
        self.assertEqual(res['total_passengers'].iloc[0], 3)
        self.assertEqual(res['lead_time_group'].iloc[0], '8-30')
        self.assertTrue(res['cabin_changed_flag'].iloc[0])
        self.assertEqual(res['booking_value_est'].iloc[0], 300.0)


if __name__ == '__main__':
    unittest.main()
