import pandas as pd
import streamlit as st

import config
from core import db
from core.model import model_status
from core.ui import current_user, html, is_admin, page_header


def _kpis(s):
    fr = (s["fractured"] / s["predictions"]) if s["predictions"] else 0
    html(
        f"""<div class="gz-kpis">
        <div class="gz-kpi"><small>Registered users</small><b>{s['users']}</b><span>{s['new_users7']} new in the last 7 days</span></div>
        <div class="gz-kpi"><small>Total scans</small><b>{s['predictions']}</b><span>{s['last7']} in the last 7 days</span></div>
        <div class="gz-kpi"><small>Fracture rate</small><b>{fr:.0%}</b><span>{s['fractured']} fractured · {s['not_fractured']} not fractured</span></div>
        <div class="gz-kpi"><small>Avg. confidence</small><b>{s['avg_conf']:.0%}</b><span>across all predictions</span></div></div>"""
    )


def render():
    if not is_admin():
        st.error("This area is for administrators only.")
        return

    me = current_user()
    page_header("Admin dashboard", "Everything happening in the app, at a glance.",
                f"Signed in as {me['email']}.")

    _, _, using_defaults = config.admin_credentials()
    if using_defaults:
        st.warning(
            "You are using the **default admin password**. Add your own `[admin]` email and password in "
            "Streamlit → App settings → Secrets (see README) and reboot the app."
        )

    t_over, t_users, t_pred, t_sys = st.tabs(["Overview", "Users", "Predictions", "System"])

    # ───────── Overview ─────────
    with t_over:
        s = db.stats()
        _kpis(s)
        preds = db.list_predictions(limit=5000)
        if preds:
            df = pd.DataFrame(preds)
            df["created_at"] = pd.to_datetime(df["created_at"])
            df["date"] = df["created_at"].dt.date
            c1, c2 = st.columns(2, gap="large")
            with c1:
                html('<div class="gz-eyebrow" style="margin-top:14px">Scans per day</div>')
                st.bar_chart(df.groupby("date").size().rename("Scans"), height=280)
            with c2:
                html('<div class="gz-eyebrow" style="margin-top:14px">Result split</div>')
                st.bar_chart(df["label"].value_counts().rename("Scans"), height=280)
            c3, c4 = st.columns(2, gap="large")
            with c3:
                html('<div class="gz-eyebrow" style="margin-top:14px">Confidence over time</div>')
                st.line_chart(df.sort_values("created_at").set_index("created_at")["confidence"], height=260)
            with c4:
                html('<div class="gz-eyebrow" style="margin-top:14px">Most active users</div>')
                st.bar_chart(df["user"].value_counts().head(8).rename("Scans"), height=260)
        else:
            st.info("No scans yet. Charts will appear after the first prediction.")

    # ───────── Users ─────────
    with t_users:
        users = db.list_users()
        udf = pd.DataFrame(users)
        udf.columns = ["ID", "Name", "Email", "Role", "Joined (UTC)", "Last login (UTC)", "Scans"]
        st.dataframe(udf, hide_index=True, width="stretch")

        html('<div class="gz-eyebrow" style="margin-top:26px">Manage a user</div>')
        others = [u for u in users if u["id"] != me["id"]]
        if not others:
            st.info("No other users yet.")
        else:
            labels = {f"{u['name']} · {u['email']} ({u['role']})": u for u in others}
            pick = labels[st.selectbox("Select user", list(labels.keys()))]
            c1, c2, c3 = st.columns(3)
            with c1:
                if pick["role"] == "user":
                    if st.button("Promote to admin", width="stretch"):
                        db.set_role(pick["id"], "admin")
                        st.rerun()
                else:
                    if st.button("Remove admin rights", width="stretch"):
                        db.set_role(pick["id"], "user")
                        st.rerun()
            with c2:
                confirm = st.checkbox("I understand this also deletes their scan history")
            with c3:
                if st.button("Delete user", type="primary", disabled=not confirm, width="stretch"):
                    db.delete_user(pick["id"])
                    st.rerun()

        st.download_button("Download users (CSV)", udf.to_csv(index=False).encode(), "users.csv", "text/csv")

    # ───────── Predictions ─────────
    with t_pred:
        preds = db.list_predictions(limit=10000)
        if not preds:
            st.info("No predictions logged yet.")
        else:
            pdf = pd.DataFrame(preds)
            f1, f2 = st.columns(2)
            with f1:
                lab = st.selectbox("Result", ["All", "fractured", "not fractured"])
            with f2:
                usr = st.selectbox("User", ["All"] + sorted(pdf["email"].unique().tolist()))
            if lab != "All":
                pdf = pdf[pdf["label"] == lab]
            if usr != "All":
                pdf = pdf[pdf["email"] == usr]
            show = pdf[["created_at", "user", "email", "filename", "label", "confidence"]].copy()
            show.columns = ["Time (UTC)", "User", "Email", "File", "Result", "Confidence"]
            st.dataframe(
                show, hide_index=True, width="stretch",
                column_config={"Confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=1, format="percent")},
            )
            st.download_button("Download predictions (CSV)", show.to_csv(index=False).encode(), "predictions.csv", "text/csv")

            html('<div class="gz-eyebrow" style="margin-top:26px">Danger zone</div>')
            ok = st.checkbox("Yes, permanently delete ALL prediction logs")
            if st.button("Clear prediction logs", disabled=not ok):
                db.clear_predictions()
                st.rerun()

    # ───────── System ─────────
    with t_sys:
        ms = model_status()
        c1, c2 = st.columns(2, gap="large")
        with c1:
            html(
                f"""<div class="gz-card"><h3>Model</h3>
                <p>File: <b>{config.MODEL_PATH.name}</b><br>Found: <b>{'yes' if ms['exists'] else 'NO, upload it to /model'}</b><br>
                Size: <b>{ms['size_mb']} MB</b><br>Input: <b>{config.IMG_SIZE}×{config.IMG_SIZE} RGB</b><br>
                Output: <b>sigmoid = P(not fractured)</b><br>Low-confidence threshold: <b>{config.LOW_CONFIDENCE:.0%}</b></p></div>"""
            )
        with c2:
            html(
                f"""<div class="gz-card"><h3>Storage</h3>
                <p>Database: <b>SQLite</b> ({db.DB_PATH.name})<br>Users stored: <b>{len(db.list_users())}</b><br>
                Uploaded images stored: <b>never</b><br>
                <span style="font-size:13px">On Streamlit Community Cloud the disk is reset whenever the app restarts or is redeployed,
                so new sign-ups and logs can disappear. The admin account is re-created automatically.</span></p></div>"""
            )
