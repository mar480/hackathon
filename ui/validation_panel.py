import streamlit as st
from services.validation_service import ValidationResult


def render_validation_result(result: ValidationResult):
    if result.ok:
        st.success("Validation completed.")
    else:
        st.error("Validation finished with errors or non-zero exit code.")

    with st.expander("Arelle command output"):
        st.code(" ".join(result.run_result.command), language="bash")
        st.subheader("stdout")
        st.text(result.run_result.stdout or "(empty)")
        st.subheader("stderr")
        st.text(result.run_result.stderr or "(empty)")

    st.subheader("Validation log")
    st.text_area("Log", value=result.log_text, height=350)

    if result.log_file_path.exists():
        st.download_button(
            "Download validation log",
            data=result.log_file_path.read_bytes(),
            file_name="validation.log",
            mime="text/plain",
        )