import numpy as np
import db_con
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import re as re
import seaborn as sns
import psycopg2
from textblob import TextBlob
from utils import get_most_hashtags, get_most_mentions, show_wordcloud
import os, sys, time

# Adding parent directory to import config.py
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

time.sleep(10)

st.set_page_config(page_title="Pumpkin Empire: a Pumpkin Spice Tweets Journey",
                   layout='wide')

### data load here, initialize connection ###
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(
        host=db_con.hostname,
        port=db_con.port,
        database=db_con.dbname,
        user=db_con.uname,
        password=db_con.pwd
    )



conn = init_connection()



## data frames ##
tweets = pd.read_sql("SELECT * FROM tweets", conn)
tweets['date'] = pd.to_datetime(tweets['date'])
tweets['Reply'] = tweets['tweet_text'].str.startswith('@')
tweets['RT'] = tweets['tweet_text'].str.startswith('RT')
tweets['polarity'] = tweets['tweet_text'].apply(lambda x: TextBlob(x).sentiment[0])
tweets['sentiment'] = tweets['polarity'].apply(lambda x: 'positive' if x > 0 else('negative' if x<0 else 'neutral'))
users = pd.read_sql("SELECT * FROM users", conn)
users['acct_created'] = pd.to_datetime(users['acct_created'])
mergedDF = pd.merge(tweets, users, how="left", left_on="author_id", right_on="user_id")


######  Setting up the analysis  #####

st.markdown("<h1 style='text-align: center; color: black; '>Pumpkin Empire: a Pumpkin Spice Tweets Journey</h1>", unsafe_allow_html=True)

##add logo/title image if we want
# title_image = Image.open('<filepath here>')
# st.image(title_image)

st.markdown("<h3 style='text-align: center; color:grey;'>Exploring the polarizing topic of Pumpkin Spice, one tweet at a time</h3>", unsafe_allow_html=True)
st.markdown(" ")


col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    st.subheader("There are {} total tweets".format(tweets.shape[0]))
    RT_tweets = tweets[tweets['RT'] == True]
    reply_tweets = tweets[tweets['Reply'] == True]
    mention_tweets = tweets[(tweets['RT'] == False) & (tweets['Reply'] == False) & (tweets['tweet_text'].str.contains('@'))]
    plain_text_tweets = tweets[~tweets['tweet_text'].str.contains("@") & ~tweets['tweet_text'].str.contains("RT")]

    len_data = [len(RT_tweets) / len(tweets), len(mention_tweets) / len(tweets), len(reply_tweets) / len(tweets),
                len(plain_text_tweets) / len(tweets)]
    item_data = ['Retweets', 'Mentions', 'Replies', 'Original Tweets']
    # define Seaborn color palette to use
    colors = sns.color_palette('rocket_r')[0:4]
    # create pie chart
    fig = plt.figure()
    plt.pie(len_data, labels=item_data, colors=colors, autopct='%.0f%%', textprops={'fontsize': 14})

    st.pyplot(fig)

    tweet_sentiment = tweets.groupby(tweets['sentiment'])
    st.table(tweet_sentiment.size())

with col2:
    st.subheader("There are {} different users".format(users['username'].nunique()))
    usertweets = mergedDF.groupby('username')
    st.markdown("**Top Accounts by PS Tweets**")
    st.table(usertweets.count()['tweet_text'].sort_values(ascending=False)[:6])
    st.markdown("#### Count of Account Creation Year")
    st.write(users.groupby(users.acct_created.dt.year).size())

with col3:
#### most hashtags chart ###
    st.pyplot(get_most_hashtags(tweets))
#### most mentions chart ###
    st.pyplot(get_most_mentions(tweets))

with st.expander("Word Cloud"):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Positive")
        st.pyplot(show_wordcloud(tweets.loc[tweets['sentiment'] == 'positive']))


    with col2:
        st.subheader("Negative")
        st.pyplot(show_wordcloud(tweets.loc[tweets['sentiment'] == 'negative']))

    with col3:
        st.subheader("Neutral")
        st.pyplot(show_wordcloud(tweets.loc[tweets['sentiment'] == 'neutral']))


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(tweets)

