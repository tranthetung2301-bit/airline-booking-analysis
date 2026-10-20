"""Unit test cho các hàm làm sạch và tạo cột dẫn xuất của Thành viên 2."""

import unittest
import numpy as np
import pandas as pd
from src.feature_engineering import (
    clean_int_col,
    clean_fare,
    clean_b6_numeric_columns,
    clean_b7_country_codes,
    create_derived_columns,
    create_monthly_summary,
)


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
