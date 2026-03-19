import streamlit as st
from models.job_options import JobOptions


def render_sidebar() -> JobOptions:
    st.sidebar.header("Options")

    action = st.sidebar.selectbox(
        "Action",
        options=["validate", "facts_table"],
        index=0,
    )

    disclosure_system = st.sidebar.selectbox(
        "Disclosure system",
        options=["none", "hmrc", "esef"],
        index=0,
    )

    plugins = st.sidebar.text_input(
        "Plugins (optional)",
        value="",
        help="Comma-separated Arelle plugin names or paths if needed.",
    )

    formula = st.sidebar.checkbox("Run formula processing", value=False)

    label_lang = st.sidebar.selectbox(
        "Label language",
        options=["en", "en-GB", "cy"],
        index=0,
    )

    include_dimensions = st.sidebar.checkbox("Include dimensions", value=True)

    return JobOptions(
        action=action,
        disclosure_system=disclosure_system,
        plugins=plugins or None,
        formula=formula,
        label_lang=label_lang,
        include_dimensions=include_dimensions,
    )