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

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp {
        background: #0b1020;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .article-title {
        color: #f8fafc;
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.25;
        margin-bottom: 1rem;
    }

    .article-meta {
        color: #91a0b8;
        font-size: 0.9rem;
        display: flex;
        gap: 20px;
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #1e293b;
    }

    .article-meta span {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .article-image {
        width: 100%;
        height: 450px;
        object-fit: cover;
        border-radius: 16px;
        margin-bottom: 2rem;
        display: block;
    }

    .article-content {
        color: #d8dfeb;
        font-size: 1.1rem;
        line-height: 1.8;
        margin-bottom: 2rem;
    }

    .action-bar {
        display: flex;
        gap: 12px;
        padding-top: 1.5rem;
        border-top: 1px solid #1e293b;
    }

    .action-btn {
        background: #1e293b;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .action-btn:hover {
        background: #2a3a5a;
    }

    .action-btn.active {
        background: #667eea;
    }

    div[data-testid="stButton"] > button {
        border-radius: 10px;
        min-height: 44px;
    }

    .back-btn {
        background: #1e293b !important;
        color: white !important;
        border: none !important;
    }

    .back-btn:hover {
        background: #2a3a5a !important;
    }

    .st-key-like_btn button {
        background: #1e293b;
    }

    .st-key-dislike_btn button {
        background: #1e293b;
    }

    .st-key-save_btn button {
        background: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# Back button
if st.button("", key="back_btn", icon=":material/arrow_back:"):
    st.switch_page("pages/ForYou.py")

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
    # Title
    st.markdown(f'<div class="article-title">{selected_article["title"]}</div>', unsafe_allow_html=True)

    # Meta info
    date = selected_article.get("date", "Unknown date")
    author = selected_article.get("author", "Unknown author")
    source = selected_article.get("source", "Unknown source")

    st.markdown(f"""
    <div class="article-meta">
        <span>📅 {date}</span>
        <span>✍️ {author}</span>
        <span>📰 {source}</span>
    </div>
    """, unsafe_allow_html=True)

    # Cover image
    if selected_article.get("cover_image"):
        st.markdown(
            f'<img src="{selected_article["cover_image"]}" class="article-image" />',
            unsafe_allow_html=True
        )

    # Content
    content = selected_article.get("content", "No content available.")
    st.markdown(f'<div class="article-content">{content}</div>', unsafe_allow_html=True)

    # Action buttons
    col_like, col_dislike, col_save, col_space = st.columns([1, 1, 1, 8])

    with col_like:
        if st.button("", key="like_btn", icon=":material/thumb_up:"):
            st.session_state["reaction"] = "like" if st.session_state["reaction"] != "like" else None

    with col_dislike:
        if st.button("", key="dislike_btn", icon=":material/thumb_down:"):
            st.session_state["reaction"] = "dislike" if st.session_state["reaction"] != "dislike" else None

    with col_save:
        if st.button("", key="save_btn", icon=":material/bookmark:"):
            if not user_id:
                st.switch_page("pages/log_in_page.py")
            else:
                if is_saved:
                    remove_saved_article(user_id, selected_article["article_id"])
                    is_saved = False
                    st.session_state["save"] = False
                else:
                    save_article_for_user(user_id, selected_article["article_id"])
                    st.session_state["save"] = True
                    is_saved = True

    # Button highlight styles
    if st.session_state["reaction"] == "like":
        st.markdown("<style>.st-key-like_btn button { background: #28a745 !important; }</style>", unsafe_allow_html=True)
    elif st.session_state["reaction"] == "dislike":
        st.markdown("<style>.st-key-dislike_btn button { background: #dc3545 !important; }</style>", unsafe_allow_html=True)

    if is_saved:
        st.markdown("<style>.st-key-save_btn button { background: #667eea !important; }</style>", unsafe_allow_html=True)

else:
    st.error("Article not found.")
    if st.button("Back to For You", icon=":material/arrow_back:"):
        st.switch_page("pages/ForYou.py")