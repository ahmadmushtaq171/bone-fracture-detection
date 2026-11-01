import pandas as pd
import streamlit as st
from PIL import Image

import config
from core import db
from core.ui import current_user, disclaimer, html, page_header


def _result_card(res: dict):
    if res["inconclusive"]:
        cls, verdict, note = "warn", "Inconclusive", (
            f"The model is only {res['confidence']:.0%} sure, which is below our {config.LOW_CONFIDENCE:.0%} threshold. "
            "Treat this as unreliable and ask a professional to review the image.")
    elif res["is_fractured"]:
        cls, verdict, note = "bad", "Fractured", (
            "The model sees patterns consistent with a fracture. Please have a doctor confirm with a proper clinical review.")
    else:
        cls, verdict, note = "ok", "Not fractured", (
            "The model sees no fracture pattern. A negative result does not rule out a fracture, "
            "since this model misses roughly 1 in 5 real ones.")
    pf, pn = res["probs"]["fractured"], res["probs"]["not fractured"]
    html(
        f"""<div class="gz-result {cls}"><div class="lbl">AI verdict</div>
        <div class="verdict">{verdict}</div>
        <div style="font-size:15px;color:var(--muted);margin-bottom:22px">Confidence <b style="color:var(--ink)">{res['confidence']:.1%}</b></div>
        <div class="gz-prob"><span>Fractured</span><span>{pf:.1%}</span></div>
        <div class="gz-bar f"><div style="width:{pf*100:.1f}%"></div></div>
        <div class="gz-prob"><span>Not fractured</span><span>{pn:.1%}</span></div>
        <div class="gz-bar n"><div style="width:{pn*100:.1f}%"></div></div>
        <div class="gz-note">{note}</div></div>"""
    )


def render():
    user = current_user()
    page_header(
        "AI Detector",
        "Upload an X-ray. Get a second opinion in seconds.",
        f"Welcome back, {user['name'].split()[0]}. Supported formats: JPG, JPEG, PNG (max 10 MB).",
    )

    left, right = st.columns(2, gap="large")
    with left:
        file = st.file_uploader("X-ray image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        img = None
        if file is not None:
            try:
                img = Image.open(file)
                img.load()
            except Exception:
                st.error("That file could not be read as an image. Please upload a valid JPG or PNG.")
                img = None
        if img is not None:
            st.image(img, caption=f"{file.name} · {img.width}×{img.height}px", width="stretch")
        analyze = st.button("Analyze X-ray", type="primary", disabled=img is None, width="stretch")

    sig = f"{file.name}:{file.size}" if file is not None else None
    if analyze and img is not None:
        try:
            from core import model

            with st.spinner("Analyzing…"):
                res = model.predict(img)
            db.log_prediction(user["id"], file.name, res["label"], res["confidence"], res["p_fractured"])
            st.session_state.last_result = {"sig": sig, "res": res}
        except FileNotFoundError as e:
            st.error(f"{e}. Make sure the model folder was uploaded to GitHub.")
        except Exception as e:  # noqa: BLE001
            st.error(f"Prediction failed: {e}")

    with right:
        last = st.session_state.get("last_result")
        if last and last["sig"] == sig and sig is not None:
            _result_card(last["res"])
        else:
            html(
                """<div class="gz-result" style="min-height:360px;display:grid;place-items:center;text-align:center">
                <div><div style="font-size:54px">🩻</div>
                <div class="verdict" style="font-size:26px;font-family:var(--font-head);font-weight:800;letter-spacing:-.03em;margin-top:10px">Your result appears here</div>
                <p style="color:var(--muted);margin-top:8px">Upload an image on the left, then press <b>Analyze X-ray</b>.</p></div></div>"""
            )

    html('<div style="height:26px"></div>')
    disclaimer()

    # ───── personal history ─────
    html('<div class="gz-section" style="padding-top:60px"><div class="gz-eyebrow">History</div><h2 class="gz-h2" style="font-size:30px">Your recent scans</h2></div>')
    rows = db.list_predictions(user_id=user["id"], limit=50)
    if rows:
        df = pd.DataFrame(rows)[["created_at", "filename", "label", "confidence"]]
        df.columns = ["Time (UTC)", "File", "Result", "Confidence"]
        st.dataframe(
            df, hide_index=True, width="stretch",
            column_config={"Confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=1, format="percent")},
        )
    else:
        st.info("No scans yet. Your results will be listed here.")
