import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

### add data load here###

st.set_page_config(page_title="Pumpkin Empire: a Pumpkin Spice Tweets Journey",
                   layout='wide')

######  Setting up the app  #####

st.title("Pumpkin Empire: a Pumpkin Spice Tweets Journey")

##add logo/title image if we want
# title_image = Image.open('<filepath here>')
# st.image(title_image)

st.markdown("Exploring the polarizing topic of Pumpkin Spice, one tweet at a time")
st.markdown("more info here if we want")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    st.markdown('column 1')
    col1.write("column 1 write")

with col2:
    st.markdown('column 2')

with col3:
    fig = plt.figure()
    plt.plot([1,2,3,4,5])

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

