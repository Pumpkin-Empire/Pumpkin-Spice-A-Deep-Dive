from PumpkinEmpire import *
import unittest
import mock
from datetime import datetime, date


class test_pumpkin_empire(unittest.TestCase):
    def test_get_date_string(self):
        test_date = date(2022, 8, 22)
        test_time = datetime(2022, 8, 22, 23, 55, 59)
        expected = "2022-08-22T23:55:59Z"
        self.assertEqual(get_date_string(test_date, test_time), expected)


if __name__ == '__main__':
    unittest.main()

# class TestCase(unittest.TestCase):
#
#     @mock.patch('yourfile.datetime')
#     def test_dt(self, mock_dt):
#         mock_dt.utcnow = mock.Mock(return_value=datetime(1901, 12, 21))
#         r = get_report_month_key()
#         self.assertEqual('190112', r)