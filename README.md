# Pumpkin-Spice-A-Deep-Dive

## Current Plan

1. Research twitter apis to find out what data is available.
   - Location
    - Date
    - Tweet
    - Demographic
    - Reactions 
    - Retweets
2. Save data to SQL database (postgresql)
3. Set up api get requests to pull data
4. Investigate initial data.
    - Make initial data plan (basic analysis)
    - Plan & timeline for additional data analysis/buildout  based on available data & time available
5. Set up docker/airflow and spark to do scheduled pulls of data
6. Analyze data and make presentable project (jupyter notebook, powerpoint presentation or other? I.e. interactive app if time)
7. Additional buildout based on time

**Avenues of analysis**
  - Word map
  - Businesses mentioned
  - Frequency throughout day
  - Frequency day after day
  - Sentiment analysis over time
  - Demographics of the tweeter
  - Location of tweeter/tweet


### Database Tables Creation

The following tables were created in a postgres Database in order to load the data from the Twitter API pull

**Tweets table**
```
CREATE TABLE tweets (
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
```

**Users table**
```
CREATE TABLE users (
user_id text,
username text,
location text,
follower_count text,
following_count int,
tweet_count int,
acct_created date,
PRIMARY KEY(user_id)
);
```