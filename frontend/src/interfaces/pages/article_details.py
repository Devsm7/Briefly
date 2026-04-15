import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from backend.app.services.db_all_articles import (
    get_news,
    save_article_for_user,
    is_article_saved,
    remove_saved_article,
)

selected_id = st.query_params.get("article_id")
user_id = st.session_state.get("user_id")

if selected_id is not None:
    selected_id = int(selected_id)

st.set_page_config(layout="centered")
articles = get_news()

if "reaction" not in st.session_state:
    st.session_state["reaction"] = None
if "save" not in st.session_state:
    st.session_state["save"] = False

selected_article = None
for article in articles:
    if article["article_id"] == selected_id:
        selected_article = article
        break
    
is_saved = False
if user_id and selected_article:
    is_saved = is_article_saved(user_id, selected_article["article_id"])

if selected_article:
    st.title(selected_article["title"])
    st.image(selected_article["cover_image"])
    st.write(selected_article["content"])

    date, author, source, space = st.columns([1, 1, 1, 1])
    with date:
        st.caption(f"Published at: {selected_article['date']}")
    with author:
        st.caption(f"Written by: {selected_article.get('author', 'Unknown')}")
    with source:
        st.caption(f"Source: {selected_article['source']}")

    like, dislike, save, space = st.columns([1, 1, 1, 12])

    with like:
        if st.button("", key="like_btn", icon=":material/thumb_up:"):
            st.session_state["reaction"] = "like"

    with dislike:
        if st.button("", key="dislike_btn", icon=":material/thumb_down:"):
            st.session_state["reaction"] = "dislike"

    with save:
        if st.button("", key="save_btn", icon=":material/bookmark:"):
            if not user_id:
                st.switch_page("pages/log_in_page.py")
            else:
                if is_saved:
                    removed = remove_saved_article(user_id, selected_article["article_id"])
                    is_saved = False
                    st.session_state["save"] = False

                else:
                    save_article_for_user(user_id, selected_article["article_id"])
                    st.session_state["save"] = True
                    is_saved = True

else:
    st.error("Article not found.")

if st.session_state["reaction"] == "like":
    st.markdown("""
    <style>
        .st-key-like_btn button,
        .st-key-like_btn button:hover {
            background-color: #28a745;
        }
    </style>
    """, unsafe_allow_html=True)
elif st.session_state["reaction"] == "dislike":
    st.markdown("""
    <style>
        .st-key-dislike_btn button,
        .st-key-dislike_btn button:hover {
            background: #dc3545;
        }
    </style>
    """, unsafe_allow_html=True)

if is_saved or st.session_state["save"]:
    st.markdown("""
    <style>
        .st-key-save_btn button,
        .st-key-save_btn button:hover {
            background: white;
            color: black;
        }
    </style>
    """, unsafe_allow_html=True)