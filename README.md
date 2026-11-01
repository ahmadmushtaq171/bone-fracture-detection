# 🦴 BoneScan AI: Bone Fracture Detection (Deep Learning Project)

A Streamlit web app around a MobileNetV2 transfer-learning model that classifies bone X-rays as **fractured** or **not fractured**.

**Features:** landing page · AI detector · model results (training curve, confusion matrix, metrics) · embedded project report · embedded presentation · sign-up / login · admin dashboard.

> ⚠️ Educational prototype (≈75 % test accuracy). Not a medical device.

---

## 1. Folder structure

```
bone-fracture-detection/
├── app.py                      ← entry point
├── config.py                   ← YOUR DETAILS + links + metrics
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── core/
│   ├── __init__.py
│   ├── db.py                   ← SQLite (users, prediction logs)
│   ├── auth.py                 ← signup / login / hashing
│   ├── model.py                ← model loading + prediction
│   ├── styles.py               ← all CSS (colours & fonts at the top)
│   └── ui.py                   ← navbar, footer, helpers
├── views/
│   ├── __init__.py
│   ├── home.py  detector.py  results.py
│   ├── report.py  presentation.py  _embed.py
│   ├── login.py  admin.py
├── model/
│   ├── bone_fracture_model.keras   ← binary: upload with "Upload files"
│   └── class_names.json
└── assets/
    ├── training_curve.png          ← binary
    └── confusion_matrix.png        ← binary
```

## 2. Before you upload: edit `config.py`

Change `STUDENT_NAME`, `UNIVERSITY`, `COURSE`, `CONTACT_EMAIL` and `GITHUB_URL`.

## 3. Create the GitHub repository

1. Go to <https://github.com> and sign in (or **Sign up**).
2. Click the **+** (top-right) → **New repository**.
3. Repository name: `bone-fracture-detection` · choose **Public** · tick nothing else → **Create repository**.
4. **Easiest way:** unzip the project, then on the new repo page click **uploading an existing file**, drag in **everything inside the folder** (keep the sub-folders), write a commit message and click **Commit changes**.
   - GitHub accepts up to 100 files per upload and 25 MB per file, so the 9.6 MB model is fine.
   - Hidden folders (`.streamlit`) sometimes don't drag in from Windows/Mac. If so, use *Add file → Create new file*, type `.streamlit/config.toml` as the name (typing `/` makes a folder) and paste the contents.
5. **Or file by file:** *Add file → Create new file*, type the path (e.g. `core/db.py`), paste the code, **Commit**. The three binary files (`.keras`, two `.png`) must go through **Add file → Upload files**.

## 4. Share your Google Drive files

Report and presentation must be viewable by anyone with the link:
Drive → right-click file → **Share** → *General access* → **Anyone with the link** → **Viewer**.

## 5. Deploy on Streamlit Community Cloud (free)

1. Open <https://share.streamlit.io> → **Continue with GitHub** and authorise.
2. **Create app** → *Deploy a public app from GitHub*.
3. Repository: `your-username/bone-fracture-detection` · Branch: `main` · Main file path: `app.py`.
4. Click **Advanced settings**:
   - **Python version:** `3.12` (TensorFlow needs 3.10–3.13).
   - **Secrets:** paste

     ```toml
     [admin]
     email = "your-admin-email@example.com"
     password = "a-strong-password"
     ```
5. **Deploy**. The first build takes a few minutes because TensorFlow is large.
6. Log in with the admin email and password above to open the **Admin** tab.

## 6. Run locally (optional, recommended before deploying)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

With no secrets file the admin login is `admin@bonescan.app` / `Admin@12345` (local testing only).

## 7. Things worth knowing

- **User data resets on Streamlit Cloud.** The free tier has a temporary disk, so accounts and scan logs created through the app disappear when the app restarts or you redeploy. The admin account is rebuilt from your secrets automatically. For permanent storage, swap `core/db.py` for a hosted database (Supabase, Neon, Firebase).
- **Logging in again after a browser refresh** is normal: sessions live in memory.
- **X-ray images are never stored**, only label, confidence, file name and time.
- **Model facts the code relies on** (from your notebook): input is raw 0–255 RGB at 224×224 (the model rescales internally); the single sigmoid output is the probability of `class_names[1]` = **"not fractured"**.
- **Re-skinning:** all colours and fonts are CSS variables at the top of `core/styles.py`.
- **Make Report/Presentation login-only** (or the detector public) by editing `REQUIRE_LOGIN` in `config.py`.
- `bone_fracture_weights.h5` is not needed, the `.keras` file already contains the weights.
