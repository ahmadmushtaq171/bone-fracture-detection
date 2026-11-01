import base64

import streamlit as st

import config
from core.ui import go, html

HERO_SVG = """
<svg viewBox="0 0 420 400" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3B5BFF"/><stop offset="1" stop-color="#7C4DFF"/></linearGradient>
    <linearGradient id="g2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7B93FF"/><stop offset="1" stop-color="#A98BFF"/></linearGradient>
    <linearGradient id="g3" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C9D3FF"/><stop offset="1" stop-color="#E2D6FF"/></linearGradient>
    <linearGradient id="side" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A0F1F" stop-opacity=".25"/><stop offset="1" stop-color="#0A0F1F" stop-opacity=".05"/></linearGradient>
  </defs>
  <ellipse cx="210" cy="352" rx="170" ry="26" fill="#3B5BFF" opacity=".10"/>
  <!-- bottom disc -->
  <path d="M60 270 L60 310 A150 48 0 0 0 360 310 L360 270 Z" fill="url(#g3)"/>
  <path d="M60 270 L60 310 A150 48 0 0 0 360 310 L360 270 Z" fill="url(#side)"/>
  <ellipse cx="210" cy="270" rx="150" ry="48" fill="#DCE3FF" stroke="#fff" stroke-width="2"/>
  <!-- middle disc -->
  <path d="M80 200 L80 240 A130 42 0 0 0 340 240 L340 200 Z" fill="url(#g2)"/>
  <path d="M80 200 L80 240 A130 42 0 0 0 340 240 L340 200 Z" fill="url(#side)"/>
  <ellipse cx="210" cy="200" rx="130" ry="42" fill="#9FB0FF" stroke="#fff" stroke-width="2"/>
  <!-- top disc -->
  <path d="M100 130 L100 170 A110 36 0 0 0 320 170 L320 130 Z" fill="url(#g1)"/>
  <path d="M100 130 L100 170 A110 36 0 0 0 320 170 L320 130 Z" fill="url(#side)"/>
  <ellipse cx="210" cy="130" rx="110" ry="36" fill="#5A74FF" stroke="#fff" stroke-width="2"/>
  <!-- scan lines on top disc -->
  <ellipse cx="210" cy="130" rx="78" ry="25" fill="none" stroke="#fff" stroke-opacity=".5" stroke-dasharray="4 6"/>
  <ellipse cx="210" cy="130" rx="44" ry="14" fill="none" stroke="#fff" stroke-opacity=".6"/>
  <text x="210" y="62" text-anchor="middle" font-size="64">🦴</text>
</svg>
"""

HERO_URI = "data:image/svg+xml;base64," + base64.b64encode(HERO_SVG.encode("utf-8")).decode()

TECH = ["TensorFlow", "Keras", "MobileNetV2", "Python", "Streamlit", "NumPy", "scikit-learn", "Matplotlib",
        "Seaborn", "Google Colab", "Kaggle", "Pillow"]


def _marquee():
    pills = "".join(f'<div class="gz-pill">{t}</div>' for t in TECH)
    html(
        f"""<div class="gz-marquee-wrap"><p>Built with an industry-standard deep-learning stack</p>
        <div class="gz-marquee"><div class="gz-track">{pills}{pills}</div></div></div>"""
    )


