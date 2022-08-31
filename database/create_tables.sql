-- Creation of tweets table
CREATE TABLE IF NOT EXISTS tweets (
tweet_id text,
author_id text,
tweet_text text,
like_count int,
quote_count int,
reply_count int,
retweet_count int,
place text,
date date,
PRIMARY KEY(tweet_id)
);

-- Creation of users table
CREATE TABLE IF NOT EXISTS users (
user_id text,
username text,
location text,
follower_count int,
following_count int,
tweet_count int,
acct_created date,
PRIMARY KEY(user_id)
);