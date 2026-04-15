import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from backend.app.db.session import SessionLocal
from backend.app.services.auth_service import auth_service

st.set_page_config(layout="centered")

if "logged_in" not in st.session_state:
    st.warning("Please log in first.")
    st.switch_page("pages/login.py")

user_id = st.session_state.get("user_id")

db = SessionLocal()
user = auth_service.get_user_by_id(db, user_id)

st.title("Profile")
st.subheader("User Information")

if user:
    st.write("**First Name:**", user.first_name)
    st.write("**Last Name:**", user.last_name)
    st.write("**Gender:**", user.gender)
    st.write("**Username:**", user.username)
else:
    st.error("User not found.")

db.close()

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("Back to For You"):
        st.switch_page("pages/ForYou.py")

with col2:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("pages/login.py")