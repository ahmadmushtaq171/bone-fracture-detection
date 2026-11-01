import streamlit as st

import config
from core import auth
from core.ui import go, html


def _after_login(user):
    st.session_state.user = user
    target = st.session_state.pop("after_login", None)
    st.session_state.page = target or ("admin" if user["role"] == "admin" else "detector")
    st.rerun()


def render(mode: str = "login"):
    """mode is 'login' or 'signup' (set by the navbar buttons)."""
    html('<div style="height:48px"></div>')
    side, form = st.columns([0.9, 1.1], gap="large")

    with side:
        html(
            f"""<div class="gz-auth-side"><div class="gz-badge" style="background:rgba(255,255,255,.1);color:#fff;border-color:rgba(255,255,255,.2)"><i></i> {config.APP_NAME}</div>
            <h2>{'Create your account.' if mode == 'signup' else 'Sign in to start screening X-rays.'}</h2>
            <p>One account gives you the live fracture detector, your personal scan history and the full project report and presentation.</p>
            <ul><li>Passwords are salted and hashed with PBKDF2</li><li>Your X-ray images are never stored</li>
            <li>Instant results with a confidence score</li><li>Role-based access for administrators</li></ul></div>"""
        )

    with form:
        html('<div style="height:10px"></div>')
        if st.session_state.get("after_login"):
            st.info("Please log in or create an account to use the detector.")

        if mode == "signup":
            html('<div class="gz-eyebrow">Sign up</div><h2 class="gz-h2" style="font-size:34px">Create a free account</h2>')
            with st.form("signup_form", clear_on_submit=False):
                name = st.text_input("Full name", placeholder="Your full name")
                email = st.text_input("Email", placeholder="you@example.com")
                c1, c2 = st.columns(2)
                with c1:
                    pwd = st.text_input("Password", type="password", placeholder="Min. 8 characters")
                with c2:
                    pwd2 = st.text_input("Confirm password", type="password", placeholder="Repeat password")
                st.caption("Use at least 8 characters, with a letter and a number.")
                ok = st.form_submit_button("Create account", type="primary", width="stretch")
            if ok:
                done, msg = auth.signup(name, email, pwd, pwd2)
                if done:
                    user = auth.login(email, pwd)
                    if user:
                        _after_login(user)
                    st.success(msg)
                else:
                    st.error(msg)
            html('<div style="height:10px"></div>')
            st.button("Already have an account? Log in", key="to_login", on_click=go, args=("login",))
        else:
            html('<div class="gz-eyebrow">Log in</div><h2 class="gz-h2" style="font-size:34px">Welcome back</h2>')
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email", placeholder="you@example.com")
                pwd = st.text_input("Password", type="password", placeholder="Your password")
                ok = st.form_submit_button("Log in", type="primary", width="stretch")
            if ok:
                if not email or not pwd:
                    st.error("Enter both your email and password.")
                else:
                    user = auth.login(email, pwd)
                    if user:
                        _after_login(user)
                    else:
                        st.error("Incorrect email or password.")
            html('<div style="height:10px"></div>')
            st.button("New here? Create an account", key="to_signup", on_click=go, args=("signup",))
