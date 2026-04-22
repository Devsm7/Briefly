import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import api_client, styles

st.set_page_config(page_title="Profile — Briefly", layout="centered")
styles.inject()

# ── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("pages/log_in_page.py")

# ── Load user data ────────────────────────────────────────────────────────────
with st.spinner("Loading profile…"):
    try:
        user = api_client.get_me()
    except Exception as e:
        st.error(f"Could not load profile: {e}")
        user = None

# ── Header ────────────────────────────────────────────────────────────────────
back_col, title_col = st.columns([1, 6])
with back_col:
    if st.button("← Back"):
        st.switch_page("pages/ForYou.py")
with title_col:
    st.markdown('<h2 style="margin:0;color:#1e1b4b;">👤 Profile</h2>', unsafe_allow_html=True)

st.divider()

# ── User info ─────────────────────────────────────────────────────────────────
if user:
    with st.container(border=True):
        st.markdown("### Account Details")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Username**  \n{user.get('username', '—')}")
            st.markdown(f"**First Name**  \n{user.get('first_name', '—')}")
        with col2:
            st.markdown(f"**Last Name**  \n{user.get('last_name', '—')}")
            st.markdown(f"**Gender**  \n{(user.get('gender') or '—').capitalize()}")

        st.caption(f"Member since {user.get('created_at', '')[:10] if user.get('created_at') else '—'}")
else:
    st.warning("Could not retrieve user data.")

st.divider()

# ── Actions ───────────────────────────────────────────────────────────────────
st.markdown("### Preferences")
if st.button("🔄 Retake survey", use_container_width=False):
    for k in ["survey_step", "survey_categories", "survey_answers"]:
        st.session_state.pop(k, None)
    st.switch_page("pages/survey_page.py")

st.divider()

if st.button("🚪 Logout", type="primary", use_container_width=False):
    st.session_state.clear()
    st.switch_page("pages/log_in_page.py")
