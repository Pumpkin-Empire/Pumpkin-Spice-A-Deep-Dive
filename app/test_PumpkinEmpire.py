from PumpkinEmpire import *
import unittest
from mock import patch
from datetime import datetime, date
from freezegun import freeze_time
from app import config_test, config_test_empty
import requests


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

    def test_create_headers(self):
        test_bearer = 'asbn3920hasn358a'
        expected = {'Authorization': f'Bearer {test_bearer}'}
        actual = create_headers(test_bearer)
        self.assertEqual(expected, actual)

    @freeze_time('2022-09-13 15:46:43')
    def test_create_url(self):
        test_search = "pumpkin spice"
        expected = ('https://api.twitter.com/2/tweets/search/recent?',
                    {'query': 'pumpkin spice', 'start_time': '2022-09-12T15:46:43Z',
                     'max_results': 100, 'tweet.fields': 'entities,geo,public_metrics',
                     'expansions': 'attachments.media_keys,author_id', 'place.fields':
                         'geo', 'user.fields': 'created_at,location,public_metrics', 'next_token': ''})
        actual = create_url(test_search)
        self.assertEqual(expected, actual)

    @freeze_time('2022-09-13 15:46:43')
    def test_create_url_max_results_changed(self):
        test_search = "pumpkin spice"
        expected = ('https://api.twitter.com/2/tweets/search/recent?',
                    {'query': 'pumpkin spice', 'start_time': '2022-09-12T15:46:43Z',
                     'max_results': 80, 'tweet.fields': 'entities,geo,public_metrics',
                     'expansions': 'attachments.media_keys,author_id', 'place.fields':
                         'geo', 'user.fields': 'created_at,location,public_metrics', 'next_token': ''})
        actual = create_url(test_search, 80)
        self.assertEqual(expected, actual)

    @freeze_time('2022-09-13 15:46:43')
    def test_create_url_max_results_less_than_ten(self):
        test_search = "pumpkin spice"
        expected = ('https://api.twitter.com/2/tweets/search/recent?',
                    {'query': 'pumpkin spice', 'start_time': '2022-09-12T15:46:43Z',
                     'max_results': 10, 'tweet.fields': 'entities,geo,public_metrics',
                     'expansions': 'attachments.media_keys,author_id', 'place.fields':
                         'geo', 'user.fields': 'created_at,location,public_metrics', 'next_token': ''})
        actual = create_url(test_search, 5)
        self.assertEqual(expected, actual)

    def test_response(self):
        # Send a request to the API server and store the response.
        response = requests.get('http://jsonplaceholder.typicode.com/todos')
        # Confirm that the request-response cycle completed successfully.
        self.assertTrue(response.ok)

    def test_connect_to_api(self):
        test_url = "http://jsonplaceholder.typicode.com/todos"
        url = create_url("pumpkin spice")
        test_bearer = 's3dfj80asv0sv3as3209nv9asDk'
        headers = create_headers(test_bearer)
        response = connect_to_api(test_url, headers, url[1])
        response_is_object = isinstance(response, list)
        self.assertTrue(response_is_object)

    def test_append_dict_values(self):
        test_dict1 = {'meta': {'next_token': 'asv9v83nv80v289', 'results': 100},
                      'includes': {'users': [{'user': 'user1', 'tweet_text': 'tweet1'},
                                             {'user': 'user2', 'tweet_text': 'tweet2'}]}, 'other': [1, 2, 3, 4]}
        test_dict2 = {'meta': {'next_token': 'NAv9v83nv80v290', 'results': 80},
                      'includes': {'users': [{'user': 'user3', 'tweet_text': 'tweet3'},
                                             {'user': 'user4', 'tweet_text': 'tweet4'}]}, 'other': [5, 6, 7, 8]}
        expected = {'meta': {'next_token': 'NAv9v83nv80v290', 'results': 80},
                    'includes': {'users': [{'user': 'user1', 'tweet_text': 'tweet1'},
                                           {'user': 'user2', 'tweet_text': 'tweet2'},
                                           {'user': 'user3', 'tweet_text': 'tweet3'},
                                           {'user': 'user4', 'tweet_text': 'tweet4'}]},
                    'other': [1, 2, 3, 4, 5, 6, 7, 8]}
        actual = append_dict_values(test_dict1, test_dict2)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
