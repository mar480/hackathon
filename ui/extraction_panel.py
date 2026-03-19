import streamlit as st
from services.fact_table_service import FactTableResult


def render_fact_table_result(result: FactTableResult):
    if result.ok:
        st.success(f"Extracted {result.row_count} facts.")
    else:
        st.error(result.error or "Fact extraction failed.")
        return

    st.dataframe(result.dataframe, use_container_width=True)

    csv_bytes = result.dataframe.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download fact table CSV",
        data=csv_bytes,
        file_name="fact_table_enriched.csv",
        mime="text/csv",
    )