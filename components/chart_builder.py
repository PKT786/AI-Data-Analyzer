"""
=========================================================
AI Data Analyzer Pro
Chart Builder Engine
Author : Punit Tech Hub
Version : 2.0
=========================================================
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import json

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from utils.logger import get_logger
from utils.validators import (
    validate_dataframe,
    validate_column_exists,
    validate_columns_exist,
)

logger = get_logger(__name__)


class ChartBuilder:
    """
    Enterprise Chart Builder.

    This class is responsible for creating all
    visualizations used throughout the application.

    Supported Charts
    ----------------

    • Bar
    • Horizontal Bar
    • Line
    • Area
    • Scatter
    • Bubble
    • Histogram
    • Box
    • Violin
    • Pie
    • Donut
    • Treemap
    • Sunburst
    • Heatmap
    • Count Plot
    • Density Plot
    • Time Series
    • Multi Line
    • Stacked Bar
    • 3D Scatter

    Every chart returns a Plotly Figure.
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        logger.info(
            "ChartBuilder initialized."
        )

    # =====================================================
    # INTERNAL HELPERS
    # =====================================================

    def _copy_df(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        return df.copy(deep=True)

    # -----------------------------------------------------

    def _validate_xy(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
    ) -> None:

        validate_columns_exist(
            df,
            [x, y],
        )

    # -----------------------------------------------------

    def _apply_layout(
        self,
        fig: go.Figure,
        title: Optional[str] = None,
    ) -> go.Figure:

        fig.update_layout(

            template="plotly_dark",

            title=title,

            font=dict(
                family="Segoe UI",
                size=14,
            ),

            margin=dict(
                l=40,
                r=40,
                t=60,
                b=40,
            ),

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),

        )

        return fig

    # -----------------------------------------------------

    def _default_title(
        self,
        chart_type: str,
        x: Optional[str] = None,
        y: Optional[str] = None,
    ) -> str:

        if x and y:

            return f"{chart_type}: {y} vs {x}"

        if x:

            return f"{chart_type}: {x}"

        return chart_type

    # =====================================================
    # BAR CHART
    # =====================================================

    def bar_chart(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        self._validate_xy(
            working_df,
            x,
            y,
        )

        fig = px.bar(

            working_df,

            x=x,

            y=y,

            color=color,

            title=title or self._default_title(
                "Bar Chart",
                x,
                y,
            ),

        )

        logger.info(
            "Bar chart created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # HORIZONTAL BAR
    # =====================================================

    def horizontal_bar_chart(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        self._validate_xy(
            working_df,
            x,
            y,
        )

        fig = px.bar(

            working_df,

            x=x,

            y=y,

            color=color,

            orientation="h",

            title=title or self._default_title(
                "Horizontal Bar",
                x,
                y,
            ),

        )

        logger.info(
            "Horizontal bar chart created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # LINE CHART
    # =====================================================

    def line_chart(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        self._validate_xy(
            working_df,
            x,
            y,
        )

        fig = px.line(

            working_df,

            x=x,

            y=y,

            color=color,

            title=title or self._default_title(
                "Line Chart",
                x,
                y,
            ),

        )

        logger.info(
            "Line chart created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # AREA CHART
    # =====================================================

    def area_chart(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        self._validate_xy(
            working_df,
            x,
            y,
        )

        fig = px.area(

            working_df,

            x=x,

            y=y,

            color=color,

            title=title or self._default_title(
                "Area Chart",
                x,
                y,
            ),

        )

        logger.info(
            "Area chart created."
        )

        return self._apply_layout(
            fig,
            title,
        )
        # =====================================================
    # SCATTER CHART
    # =====================================================

    def scatter_chart(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        size: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        self._validate_xy(
            working_df,
            x,
            y,
        )

        fig = px.scatter(

            working_df,

            x=x,

            y=y,

            color=color,

            size=size,

            title=title or self._default_title(
                "Scatter Chart",
                x,
                y,
            ),

        )

        logger.info(
            "Scatter chart created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # BUBBLE CHART
    # =====================================================

    def bubble_chart(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        size: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_columns_exist(
            working_df,
            [x, y, size],
        )

        fig = px.scatter(

            working_df,

            x=x,

            y=y,

            size=size,

            color=color,

            title=title or self._default_title(
                "Bubble Chart",
                x,
                y,
            ),

        )

        logger.info(
            "Bubble chart created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # HISTOGRAM
    # =====================================================

    def histogram_chart(
        self,
        df: pd.DataFrame,
        column: str,
        color: Optional[str] = None,
        bins: Optional[int] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_column_exists(
            working_df,
            column,
        )

        fig = px.histogram(

            working_df,

            x=column,

            color=color,

            nbins=bins,

            title=title or f"Histogram : {column}",

        )

        logger.info(
            "Histogram created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # BOX PLOT
    # =====================================================

    def box_chart(
        self,
        df: pd.DataFrame,
        y: str,
        x: Optional[str] = None,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_column_exists(
            working_df,
            y,
        )

        if x:

            validate_column_exists(
                working_df,
                x,
            )

        fig = px.box(

            working_df,

            x=x,

            y=y,

            color=color,

            title=title or f"Box Plot : {y}",

        )

        logger.info(
            "Box plot created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # VIOLIN PLOT
    # =====================================================

    def violin_chart(
        self,
        df: pd.DataFrame,
        y: str,
        x: Optional[str] = None,
        color: Optional[str] = None,
        box: bool = True,
        points: str = "outliers",
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_column_exists(
            working_df,
            y,
        )

        if x:

            validate_column_exists(
                working_df,
                x,
            )

        fig = px.violin(

            working_df,

            x=x,

            y=y,

            color=color,

            box=box,

            points=points,

            title=title or f"Violin Plot : {y}",

        )

        logger.info(
            "Violin plot created."
        )

        return self._apply_layout(
            fig,
            title,
        )
        # =====================================================
    # PIE CHART
    # =====================================================

    def pie_chart(
        self,
        df: pd.DataFrame,
        names: str,
        values: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_columns_exist(
            working_df,
            [names, values],
        )

        fig = px.pie(

            working_df,

            names=names,

            values=values,

            color=color,

            title=title or f"Pie Chart : {values}",

        )

        logger.info(
            "Pie chart created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # DONUT CHART
    # =====================================================

    def donut_chart(
        self,
        df: pd.DataFrame,
        names: str,
        values: str,
        color: Optional[str] = None,
        hole: float = 0.45,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_columns_exist(
            working_df,
            [names, values],
        )

        fig = px.pie(

            working_df,

            names=names,

            values=values,

            color=color,

            hole=hole,

            title=title or f"Donut Chart : {values}",

        )

        logger.info(
            "Donut chart created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # TREEMAP
    # =====================================================

    def treemap_chart(
        self,
        df: pd.DataFrame,
        path: List[str],
        values: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_columns_exist(
            working_df,
            path + [values],
        )

        fig = px.treemap(

            working_df,

            path=path,

            values=values,

            color=color,

            title=title or "Treemap",

        )

        logger.info(
            "Treemap created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # SUNBURST
    # =====================================================

    def sunburst_chart(
        self,
        df: pd.DataFrame,
        path: List[str],
        values: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_columns_exist(
            working_df,
            path + [values],
        )

        fig = px.sunburst(

            working_df,

            path=path,

            values=values,

            color=color,

            title=title or "Sunburst",

        )

        logger.info(
            "Sunburst created."
        )

        return self._apply_layout(
            fig,
            title,
        )
        # =====================================================
    # HEATMAP CHART
    # =====================================================

    def heatmap_chart(
        self,
        df: pd.DataFrame,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        numeric_df = working_df.select_dtypes(include=np.number)

        corr = numeric_df.corr()

        fig = px.imshow(

            corr,

            text_auto=True,

            color_continuous_scale="RdBu",

            title=title or "Heatmap : Correlation",

        )

        logger.info(
            "Heatmap created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # COUNT PLOT
    # =====================================================

    def count_plot(
        self,
        df: pd.DataFrame,
        column: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_column_exists(
            working_df,
            column,
        )

        fig = px.histogram(

            working_df,

            x=column,

            color=color,

            title=title or f"Count Plot : {column}",

        )

        logger.info(
            "Count plot created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # DENSITY PLOT
    # =====================================================

    def density_plot(
        self,
        df: pd.DataFrame,
        column: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_column_exists(
            working_df,
            column,
        )

        fig = px.histogram(

            working_df,

            x=column,

            color=color,

            marginal="rug",

            histnorm="density",

            title=title or f"Density Plot : {column}",

        )

        logger.info(
            "Density plot created."
        )

        return self._apply_layout(
            fig,
            title,
        )
        # =====================================================
    # TIME SERIES CHART
    # =====================================================

    def time_series_chart(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_columns_exist(
            working_df,
            [x, y],
        )

        working_df = working_df.sort_values(by=x)

        fig = px.line(

            working_df,

            x=x,

            y=y,

            color=color,

            title=title or f"Time Series : {y}",

        )

        logger.info(
            "Time series chart created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # MULTI LINE CHART
    # =====================================================

    def multi_line_chart(
        self,
        df: pd.DataFrame,
        x: str,
        y: List[str],
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_columns_exist(
            working_df,
            [x] + y,
        )

        fig = go.Figure()

        for column in y:

            fig.add_trace(

                go.Scatter(

                    x=working_df[x],

                    y=working_df[column],

                    mode="lines",

                    name=column,

                )

            )

        fig.update_layout(

            title=title or "Multi Line Chart",

        )

        logger.info(
            "Multi line chart created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # STACKED BAR CHART
    # =====================================================

    def stacked_bar_chart(
        self,
        df: pd.DataFrame,
        x: str,
        y: List[str],
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_columns_exist(
            working_df,
            [x] + y,
        )

        fig = go.Figure()

        for column in y:

            fig.add_trace(

                go.Bar(

                    x=working_df[x],

                    y=working_df[column],

                    name=column,

                )

            )

        fig.update_layout(

            barmode="stack",

            title=title or "Stacked Bar Chart",

        )

        logger.info(
            "Stacked bar chart created."
        )

        return self._apply_layout(
            fig,
            title,
        )

    # =====================================================
    # 3D SCATTER CHART
    # =====================================================

    def scatter_3d_chart(
        self,
        df: pd.DataFrame,
        x: str,
        y: str,
        z: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:

        working_df = self._copy_df(df)

        validate_columns_exist(
            working_df,
            [x, y, z],
        )

        fig = px.scatter_3d(

            working_df,

            x=x,

            y=y,

            z=z,

            color=color,

            title=title or "3D Scatter",

        )

        logger.info(
            "3D scatter chart created."
        )

        return fig

    # =====================================================
    # MAIN CHART DISPATCHER
    # =====================================================

    def create_chart(
        self,
        df: pd.DataFrame,
        chart_type: str,
        **kwargs: Any,
    ) -> go.Figure:

        chart_type = chart_type.lower()

        if chart_type == "bar":

            return self.bar_chart(df, **kwargs)

        elif chart_type == "horizontal_bar":

            return self.horizontal_bar_chart(df, **kwargs)

        elif chart_type == "line":

            return self.line_chart(df, **kwargs)

        elif chart_type == "area":

            return self.area_chart(df, **kwargs)

        elif chart_type == "scatter":

            return self.scatter_chart(df, **kwargs)

        elif chart_type == "bubble":

            return self.bubble_chart(df, **kwargs)

        elif chart_type == "histogram":

            return self.histogram_chart(df, **kwargs)

        elif chart_type == "box":

            return self.box_chart(df, **kwargs)

        elif chart_type == "violin":

            return self.violin_chart(df, **kwargs)

        elif chart_type == "pie":

            return self.pie_chart(df, **kwargs)

        elif chart_type == "donut":

            return self.donut_chart(df, **kwargs)

        elif chart_type == "treemap":

            return self.treemap_chart(df, **kwargs)

        elif chart_type == "sunburst":

            return self.sunburst_chart(df, **kwargs)

        elif chart_type == "heatmap":

            return self.heatmap_chart(df, **kwargs)

        elif chart_type == "count":

            return self.count_plot(df, **kwargs)

        elif chart_type == "density":

            return self.density_plot(df, **kwargs)

        elif chart_type == "time_series":

            return self.time_series_chart(df, **kwargs)

        elif chart_type == "multi_line":

            return self.multi_line_chart(df, **kwargs)

        elif chart_type == "stacked_bar":

            return self.stacked_bar_chart(df, **kwargs)

        elif chart_type == "scatter_3d":

            return self.scatter_3d_chart(df, **kwargs)

        else:

            raise ValueError(
                f"Unsupported chart type: {chart_type}"
            )

    # =====================================================
    # EXPORT FUNCTIONS
    # =====================================================

    def export_html(
        self,
        fig: go.Figure,
        file_path: str,
    ) -> str:

        html = pio.to_html(fig)

        with open(file_path, "w", encoding="utf-8") as f:

            f.write(html)

        logger.info(
            "HTML exported."
        )

        return file_path

    # -----------------------------------------------------

    def export_json(
        self,
        fig: go.Figure,
    ) -> str:

        return json.dumps(

            fig,

            cls=pio.utils.PlotlyJSONEncoder,

        )

    # -----------------------------------------------------

    def export_png(
        self,
        fig: go.Figure,
        file_path: str,
    ) -> str:

        fig.write_image(file_path)

        logger.info(
            "PNG exported."
        )

        return file_path

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        working_df = self._copy_df(df)

        numeric_df = working_df.select_dtypes(
            include=np.number
        )

        stats = {

            "rows": len(working_df),

            "columns": len(working_df.columns),

            "memory_mb": round(

                working_df.memory_usage(

                    deep=True

                ).sum()

                / 1024

                / 1024,

                2,

            ),

            "numeric_summary": {

                col: {

                    "mean": float(numeric_df[col].mean()),

                    "std": float(numeric_df[col].std()),

                    "min": float(numeric_df[col].min()),

                    "max": float(numeric_df[col].max()),

                }

                for col in numeric_df.columns

            },

        }

        logger.info(
            "Statistics generated."
        )

        return stats


# =====================================================
# GLOBAL INSTANCE
# =====================================================

chart_builder = ChartBuilder()