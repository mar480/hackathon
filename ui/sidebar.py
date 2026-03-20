import streamlit as st
from models.job_options import JobOptions


def render_sidebar() -> JobOptions:
    st.sidebar.header("Options")

    action = st.sidebar.selectbox(
        "Action",
        options=["facts_table", "validate"],
        index=0,
    )

    disclosure_system = "none"
    label_lang = "en"
    include_dimensions = True

    if action == "validate":
        disclosure_system = st.sidebar.selectbox(
            "Disclosure system",
            options=["esef", "hmrc"],
            index=0,
        )
    else:
        label_lang = st.sidebar.selectbox(
            "Label language",
            options=["en", "cy"],
            index=0,
        )

        include_dimensions = st.sidebar.checkbox(
            "Include dimensions",
            value=True,
        )

    plugins = st.sidebar.text_input(
        "Plugins (optional)",
        value="",
        help="Comma-separated Arelle plugin names or paths if needed.",
    )

    return JobOptions(
        action=action,
        disclosure_system=disclosure_system,
        plugins=plugins or None,
        formula=False,
        label_lang=label_lang,
        include_dimensions=include_dimensions,
    )