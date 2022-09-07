import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import re as re
import seaborn as sns
import psycopg2
from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.tokenize.api import TokenizerI
from sklearn import model_selection
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
from nltk.corpus import stopwords



def get_most_hashtags(data):
    ###finding hashtags and counting to get top hashtags used ###
    hashtags = []
    hashtag_pattern = re.compile(r"#[a-zA-Z]+")
    hashtag_matches = list(data['tweet_text'].apply(hashtag_pattern.findall))
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
    colors = sns.color_palette('rocket_r')
    fig, ax = plt.subplots()  # figsize=(12, 12))
    y_pos = np.arange(len(hashtag_ordered_keys))
    ax.barh(y_pos, list(hashtag_ordered_values)[::-1], align='center', color=colors, edgecolor='black', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(hashtag_ordered_keys)[::-1])
    ax.set_xlabel("Number of tags")
    ax.set_title("Most used #hashtags", fontsize=20)
    plt.tight_layout(pad=3)
    return fig

def get_most_mentions(data):
    ####mentions data for most mentions chart####
    mentions = []
    mention_pattern = re.compile(r"@[a-zA-z_]+")
    mention_matches = list(data['tweet_text'].apply(mention_pattern.findall))
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
    colors = sns.color_palette('rocket_r')
    fig, ax = plt.subplots()  # figsize=(12, 12))
    y_pos = np.arange(len(mentions_ordered_values))
    ax.barh(y_pos, list(mentions_ordered_values)[::-1], align='center', color=colors[1], edgecolor='black', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(mentions_ordered_keys)[::-1])
    ax.set_xlabel("Number of Mentions")
    ax.set_title("Most Frequently Mentioned Accounts", fontsize=20)
    return fig


def show_wordcloud(data):

    stopword = stopwords.words('english')
    # adding some irrelevant words to our stopwords after running the tokenizer below.
    extended_stop = ['https', 'stud_status', '//t.co/7pw885i0zw', 'ashnikko', 'lvnareclps', "n't", 'digitalprex',
                     '//t.co/qthygenygi',
                     'ik', 'een', 'heb', 'ca', 'teresamaly', 'bigtoofedblonde', 'ikuflyinn', 'mi', 'llego', 'en',
                     'kaars', 'botten', 'nipple', 'nipples',
                     'kaarsen', 'fuck', 'fuc', 'bitch', 'like_count', 'False', 'tweet_id', 'RT', 'author_id', 'rows',
                     'm', 'gt', 'True', 'polarity', 'sentiment', 'columns', 'positive', 'negative', 'neutral',
                     'Reply', 'x']
    stopword.extend(extended_stop)
    STOPWORDS.update(extended_stop)

    wordcloud = WordCloud(
        background_color='white',
        colormap='rocket_r',
        stopwords=STOPWORDS,
        max_words=200,
        max_font_size=40,
        scale=3,
        random_state=1
    ).generate(str(data))

    plt.imshow(wordcloud, interpolation= 'bilinear')
    plt.axis('off')
    plt.show()



