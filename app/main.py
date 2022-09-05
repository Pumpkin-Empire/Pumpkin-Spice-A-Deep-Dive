from PumpkinEmpire import *
# import numpy as np
import db_con
import streamlit as st
import pandas as pd
# import plotly.express as px
import matplotlib.pyplot as plt
# import re as re
import seaborn as sns
import psycopg2
from textblob import TextBlob
from utils import get_most_hashtags, get_most_mentions, show_wordcloud
# import time

# Gives time for API request & database write to finish before trying to connect.
# time.sleep(10)

hostname = db_con.hostname
port = db_con.port
database = db_con.dbname
user = db_con.uname
pwd = db_con.pwd

# topic = None
st.set_page_config(page_title=f"Pumpkin Empire", layout='wide')


# data load here, initialize connection
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(
        host=hostname,
        port=port,
        database=database,
        user=user,
        password=pwd
    )


conn = init_connection()



# data frames
tweets = pd.read_sql("SELECT * FROM tweets", conn)
tweets['date'] = pd.to_datetime(tweets['date'])
tweets['Reply'] = tweets['tweet_text'].str.startswith('@')
tweets['RT'] = tweets['tweet_text'].str.startswith('RT')
tweets['polarity'] = tweets['tweet_text'].apply(lambda x: TextBlob(x).sentiment[0])
tweets['sentiment'] = tweets['polarity'].apply(lambda x: 'positive' if x > 0 else('negative' if x<0 else 'neutral'))
users = pd.read_sql("SELECT * FROM users", conn)
users['acct_created'] = pd.to_datetime(users['acct_created'])
mergedDF = pd.merge(tweets, users, how="left", left_on="author_id", right_on="user_id")
user_stack = mergedDF.groupby(mergedDF.acct_created.dt.year)['sentiment'].value_counts()

# with st.form(key ='Form1'):
#     with st.sidebar:
#         user_word = st.text_input("Enter a keyword", "habs")
#         select_language = st.radio('Tweet language', ('All', 'English', 'French'))
#         include_retweets = st.checkbox('Include retweets in data')
#         num_of_tweets = st.number_input('Maximum number of tweets', 100)
#         submitted1 = st.form_submit_button(label = 'Search Twitter 🔎')

# topic = None

topics = tweets['topic'].drop_duplicates()

topic = None
next_token = None

with st.form(key='Form'):
    with st.sidebar:
        search_term = st.text_input('Type a topic and click Search to add to the database')
        submitted = st.form_submit_button(label="Search")
        if submitted and len(search_term) > 0:
            search_term = search_term.title()
            streamlit_connect(search_term, next_token)
            time.sleep(3)
            # topic = search_term
            st.experimental_rerun()

if topic is None:
    topic = st.sidebar.selectbox('Previous Searches', topics[::-1])


