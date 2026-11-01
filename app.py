"""BoneScan AI: main entry point.  Run locally with:  streamlit run app.py"""
import streamlit as st

# import config

st.set_page_config(
    page_title=f"{config.APP_NAME} · {config.TAGLINE}",
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

from core import auth, db, ui  # noqa: E402


@st.cache_resource
def _boot():
    db.init_db()
    auth.ensure_admin()
    return True


_boot()

# ───── session defaults ─────
st.session_state.setdefault("page", "home")
st.session_state.setdefault("user", None)

# ───── access control (runs BEFORE the navbar so the highlighted tab is always right) ─────
page = st.session_state.page
user = st.session_state.user
if page in config.REQUIRE_LOGIN and not user:
    st.session_state.after_login = page
    st.session_state.page = page = "login"
if page == "admin" and not ui.is_admin():
    st.session_state.page = page = "home"
if page in ("login", "signup") and user:
    st.session_state.page = page = "detector"

ui.inject_css()
ui.navbar()

# ───── router (views are imported lazily so TensorFlow only loads when the detector runs) ─────
if page == "home":
    from views import home
    home.render()
elif page == "detector":
    from views import detector
    detector.render()
elif page == "results":
    from views import results
    results.render()
elif page == "report":
    from views import report
    report.render()
elif page == "presentation":
    from views import presentation
    presentation.render()
elif page in ("login", "signup"):
    from views import login
    login.render(page)
elif page == "admin":
    from views import admin
    admin.render()
else:
    from views import home
    home.render()

ui.footer()
