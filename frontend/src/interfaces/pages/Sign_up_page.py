import streamlit as st
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from backend.app.db.session import SessionLocal
from backend.app.services.auth_service import auth_service
from backend.app.schemas.user import UserCreate

st.set_page_config(layout="centered")

st.title("Sign Up")
st.write("Create a new account to get started.")
st.text_input("Username", key="username")
st.text_input("First Name", key="first_name")
st.text_input("Last Name", key="last_name")
st.selectbox("Gender", ["Male", "Female"], key="gender")

if st.button("Sign Up"):
    username = st.session_state["username"].strip()
    first_name = st.session_state["first_name"].strip()
    last_name = st.session_state["last_name"].strip()
    gender = st.session_state["gender"]

    if not username or not first_name or not last_name or not gender:
        st.error("Please fill in all fields.")
    else:
        db = SessionLocal()
        try:
            payload = UserCreate(
                username=username,
                first_name=first_name,
                last_name=last_name,
                gender=gender
            )

            user = auth_service.register_user(db, payload)

            st.success("Account created successfully!")
            st.session_state["user_id"] = user.id
            st.session_state["logged_in"] = True

        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Something went wrong: {e}")
        finally:
            db.close()
    st.switch_page("pages/ForYou.py")

if st.button("Go to Log In"):
    st.switch_page("pages/log_in_page.py")


    