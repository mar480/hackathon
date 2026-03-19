import streamlit as st


def render_uploader():
    return st.file_uploader(
        "Upload XBRL, iXBRL, XML, or ZIP",
        type=["xhtml", "html", "htm", "xml", "xbrl", "zip"],
        accept_multiple_files=False,
    )