try:
    ######  Setting up the app  #####
    tweets = pd.read_sql(f"SELECT * FROM tweets where topic = '{topic}'", conn)
    tweets['date'] = pd.to_datetime(tweets['date'])
    tweets['Reply'] = tweets['tweet_text'].str.startswith('@')
    tweets['RT'] = tweets['tweet_text'].str.startswith('RT')
    tweets['polarity'] = tweets['tweet_text'].apply(lambda x: TextBlob(x).sentiment[0])
    tweets['sentiment'] = tweets['polarity'].apply(
        lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral'))
    users = pd.read_sql("SELECT * FROM users", conn)
    users['acct_created'] = pd.to_datetime(users['acct_created'])
    mergedDF = pd.merge(tweets, users, how="left", left_on="author_id", right_on="user_id")
    user_stack = mergedDF.groupby(mergedDF.acct_created.dt.year)['sentiment'].value_counts()

    print(tweets.loc[tweets['polarity'] < 0])


    ######  Setting up the analysis  #####
    if topic is not None:
        topic = topic.title()
        st.markdown(f"<h1 style='text-align: center; color: black; '>{topic}: a {topic} Tweets Journey</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color:grey;'>Exploring the polarizing "
                    f"topic of {topic}, one tweet at a time</h3>", unsafe_allow_html=True)
        vert_space = '<div style="padding: 30px 5px;"></div>'
        st.markdown(vert_space, unsafe_allow_html=True)
    elif len(topics) != 0 :
        st.markdown("<h1 style='text-align: center; color: black'>Please enter a new"
                    " search or select a topic in the sidebar.</h1>", unsafe_allow_html=True)
    # add logo/title image if we want
    # title_image = Image.open('<filepath here>')
    # st.image(title_image)

    col4, col5, col6 = st.columns([1, 1, 2])
    col7, col8 = st.columns(2)

    with st.container():
        with col4:
            st.subheader("There are {} total tweets".format(tweets.shape[0]))
            st.markdown(' ')
            RT_tweets = tweets[tweets['RT'] == True]
            reply_tweets = tweets[tweets['Reply'] == True]
            mention_tweets = tweets[(tweets['RT'] == False) & (tweets['Reply'] == False)
                                    & (tweets['tweet_text'].str.contains('@'))]
            plain_text_tweets = tweets[~tweets['tweet_text'].str.contains("@")
                                       & ~tweets['tweet_text'].str.contains("RT")]

            len_data = [len(RT_tweets) / len(tweets), len(mention_tweets) / len(tweets),
                        len(reply_tweets) / len(tweets), len(plain_text_tweets) / len(tweets)]
            item_data = ['Retweets', 'Mentions', 'Replies', 'Original Tweets']
            # define Seaborn color palette to use
            colors = sns.color_palette('rocket_r')[0:4]
            # create pie chart
            fig = plt.figure()
            plt.pie(len_data, labels=item_data, colors=colors, autopct='%.0f%%', textprops={'fontsize': 14})
            plt.axis('equal')

            st.pyplot(fig)
            plt.cla()

            tweet_sentiment = tweets.groupby(tweets['sentiment']).size().reset_index(name='Count')
            hide_table_row_index  = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            st.table(tweet_sentiment)

        with col5:
            st.subheader("There are {} unique accounts tweeting".format(users['username'].nunique()))
            st.markdown('')
            usertweets = mergedDF.groupby('username').count()['tweet_text'].sort_values(ascending=False)\
                .reset_index(name="Tweet Count")
            # tweet_sentiment = tweets.groupby(tweets['sentiment']).size().reset_index(name='Count')
            st.markdown("#### Top 10 Accounts by Tweet Count")
            st.table(usertweets[:10])

        with col6:
            st.markdown("<h3 style='text-align: center; color:black;'>"
                        "Account Creation Date and Sentiment</h3>", unsafe_allow_html=True)
            # st.bar_chart(data=users.groupby(users.acct_created.dt.year).size(), y=1500, use_container_width=True)
            ###User account creation chart by sentiment#####
            color_pallette = sns.color_palette("Spectral")
            user_stack_chart = user_stack.unstack()
            user_stack_chart.plot.bar(stacked=True, color=color_pallette)
            plt.xlabel('Year Account Created')
            plt.legend(bbox_to_anchor=(1.05, 1))
            st.pyplot(plt.show(), user_container_width=True)
            with st.expander('User Account Created Year'):
                st.write(users.groupby(users.acct_created.dt.year).size())
            plt.cla()


    with st.container():
        with col7:
            #### most hashtags chart ###
            st.pyplot(get_most_hashtags(tweets))
        with col8:
            #### most mentions chart ###
            st.pyplot(get_most_mentions(tweets))

    with st.expander("Word Cloud"):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Positive")
            temp_df = tweets.loc[tweets['sentiment'] == 'positive']
            pos_fig = show_wordcloud(temp_df['tweet_text'])
            st.pyplot(pos_fig)
            plt.cla()

        with col2:
            st.subheader("Negative")
            temp_df = tweets.loc[tweets['sentiment'] == 'negative']
            st.pyplot(show_wordcloud(temp_df['tweet_text']))
            plt.cla()

        with col3:
            st.subheader("Neutral")
            temp_df = tweets.loc[tweets['sentiment'] == 'neutral']
            st.pyplot(show_wordcloud(temp_df['tweet_text']))
            plt.cla()

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(tweets)
except ZeroDivisionError:
    st.markdown('Please enter your first topic in the sidebar search box')


