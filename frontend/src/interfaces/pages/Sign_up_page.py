import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import api_client, styles

st.set_page_config(page_title="Sign Up — Briefly", layout="centered")
styles.inject()

st.title("Create an account")
st.write("Join Briefly and get personalised news")

with st.container():
    username   = st.text_input("Username",   placeholder="janedoe",  key="reg_username")
    first_name = st.text_input("First Name", placeholder="Jane",     key="reg_first_name")
    last_name  = st.text_input("Last Name",  placeholder="Doe",      key="reg_last_name")
    gender     = st.radio("Gender", ["Male", "Female"], horizontal=True, key="reg_gender")

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        submit = st.button("Create account", use_container_width=True, type="primary")

    if submit:
        errors = []
        u = username.strip()
        if not u:
            errors.append("Username is required.")
        elif len(u) < 3:
            errors.append("Username must be at least 3 characters.")
        elif not u.replace("_", "").isalnum():
            errors.append("Username: letters, numbers, and underscores only.")
        if not first_name.strip():
            errors.append("First name is required.")
        if not last_name.strip():
            errors.append("Last name is required.")

        if errors:
            for e in errors:
                st.markdown(f'<div class="err-box">{e}</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Creating account…"):
                try:
                    api_client.register(
                        u, first_name.strip(), last_name.strip(), gender.lower()
                    )
                    # Auto-login to get a token
                    data = api_client.login(u)
                    st.session_state["token"]    = data["access_token"]
                    st.session_state["username"] = u
                    st.session_state["logged_in"] = True
                    st.success("Account created!")
                    st.switch_page("pages/survey_page.py")
                except RuntimeError as e:
                    st.markdown(f'<div class="err-box">{e}</div>', unsafe_allow_html=True)
                except Exception:
                    st.markdown('<div class="err-box">Could not reach the server. Please try again.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("Already have an account?")
    if st.button("Sign in →"):
        st.switch_page("pages/log_in_page.py")
