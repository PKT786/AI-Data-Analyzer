"""
=========================================================
AI Data Analyzer Pro
Reports
Author : Punit Tech Hub
Version : 2.0
=========================================================
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import streamlit as st

from components.report_builder import report_builder

from utils.logger import get_logger
from utils.session_manager import session_manager

logger = get_logger(__name__)

# =====================================================
# PAGE CONFIGURATION
# =====================================================

import auth
auth.require_login()

# =====================================================
# PAGE INITIALIZATION
# =====================================================

def initialize_page() -> None:
    """
    Initialize Reports page.
    """

    st.title("📄 Reports")

    st.caption(
        """
        Generate professional reports containing
        AI insights, dashboard summaries and
        dataset analysis.
        """
    )

    st.divider()

    logger.info(
        "Reports page initialized."
    )


# =====================================================
# LOAD REPORT DATA
# =====================================================

def load_report_data() -> Optional[Dict[str, Any]]:
    """
    Load all required report data.
    """

    # The Upload Data / Data Cleaning pages store the working dataframe
    # under st.session_state.cleaned_df (falling back to .dataset for a
    # dataset that hasn't been through the cleaning step yet).
    dataset = st.session_state.get("cleaned_df")

    if dataset is None:

        dataset = st.session_state.get("dataset")

    # The AI Insights page stores its output as a DashboardResult under
    # st.session_state.dashboard_result.
    dashboard_result = st.session_state.get("dashboard_result")

    insights = dashboard_result.executive_summary if dashboard_result else None

    dashboard = dashboard_result.dashboard if dashboard_result else None

    dataset_info = None

    if dataset is not None:

        dataset_info = {
            "rows": len(dataset),
            "columns": len(dataset.columns),
        }

    if dataset is None:

        st.warning(

            """
            No dataset available.

            Please upload and analyze
            a dataset first.
            """

        )

        logger.warning(
            "Dataset unavailable for reports."
        )

        return None

    return {

        "dataset": dataset,

        "insights": insights,

        "dashboard": dashboard,

        "dataset_info": dataset_info,

    }


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def generated_report() -> Any:
    """
    Return generated report from session.
    """

    return session_manager.get(
        "generated_report"
    )


# -----------------------------------------------------

def report_available() -> bool:
    """
    Check whether report already exists.
    """

    return generated_report() is not None


# -----------------------------------------------------

def horizontal_space() -> None:
    """
    Small visual separator.
    """

    st.markdown(

        "<br>",

        unsafe_allow_html=True,

    )
# =====================================================
# REPORT OVERVIEW
# =====================================================

def show_report_summary(
    report_data: Dict[str, Any],
) -> None:
    """
    Display report overview.
    """

    st.subheader(
        "Report Overview"
    )

    dataset = report_data.get(
        "dataset"
    )

    insights = report_data.get(
        "insights"
    )

    dashboard = report_data.get(
        "dashboard"
    )

    dataset_info = report_data.get(
        "dataset_info",
        {},
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Rows",

            dataset_info.get(
                "rows",
                len(dataset),
            ),

        )

    with col2:

        st.metric(

            "Columns",

            dataset_info.get(
                "columns",
                len(dataset.columns),
            ),

        )

    with col3:

        st.metric(

            "AI Insights",

            "Available" if insights else "Unavailable",

        )

    with col4:

        st.metric(

            "Dashboard",

            "Ready" if dashboard else "Unavailable",

        )

    horizontal_space()


# =====================================================
# REPORT SECTION SELECTION
# =====================================================

def show_report_selection() -> Dict[str, bool]:
    """
    Select report sections.

    Returns
    -------
    Dictionary of selected report sections.
    """

    st.subheader(
        "Report Sections"
    )

    st.caption(
        """
        Choose the sections that should
        be included in the generated report.
        """
    )

    sections = {}

    col1, col2 = st.columns(2)

    with col1:

        sections["executive_summary"] = st.checkbox(

            "Executive Summary",

            value=True,

        )

        sections["ai_insights"] = st.checkbox(

            "AI Insights",

            value=True,

        )

        sections["dataset_health"] = st.checkbox(

            "Dataset Health",

            value=True,

        )

    with col2:

        sections["dashboard_summary"] = st.checkbox(

            "Dashboard Summary",

            value=True,

        )

        sections["cleaning_summary"] = st.checkbox(

            "Data Cleaning Summary",

            value=True,

        )

    st.info(

        """
        Recommended:
        Keep all report sections enabled
        for a complete business report.
        """

    )

    horizontal_space()

    return sections
# =====================================================
# EXPORT FORMAT
# =====================================================

def show_export_formats() -> str:
    """
    Select report export format.

    Returns
    -------
    Selected export format.
    """

    st.subheader(
        "Export Format"
    )

    export_format = st.radio(

        "Choose Report Format",

        options=[

            "PDF",

            "Word",

            "Excel",

            "HTML",

            "Text",

        ],

        horizontal=True,

    )

    horizontal_space()

    return export_format


# =====================================================
# GENERATE REPORT
# =====================================================

def generate_report(
    report_data: Dict[str, Any],
    sections: Dict[str, bool],
    export_format: str,
) -> None:
    """
    Generate report using Report Builder.
    """

    st.subheader(
        "Generate Report"
    )

    if st.button(

        "📄 Generate Report",

        type="primary",

        use_container_width=True,

    ):

        try:

            logger.info(
                "Generating report."
            )

            with st.spinner(
                "Generating report..."
            ):

                report = report_builder.build_complete_report(
                    df=report_data.get("dataset"),
                )

            session_manager.set(

                "generated_report",

                report,

            )

            session_manager.set(

                "report_format",

                export_format,

            )

            session_manager.set(

                "report_sections",

                sections,

            )

            logger.info(
                "Report generated successfully."
            )

            st.success(
                "✅ Report generated successfully."
            )

        except Exception as ex:

            logger.exception(ex)

            st.error(

                f"Report generation failed.\n\n{ex}"

            )

    horizontal_space()
# =====================================================
# REPORT PREVIEW
# =====================================================

def preview_report() -> None:
    """
    Preview generated report.
    """

    report = generated_report()

    if report is None:

        return

    st.subheader(
        "Report Preview"
    )

    #
    # Text Report
    #

    if isinstance(
        report,
        str,
    ):

        st.text_area(

            "Generated Report",

            value=report,

            height=500,

        )

    #
    # Dictionary Report (from ReportBuilder.build_complete_report)
    #

    elif isinstance(
        report,
        dict,
    ):

        summary = report.get("executive_summary", {}).get("summary_text", "")
        health = report.get("conclusion", {}).get("health", {})
        insights = report.get("business_insights", [])
        recommendations = report.get("recommendations", [])

        st.markdown(f"**Executive Summary**\n\n{summary}")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Data Health Score", health.get("score", "N/A"))
        with c2:
            st.metric("Health Status", health.get("status", "N/A"))

        if insights:
            st.markdown("**Business Insights**")
            for item in insights:
                st.write(f"• {item}")

        if recommendations:
            st.markdown("**Recommendations**")
            for item in recommendations:
                st.write(f"• {item}")

        with st.expander("View Raw Report Data"):
            st.json(report, expanded=False)

    #
    # DataFrame Report
    #

    else:

        try:

            st.dataframe(

                report,

                use_container_width=True,

                hide_index=True,

            )

        except Exception:

            st.write(
                report
            )

    horizontal_space()


# =====================================================
# DOWNLOAD REPORT
# =====================================================

def download_report() -> None:
    """
    Download generated report.
    """

    report = generated_report()

    if report is None:

        return

    st.subheader(
        "Download Report"
    )

    report_format = session_manager.get(
        "report_format",
        "Text",
    )

    extension_map = {

        "PDF": "pdf",

        "Word": "docx",

        "Excel": "xlsx",

        "HTML": "html",

        "Text": "txt",

    }

    extension = extension_map.get(

        report_format,

        "txt",

    )

    #
    # Convert report to downloadable content using the matching
    # ReportBuilder export method for the selected format.
    #

    if isinstance(report, str):

        download_content = report

    elif isinstance(report, dict):

        try:
            if report_format == "PDF":
                download_content = report_builder.export_pdf(report)
            elif report_format == "Word":
                download_content = report_builder.export_word(report)
            elif report_format == "Excel":
                download_content = report_builder.export_excel(report)
            elif report_format == "HTML":
                download_content = report_builder.export_html(report)
            else:
                download_content = report_builder.export_text(report)
        except Exception as ex:
            logger.exception(ex)
            st.error(f"Could not build the {report_format} file: {ex}")
            return

    else:

        try:

            download_content = report.to_csv(
                index=False
            )

        except Exception:

            download_content = str(
                report
            )

    mime_map = {

        "pdf": "application/pdf",

        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        "html": "text/html",

        "txt": "text/plain",

    }

    st.download_button(

        label=f"📥 Download {report_format} Report",

        data=download_content,

        file_name=f"report.{extension}",

        mime=mime_map.get(
            extension,
            "text/plain",
        ),

        use_container_width=True,

    )

    horizontal_space()
# =====================================================
# SIDEBAR
# =====================================================

def render_sidebar() -> None:
    """
    Render Reports sidebar.
    """

    with st.sidebar:

        st.title("AI Data Analyzer Pro")

        st.markdown("---")

        st.subheader("Reports")

        report_data = load_report_data()

        if report_data is not None:

            info = report_data.get(
                "dataset_info",
                {},
            )

            st.write(
                f"**Rows** : {info.get('rows', 'N/A')}"
            )

            st.write(
                f"**Columns** : {info.get('columns', 'N/A')}"
            )

            st.write(
                f"**Insights** : {'Yes' if report_data.get('insights') else 'No'}"
            )

            st.write(
                f"**Dashboard** : {'Yes' if report_data.get('dashboard') else 'No'}"
            )

        st.markdown("---")

        if report_available():

            st.success(
                "✅ Report Ready"
            )

        else:

            st.info(
                "No report generated yet."
            )

        st.markdown("---")

        st.caption(
            """
            Generate professional business
            reports from AI analysis.
            """
        )


# =====================================================
# FOOTER
# =====================================================

def render_footer() -> None:
    """
    Render footer.
    """

    st.divider()

    st.caption(
        "© 2026 Punit Tech Hub | AI Data Analyzer Pro"
    )


# =====================================================
# MAIN PAGE
# =====================================================

def main() -> None:
    """
    Reports Page.
    """

    initialize_page()

    render_sidebar()

    report_data = load_report_data()

    if report_data is None:

        render_footer()

        return

    show_report_summary(
        report_data
    )

    sections = show_report_selection()

    export_format = show_export_formats()

    generate_report(

        report_data,

        sections,

        export_format,

    )

    if report_available():

        preview_report()

        download_report()

    render_footer()


# =====================================================
# PAGE EXECUTION
# =====================================================

if __name__ == "__main__":

    try:

        logger.info(
            "Opening Reports page."
        )

        main()

    except Exception as ex:

        logger.exception(ex)

        st.error(
            "Unexpected error occurred."
        )

        st.exception(ex)
