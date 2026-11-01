"""SQLite storage for users and prediction logs (no X-ray images are ever stored)."""
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

import config

DB_PATH = config.BASE_DIR / "data" / "app.db"


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


@contextmanager
def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init_db():
    with connect() as con:
        con.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt          TEXT NOT NULL,
                role          TEXT NOT NULL DEFAULT 'user',
                created_at    TEXT NOT NULL,
                last_login    TEXT
            );
            CREATE TABLE IF NOT EXISTS predictions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                filename    TEXT,
                label       TEXT NOT NULL,
                confidence  REAL NOT NULL,
                p_fractured REAL NOT NULL,
                created_at  TEXT NOT NULL
            );
            """
        )


# ───────────── users ─────────────
def create_user(name, email, password_hash, salt, role="user"):
    with connect() as con:
        cur = con.execute(
            "INSERT INTO users (name,email,password_hash,salt,role,created_at) VALUES (?,?,?,?,?,?)",
            (name, email, password_hash, salt, role, now()),
        )
        return cur.lastrowid


def get_user_by_email(email):
    with connect() as con:
        row = con.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None


def touch_login(user_id):
    with connect() as con:
        con.execute("UPDATE users SET last_login = ? WHERE id = ?", (now(), user_id))


def list_users():
    with connect() as con:
        rows = con.execute(
            """SELECT u.id, u.name, u.email, u.role, u.created_at, u.last_login,
                      (SELECT COUNT(*) FROM predictions p WHERE p.user_id = u.id) AS scans
               FROM users u ORDER BY u.id"""
        ).fetchall()
        return [dict(r) for r in rows]


def update_password(user_id, password_hash, salt):
    with connect() as con:
        con.execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (password_hash, salt, user_id))


def set_role(user_id, role):
    with connect() as con:
        con.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))


def delete_user(user_id):
    with connect() as con:
        con.execute("DELETE FROM users WHERE id = ?", (user_id,))


# ───────────── predictions ─────────────
def log_prediction(user_id, filename, label, confidence, p_fractured):
    with connect() as con:
        con.execute(
            "INSERT INTO predictions (user_id,filename,label,confidence,p_fractured,created_at) VALUES (?,?,?,?,?,?)",
            (user_id, filename, label, float(confidence), float(p_fractured), now()),
        )


def list_predictions(user_id=None, limit=1000):
    q = """SELECT p.id, u.name AS user, u.email, p.filename, p.label,
                  p.confidence, p.p_fractured, p.created_at
           FROM predictions p JOIN users u ON u.id = p.user_id"""
    args = []
    if user_id is not None:
        q += " WHERE p.user_id = ?"
        args.append(user_id)
    q += " ORDER BY p.id DESC LIMIT ?"
    args.append(limit)
    with connect() as con:
        return [dict(r) for r in con.execute(q, args).fetchall()]


def clear_predictions():
    with connect() as con:
        con.execute("DELETE FROM predictions")


def stats():
    with connect() as con:
        g = lambda q: con.execute(q).fetchone()[0]
        return {
            "users": g("SELECT COUNT(*) FROM users"),
            "admins": g("SELECT COUNT(*) FROM users WHERE role='admin'"),
            "predictions": g("SELECT COUNT(*) FROM predictions"),
            "fractured": g("SELECT COUNT(*) FROM predictions WHERE label='fractured'"),
            "not_fractured": g("SELECT COUNT(*) FROM predictions WHERE label='not fractured'"),
            "avg_conf": g("SELECT COALESCE(AVG(confidence),0) FROM predictions"),
            "last7": g("SELECT COUNT(*) FROM predictions WHERE created_at >= datetime('now','-7 days')"),
            "new_users7": g("SELECT COUNT(*) FROM users WHERE created_at >= datetime('now','-7 days')"),
        }
