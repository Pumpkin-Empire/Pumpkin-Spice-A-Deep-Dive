import numpy as np
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
import plotly.express as px
import matplotlib.pyplot as plt
import re as re
import seaborn as sns
import psycopg2

st.set_page_config(page_title="Pumpkin Empire: a Pumpkin Spice Tweets Journey",
                   layout='wide')

### data load here, initialize connection ###
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()



## data frames ##
tweets = pd.read_sql("SELECT * FROM tweets", conn)
tweets['date'] = pd.to_datetime(tweets['date'])
tweets['Reply'] = tweets['tweet_text'].str.startswith('@')
tweets['RT'] = tweets['tweet_text'].str.startswith('RT')
users = pd.read_sql("SELECT * FROM users", conn)
users['acct_created'] = pd.to_datetime(users['acct_created'])
mergedDF = pd.merge(tweets, users, how="left", left_on="author_id", right_on="user_id")


######  Setting up the app  #####

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

with col2:
    st.subheader("There are {} different users".format(users['username'].nunique()))
    usertweets = mergedDF.groupby('username')
    st.write(usertweets.count()['tweet_text'].sort_values(ascending=False)[:6])

with col3:
    ###finding hashtags and counting to get top hashtags used ###
    hashtags = []
    hashtag_pattern = re.compile(r"#[a-zA-Z]+")
    hashtag_matches = list(tweets['tweet_text'].apply(hashtag_pattern.findall))
    hashtag_dict = {}
    for match in hashtag_matches:
        for singlematch in match:
            if singlematch not in hashtag_dict.keys():
                hashtag_dict[singlematch] = 1
            else:
                hashtag_dict[singlematch] = hashtag_dict[singlematch] + 1
    hashtag_ordered_list = sorted(hashtag_dict.items(), key=lambda x: x[1])
    hashtag_ordered_list = hashtag_ordered_list[::-1]
    hashtag_ordered_values = []
    hashtag_ordered_keys = []
    for item in hashtag_ordered_list[:11]:
        hashtag_ordered_keys.append(item[0])
        hashtag_ordered_values.append(item[1])

    fig, ax = plt.subplots(figsize=(12, 12))
    y_pos = np.arange(len(hashtag_ordered_keys))
    ax.barh(y_pos, list(hashtag_ordered_values)[::-1], align='center', color='green', edgecolor='black', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(hashtag_ordered_keys)[::-1])
    ax.set_xlabel("Number of tags")
    ax.set_title("Most used #hashtags", fontsize=20)
    plt.tight_layout(pad=3)

    st.pyplot(fig)

####mentions data for most mentions chart####
    mentions = []
    mention_pattern = re.compile(r"@[a-zA-z_]+")
    mention_matches = list(tweets['tweet_text'].apply(mention_pattern.findall))
    mentions_dict = {}
    for match in mention_matches:
        for singlematch in match:
            if singlematch not in mentions_dict.keys():
                mentions_dict[singlematch] = 1
            else:
                mentions_dict[singlematch] = mentions_dict[singlematch] + 1
    mentions_ordered_list = sorted(mentions_dict.items(), key=lambda x: x[1])
    mentions_ordered_list = mentions_ordered_list[::-1]
    mentions_ordered_values = []
    mentions_ordered_keys = []
    for item in mentions_ordered_list[:11]:
        mentions_ordered_keys.append(item[0])
        mentions_ordered_values.append(item[1])

    fig, ax = plt.subplots(figsize=(12, 12))
    y_pos = np.arange(len(mentions_ordered_values))
    ax.barh(y_pos, list(mentions_ordered_values)[::-1], align='center', color='yellow', edgecolor='black', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(mentions_ordered_keys)[::-1])
    ax.set_xlabel("Number of Mentions")
    ax.set_title("Most Frequently Mentioned Accounts", fontsize=20)

    st.pyplot(fig)

with st.expander("Word Cloud"):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Positive")
        st.markdown("insert positive wordcloud here")

    with col2:
        st.subheader("negative")
        st.markdown("insert negative wordcloud")

    with col3:
        st.subheader("neutral")
        st.markdown("insert neutral wordcloud")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(tweets)

