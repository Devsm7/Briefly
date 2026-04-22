import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import api_client, styles

st.set_page_config(page_title="Library — Briefly", layout="wide", initial_sidebar_state="collapsed")
styles.inject()

# ── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("pages/log_in_page.py")

# ── Top navbar ────────────────────────────────────────────────────────────────
title_col, back_col = st.columns([10, 1])
with title_col:
    st.markdown('<h2 style="margin:0;color:#1e1b4b;">🔖 Saved Articles</h2>', unsafe_allow_html=True)
with back_col:
    if st.button("", key="go_home", icon=":material/home:", use_container_width=True):
        st.switch_page("pages/ForYou.py")

st.markdown('<p style="color:#6b7280;margin-top:-0.5rem;">Your personal reading library</p>', unsafe_allow_html=True)
st.divider()

# ── Load saved articles ───────────────────────────────────────────────────────
with st.spinner("Loading saved articles…"):
    try:
        articles = api_client.get_library()
    except Exception as e:
        st.error(f"Could not load library: {e}")
        articles = []

if not articles:
    st.info("No saved articles yet. Browse the feed and bookmark articles to see them here.")
    if st.button("Go to feed →"):
        st.switch_page("pages/ForYou.py")
    st.stop()

# ── Article grid (3 columns) ──────────────────────────────────────────────────
def article_card(article: dict):
    with st.container(border=True):
        if article.get("cover_image"):
            st.image(article["cover_image"], use_container_width=True)

        if article.get("category"):
            st.markdown(
                f'<span class="badge">{article["category"].upper()}</span>',
                unsafe_allow_html=True,
            )

        if st.button("Read more..", key=f"saved_{article['article_id']}"):
            st.session_state["selected_article_id"] = article["article_id"]
        
            st.query_params["article_id"] = article["article_id"]
            st.switch_page("pages/article_details.py", query_params={"article_id": article["article_id"]})


def news_grid(articles, num_columns=3):
    columns = st.columns(num_columns)
    for i, article in enumerate(articles):
        with columns[i % num_columns]:
            article_card(article)

        preview = article.get("preview") or article.get("description") or ""
        if preview:
            st.markdown(
                f'<p class="article-card-preview">{preview[:200]}…</p>',
                unsafe_allow_html=True,
            )

        st.caption(f"📅 {article.get('date', '')}  ·  {article.get('source', '')}")

        if st.button("Read more →", key=f"saved_{article['article_id']}", use_container_width=True):
            st.session_state["selected_article_id"] = article["article_id"]
            st.switch_page("pages/article_details.py",
                           query_params={"article_id": article["article_id"]})


cols = st.columns(3)
for i, article in enumerate(articles):
    with cols[i % 3]:
        article_card(article)
