import pandas as pd
import streamlit as st

import config
from core.ui import disclaimer, html, page_header


def render():
    page_header(
        "Model results",
        "Every number behind the model, including the weak spots.",
        "All values come from the training notebook: 1,000 training, 200 validation and 300 held-out test X-rays.",
    )

    cm = config.CONFUSION
    rec_f = cm[0][0] / sum(cm[0])
    html(
        f"""<div class="gz-kpis">
        <div class="gz-kpi"><small>Test accuracy</small><b>{config.TEST_ACCURACY:.0%}</b><span>300 unseen X-rays</span></div>
        <div class="gz-kpi"><small>Validation accuracy</small><b>{config.FINAL_VAL_ACC:.1%}</b><span>after epoch 6</span></div>
        <div class="gz-kpi"><small>Training accuracy</small><b>{config.FINAL_TRAIN_ACC:.1%}</b><span>after epoch 6</span></div>
        <div class="gz-kpi"><small>Fracture recall</small><b>{rec_f:.0%}</b><span>{cm[0][0]} of {sum(cm[0])} fractures found</span></div></div>"""
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        html('<div class="gz-eyebrow">Training curve</div>')
        st.image(str(config.ASSETS / "training_curve.png"), width="stretch")
        st.caption("Validation accuracy stays above training accuracy because dropout and augmentation are active only while training.")
    with c2:
        html('<div class="gz-eyebrow">Confusion matrix</div>')
        st.image(str(config.ASSETS / "confusion_matrix.png"), width="stretch")
        st.caption(f"{cm[0][1]} fractures were missed (false negatives) and {cm[1][0]} healthy X-rays were flagged (false positives).")

    html('<div class="gz-section" style="padding-top:50px"><div class="gz-eyebrow">Classification report</div></div>')
    rep = pd.DataFrame(config.CLASS_REPORT).T
    rep.loc["accuracy"] = [config.TEST_ACCURACY, config.TEST_ACCURACY, config.TEST_ACCURACY, 300]
    rep.columns = ["Precision", "Recall", "F1-score", "Support"]
    rep["Support"] = rep["Support"].astype(int)
    st.dataframe(rep.style.format({"Precision": "{:.2f}", "Recall": "{:.2f}", "F1-score": "{:.2f}"}), width="stretch")

    html('<div class="gz-section" style="padding-top:50px"><div class="gz-eyebrow">Epoch by epoch</div></div>')
    log = pd.DataFrame(config.EPOCH_LOG).set_index("Epoch")
    a, b = st.columns(2, gap="large")
    with a:
        st.line_chart(log[["Train acc", "Val acc"]], height=280)
    with b:
        st.line_chart(log[["Train loss", "Val loss"]], height=280)
    st.dataframe(log.style.format("{:.4f}"), width="stretch")

    html(
        """<div class="gz-section" style="padding-top:50px"><div class="gz-eyebrow">Architecture &amp; training setup</div>
        <div class="gz-grid3" style="margin-top:14px">
        <div class="gz-card"><h3>Model</h3><p>Input 224×224×3 → RandomFlip → RandomRotation(0.08) → Rescaling(1/127.5, −1) →
        <b>MobileNetV2</b> (ImageNet, frozen) → GlobalAveragePooling → Dropout(0.3) → Dense(1, sigmoid)</p></div>
        <div class="gz-card"><h3>Training</h3><p>Adam optimizer, binary cross-entropy, batch size 32, 6 epochs, seed 42.
        Only the classification head is trained, the backbone stays frozen.</p></div>
        <div class="gz-card"><h3>Data</h3><p>Kaggle “Fracture Multi-Region X-ray Data”. Balanced subset:
        500 / 100 / 150 images per class for train / validation / test. Corrupted files are skipped.</p></div></div></div>"""
    )

    html('<div class="gz-section" style="padding-top:50px"><div class="gz-eyebrow">Honest limitations</div></div>')
    st.markdown(
        "- Trained on only **1,000 images for 6 epochs** with a frozen backbone, so there is clear room to improve (fine-tuning, more data, more epochs).\n"
        f"- It misses about **{cm[0][1] / sum(cm[0]):.0%}** of real fractures. That is far too many for clinical use.\n"
        "- The dataset mixes several body regions, so the model learns a general “fracture look” rather than region-specific rules.\n"
        "- It cannot tell whether an uploaded image is actually an X-ray. Non-X-ray images will still receive a prediction."
    )
    html('<div style="height:10px"></div>')
    disclaimer()
