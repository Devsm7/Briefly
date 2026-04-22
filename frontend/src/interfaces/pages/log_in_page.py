import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from backend.app.db.session import SessionLocal
from backend.app.services.auth_service import auth_service

st.set_page_config(layout="centered")

st.title("Sign In")
st.write("Welcome back! Please log in.")

st.text_input("Username", key="login_username")

if st.button("Sign In"):
    username = st.session_state["login_username"].strip()

    if not username:
        st.error("Please enter your username.")
    else:
        db = SessionLocal()
        try:
            user = auth_service.authenticate_user(db, username)

            if not user:
                st.error("User not found.")
            else:
                st.success("Login successful!")

                st.session_state["user_id"] = user.id
                st.session_state["username"] = user.username
                st.session_state["logged_in"] = True

                st.switch_page("pages/ForYou.py")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
        finally:
            db.close()

if st.button("Go to Sign Up"):
    st.switch_page("pages/Sign_up_page.py")