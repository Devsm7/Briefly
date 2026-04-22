import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import api_client, styles

st.set_page_config(page_title="Article — Briefly", layout="centered")
styles.inject()

# ── Resolve article ID ────────────────────────────────────────────────────────
article_id_param = st.query_params.get("article_id") or st.session_state.get("selected_article_id")
if article_id_param is None:
    st.error("No article selected.")
    if st.button("← Back to feed"):
        st.switch_page("pages/ForYou.py")
    st.stop()

try:
    article_id = int(article_id_param)
except ValueError:
    st.error("Invalid article ID.")
    st.stop()

user_logged_in = st.session_state.get("logged_in", False)

# ── Load all articles and find the one we need ─────────────────────────────────
with st.spinner("Loading article…"):
    try:
        articles = api_client.get_news()
    except Exception as e:
        st.error(f"Could not load articles: {e}")
        st.stop()

selected = next((a for a in articles if a["article_id"] == article_id), None)

if not selected:
    st.error("Article not found.")
    if st.button("← Back to feed"):
        st.switch_page("pages/ForYou.py")
    st.stop()

# ── Saved state (check on first render only) ──────────────────────────────────
if f"is_saved_{article_id}" not in st.session_state:
    if user_logged_in:
        st.session_state[f"is_saved_{article_id}"] = api_client.check_saved(article_id)
    else:
        st.session_state[f"is_saved_{article_id}"] = False

if f"reaction_{article_id}" not in st.session_state:
    st.session_state[f"reaction_{article_id}"] = None

is_saved = st.session_state[f"is_saved_{article_id}"]
reaction = st.session_state[f"reaction_{article_id}"]

# ── Back button ───────────────────────────────────────────────────────────────
if st.button("← Back to feed"):
    st.switch_page("pages/ForYou.py")

# ── Article header ────────────────────────────────────────────────────────────
if selected.get("category"):
    st.markdown(f'<span class="badge">{selected["category"].upper()}</span>', unsafe_allow_html=True)

st.title(selected["title"])

if selected.get("cover_image"):
    st.image(selected["cover_image"], use_container_width=True)

# Meta row
date_col, author_col, source_col, _ = st.columns([2, 2, 2, 1])
with date_col:
    st.caption(f"📅 {selected.get('date', '')}")
with author_col:
    st.caption(f"✍️ {selected.get('author', 'Unknown')}")
with source_col:
    st.caption(f"📰 {selected.get('source', '')}")

st.divider()

# ── Article body ──────────────────────────────────────────────────────────────
content = selected.get("content") or selected.get("preview") or ""
st.markdown(content)

if selected.get("url"):
    st.markdown(f"[Read original article →]({selected['url']})")

st.divider()

# ── Interaction buttons ───────────────────────────────────────────────────────
like_col, dislike_col, save_col, _ = st.columns([1, 1, 1, 6])

with like_col:
    liked = reaction == "like"
    if st.button("", key="like_btn", icon=":material/thumb_up:"):
        st.session_state[f"reaction_{article_id}"] = None if liked else "like"
        st.rerun()

with dislike_col:
    disliked = reaction == "dislike"
    if st.button("", key="dislike_btn", icon=":material/thumb_down:"):
        st.session_state[f"reaction_{article_id}"] = None if disliked else "dislike"
        st.rerun()

with save_col:
    if st.button("", key="save_btn", icon=":material/bookmark:"):
        if not user_logged_in:
            st.switch_page("pages/log_in_page.py")
        else:
            try:
                if is_saved:
                    api_client.unsave_article(article_id)
                    st.session_state[f"is_saved_{article_id}"] = False
                else:
                    api_client.save_article(article_id)
                    st.session_state[f"is_saved_{article_id}"] = True
                st.rerun()
            except RuntimeError as e:
                st.error(str(e))

# ── Visual feedback for buttons ───────────────────────────────────────────────
reaction_after = st.session_state[f"reaction_{article_id}"]
is_saved_after = st.session_state[f"is_saved_{article_id}"]

css_parts = []
if reaction_after == "like":
    css_parts.append(".st-key-like_btn button, .st-key-like_btn button:hover { background:#16a34a!important; color:white!important; }")
elif reaction_after == "dislike":
    css_parts.append(".st-key-dislike_btn button, .st-key-dislike_btn button:hover { background:#dc2626!important; color:white!important; }")

if is_saved_after:
    css_parts.append(".st-key-save_btn button, .st-key-save_btn button:hover { background:#4f46e5!important; color:white!important; }")

if css_parts:
    st.markdown(f"<style>{''.join(css_parts)}</style>", unsafe_allow_html=True)
