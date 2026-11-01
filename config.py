"""
Central configuration. Edit the values in the "YOUR DETAILS" block, nothing else needs to change.
"""
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# ───────────────────────── YOUR DETAILS ─────────────────────────
APP_NAME = "BoneScan AI"
APP_ICON = "🦴"
TAGLINE = "Fracture detection powered by deep learning"
STUDENT_NAME = "Ahmad Mushtaq"
ROLL_NO = "SU92-BSCSM-F22-171"
COURSE = "Deep Learning Project"
UNIVERSITY = "Your University"
CONTACT_EMAIL = "your.email@example.com"
GITHUB_URL = "https://github.com/ahmadmushtaq171/bone-fracture-detection"

REPORT_URL = (
    "https://docs.google.com/document/d/1fRYygyQGFRRIyugYKPS8V1C8O06Epiyx/edit"
    "?usp=sharing&ouid=102969733195424319345&rtpof=true&sd=true"
)
PRESENTATION_URL = (
    "https://docs.google.com/presentation/d/1vweOdR2bLCvUDs62gW00GnIABs-d5Ocn/edit"
    "?usp=sharing&ouid=102969733195424319345&rtpof=true&sd=true"
)
# ────────────────────────────────────────────────────────────────

# Pages that require a logged-in user. Remove a key to make that page public.
REQUIRE_LOGIN = {"detector"}

# Top navigation (key, label)
NAV = [
    ("home", "Home"),
    ("detector", "Detector"),
    ("results", "Results"),
    ("report", "Report"),
    ("presentation", "Presentation"),
]

# ───────────────────────── Model ─────────────────────────
MODEL_PATH = BASE_DIR / "model" / "bone_fracture_model.keras"
CLASS_NAMES_PATH = BASE_DIR / "model" / "class_names.json"
IMG_SIZE = 224
LOW_CONFIDENCE = 0.60  # below this the app says "inconclusive"

ASSETS = BASE_DIR / "assets"

# ─────────── Numbers taken from the Colab notebook outputs ───────────
TEST_ACCURACY = 0.75
FINAL_TRAIN_ACC = 0.840
FINAL_VAL_ACC = 0.845
# confusion matrix rows = actual [fractured, not fractured], cols = predicted
CONFUSION = [[117, 33], [42, 108]]
CLASS_REPORT = {
    "fractured":     {"precision": 0.74, "recall": 0.78, "f1": 0.76, "support": 150},
    "not fractured": {"precision": 0.77, "recall": 0.72, "f1": 0.74, "support": 150},
}
EPOCH_LOG = [
    {"Epoch": 1, "Train acc": 0.6010, "Val acc": 0.7400, "Train loss": 0.6779, "Val loss": 0.5545},
    {"Epoch": 2, "Train acc": 0.7180, "Val acc": 0.7900, "Train loss": 0.5474, "Val loss": 0.4863},
    {"Epoch": 3, "Train acc": 0.7720, "Val acc": 0.8200, "Train loss": 0.4780, "Val loss": 0.4563},
    {"Epoch": 4, "Train acc": 0.7670, "Val acc": 0.8450, "Train loss": 0.4392, "Val loss": 0.4210},
    {"Epoch": 5, "Train acc": 0.8070, "Val acc": 0.8250, "Train loss": 0.4269, "Val loss": 0.4169},
    {"Epoch": 6, "Train acc": 0.8400, "Val acc": 0.8450, "Train loss": 0.3887, "Val loss": 0.3955},
]

# ───────────────────────── Admin account ─────────────────────────
DEFAULT_ADMIN_EMAIL = "admin@bonescan.app"
DEFAULT_ADMIN_PASSWORD = "Admin@12345"


def admin_credentials():
    """Returns (email, password, using_defaults). Prefers Streamlit secrets."""
    try:
        import streamlit as st
        sec = st.secrets["admin"]
        email, pwd = str(sec["email"]).strip().lower(), str(sec["password"])
        if email and pwd:
            return email, pwd, False
    except Exception:
        pass
    return DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD, True


# ───────────────────────── Google Drive helpers ─────────────────────────
def drive_id(url: str) -> str:
    m = re.search(r"/d/([A-Za-z0-9_-]+)", url)
    return m.group(1) if m else ""


REPORT_ID = drive_id(REPORT_URL)
PRESENTATION_ID = drive_id(PRESENTATION_URL)


def drive_preview(file_id: str) -> str:
    return f"https://drive.google.com/file/d/{file_id}/preview"


def drive_download(file_id: str) -> str:
    return f"https://drive.google.com/uc?export=download&id={file_id}"
