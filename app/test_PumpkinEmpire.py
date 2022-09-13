from PumpkinEmpire import *
import unittest
from mock import patch
from datetime import datetime, date
from freezegun import freeze_time
from app import config_test, config_test_empty


class TestPumpkinEmpire(unittest.TestCase):
    def test_get_date_string(self):
        test_date = date(2022, 8, 22)
        test_time = datetime(2022, 8, 22, 23, 55, 59)
        expected = "2022-08-22T23:55:59Z"
        self.assertEqual(get_date_string(test_date, test_time), expected)

    @freeze_time("2022-08-22 14:03:11")
    def test_get_current_date_and_time(self):
        expected = "2022-08-22 14:03:11"
        actual = get_current_date_and_time()
        self.assertEqual(expected, actual)

    def test_auth(self):
        expected = "asbn3920hasn358a"
        with patch('PumpkinEmpire.config', new=config_test):
            actual = auth()
        self.assertEqual(expected, actual)

    def test_auth_no_file(self):
        with patch('PumpkinEmpire.config', new=config_test_empty):
            with self.assertRaises(AttributeError):
                auth()


if __name__ == '__main__':
    unittest.main()

# class TestCase(unittest.TestCase):
#
#     @mock.patch('yourfile.datetime')
#     def test_dt(self, mock_dt):
#         mock_dt.utcnow = mock.Mock(return_value=datetime(1901, 12, 21))
#         r = get_report_month_key()
#         self.assertEqual('190112', r)
