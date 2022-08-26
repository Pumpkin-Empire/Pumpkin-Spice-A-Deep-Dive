
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Date

Base = declarative_base()

class user(Base):
    __tablename__ = 'users'
    user_id = Column(String, primarykey=True),
    username = Column(String),
    location = Column(String),
    follower_count = Column(Integer),
    following_count = Column(Integer),
    tweet_count = Column(Integer),
    acct_created = Column(Date)

    def __init__(self, user_id, username, location, follower_count, following_count, tweet_count, acct_date):
        self.user_id = user_id,
        self.username = username,
        self.location = location,
        self.follower_count = follower_count,
        self.following_count = following_count,
        self.tweet_count = tweet_count,
        self.acct_created = acct_date


class Tweet(Base):
    __tablename__ = 'tweets'
    tweet_id = Column(String, primary_key=True),
    author_id = Column(String)
    tweet_text = Column(String)
    like_count = Column(Integer)
    quote_count = Column(Integer)
    reply_count = Column(Integer)
    retweet_count = Column(Integer)
    place = Column(String)
    date = Column(Date)

    def __init__(self, tweet_id, author_id, tweet_text, like_count, quote_count,
                 reply_count, retweet_count, place, date):
        self.tweet_id = tweet_id
        self.author_id = author_id
        self.tweet_text = tweet_text
        self.like_count = like_count
        self.quote_count = quote_count
        self.reply_count = reply_count
        self.retweet_count = retweet_count
        self.place = place
        self.date = date




