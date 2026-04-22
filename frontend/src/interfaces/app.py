import streamlit as st

st.set_page_config(page_title="Briefly", layout="centered")

if st.session_state.get("logged_in"):
    st.switch_page("pages/ForYou.py")
else:
    st.switch_page("pages/log_in_page.py")