def render():
    # ───────────────── HERO ─────────────────
    with st.container(key="hero"):
        left, right = st.columns([1.15, 0.85], gap="large", vertical_alignment="center")
        with left:
            html(
                f"""<div class="gz-badge"><i></i> Deep learning · Medical imaging</div>
                <h1 class="gz-h1">We read the X-ray, <em>then flag the fracture</em> in seconds.</h1>
                <p class="gz-lead">{config.APP_NAME} is a convolutional neural network, trained with transfer learning on
                MobileNetV2, that classifies bone X-rays as <b>fractured</b> or <b>not fractured</b>. Upload an image,
                get a confidence score, and audit every metric behind the model.</p>"""
            )
            b1, b2, _ = st.columns([1, 1, 0.8])
            with b1:
                st.button("Try the detector", key="hero_try", type="primary", on_click=go, args=("detector",), width="stretch")
            with b2:
                st.button("View project report", key="hero_report", on_click=go, args=("report",), width="stretch")
            html(
                f"""<div class="gz-stats">
                <div><b>{config.TEST_ACCURACY:.0%}</b><span>Test accuracy</span></div>
                <div><b>{config.FINAL_VAL_ACC:.1%}</b><span>Validation accuracy</span></div>
                <div><b>1,500</b><span>X-rays used</span></div>
                <div><b>224²</b><span>Input size</span></div></div>"""
            )
        with right:
            html(
                f"""<div class="gz-illus"><img src="{HERO_URI}" alt="">
                <div class="gz-chip a">🟢 &nbsp;Not fractured · 91%</div>
                <div class="gz-chip b">🔴 &nbsp;Fractured · 94%</div></div>"""
            )

    _marquee()

    # ───────────────── WHAT WE DO ─────────────────
    html(
        """<div class="gz-section" id="what"><div class="gz-split"><div>
        <div class="gz-eyebrow">What we do</div>
        <h2 class="gz-h2">Most fracture workflows don't have an imaging problem. They have a speed problem.</h2>
        <p class="gz-p">Radiologists are overloaded and a second pair of eyes is not always available. We built a deep-learning
        classifier that screens a bone X-ray in under a second and tells you how sure it is, so the cases that need a human
        look reach one faster.</p>
        <p class="gz-p">We start with the data, because a clever model on dirty data just fails faster. Every image is validated,
        the classes are balanced, and every number on this site comes straight from the training notebook.</p></div>
        <div class="gz-flow">
          <div class="row"><span>🩻</span>Upload X-ray<small>JPG / PNG</small></div>
          <div class="row"><span>⚙️</span>Resize to 224 × 224<small>RGB</small></div>
          <div class="row"><span>🧠</span>MobileNetV2 features<small>ImageNet weights</small></div>
          <div class="row"><span>📊</span>Sigmoid probability<small>0 → 1</small></div>
          <div class="row"><span>✅</span>Verdict + confidence<small>in seconds</small></div>
        </div></div></div>"""
    )
    st.button("See how it works ↓", key="what_btn", on_click=go, args=("results",))

    # ───────────────── PRINCIPLES ─────────────────
    html(
        """<div class="gz-section"><div class="gz-eyebrow">Principles</div>
        <h2 class="gz-h2">Why the model actually works</h2>
        <div class="gz-grid4">
        <div class="gz-card"><div class="gz-num"><span>01</span><span>🧱</span></div>
          <h3>Transfer learning is the backbone</h3>
          <p>A frozen MobileNetV2 pre-trained on ImageNet already knows edges, textures and shapes. We only train the small classification head, so 1,000 images are enough.</p></div>
        <div class="gz-card"><div class="gz-num"><span>02</span><span>🔄</span></div>
          <h3>Augment the data, not the effort</h3>
          <p>Random horizontal flips and ±8% rotations are built into the model, so every epoch sees slightly different images and overfitting stays low.</p></div>
        <div class="gz-card"><div class="gz-num"><span>03</span><span>📐</span></div>
          <h3>Metrics you can audit</h3>
          <p>Confusion matrix, precision, recall and F1 on a held-out set of 300 unseen X-rays. No cherry-picked numbers, including the weak spots.</p></div>
        <div class="gz-card"><div class="gz-num"><span>04</span><span>⚡</span></div>
          <h3>Light enough to run anywhere</h3>
          <p>MobileNetV2 is built for speed. The whole model is under 10 MB and predicts on a CPU, which is why it can live in a free web app.</p></div>
        </div></div>"""
    )

    # ───────────────── HOW IT WORKS ─────────────────
    html(
        """<div class="gz-section"><div class="gz-eyebrow">How it works</div>
        <h2 class="gz-h2">How we put this to work</h2>
        <div class="gz-grid4">
        <div class="gz-step"><div class="big">01</div><h3>UPLOAD</h3><p>You sign in and drop in a bone X-ray as a JPG or PNG image.</p></div>
        <div class="gz-step"><div class="big">02</div><h3>PREPROCESS</h3><p>The image is converted to RGB and resized to 224 × 224 exactly like the training data.</p></div>
        <div class="gz-step"><div class="big">03</div><h3>PREDICT</h3><p>The CNN outputs one probability. Above 0.5 means not fractured, below means fractured.</p></div>
        <div class="gz-step"><div class="big">04</div><h3>REVIEW</h3><p>You get the verdict, the confidence and a clear warning when the model is unsure.</p></div>
        </div></div>"""
    )

    # ───────────────── WHY ─────────────────
    html(
        """<div class="gz-dark"><div class="gz-eyebrow">Why this project</div>
        <h2 class="gz-h2">Most student projects end at a notebook. This one ships.</h2>
        <p class="gz-p">One product instead of five loose files: a trained model, a secure login, an admin dashboard with live usage
        analytics, the full project report and the final presentation, all in one place.</p></div>"""
    )
    c1, _ = st.columns([1, 3])
    with c1:
        st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
        st.button("Create a free account", key="why_btn", type="primary", on_click=go, args=("signup",))

    # ───────────────── WHAT WE BUILD ─────────────────
    html(
        """<div class="gz-section"><div class="gz-eyebrow">What we built</div>
        <h2 class="gz-h2">One project for every part of the system</h2>
        <div class="gz-list">
        <div class="gz-li"><div class="n">01</div><div class="t">Fracture Detector</div><div class="d">Upload an X-ray, get a verdict with a confidence bar and a personal scan history.</div></div>
        <div class="gz-li"><div class="n">02</div><div class="t">Model Results</div><div class="d">Training curve, confusion matrix, classification report and epoch-by-epoch logs.</div></div>
        <div class="gz-li"><div class="n">03</div><div class="t">Project Report</div><div class="d">The full written report, readable right here with a one-click download.</div></div>
        <div class="gz-li"><div class="n">04</div><div class="t">Presentation</div><div class="d">The final slide deck embedded in the app, ready for the viva.</div></div>
        <div class="gz-li"><div class="n">05</div><div class="t">Login &amp; Sign-up</div><div class="d">Salted PBKDF2 password hashing and role-based access (user / admin).</div></div>
        <div class="gz-li"><div class="n">06</div><div class="t">Admin Dashboard</div><div class="d">Users, scans, fracture rate, confidence trends, CSV export and user management.</div></div>
        </div></div>"""
    )

    # ───────────────── CASE CARDS ─────────────────
    html(
        """<div class="gz-section"><div class="gz-eyebrow">Under the hood</div>
        <h2 class="gz-h2">Real pipeline. Real numbers.</h2>
        <div class="gz-grid3">
        <div class="gz-case"><span class="gz-tag">Data</span><h3>Fracture Multi-Region X-ray</h3>
          <h5>The problem</h5><p>Raw X-ray datasets are large, unbalanced and contain corrupt files that crash training.</p>
          <h5>What we built</h5><p>A loader that validates every image and samples a balanced, seeded subset: 500 / 100 / 150 per class for train / val / test.</p>
          <div class="gz-metric"><div><small>Images used</small><b>Raw dump <i>→</i> 1,500 balanced</b></div></div></div>
        <div class="gz-case"><span class="gz-tag">Model</span><h3>MobileNetV2 + custom head</h3>
          <h5>The problem</h5><p>Training a CNN from scratch needs hundreds of thousands of images and a lot of GPU time.</p>
          <h5>What we built</h5><p>A frozen ImageNet backbone with global pooling, 30% dropout and a single sigmoid unit, trained for 6 epochs with Adam.</p>
          <div class="gz-metric"><div><small>Validation accuracy</small><b>74% <i>→</i> 84.5%</b></div></div></div>
        <div class="gz-case"><span class="gz-tag">Deployment</span><h3>From Colab to the browser</h3>
          <h5>The problem</h5><p>A notebook is not a product. Nobody else can use it, and nobody can see who used it.</p>
          <h5>What we built</h5><p>This Streamlit app: authentication, a live detector, an admin analytics dashboard, the report and the presentation.</p>
          <div class="gz-metric"><div><small>Time to a result</small><b>Run a notebook <i>→</i> a few seconds</b></div></div></div>
        </div></div>"""
    )

    # ───────────────── FAQ ─────────────────
    html(
        """<div class="gz-section"><div class="gz-eyebrow">FAQ</div>
        <h2 class="gz-h2">The questions we hear most.</h2></div>"""
    )
    faqs = [
        ("How accurate is the model?",
         f"On 300 unseen test X-rays it scored {config.TEST_ACCURACY:.0%} accuracy. It finds 78% of real fractures (recall) and is right 74% of the time when it says 'fractured'. That is a solid result for a small, fast transfer-learning model, but far below clinical standards."),
        ("Can I use it for a real diagnosis?",
         "No. This is an educational prototype. Always have a qualified doctor or radiologist read the X-ray. The detector is a demonstration of deep learning, not a medical device."),
        ("What data was it trained on?",
         "The public 'Fracture Multi-Region X-ray Data' dataset from Kaggle. We used 1,000 images for training, 200 for validation and 300 for testing, balanced between the two classes."),
        ("Are my uploaded X-rays stored?",
         "No. The image is processed in memory and discarded. Only the result (label, confidence, file name and time) is saved so you can see your own history."),
        ("What happens if the model is unsure?",
         f"When the winning class has less than {config.LOW_CONFIDENCE:.0%} confidence the app labels the result as inconclusive instead of pretending to be certain."),
        ("What is the admin dashboard?",
         "A protected area for administrators showing total users, scans, the fracture-vs-normal split, confidence trends, and tools to manage accounts and export data."),
    ]
    for q, a in faqs:
        with st.expander(q):
            st.write(a)

    # ───────────────── CTA ─────────────────
    html(
        """<div class="gz-dark" style="margin-top:70px"><div class="gz-eyebrow">Get started</div>
        <h2 class="gz-h2">Let's put deep learning to work on an X-ray.</h2>
        <p class="gz-p">Create an account in under a minute and run your first scan.</p></div>"""
    )
    c1, c2, _ = st.columns([1, 1, 3])
    with c1:
        st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
        st.button("Sign up free", key="cta_signup", type="primary", on_click=go, args=("signup",), width="stretch")
    with c2:
        st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
        st.button("See the presentation", key="cta_pres", on_click=go, args=("presentation",), width="stretch")
