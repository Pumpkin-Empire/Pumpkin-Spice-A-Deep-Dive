import config
import pandas as pd
from rauth import OAuth1Service

twitter = OAuth1Service(
    name='twitter',
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,

)


def auth():
    return config.bearer_token


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

