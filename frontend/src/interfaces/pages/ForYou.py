import streamlit as st

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from backend.app.services.db_all_articles import get_news

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)



if not st.session_state.get("logged_in", False) or not st.session_state.get("user_id"):
    st.warning("Please sign up or log in first.")
    st.switch_page("pages/log_in_page.py")
    st.stop()

user_id = st.session_state.get("user_id")
username = st.session_state.get("username")



def article_card(article):
    with st.container():
        st.image(article['cover_image'])
        st.subheader(article['title']) 
        st.write(article['preview'])
        st.caption(article['date'])
        if st.button("read more..", key=article["article_id"]): 
            st.session_state["selected_article_id"] = article["article_id"]
            st.switch_page("pages/article_details.py")
            st.stop() 

def news_grid(articles, num_columns=3):
    columns=st.columns(num_columns)
    for i,article in enumerate(articles):
        column_index = i % num_columns
        with columns[column_index]:
            article_card(article)


def for_you_page():
    title,saved,profile = st.columns([10,1,1])
    with title:
        st.markdown("# For you page<br>", unsafe_allow_html=True)
    with saved:
        if st.button("", key="saved_page",icon=":material/bookmark:",use_container_width=True):
            st.switch_page("pages/saved_articles_page.py")
    with profile:
        if st.button("", key="profile_page",icon=":material/account_circle:",use_container_width=True):
            st.switch_page("pages/profile_page.py")
    articles = get_news() 

    #articles = get_mock_articles()#temp
    news_grid(articles)
for_you_page()
