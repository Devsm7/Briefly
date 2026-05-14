import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

import streamlit as st
import api_client

st.set_page_config(layout="centered")

st.title("Sign In")
st.write("Welcome back! Please select a user to log in.")

# Get all users via API
try:
    users_response = api_client._handle(api_client.requests.get(
        f"{api_client.BASE_URL}/api/v1/auth/users",
        timeout=api_client._TIMEOUT,
    ))
    users = users_response if isinstance(users_response, list) else []
except Exception:
    st.error("Unable to load users. Is the server running?")
    st.stop()

user_options = [("", "Select a user")] + [(str(u["id"]), u["username"]) for u in users]

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
        try:
            username = next((u["username"] for u in users if str(u["id"]) == selected_user_id), selected_user_id)
            token_data = api_client.login(username)
            st.session_state["token"] = token_data["access_token"]
            st.session_state["user_id"] = int(selected_user_id)
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login successful!")
            st.switch_page("pages/ForYou.py")
        except RuntimeError as e:
            st.error(f"Login failed: {e}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

if st.button("Go to Sign Up"):
    st.switch_page("pages/Sign_up_page.py")
