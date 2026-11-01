"""Shared UI helpers: CSS injection, html(), navbar, page header, footer, auth guard."""
import streamlit as st

import config
from core.styles import CSS


def html(s: str):
    """Render raw HTML. Blank lines / indentation are stripped so Markdown never turns it into a code block."""
    cleaned = "\n".join(line.strip() for line in s.splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def inject_css():
    page = st.session_state.get("page", "home")
    active = ""
    if page in {k for k, _ in config.NAV} | {"admin"}:  # login/signup keep their own dark button style
        active = f".st-key-nav_{page} button{{color:var(--brand)!important;background:#EEF1FF!important;}}"
    st.markdown(f"<style>{CSS}\n{active}</style>", unsafe_allow_html=True)


def go(page: str):
    st.session_state.page = page


def logout():
    st.session_state.user = None
    st.session_state.page = "home"


def current_user():
    return st.session_state.get("user")


def is_admin() -> bool:
    u = current_user()
    return bool(u and u.get("role") == "admin")


def navbar():
    user = current_user()
    nav = list(config.NAV)
    if is_admin():
        nav.append(("admin", "Admin"))

    widths = [2.1] + [1.0] * len(nav) + [0.35] + ([1.0] if user else [0.9, 1.0])
    with st.container(key="navbar"):
        cols = st.columns(widths, vertical_alignment="center")
        with cols[0]:
            html(
                f"""<div class="gz-logo"><div class="mark">{config.APP_ICON}</div>
                {config.APP_NAME.split()[0].upper()}<small>{" ".join(config.APP_NAME.split()[1:]).upper()}</small></div>"""
            )
        for i, (key, label) in enumerate(nav, start=1):
            with cols[i]:
                st.button(label, key=f"nav_{key}", on_click=go, args=(key,), width="stretch")
        base = len(nav) + 2
        if user:
            with cols[base]:
                st.button("Log out", key="nav_logout", on_click=logout, width="stretch")
        else:
            with cols[base]:
                st.button("Log in", key="nav_login", on_click=go, args=("login",), width="stretch")
            with cols[base + 1]:
                st.button("Sign up", key="nav_signup", on_click=go, args=("signup",), width="stretch")


def page_header(eyebrow: str, title: str, subtitle: str = ""):
    html(
        f"""<div class="gz-page"><div class="gz-eyebrow">{eyebrow}</div>
        <h1 class="gz-h2">{title}</h1>
        {f'<p class="gz-p">{subtitle}</p>' if subtitle else ''}</div>"""
    )


def disclaimer():
    html(
        """<div class="gz-disclaimer"><b>Educational prototype, not a medical device.</b>
        This model was trained for a university deep-learning project and reaches about 75% accuracy on its test set.
        It must never replace a radiologist or a doctor's diagnosis.</div>"""
    )


def footer():
    roll = getattr(config, "ROLL_NO", "")
    roll_li = f"<li>Roll No: {roll}</li>" if roll else ""
    html(
        f"""<div class="gz-footer"><div class="gz-footer-grid">
        <div><div class="gz-logo"><div class="mark">{config.APP_ICON}</div>{config.APP_NAME.split()[0].upper()}
        <small>{" ".join(config.APP_NAME.split()[1:]).upper()}</small></div>
        <p style="margin-top:14px;max-width:340px">{config.TAGLINE}. Built with TensorFlow, Keras and Streamlit.</p></div>
        <div><h4>Product</h4><ul><li>Fracture detector</li><li>Model results</li><li>Admin dashboard</li><li>Secure login</li></ul></div>
        <div><h4>Project</h4><ul><li>{config.COURSE}</li><li>{config.UNIVERSITY}</li><li>By {config.STUDENT_NAME}</li>{roll_li}</ul></div>
        <div><h4>Contact</h4><ul><li>{config.CONTACT_EMAIL}</li><li><a href="{config.GITHUB_URL}" target="_blank">GitHub repository</a></li></ul></div>
        </div>
        <div class="gz-copy"><span>© 2026 {config.APP_NAME}. Educational use only.</span>
        <span>Dataset: Fracture Multi-Region X-ray (Kaggle) · Model: MobileNetV2</span></div></div>"""
    )
