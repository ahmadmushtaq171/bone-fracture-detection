"""BoneScan AI: main entry point.  Run locally with:  streamlit run app.py"""
import streamlit as st

import config

st.set_page_config(
    page_title=f"{config.APP_NAME} · {config.TAGLINE}",
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ───── self-healing file layout + friendly diagnostics ─────
import importlib  # noqa: E402
import os  # noqa: E402
import shutil  # noqa: E402
from pathlib import Path  # noqa: E402

_ROOT = Path(__file__).resolve().parent
_REQUIRED = [
    "config.py", "core/__init__.py", "core/auth.py", "core/db.py", "core/model.py", "core/styles.py", "core/ui.py",
    "views/__init__.py", "views/home.py", "views/detector.py", "views/results.py", "views/report.py",
    "views/presentation.py", "views/_embed.py", "views/login.py", "views/admin.py",
    "model/bone_fracture_model.keras", "model/class_names.json",
    "assets/training_curve.png", "assets/confusion_matrix.png",
]


# --- organizer start ---
def _organize_files(root, required):
    """If files were uploaded to GitHub flat (no folders), copy each one into the folder it belongs in.
    Matching is by file name, ignoring upper/lower case, wherever the file sits in the repo."""
    index = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", "data")]
        for fn in filenames:
            index.setdefault(fn.lower(), []).append(Path(dirpath) / fn)
    changed = []
    for rel in required:
        target = root / rel
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.name == "__init__.py":
            target.write_text("# package marker\n")
            changed.append(rel)
            continue
        for cand in index.get(target.name.lower(), []):
            if cand != target:
                shutil.copy2(cand, target)
                changed.append(rel)
                break
    if changed:
        importlib.invalidate_caches()
    return changed
# --- organizer end ---


try:
    _organize_files(_ROOT, _REQUIRED)
except Exception as _e:  # noqa: BLE001
    st.warning(f"Could not auto-arrange the project files: {_e}")

_missing = [f for f in _REQUIRED if not (_ROOT / f).exists()]
if _missing:
    st.error("Some project files are still missing from your GitHub repository. Upload them (any folder is fine) and the app will fix the layout itself.")
    st.code("\n".join(_missing))
    st.write("Files/folders found at the top level of the repo:", sorted(p.name for p in _ROOT.iterdir()))
    st.stop()

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
