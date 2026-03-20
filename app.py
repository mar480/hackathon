from pathlib import Path
import streamlit as st

from config.settings import OUTPUT_DIR
from models.job_options import JobOptions
from services.arelle_runner import ArelleRunner
from services.validation_service import ValidationService
from services.fact_table_service import FactTableService
from ui.sidebar import render_sidebar
from ui.upload_panel import render_uploader
from ui.validation_panel import render_validation_result
from ui.extraction_panel import render_fact_table_result
from utils.files import validate_uploaded_file
from utils.temp_workspace import temp_workspace


st.set_page_config(
    page_title="FRC Hackathon Arelle",
    layout="wide",
    page_icon = r"ui\img\favicon.png",
)

OUTPUT_DIR.mkdir(exist_ok=True)

st.title("FRC Hackathon Arelle")
st.caption("Upload a filing, extract facts or validate, and download the result.")

options: JobOptions = render_sidebar()
uploaded_file = render_uploader()

runner = ArelleRunner()
validation_service = ValidationService(runner)
fact_table_service = FactTableService()

if uploaded_file is not None:
    errors = validate_uploaded_file(uploaded_file)

    if errors:
        for error in errors:
            st.error(error)
    else:
        st.info(f"Ready to process: {uploaded_file.name}")

        if st.button("Run"):
            with st.spinner("Processing with Arelle..."):
                with temp_workspace() as workspace:
                    input_path = workspace / uploaded_file.name
                    input_path.write_bytes(uploaded_file.getvalue())

                    if options.action == "validate":
                        result = validation_service.validate(
                            file_path=input_path,
                            workspace=workspace,
                            options=options,
                        )
                        render_validation_result(result)

                    elif options.action == "facts_table":
                        result = fact_table_service.build_fact_table(
                            file_path=input_path,
                            options=options,
                        )
                        render_fact_table_result(result)

                    else:
                        st.error(f"Unsupported action: {options.action}")
else:
    st.write("Upload a file to begin.")