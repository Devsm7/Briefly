import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import api_client, styles

st.set_page_config(page_title="For You — Briefly", layout="wide", initial_sidebar_state="collapsed")
styles.inject()

# ── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("pages/log_in_page.py")

# ── Top navbar ────────────────────────────────────────────────────────────────
title_col, saved_col, profile_col = st.columns([10, 1, 1])
with title_col:
    st.markdown('<h1 style="margin:0;color:#1e1b4b;">✦ Briefly</h1>', unsafe_allow_html=True)
with saved_col:
    if st.button("", key="go_saved", icon=":material/bookmark:", use_container_width=True):
        st.switch_page("pages/saved_articles_page.py")
with profile_col:
    if st.button("", key="go_profile", icon=":material/account_circle:", use_container_width=True):
        st.switch_page("pages/profile_page.py")

st.markdown('<p style="color:#6b7280;margin-top:-0.5rem;">Your personalised news feed</p>', unsafe_allow_html=True)
st.divider()

# ── Category filter ────────────────────────────────────────────────────────────
FILTER_OPTIONS = ["All", "Tech", "Politics", "Sport"]
selected_filter = st.segmented_control(
    "Category",
    options=FILTER_OPTIONS,
    default="All",
    label_visibility="collapsed",
    key="feed_filter",
)

# ── Load articles ─────────────────────────────────────────────────────────────
with st.spinner("Loading articles…"):
    try:
        articles = api_client.get_news()
    except Exception as e:
        st.error(f"Could not load articles: {e}")
        articles = []

# Apply filter
if selected_filter and selected_filter != "All":
    articles = [a for a in articles if (a.get("category") or "").lower() == selected_filter.lower()]

if not articles:
    st.info("No articles found.")
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

        st.markdown(
            f'<p class="article-card-title">{article["title"]}</p>',
            unsafe_allow_html=True,
        )

        preview = article.get("preview") or article.get("description") or ""
        if preview:
            st.markdown(
                f'<p class="article-card-preview">{preview[:200]}…</p>',
                unsafe_allow_html=True,
            )

        st.caption(f"📅 {article.get('date', '')}  ·  {article.get('source', '')}")

        if st.button("Read more →", key=f"read_{article['article_id']}", use_container_width=True):
            st.session_state["selected_article_id"] = article["article_id"]
            st.switch_page("pages/article_details.py",
                           query_params={"article_id": article["article_id"]})


cols = st.columns(3)
for i, article in enumerate(articles):
    with cols[i % 3]:
        article_card(article)
