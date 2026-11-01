"""Shared helper: show a Google Drive document or slide deck inside the app."""
import streamlit as st
import streamlit.components.v1 as components

import config
from core.ui import html, page_header


def show(*, eyebrow, title, subtitle, file_id, source_url, kind, height=780):
    page_header(eyebrow, title, subtitle)

    a, b, c, _ = st.columns([1, 1, 1, 2])
    with a:
        st.link_button("Open in Google Drive", source_url, width="stretch")
    with b:
        st.link_button("Download", config.drive_download(file_id), width="stretch")
    with c:
        st.link_button("Full-screen viewer", config.drive_preview(file_id), width="stretch")

    alt_name = "Google Docs viewer" if kind == "doc" else "Google Slides viewer"
    alt_url = (
        f"https://docs.google.com/document/d/{file_id}/preview" if kind == "doc"
        else f"https://docs.google.com/presentation/d/{file_id}/embed?start=false&loop=false&delayms=3000"
    )
    default_name = "Drive viewer (recommended)"
    options = {default_name: config.drive_preview(file_id), alt_name: alt_url}
    key = f"viewer_{kind}"
    with st.expander("Viewer not loading?"):
        st.write(
            "1. In Google Drive, right-click the file → **Share** → set *General access* to **Anyone with the link (Viewer)**.\n"
            "2. Try the alternate viewer below.\n"
            "3. If your browser blocks third-party content, use the **Open in Google Drive** button."
        )
        st.selectbox("Viewer", list(options.keys()), key=key)
    src = options[st.session_state.get(key, default_name)]

    html('<div style="height:14px"></div>')
    components.iframe(src, height=height, scrolling=True)
