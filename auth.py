"""Authentication: salted PBKDF2 password hashing, signup, login, admin seeding."""
import hashlib
import hmac
import re
import secrets
import sqlite3

import config
from core import db

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_ITERATIONS = 200_000


def hash_password(password: str, salt_hex: str | None = None):
    salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _ITERATIONS)
    return digest.hex(), salt.hex()


def verify_password(password: str, password_hash: str, salt_hex: str) -> bool:
    candidate, _ = hash_password(password, salt_hex)
    return hmac.compare_digest(candidate, password_hash)


def validate_signup(name, email, password, confirm):
    if len(name.strip()) < 2:
        return "Please enter your full name."
    if not _EMAIL_RE.match(email.strip()):
        return "Please enter a valid email address."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if not (re.search(r"[A-Za-z]", password) and re.search(r"\d", password)):
        return "Password must contain at least one letter and one number."
    if password != confirm:
        return "Passwords do not match."
    return None


def signup(name, email, password, confirm):
    """Returns (ok, message)."""
    err = validate_signup(name, email, password, confirm)
    if err:
        return False, err
    email = email.strip().lower()
    h, s = hash_password(password)
    try:
        db.create_user(name.strip(), email, h, s, role="user")
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    return True, "Account created. You can log in now."


def login(email, password):
    """Returns a session user dict, or None when credentials are wrong."""
    user = db.get_user_by_email(email.strip().lower())
    if not user or not verify_password(password, user["password_hash"], user["salt"]):
        return None
    db.touch_login(user["id"])
    return {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}


def ensure_admin():
    """Keep the admin account in sync with Streamlit secrets (or the local-dev defaults).

    * creates it if missing, makes sure it has the admin role
    * if the password in secrets changed, the stored hash is updated
    * once real secrets are configured, the well-known default admin account is deleted
    """
    email, pwd, using_defaults = config.admin_credentials()
    existing = db.get_user_by_email(email)
    h, s = hash_password(pwd)
    if existing is None:
        db.create_user("Administrator", email, h, s, role="admin")
    else:
        if existing["role"] != "admin":
            db.set_role(existing["id"], "admin")
        if not verify_password(pwd, existing["password_hash"], existing["salt"]):
            db.update_password(existing["id"], h, s)

    if not using_defaults and email != config.DEFAULT_ADMIN_EMAIL:
        default = db.get_user_by_email(config.DEFAULT_ADMIN_EMAIL)
        if default:
            db.delete_user(default["id"])
