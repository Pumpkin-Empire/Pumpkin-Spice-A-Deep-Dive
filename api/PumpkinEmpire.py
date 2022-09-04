import sys
import psycopg2
import requests
import time
import sqlalchemy.exc
import db_con
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
import config


def get_date_string() -> str:
    """Returns today's date and time from 24hrs ago, to use
    when searching for tweets from previous day. Formatted for Twitter API v2
    query:   '2022-08-23T00:01:00Z' """
    yesterday = date.today() - timedelta(days=1)
    current_time = datetime.now()
    time_and_formatting = 'T' + current_time.strftime("%H:%M:%S") + 'Z'
    return str(yesterday) + time_and_formatting


def print_current_date_and_time():
    """"Prints the current date & time"""
    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))


def auth():
    """Get bearer token from config.py"""
    return config.bearer_token


def create_headers(bearer_token) -> dict:
    """Create headers for Twitter API request."""
    header = {"Authorization": "Bearer {}".format(bearer_token)}
    return header


def create_url(max_results=100) -> tuple:
    """Create full URL for Twitter API request."""
    search_url = "https://api.twitter.com/2/tweets/search/recent?"
    query_params = {'query': search,
                    'start_time': get_date_string(),
                    'max_results': max_results,
                    'tweet.fields': 'entities,geo,public_metrics',
                    'expansions': 'attachments.media_keys,author_id',
                    'place.fields': 'geo',
                    'user.fields': 'created_at,location,public_metrics',
                    'next_token': ''}
    return search_url, query_params


def connect_to_api(url, headers, params, next_token=None):
    """Create API connection"""
    params['next_token'] = next_token
    twitter_response = requests.request("GET", url, headers=headers, params=params)
    print("Endpoint Response Code: " + str(twitter_response.status_code), flush=True)
    if twitter_response.status_code != 200:
        raise Exception(twitter_response.status_code, twitter_response.text)
    return twitter_response.json()


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


def loop_connect(next_token) -> tuple:
    """Connects to Twitter API multiple times. Current parameters for requests
    per call and requests per window are based on free use of Twitter's API.

    Returns: All responses appended to a single dict."""
    max_requests_per_call = 100
    max_requests_per_window = 180

    # Create URL for response
    bearer_token = config.bearer_token
    headers = create_headers(bearer_token)
    url = create_url(max_requests_per_call)
    next_token = next_token

    # Get Initial Response
    json_response = connect_to_api(url[0], headers, url[1], next_token)

    # Update how many items we can request
    requests_per_call = max_requests_per_window - max_requests_per_call
    while requests_per_call > 0:
        url = create_url(requests_per_call)
        try:
            next_token = json_response['meta']['next_token']
        except KeyError:
            next_token = None
        temp_response = connect_to_api(url[0], headers, url[1], next_token)
        json_response = append_dict_values(json_response, temp_response)
        requests_per_call = requests_per_call - max_requests_per_call
    return json_response, next_token


def connect_loop():
    """Continuously makes API requests on a fifteen-minute timer.
    Closes when the Docker container is stopped."""
    print_current_date_and_time()

    next_token = None

    while True:

        # Open postgres connection
        engine = create_engine("postgresql://{user}:{pw}@{host}:{port}/{db}".format
                               (host=hostname, port=port, db=dbname, user=uname, pw=pwd),
                               pool_size=20, max_overflow=0)
        try:
            engine.connect()
            print("Database connection opened", flush=True)
        except (psycopg2.OperationalError, sqlalchemy.exc.OperationalError):
            print("OperationalError: Database not running. Please restart Docker "
                  "containers")
            break
        # local engine
        # engine = create_engine("postgresql://{user}:{pw}@{host}/{db}".format(
        #     host=hostname, db=dbname, user=uname, pw=pwd), pool_size=20,
        #     max_overflow=0)

        response, next_token = loop_connect(next_token)
        add_tweets_to_db(response, engine)
        add_users_to_db(response, engine)

        # End postgres connection
        engine.dispose()
        print("Database connection closed", flush=True)

        # Wait ~15min for next request
        print("\nWaiting 15 minutes until next request\n", flush=True)
        time.sleep(900)


def add_tweets_to_db(twitter_response: dict, engine):
    """Connects to postgres database and inserts Tweets to the tweets table."""
    for twit in twitter_response['data']:
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
        tweet = session.query(Tweet).filter_by(tweet_id=twit['id']).first()
        if not tweet:
            tweet_id = twit['id']
            author_id = twit['author_id']
            tweet_text = twit['text']
            like_count = twit['public_metrics']['like_count']
            quote_count = twit['public_metrics']['quote_count']
            reply_count = twit['public_metrics']['reply_count']
            retweet_count = twit['public_metrics']['retweet_count']
            request_date = datetime.today().strftime('%Y-%m-%d')
            topic = config.search
            tweet = Tweet(tweet_id, author_id, tweet_text, like_count, quote_count,
                          reply_count, retweet_count, request_date, topic)
            session.add(tweet)
            session.commit()
    print("Successfully wrote tweets to database", flush=True)


def add_users_to_db(twitter_response: dict, engine):
    """Connects to postgres database and inserts Tweets to the users table."""
    for acct in twitter_response['includes']['users']:
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
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
            user = User(user_id, username, location, follower_count, following_count,
                        tweet_count, acct_date)

            session.add(user)
            session.commit()
    print("Successfully wrote users to database", flush=True)


if __name__ == "__main__":

    # Get the user configuration
    print_current_date_and_time()
    print("Attempting to get configuration from config.py")
    try:
        hostname = db_con.hostname
    except AttributeError:
        print('Please configure config.py, hostname')
        sys.exit()
    try:
        dbname = db_con.dbname
    except AttributeError:
        print('Please configure config.py, dbname')
        sys.exit()
    try:
        uname = db_con.uname
    except AttributeError:
        print('Please configure config.py, uname')
        sys.exit()
    try:
        pwd = db_con.pwd
    except AttributeError:
        print('Please configure config.py, pwd')
        sys.exit()
    try:
        port = db_con.port
    except AttributeError:
        print('Please configure config.py, port')
        sys.exit()
    try:
        search = config.search
    except AttributeError:
        search = 'pumpkin spice'
    print("Configuration set\n")

    # Start the API request & database write loop.
    print_current_date_and_time()
    print("Beginning request cycle\n")
    connect_loop()
