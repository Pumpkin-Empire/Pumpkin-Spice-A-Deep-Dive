import json

import requests

import config
import pandas as pd
from rauth import OAuth1Service
from datetime import datetime

twitter = OAuth1Service(
    name='twitter',
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,

)


def get_date_string() -> str:
    """Returns today's date and time at 12:01AM, formatted for Twitter API v2
    query:   '2022-08-23T00:01:00Z' """
    today = datetime.today().strftime('%Y-%m-%d')
    time_and_formatting = 'T00:01:00Z'
    return today + time_and_formatting


def auth():
    return config.bearer_token


def create_headers(bearer_token) -> str:
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url(max_results=100) -> tuple:
    search_url = "https://api.twitter.com/2/tweets/search/recent?"
    query_params = {'query': "pumpkin spice",
                    'start_time': get_date_string(),
                    'max_results': max_results,
                    'tweet.fields': 'entities,geo,public_metrics',
                    'expansions': 'attachments.media_keys,author_id',
                    'place.fields': 'geo',
                    'user.fields': 'created_at,location,public_metrics',
                    'next_token': {}}
    return search_url, query_params


def connect_to_api(url, headers, params, next_token = None):
    params['next_token'] = next_token
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


bearer_token = config.bearer_token
headers = create_headers(bearer_token)
url = create_url()
json_response = connect_to_api(url[0], headers, url[1])
print(json.dumps(json_response, indent=4, sort_keys=True))