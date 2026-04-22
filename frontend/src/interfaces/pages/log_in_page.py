import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import api_client, styles

st.set_page_config(page_title="Sign In — Briefly", layout="centered")
styles.inject()

st.markdown('<div class="auth-bg">', unsafe_allow_html=True)

with st.container():
    st.markdown("""
        <div class="card">
            <p class="card-title">Welcome back</p>
            <p class="card-desc">Sign in to your Briefly account</p>
        </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter your username", key="login_username")

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        sign_in = st.button("Sign in", use_container_width=True, type="primary")

    if sign_in:
        if not username.strip():
            st.markdown('<div class="err-box">Please enter your username.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Signing in…"):
                try:
                    data = api_client.login(username.strip())
                    st.session_state["token"] = data["access_token"]
                    st.session_state["username"] = username.strip()
                    st.session_state["logged_in"] = True
                    st.success("Login successful!")
                    st.switch_page("pages/ForYou.py")
                except RuntimeError as e:
                    st.markdown(f'<div class="err-box">{e}</div>', unsafe_allow_html=True)
                except Exception:
                    st.markdown('<div class="err-box">Could not reach the server. Please try again.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "Don't have an account? &nbsp;",
        unsafe_allow_html=True,
    )
    if st.button("Create one →"):
        st.switch_page("pages/Sign_up_page.py")

st.markdown("</div>", unsafe_allow_html=True)
