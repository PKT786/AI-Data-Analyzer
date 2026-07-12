"""
==========================================================
AI DATA ANALYZER PRO
AI INSIGHTS
==========================================================
This page performs:

• AI Dataset Analysis
• KPI Generation
• Dashboard Generation
• Executive Summary
• Chart Recommendations

Dashboard rendering happens in 5_Dashboard.py.
This page never builds charts and never builds a Dashboard
directly - both are delegated to DashboardAI.
==========================================================
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd
import streamlit as st

from components.dashboard_ai import DashboardAI
from components.dashboard_models import DashboardResult

logger = logging.getLogger(__name__)

st.set_page_config(page_title="AI Insights", page_icon="🧠", layout="wide")

import auth
auth.require_login()


# ==========================================================
# Session State
# ==========================================================

@dataclass
class AIInsightSession:
    dataframe: Optional[pd.DataFrame] = None
    analysis_completed: bool = False
    is_generating: bool = False


# ==========================================================
# AI Insights Page
# ==========================================================

class AIInsightsPage:

    def __init__(self):
        self.state = AIInsightSession()
        self.dashboard_ai = DashboardAI()
        self.load_dataframe()
        logger.info("AI Insights initialized.")

    # ------------------------------------------------------
    def load_dataframe(self):
        """Load cleaned dataframe from session (falls back to the raw upload)."""

        if "cleaned_df" in st.session_state and st.session_state.cleaned_df is not None:
            self.state.dataframe = st.session_state.cleaned_df
        elif "dataset" in st.session_state and st.session_state.dataset is not None:
            self.state.dataframe = st.session_state.dataset

    # ------------------------------------------------------
    @property
    def dataframe(self):
        return self.state.dataframe

    @property
    def row_count(self):
        return 0 if self.dataframe is None else len(self.dataframe)

    @property
    def column_count(self):
        return 0 if self.dataframe is None else len(self.dataframe.columns)

    # ======================================================
    # Header
    # ======================================================

    def render_header(self):
        st.title("🧠 AI Insights")
        st.markdown(
            """
Generate intelligent dashboards powered by AI.

The AI engine analyzes your dataset and automatically:

