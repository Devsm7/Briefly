import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from backend.app.services.db_all_articles import get_saved_articles

st.set_page_config(layout="wide")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.switch_page("pages/log_in_page.py")

user_id = st.session_state.get("user_id")


def article_card(article):
    with st.container():
        if article.get("cover_image"):
            st.image(article["cover_image"])

        st.subheader(article["title"])
        st.write(article["preview"])
        st.caption(article["date"])

        if st.button("Read more..", key=f"saved_{article['article_id']}"):
            st.session_state["selected_article_id"] = article["article_id"]
            st.query_params["article_id"] = article["article_id"]
            st.switch_page("pages/article_details.py", query_params={"article_id": article["article_id"]})


def news_grid(articles, num_columns=3):
    columns = st.columns(num_columns)
    for i, article in enumerate(articles):
        with columns[i % num_columns]:
            article_card(article)


st.title("Saved Articles")

articles = get_saved_articles(user_id)

if not articles:
    st.info("No saved articles yet.")
else:
    news_grid(articles)

if st.button("Back to For You"):
    st.switch_page("pages/ForYou.py")