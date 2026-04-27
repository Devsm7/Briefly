import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from backend.app.db.session import SessionLocal
from backend.app.services.auth_service import auth_service

st.set_page_config(layout="centered")

st.title("Sign In")
st.write("Welcome back! Please select a user to log in.")

# Get all users for dropdown
db = SessionLocal()
users = auth_service.get_all_users(db)
db.close()

# Create list of tuples for selectbox
user_options = [("", "Select a user")] + [(str(u.id), u.username) for u in users]

selected_user_id = st.selectbox(
    "Select User",
    options=[u[0] for u in user_options],
    format_func=lambda x: next((u[1] for u in user_options if u[0] == x), x),
    label_visibility="collapsed"
)

if st.button("Sign In"):
    if not selected_user_id:
        st.error("Please select a user.")
    else:
        db = SessionLocal()
        try:
            user = auth_service.get_user_by_id(db, int(selected_user_id))

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