- Detects business domain
- Selects dashboard type
- Recommends KPIs
- Generates multiple charts
- Picks a fresh premium theme every time
- Creates an executive summary
"""
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Rows", f"{self.row_count:,}")
        with c2:
            st.metric("Columns", self.column_count)
        with c3:
            st.metric("Status", "Ready" if self.dataframe is not None else "No Data")

    # ======================================================
    # Dashboard Generation
    # ======================================================

    def generate_dashboard(self) -> Optional[DashboardResult]:
        """Execute DashboardAI and return a DashboardResult."""

        if self.dataframe is None:
            st.error("No dataset available. Please upload and clean a dataset first.")
            return None

        self.state.is_generating = True
        with st.spinner("🤖 AI is analyzing your dataset and building your dashboard..."):
            try:
                dataset_name = st.session_state.get("uploaded_file_name")
                result = self.dashboard_ai.analyze_dataset(self.dataframe, dataset_name=dataset_name)
                self.state.analysis_completed = True
                logger.info("Dashboard generated successfully.")
                return result
            except Exception as ex:
                logger.exception(ex)
                st.exception(ex)
                return None
            finally:
                self.state.is_generating = False

    # ======================================================
    # AI Controls
    # ======================================================

    def render_controls(self) -> Optional[DashboardResult]:
        st.divider()

        generate = st.button("🚀 Generate AI Dashboard", type="primary", use_container_width=True)

        if not generate:
            return None

        result = self.generate_dashboard()
        if result is not None:
            self.save_dashboard_result(result)
        return result

    # ======================================================
    # Business Domain
    # ======================================================

    def render_business_domain(self, result: DashboardResult):
        st.subheader("🏢 Business Domain")

        c1, c2 = st.columns([2, 1])
        with c1:
            st.info(f"**Detected Domain:** {result.business_domain.value}")
            st.write(f"**Dashboard Type:** {result.dashboard.title}")
        with c2:
            st.metric("Confidence", f"{result.confidence.overall * 100:.0f}%")

    # ======================================================
    # Executive Summary
    # ======================================================

    def render_summary(self, result: DashboardResult):
        st.subheader("📝 Executive Summary")
        st.write(result.executive_summary)

    # ======================================================
    # KPIs
    # ======================================================

    def render_kpis(self, result: DashboardResult):
        st.subheader("📌 Recommended KPIs")

        kpis = result.kpis or []
        if not kpis:
            st.caption("No numeric KPIs detected in this dataset.")
            return

        cols = st.columns(min(len(kpis), 4))
        for i, kpi in enumerate(kpis):
            with cols[i % len(cols)]:
                delta = kpi.get("delta")
                st.metric(
                    kpi.get("label", "KPI"),
                    kpi.get("value", "N/A"),
                    delta=f"{delta}%" if delta is not None else None,
                )

    # ======================================================
    # Recommendations
    # ======================================================

    def render_recommendations(self, result: DashboardResult):
        st.subheader("💡 AI Recommendations")
        for rec in result.recommendations:
            st.info(f"• {rec}")

    # ======================================================
    # Save Dashboard Result
    # ======================================================

    def save_dashboard_result(self, result: DashboardResult):
        """Store the DashboardResult in session for 5_Dashboard.py to render."""

        if result is None:
            return

        st.session_state.dashboard_result = result
        st.session_state.dashboard_ready = True
        st.session_state.selected_theme = result.dashboard.theme.name

        logger.info("Dashboard stored in session (%d widgets).", len(result.dashboard.widgets))

    # ======================================================
    # Dashboard Preview
    # ======================================================

    def render_dashboard_preview(self, result: DashboardResult):
        st.subheader("📊 Dashboard Preview")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Widgets", len(result.dashboard.widgets))
        with c2:
            st.metric("KPIs", len(result.kpis))
        with c3:
            st.metric("Recommendations", len(result.recommendations))

        st.success(
            "✅ Dashboard generated successfully. Open **5 Dashboard** in the sidebar to view it, "
            "add more charts, switch themes, or export it."
        )

    # ======================================================
    # Process Dashboard
    # ======================================================

    def process_dashboard(self, result: Optional[DashboardResult]):
        if result is None:
            return

        self.render_business_domain(result)
        self.render_summary(result)
        self.render_kpis(result)
        self.render_recommendations(result)
        self.render_dashboard_preview(result)

    # ======================================================
    # AI Status Panel
    # ======================================================

    def render_status_panel(self):
        st.divider()
        c1, c2, c3 = st.columns(3)

        with c1:
            if self.state.analysis_completed:
                st.success("✅ Analysis Completed")
            else:
                st.info("Waiting for analysis")

        with c2:
            if st.session_state.get("dashboard_result") is not None:
                st.success("📊 Dashboard Ready")
            else:
                st.info("Dashboard not generated")

        with c3:
            if self.state.is_generating:
                st.warning("🤖 AI Running")
            else:
                st.success("Idle")

    # ======================================================
    # Next Steps
    # ======================================================

    def render_next_steps(self):
        if st.session_state.get("dashboard_result") is None:
            return

        st.divider()
        st.success(
            """
### 🎉 AI Analysis Completed Successfully

Your dashboard has been generated and saved.

### Next Steps

1. Open **5 Dashboard**
2. View the AI generated charts
3. Add more charts or switch the theme
4. Export the dashboard (PDF / PPT / Excel / HTML)
"""
        )

    # ======================================================
    # Render Page
    # ======================================================

    def render(self):
        self.render_header()

        result = self.render_controls()

        if result is None:
            existing = st.session_state.get("dashboard_result")
            if existing is not None:
                self.process_dashboard(existing)
            self.render_status_panel()
            self.render_next_steps()
            return

        self.process_dashboard(result)
        self.render_status_panel()
        self.render_next_steps()


# ==========================================================
# Main
# ==========================================================

def main():
    try:
        page = AIInsightsPage()
        page.render()
    except Exception as ex:
        logger.exception(ex)
        st.exception(ex)


main()
