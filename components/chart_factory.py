"""
===========================================================
AI DATA ANALYZER PRO
Chart Factory
Version : 2.0 Enterprise
-----------------------------------------------------------

Responsible for chart creation ONLY.

Input:  DataFrame + chart type
Output: DashboardWidget

Never returns a Dashboard - that is dashboard_designer.py's job.
===========================================================
"""

from __future__ import annotations

import logging
from typing import List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.dashboard_models import (
    ChartType,
    DashboardTheme,
    DashboardWidget,
    DatasetProfile,
    WidgetPosition,
)

logger = logging.getLogger(__name__)

DEFAULT_THEME = DashboardTheme()


# ==========================================================
# Dataset Profiling (used by chart_factory + dashboard_ai)
# ==========================================================


def profile_dataset(df: pd.DataFrame) -> DatasetProfile:
    """Build a DatasetProfile describing the shape of a dataframe."""

    numeric_cols = list(df.select_dtypes(include=["number"]).columns)
    datetime_cols = list(df.select_dtypes(include=["datetime", "datetimetz"]).columns)

    # Detect string columns that actually look like dates
    for col in df.select_dtypes(include=["object"]).columns:
        if col in datetime_cols:
            continue
        try:
            sample = df[col].dropna().head(20)
            if len(sample):
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    parsed = pd.to_datetime(sample, errors="coerce", format="mixed")
                if parsed.notna().mean() > 0.8:
                    datetime_cols.append(col)
        except Exception:
            pass

    categorical_cols = [
        c for c in df.columns
        if c not in numeric_cols and c not in datetime_cols
    ]

    return DatasetProfile(
        row_count=int(len(df)),
        column_count=int(len(df.columns)),
        numeric_columns=numeric_cols,
        categorical_columns=categorical_cols,
        datetime_columns=datetime_cols,
        missing_values=int(df.isna().sum().sum()),
        duplicate_rows=int(df.duplicated().sum()),
        memory_usage_mb=round(df.memory_usage(deep=True).sum() / (1024 ** 2), 3),
        target_column=numeric_cols[0] if numeric_cols else None,
    )


# ==========================================================
# Chart Styling
# ==========================================================


def _style_figure(fig: go.Figure, theme: DashboardTheme, title: str) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=theme.text_color, family=theme.font_family)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=theme.text_color, family=theme.font_family),
        margin=dict(l=30, r=20, t=50, b=30),
        legend=dict(font=dict(color=theme.text_color)),
        colorway=theme.chart_colorway,
        height=340,
    )
    fig.update_xaxes(showgrid=False, color=theme.muted_text)
    fig.update_yaxes(showgrid=True, gridcolor=theme.border_color, color=theme.muted_text)
    return fig


# ==========================================================
# Chart Factory
# ==========================================================


