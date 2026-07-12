"""
==========================================================
AI DATA ANALYZER PRO
Premium Dashboard Renderer
==========================================================
This page RENDERS the dashboard built by DashboardAI.

It also lets the user:
    • generate additional charts and add them to the
      dashboard (DashboardDesigner + ChartFactory)
    • switch / shuffle the theme so the dashboard
      background changes dynamically
    • export the dashboard (PDF / PNG / Excel / PPT / HTML)

This page never performs AI analysis and never mutates the
DashboardResult returned by DashboardAI - it only adds
widgets/theme to the Dashboard object it contains.
==========================================================
"""

from __future__ import annotations

import logging
from datetime import datetime

import streamlit as st

from components.chart_factory import ChartFactory
from components.dashboard_designer import DashboardDesigner
from components.dashboard_exporter import DashboardExporter
from components.dashboard_models import ChartType, DashboardResult
from components.dashboard_themes import ThemeManager

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

import auth
auth.require_login()


# ==========================================================
# Premium Dashboard Page
# ==========================================================

class PremiumDashboardPage:

    def __init__(self):
        self.designer = DashboardDesigner()
        self.chart_factory = ChartFactory()
        self.theme_manager = ThemeManager()
        self.exporter = DashboardExporter()

        self.result: DashboardResult | None = st.session_state.get("dashboard_result")
        self.dataframe = st.session_state.get("cleaned_df")

    # ------------------------------------------------------
    @property
    def dashboard(self):
        return None if self.result is None else self.result.dashboard

    # ======================================================
    # Empty state
    # ======================================================

    def render_empty_state(self):
        st.title("📊 Dashboard")
        st.warning(
            "No dashboard has been generated yet.\n\n"
            "Please open **4 AI Insights** and click **Generate AI Dashboard** first."
        )

    # ======================================================
    # Theming - global CSS injection
    # ======================================================

    def inject_theme_css(self):
        theme = self.dashboard.theme
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: {theme.background_gradient};
            }}
            .db-header {{
                background: {theme.header_gradient};
                color: {theme.header_text_color};
                padding: 28px 34px;
                border-radius: {theme.border_radius}px;
                margin-bottom: 20px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.18);
            }}
            .db-header h1 {{
                margin: 0; font-size: 30px; color: {theme.header_text_color};
            }}
            .db-header p {{
                margin: 6px 0 0; opacity: 0.92; color: {theme.header_text_color};
            }}
            .kpi-card {{
                background: {theme.card_background};
                border: 1px solid {theme.border_color};
                border-radius: {theme.border_radius}px;
                padding: 16px 18px;
                box-shadow: 0 4px 14px rgba(0,0,0,0.08);
            }}
            .kpi-label {{
                color: {theme.muted_text}; font-size: 12px; text-transform: uppercase;
                letter-spacing: .04em; font-weight: 600;
            }}
            .kpi-value {{
                color: {theme.primary}; font-size: 26px; font-weight: 800; margin-top: 2px;
            }}
            .chart-card {{
                background: {theme.card_background};
                border: 1px solid {theme.border_color};
                border-radius: {theme.border_radius}px;
                padding: 14px 16px 4px;
                box-shadow: 0 4px 14px rgba(0,0,0,0.08);
                margin-bottom: 18px;
            }}
            .chart-title {{
                color: {theme.text_color}; font-size: 15px; font-weight: 700; margin-bottom: 4px;
            }}
            section[data-testid="stSidebar"] {{
                background: {theme.card_background};
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    # ======================================================
    # Header banner
    # ======================================================

    def render_header(self):
        dashboard = self.dashboard
        st.markdown(
            f"""
            <div class="db-header">
                <h1>📊 {dashboard.title}</h1>
                <p>{dashboard.subtitle}</p>
                <p style="font-size:12px;">Theme: {dashboard.theme.name} • Updated {datetime.now().strftime('%d %b %Y, %H:%M')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ======================================================
    # KPI strip
    # ======================================================

    def render_kpis(self):
        kpis = self.dashboard.kpis or []
        if not kpis:
            return

        cols = st.columns(len(kpis))
        for col, kpi in zip(cols, kpis):
            with col:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-label">{kpi.get('label', '')}</div>
                        <div class="kpi-value">{kpi.get('value', '')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.write("")

    # ======================================================
    # Widget grid
    # ======================================================

    def render_widgets(self):
        widgets = [w for w in self.dashboard.widgets if w.visible]

        if not widgets:
            st.info("This dashboard has no charts yet. Use **Add Chart** in the sidebar to create one.")
            return

        columns_per_row = 3
        for i in range(0, len(widgets), columns_per_row):
            row_widgets = widgets[i:i + columns_per_row]
            cols = st.columns(len(row_widgets))
            for col, widget in zip(cols, row_widgets):
                with col:
                    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="chart-title">{widget.title}</div>', unsafe_allow_html=True)
                    if widget.chart is not None:
                        st.plotly_chart(
                            widget.chart,
                            use_container_width=True,
                            config={"displaylogo": False},
                            key=f"chart_{widget.id}",
                        )
                    remove = st.button("🗑 Remove", key=f"remove_{widget.id}", use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                    if remove:
                        self.designer.remove_widget(self.dashboard, widget.id)
                        st.rerun()

    # ======================================================
    # Summary + recommendations
    # ======================================================

    def render_summary(self):
        with st.expander("📝 Executive Summary & Recommendations", expanded=False):
            st.write(self.dashboard.summary)
            for rec in self.dashboard.recommendations:
                st.info(f"• {rec}")

    # ======================================================
    # Sidebar - theme controls
    # ======================================================

    def render_theme_controls(self):
        st.sidebar.subheader("🎨 Theme")

        theme_names = self.theme_manager.list_themes()
        current_name = self.dashboard.theme.name
        default_index = theme_names.index(current_name) if current_name in theme_names else 0

        selected = st.sidebar.selectbox("Dashboard theme", theme_names, index=default_index)
        if selected != current_name:
            self.dashboard.theme = self.theme_manager.get_theme(selected)
            self._restyle_charts()
            st.session_state.selected_theme = selected
            st.rerun()

        if st.sidebar.button("🎲 Shuffle Colors (New Look)", use_container_width=True):
            self.dashboard.theme = self.theme_manager.random_theme(exclude=current_name)
            self._restyle_charts()
            st.session_state.selected_theme = self.dashboard.theme.name
            st.rerun()

        st.sidebar.caption(
            "Every dashboard you generate on **4 AI Insights** already gets a random "
            "premium theme automatically - use this to pick a specific one instead."
        )

    def _restyle_charts(self):
        """Re-tint existing plotly figures with the newly selected theme's colours."""
        theme = self.dashboard.theme
        for widget in self.dashboard.widgets:
            if widget.chart is None:
                continue
            try:
                widget.chart.update_layout(
                    colorway=theme.chart_colorway,
                    font=dict(color=theme.text_color, family=theme.font_family),
                    title=dict(font=dict(color=theme.text_color)),
                )
            except Exception as ex:
                logger.warning("Could not restyle widget '%s': %s", widget.title, ex)

    # ======================================================
    # Sidebar - filters (mirrors example dashboards)
    # ======================================================

    def render_filters(self):
        if self.dataframe is None or self.dataframe.empty:
            return None

        st.sidebar.subheader("🔎 Filters")
        df = self.dataframe
        categorical_cols = [
            c for c in df.select_dtypes(include=["object", "category"]).columns
            if df[c].nunique() <= 30
        ][:3]

        if not categorical_cols:
            st.sidebar.caption("No filterable columns detected.")
            return df

        filtered = df.copy()
        for col in categorical_cols:
            options = sorted(df[col].dropna().unique().tolist())
            selected = st.sidebar.multiselect(col, options, key=f"filter_{col}")
            if selected:
                filtered = filtered[filtered[col].isin(selected)]

        return filtered

    # ======================================================
    # Sidebar - add chart
    # ======================================================

    def render_add_chart(self, filtered_df):
        st.sidebar.subheader("➕ Add Chart")

        df = filtered_df if filtered_df is not None else self.dataframe
        if df is None or df.empty:
            st.sidebar.caption("Upload a dataset to add custom charts.")
            return

        numeric_cols = list(df.select_dtypes(include=["number"]).columns)
        all_cols = list(df.columns)

        chart_type_name = st.sidebar.selectbox(
            "Chart type",
            [c.value for c in ChartType if c != ChartType.KPI],
            key="add_chart_type",
        )
        x_col = st.sidebar.selectbox("X / Category", all_cols, key="add_chart_x")
        y_options = numeric_cols or all_cols
        y_col = st.sidebar.selectbox("Y / Value", y_options, key="add_chart_y")

        if st.sidebar.button("✨ Generate & Add Chart", use_container_width=True, type="primary"):
            try:
                widget = self.chart_factory.create_chart(
                    df,
                    ChartType(chart_type_name),
                    x=x_col,
                    y=y_col,
                    theme=self.dashboard.theme,
                )
                self.designer.add_widget(self.dashboard, widget)
                st.sidebar.success(f"Added: {widget.title}")
                st.rerun()
            except Exception as ex:
                logger.exception(ex)
                st.sidebar.error(f"Could not create chart: {ex}")

    # ======================================================
    # Sidebar - export
    # ======================================================

    def render_export(self):
        st.sidebar.subheader("⬇️ Export Dashboard")
        dashboard = self.dashboard

        fmt = st.sidebar.selectbox("Format", ["HTML", "PNG", "Excel", "PowerPoint", "PDF"], key="export_fmt")

        if st.sidebar.button("Prepare Download", use_container_width=True):
            with st.spinner(f"Exporting {fmt}..."):
                file_bytes, filename, mime = None, None, None

                if fmt == "HTML":
                    html = self.exporter.export_html(dashboard)
                    file_bytes, filename, mime = html.encode("utf-8"), "dashboard.html", "text/html"
                elif fmt == "PNG":
                    file_bytes = self.exporter.export_png(dashboard)
                    filename, mime = "dashboard.png", "image/png"
                elif fmt == "Excel":
                    file_bytes = self.exporter.export_excel(dashboard)
                    filename, mime = "dashboard.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif fmt == "PowerPoint":
                    file_bytes = self.exporter.export_powerpoint(dashboard)
                    filename, mime = "dashboard.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                elif fmt == "PDF":
                    file_bytes = self.exporter.export_pdf(dashboard)
                    filename, mime = "dashboard.pdf", "application/pdf"

                if file_bytes:
                    st.sidebar.download_button(
                        "📥 Download",
                        data=file_bytes,
                        file_name=filename,
                        mime=mime,
                        use_container_width=True,
                    )
                else:
                    st.sidebar.error("Export failed. Check the logs for details.")

    # ======================================================
    # Render
    # ======================================================

    def render(self):
        if self.result is None or self.dashboard is None:
            self.render_empty_state()
            return

        self.inject_theme_css()
        self.render_header()
        self.render_kpis()
        self.render_summary()

        filtered_df = self.render_filters()
        self.render_theme_controls()
        self.render_add_chart(filtered_df)
        self.render_export()

        st.divider()
        self.render_widgets()


# ==========================================================
# Main
# ==========================================================

def main():
    try:
        page = PremiumDashboardPage()
        page.render()
    except Exception as ex:
        logger.exception(ex)
        st.exception(ex)


main()
