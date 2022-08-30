# import json
import requests
import config
# import pandas as pd
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

hostname = config.hostname
dbname = config.dbname
uname = config.uname
pwd = config.pwd
port = config.port

engine = create_engine("postgresql://{user}:{pw}@{host}:{port}/{db}".format(host=hostname, port=port, db=dbname, user=uname, pw=pwd), pool_size=20, max_overflow=0)


def get_date_string() -> str:
    """Returns today's date and time from 24hrs ago, to use
    when searching for tweets from previous day. Formatted for Twitter API v2
    query:   '2022-08-23T00:01:00Z' """
    yesterday = date.today() - timedelta(days = 1)
    # today = datetime.today().strftime('%Y-%m-%d')
    now = datetime.now()
    time_and_formatting  = 'T' + now.strftime("%H:%M:%S") + 'Z'
    return str(yesterday) + time_and_formatting





def auth():
    return config.bearer_token


def create_headers(bearer_token) -> dict:
    header = {"Authorization": "Bearer {}".format(bearer_token)}
    return header


def create_url(max_results=10) -> tuple:
    search_url = "https://api.twitter.com/2/tweets/search/recent?"
    query_params = {'query': "pumpkin spice",
                    'start_time': get_date_string(),
                    'max_results': max_results,
                    'tweet.fields': 'entities,geo,public_metrics',
                    'expansions': 'attachments.media_keys,author_id',
                    'place.fields': 'geo',
                    'user.fields': 'created_at,location,public_metrics',
                    'next_token': ''}
    return search_url, query_params


def connect_to_api(url, headers, params, next_token=None):
    params['next_token'] = next_token
    response = requests.request("GET", url, headers=headers, params=params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def append_dict_values(base_dict: dict, append_dict: dict) -> dict:
    """For appending multiple response objects in to one.
    Input dict values are lists, this appends the lists together without replacing
    original values. 'meta' key does not get appended."""
    base_dict_keys = list(base_dict.keys())
    for key in base_dict_keys:
        if key == 'meta':
            base_dict[key] = append_dict[key]
        elif key == 'includes':
            base_dict[key]['users'].extend(append_dict[key]['users'])
        else:
            base_dict[key].extend(append_dict[key])
    return base_dict


def loop_connect() -> dict:

    # May be able to make these global, depending on the automation used later.
    max_requests_per_call = 10
    max_requests_per_window = 20
    url = create_url(max_requests_per_call)

    # Get Initial Response
    json_response = connect_to_api(url[0], headers, url[1])

    # Update how many items we can request
    requests_per_call = max_requests_per_window - max_requests_per_call
    while requests_per_call > 0:
        url = create_url(requests_per_call)
        temp_response = connect_to_api(url[0], headers, url[1], json_response['meta']['next_token'])
        json_response = append_dict_values(json_response, temp_response)
        requests_per_call = requests_per_call - max_requests_per_call
    return json_response


def add_tweets_to_db(response: dict):
    for twit in response['data']:
        Session = sessionmaker(bind=engine)
        session = Session()
        tweet = session.query(Tweet).filter_by(tweet_id=twit['id']).first()
        if not tweet:
            tweet_id = twit['id']
            author_id = twit['author_id']
            tweet_text = twit['text']
            like_count = twit['public_metrics']['like_count']
            quote_count = twit['public_metrics']['quote_count']
            reply_count = twit['public_metrics']['reply_count']
            retweet_count = twit['public_metrics']['retweet_count']
            place = ''
            try:
                if type(twit['entities']) == dict:
                    try:
                        if type(twit['entities']['annotations']) == dict:
                            place = twit.get('entities', {}).get('annotations', {}).get('normalized_text')
                    except KeyError:
                        place = None
            except KeyError:
                place = None
            date = datetime.today().strftime('%Y-%m-%d')
            tweet = Tweet(tweet_id, author_id, tweet_text, like_count, quote_count,
                          reply_count, retweet_count, place, date)

            session.add(tweet)
            session.commit()
    print("Successfully wrote to database.")


def add_users_to_db(response: dict):
    for acct in response['includes']['users']: ##maybe could make this ['includes']['users'] then update vars below?
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter_by(user_id=acct['id']).first()
        if not user:
            user_id = acct['id']
            username = acct['username']
            try:
                location = acct['location']
            except KeyError:
                location = None
            follower_count = acct['public_metrics']['followers_count']
            following_count = acct['public_metrics']['following_count']
            tweet_count = acct['public_metrics']['tweet_count']
            acct_date = acct['created_at']
            user = User(user_id, username, location, follower_count, following_count, tweet_count, acct_date)

            session.add(user)
            session.commit()
    print("Successfully wrote to database")



# loop_connect()
# 180 tweets per 15 minutes.
# bearer_token = config.bearer_token
# headers = create_headers(bearer_token)
# url = create_url()
# json_response = connect_to_api(url[0], headers, url[1])
# print(type(json_response))
# print(json.dumps(json_response, indent=4, sort_keys=True))

# dict1 = {'data': [{'user': 'roy', 'tweet': 'hey there friendo'}, {'user': 'kendra', 'tweet': \
#   'nick get back to work'}], 'meta': [1, 2]}
# dict2 = {'data': [{'user': 'bevin', 'tweet': 'not your friendo buddyo'}, {'user': 'kris', \
#   'tweet': 'nick is MVP'}], 'meta': [3, 4]}
# print(append_dict_values(dict1, dict2))

# print(loop_connect())
# print(json.dumps(loop_connect(), indent=4, sort_keys=True))

if __name__ == "__main__":
    bearer_token = config.bearer_token
    headers = create_headers(bearer_token)
    url = create_url()
    response = loop_connect()
    add_tweets_to_db(response)
    add_users_to_db(response)