class ChartFactory:
    """Generates themed DashboardWidgets from a pandas DataFrame."""

    # ------------------------------------------------------
    # Generic dispatcher (API_CONTRACT.md: create_chart)
    # ------------------------------------------------------

    def create_chart(
        self,
        df: pd.DataFrame,
        chart_type: ChartType,
        x: Optional[str] = None,
        y: Optional[str] = None,
        title: Optional[str] = None,
        theme: Optional[DashboardTheme] = None,
        agg: str = "sum",
    ) -> DashboardWidget:
        """Create a single DashboardWidget for the given chart type."""

        theme = theme or DEFAULT_THEME
        chart_type = ChartType(chart_type) if not isinstance(chart_type, ChartType) else chart_type
        title = title or self._auto_title(chart_type, x, y)

        builder = {
            ChartType.BAR: self._bar,
            ChartType.LINE: self._line,
            ChartType.AREA: self._area,
            ChartType.PIE: self._pie,
            ChartType.DONUT: self._donut,
            ChartType.SCATTER: self._scatter,
            ChartType.HISTOGRAM: self._histogram,
            ChartType.HEATMAP: self._heatmap,
            ChartType.TREEMAP: self._treemap,
            ChartType.FUNNEL: self._funnel,
            ChartType.GAUGE: self._gauge,
            ChartType.TABLE: self._table,
        }.get(chart_type)

        if builder is None:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        fig, data = builder(df, x, y, theme, agg)
        fig = _style_figure(fig, theme, title)

        return DashboardWidget(
            title=title,
            chart_type=chart_type,
            chart=fig,
            data=data,
            description=f"{chart_type.value.title()} chart of {y or x or 'dataset'}",
            position=WidgetPosition(width=4, height=3),
        )

    # ------------------------------------------------------
    # KPI Card
    # ------------------------------------------------------

    def create_kpi_card(
        self,
        df: pd.DataFrame,
        column: str,
        agg: str = "sum",
        label: Optional[str] = None,
    ) -> dict:
        """Return a KPI dict: {label, value, delta}."""

        if column not in df.columns or df.empty:
            return {"label": label or column, "value": "N/A", "delta": None}

        series = pd.to_numeric(df[column], errors="coerce").dropna()
        if series.empty:
            return {"label": label or column, "value": "N/A", "delta": None}

        value = {
            "sum": series.sum(),
            "mean": series.mean(),
            "count": series.count(),
            "max": series.max(),
            "min": series.min(),
        }.get(agg, series.sum())

        half = max(len(series) // 2, 1)
        delta = None
        if len(series) > 1:
            first_half = series.iloc[:half].mean()
            second_half = series.iloc[half:].mean()
            if first_half:
                delta = round(((second_half - first_half) / abs(first_half)) * 100, 1)

        return {
            "label": label or column.replace("_", " ").title(),
            "value": self._format_number(value),
            "raw_value": value,
            "delta": delta,
        }

    # ------------------------------------------------------
    # Domain dashboards -> List[DashboardWidget]
    # ------------------------------------------------------

    def create_sales_dashboard(self, df, theme=None) -> List[DashboardWidget]:
        return self._auto_widgets(df, theme, focus="sales")

    def create_financial_dashboard(self, df, theme=None) -> List[DashboardWidget]:
        return self._auto_widgets(df, theme, focus="finance")

    def create_hr_dashboard(self, df, theme=None) -> List[DashboardWidget]:
        return self._auto_widgets(df, theme, focus="hr")

    def create_marketing_dashboard(self, df, theme=None) -> List[DashboardWidget]:
        return self._auto_widgets(df, theme, focus="marketing")

    def create_operations_dashboard(self, df, theme=None) -> List[DashboardWidget]:
        return self._auto_widgets(df, theme, focus="operations")

    def create_executive_dashboard(self, df, theme=None) -> List[DashboardWidget]:
        return self._auto_widgets(df, theme, focus="executive")

    # ------------------------------------------------------
    # Auto widget builder (shared engine behind all *_dashboard methods)
    # ------------------------------------------------------

    def _auto_widgets(
        self,
        df: pd.DataFrame,
        theme: Optional[DashboardTheme],
        focus: str = "executive",
        max_widgets: int = 6,
    ) -> List[DashboardWidget]:

        theme = theme or DEFAULT_THEME
        profile = profile_dataset(df)
        widgets: List[DashboardWidget] = []

        numeric = profile.numeric_columns
        categorical = [c for c in profile.categorical_columns if df[c].nunique() <= 30]
        datetime_cols = profile.datetime_columns

        plans = []

        # Category x numeric bar chart
        if categorical and numeric:
            plans.append((ChartType.BAR, categorical[0], numeric[0]))

        # Trend over time
        if datetime_cols and numeric:
            plans.append((ChartType.LINE, datetime_cols[0], numeric[0]))

        # Distribution pie of first categorical
        if categorical:
            second_cat = categorical[1] if len(categorical) > 1 else categorical[0]
            second_num = numeric[1] if len(numeric) > 1 else (numeric[0] if numeric else None)
            if second_num:
                plans.append((ChartType.DONUT, second_cat, second_num))

        # Second numeric distribution
        if len(numeric) >= 1:
            plans.append((ChartType.HISTOGRAM, numeric[0], None))

        # Scatter of two numerics
        if len(numeric) >= 2:
            plans.append((ChartType.SCATTER, numeric[0], numeric[1]))

        # Area chart of second numeric over category
        if categorical and len(numeric) >= 2:
            plans.append((ChartType.AREA, categorical[0], numeric[1]))

        if len(numeric) >= 2 and not datetime_cols:
            plans.append((ChartType.TREEMAP, categorical[0] if categorical else numeric[0], numeric[0]))

        for chart_type, x, y in plans[:max_widgets]:
            try:
                widget = self.create_chart(df, chart_type, x=x, y=y, theme=theme)
                widgets.append(widget)
            except Exception as ex:  # keep dashboard resilient to bad columns
                logger.warning("Skipping widget %s(%s,%s): %s", chart_type, x, y, ex)

        return widgets

    # ------------------------------------------------------
    # Chart builders
    # ------------------------------------------------------

    def _agg_frame(self, df, x, y, agg):
        grouped = df.groupby(x, dropna=False)[y].agg(agg).reset_index()
        grouped = grouped.sort_values(y, ascending=False).head(15)
        return grouped

    def _bar(self, df, x, y, theme, agg):
        data = self._agg_frame(df, x, y, agg)
        fig = px.bar(data, x=x, y=y, color=x, color_discrete_sequence=theme.chart_colorway)
        fig.update_traces(showlegend=False)
        return fig, data

    def _line(self, df, x, y, theme, agg):
        data = df[[x, y]].dropna().copy()
        try:
            data[x] = pd.to_datetime(data[x], errors="coerce")
        except Exception:
            pass
        data = data.groupby(x)[y].agg(agg).reset_index().sort_values(x)
        fig = px.line(data, x=x, y=y, markers=True, color_discrete_sequence=theme.chart_colorway)
        return fig, data

    def _area(self, df, x, y, theme, agg):
        data = self._agg_frame(df, x, y, agg)
        fig = px.area(data, x=x, y=y, color_discrete_sequence=theme.chart_colorway)
        return fig, data

    def _pie(self, df, x, y, theme, agg):
        data = self._agg_frame(df, x, y, agg).head(8)
        fig = px.pie(data, names=x, values=y, color_discrete_sequence=theme.chart_colorway)
        return fig, data

    def _donut(self, df, x, y, theme, agg):
        data = self._agg_frame(df, x, y, agg).head(8)
        fig = px.pie(data, names=x, values=y, hole=0.55, color_discrete_sequence=theme.chart_colorway)
        return fig, data

    def _scatter(self, df, x, y, theme, agg):
        data = df[[x, y]].dropna()
        if len(data) > 1000:
            data = data.sample(1000, random_state=42)
        fig = px.scatter(data, x=x, y=y, color_discrete_sequence=theme.chart_colorway, opacity=0.75)
        return fig, data

    def _histogram(self, df, x, y, theme, agg):
        data = df[[x]].dropna()
        fig = px.histogram(data, x=x, color_discrete_sequence=theme.chart_colorway, nbins=25)
        return fig, data

    def _heatmap(self, df, x, y, theme, agg):
        numeric_df = df.select_dtypes(include=["number"])
        corr = numeric_df.corr(numeric_only=True) if not numeric_df.empty else pd.DataFrame()
        fig = px.imshow(
            corr, text_auto=".2f",
            color_continuous_scale=[theme.background, theme.primary],
        )
        return fig, corr

    def _treemap(self, df, x, y, theme, agg):
        data = self._agg_frame(df, x, y, agg)
        fig = px.treemap(data, path=[x], values=y, color=y, color_continuous_scale=[theme.secondary, theme.accent])
        return fig, data

    def _funnel(self, df, x, y, theme, agg):
        data = self._agg_frame(df, x, y, agg).head(8)
        fig = px.funnel(data, x=y, y=x, color_discrete_sequence=theme.chart_colorway)
        return fig, data

    def _gauge(self, df, x, y, theme, agg):
        col = x if pd.api.types.is_numeric_dtype(df.get(x, pd.Series(dtype=float))) else y
        value = float(pd.to_numeric(df[col], errors="coerce").dropna().mean()) if col else 0.0
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            gauge={"axis": {"range": [0, max(value * 1.6, 1)]}, "bar": {"color": theme.primary}},
        ))
        return fig, pd.DataFrame({"value": [value]})

    def _table(self, df, x, y, theme, agg):
        preview = df.head(20)
        fig = go.Figure(go.Table(
            header=dict(values=list(preview.columns), fill_color=theme.primary, font=dict(color="white")),
            cells=dict(values=[preview[c] for c in preview.columns], fill_color=theme.card_background),
        ))
        return fig, preview

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------

    def _auto_title(self, chart_type: ChartType, x, y) -> str:
        parts = [p for p in [y, "by", x] if p]
        base = " ".join(parts) if len(parts) > 1 else (x or y or "Chart")
        return f"{base}".title()

    def _format_number(self, value: float) -> str:
        try:
            value = float(value)
        except (TypeError, ValueError):
            return str(value)

        abs_value = abs(value)
        if abs_value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f}B"
        if abs_value >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"
        if abs_value >= 1_000:
            return f"{value / 1_000:.2f}K"
        if float(value).is_integer():
            return f"{int(value):,}"
        return f"{value:,.2f}"
