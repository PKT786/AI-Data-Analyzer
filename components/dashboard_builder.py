"""
=========================================================
AI Data Analyzer Pro
Dashboard Builder
Author : Punit Tech Hub
Version : 2.0
=========================================================
"""

from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from components.dataset_health import dataset_health
from components.chart_builder import chart_builder

from utils.logger import get_logger
from utils.validators import validate_dataframe

logger = get_logger(__name__)


class DashboardBuilder:
    """
    Enterprise Dashboard Builder.

    This class prepares dashboard metadata,
    KPI cards, layouts and chart recommendations.

    No Streamlit code exists here.
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        logger.info(
            "DashboardBuilder initialized."
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

    def _health_report(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        """
        Cached entry point for Dataset Health.
        """

        return dataset_health.generate_report(df)

    # -----------------------------------------------------

    def _quality_label(
        self,
        score: int,
    ) -> str:

        if score >= 90:
            return "Excellent"

        if score >= 75:
            return "Good"

        if score >= 60:
            return "Average"

        if score >= 40:
            return "Poor"

        return "Critical"

    # =====================================================
    # KPI BUILDER
    # =====================================================

    def build_kpis(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Build dashboard KPI cards.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        report = self._health_report(
            working_df
        )

        dataset = report["dataset"]

        kpis = {

            "rows": dataset["rows"],

            "columns": dataset["columns"],

            "missing":

                dataset["missing_cells"],

            "duplicates":

                dataset["duplicate_rows"],

            "quality_score":

                report["quality_score"],

            "quality":

                self._quality_label(

                    report["quality_score"]

                ),

            "memory_mb":

                dataset["memory_mb"],

            "numeric_columns":

                dataset["numeric_columns"],

            "categorical_columns":

                dataset["categorical_columns"],

            "datetime_columns":

                dataset["datetime_columns"],

        }

        logger.info(
            "Dashboard KPIs generated."
        )

        return kpis
        # =====================================================
    # SUMMARY BUILDER
    # =====================================================

    def build_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Build executive summary.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        report = self._health_report(
            working_df
        )

        dataset = report["dataset"]

        score = report["quality_score"]

        quality = self._quality_label(
            score
        )

        summary = {

            "title":
                "Dataset Executive Summary",

            "subtitle":
                f"{dataset['rows']} rows • "
                f"{dataset['columns']} columns",

            "health":
                quality,

            "quality_score":
                score,

            "recommendations":
                report["recommendations"],

        }

        logger.info(
            "Dashboard summary generated."
        )

        return summary

    # =====================================================
    # CHART SUGGESTIONS
    # =====================================================

    def suggest_charts(
        self,
        df: pd.DataFrame,
    ) -> List[Dict[str, Any]]:
        """
        Suggest charts automatically based on
        dataset structure.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        suggestions = []

        numeric_columns = working_df.select_dtypes(

            include="number"

        ).columns.tolist()

        categorical_columns = working_df.select_dtypes(

            include=["object", "category", "string"]

        ).columns.tolist()

        datetime_columns = working_df.select_dtypes(

            include=["datetime", "datetimetz"]

        ).columns.tolist()

        # ---------------------------------------------
        # Numeric Distribution
        # ---------------------------------------------

        for column in numeric_columns:

            suggestions.append(

                {

                    "title":
                        f"Distribution of {column}",

                    "chart":
                        "histogram",

                    "kwargs": {

                        "column": column,

                    },

                }

            )

        # ---------------------------------------------
        # Numeric Relationships
        # ---------------------------------------------

        if len(numeric_columns) >= 2:

            suggestions.append(

                {

                    "title":
                        "Correlation Heatmap",

                    "chart":
                        "heatmap",

                    "kwargs": {},

                }

            )

            suggestions.append(

                {

                    "title":
                        f"{numeric_columns[1]} vs {numeric_columns[0]}",

                    "chart":
                        "scatter",

                    "kwargs": {

                        "x": numeric_columns[0],

                        "y": numeric_columns[1],

                    },

                }

            )

        # ---------------------------------------------
        # Category Charts
        # ---------------------------------------------

        for column in categorical_columns:

            unique = working_df[column].nunique()

            if unique <= 10:

                suggestions.append(

                    {

                        "title":
                            f"{column} Composition",

                        "chart":
                            "pie",

                        "kwargs": {

                            "names": column,

                            "values": column,

                        },

                    }

                )

            else:

                suggestions.append(

                    {

                        "title":
                            f"{column} Frequency",

                        "chart":
                            "count",

                        "kwargs": {

                            "column": column,

                        },

                    }

                )

        # ---------------------------------------------
        # Time Series
        # ---------------------------------------------

        if datetime_columns and numeric_columns:

            suggestions.append(

                {

                    "title":
                        "Time Series Trend",

                    "chart":
                        "time_series",

                    "kwargs": {

                        "x": datetime_columns[0],

                        "y": numeric_columns[0],

                    },

                }

            )

        logger.info(

            "Chart suggestions generated."

        )

        return suggestions
        # =====================================================
    # EXECUTIVE SECTION
    # =====================================================

    def executive_section(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Build Executive Dashboard section.
        """

        validate_dataframe(df)

        section = {

            "title": "Executive Overview",

            "description": (
                "High level summary of the dataset."
            ),

            "kpis": self.build_kpis(df),

            "summary": self.build_summary(df),

            "charts": [],

        }

        logger.info(
            "Executive section generated."
        )

        return section

    # =====================================================
    # QUALITY SECTION
    # =====================================================

    def quality_section(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Dataset quality section.
        """

        validate_dataframe(df)

        report = self._health_report(df)

        section = {

            "title": "Dataset Quality",

            "description":
                "Missing values, duplicates and quality metrics.",

            "missing": report["missing"],

            "duplicates": report["duplicates"],

            "memory": report["memory"],

            "quality_score": report["quality_score"],

            "recommendations": report["recommendations"],

        }

        logger.info(
            "Quality section generated."
        )

        return section

    # =====================================================
    # DISTRIBUTION SECTION
    # =====================================================

    def distribution_section(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Distribution related charts.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        numeric_columns = working_df.select_dtypes(

            include="number"

        ).columns.tolist()

        charts = []

        for column in numeric_columns:

            charts.append(

                {

                    "title":
                        f"{column} Histogram",

                    "chart":
                        "histogram",

                    "kwargs": {

                        "column": column,

                    },

                }

            )

            charts.append(

                {

                    "title":
                        f"{column} Box Plot",

                    "chart":
                        "box",

                    "kwargs": {

                        "y": column,

                    },

                }

            )

        section = {

            "title":
                "Distribution Analysis",

            "description":
                "Distribution and outlier visualization.",

            "charts":
                charts,

        }

        logger.info(
            "Distribution section generated."
        )

        return section

    # =====================================================
    # RELATIONSHIP SECTION
    # =====================================================

    def relationship_section(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Relationship analysis section.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        numeric_columns = working_df.select_dtypes(

            include="number"

        ).columns.tolist()

        charts = []

        if len(numeric_columns) >= 2:

            charts.append(

                {

                    "title":
                        "Correlation Heatmap",

                    "chart":
                        "heatmap",

                    "kwargs": {},

                }

            )

            charts.append(

                {

                    "title":
                        "Scatter Relationship",

                    "chart":
                        "scatter",

                    "kwargs": {

                        "x": numeric_columns[0],

                        "y": numeric_columns[1],

                    },

                }

            )

        if len(numeric_columns) >= 3:

            charts.append(

                {

                    "title":
                        "Bubble Analysis",

                    "chart":
                        "bubble",

                    "kwargs": {

                        "x": numeric_columns[0],

                        "y": numeric_columns[1],

                        "size": numeric_columns[2],

                    },

                }

            )

        section = {

            "title":
                "Relationship Analysis",

            "description":
                "Correlation and relationships.",

            "charts":
                charts,

        }

        logger.info(
            "Relationship section generated."
        )

        return section

    # =====================================================
    # TIME SERIES SECTION
    # =====================================================

    def time_series_section(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Time series dashboard section.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        datetime_columns = working_df.select_dtypes(

            include=["datetime", "datetimetz"]

        ).columns.tolist()

        numeric_columns = working_df.select_dtypes(

            include="number"

        ).columns.tolist()

        charts = []

        if datetime_columns and numeric_columns:

            charts.append(

                {

                    "title":
                        "Time Trend",

                    "chart":
                        "time_series",

                    "kwargs": {

                        "x": datetime_columns[0],

                        "y": numeric_columns[0],

                    },

                }

            )

            charts.append(

                {

                    "title":
                        "Area Trend",

                    "chart":
                        "area",

                    "kwargs": {

                        "x": datetime_columns[0],

                        "y": numeric_columns[0],

                    },

                }

            )

        section = {

            "title":
                "Time Series Analysis",

            "description":
                "Trend visualization over time.",

            "charts":
                charts,

        }

        logger.info(
            "Time series section generated."
        )

        return section
        # =====================================================
    # DASHBOARD LAYOUT
    # =====================================================

    def build_layout(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Build dashboard layout metadata.
        """

        validate_dataframe(df)

        layout = {

            "rows": [

                {

                    "name": "Executive",

                    "columns": 4,

                    "section": "executive",

                },

                {

                    "name": "Quality",

                    "columns": 2,

                    "section": "quality",

                },

                {

                    "name": "Distribution",

                    "columns": 2,

                    "section": "distribution",

                },

                {

                    "name": "Relationship",

                    "columns": 2,

                    "section": "relationship",

                },

                {

                    "name": "Time Series",

                    "columns": 2,

                    "section": "time_series",

                },

            ]

        }

        logger.info(
            "Dashboard layout generated."
        )

        return layout

    # =====================================================
    # DASHBOARD CONFIGURATION
    # =====================================================

    def dashboard_config(
        self,
    ) -> Dict[str, Any]:
        """
        Dashboard configuration.
        """

        config = {

            "title": "AI Data Analyzer Dashboard",

            "page_icon": "📊",

            "layout": "wide",

            "theme": "dark",

            "sidebar_state": "expanded",

        }

        logger.info(
            "Dashboard configuration generated."
        )

        return config

    # =====================================================
    # COMPLETE DASHBOARD
    # =====================================================

    def build_dashboard(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Build complete dashboard object.
        """

        validate_dataframe(df)

        dashboard = {

            "config": self.dashboard_config(),

            "summary": self.build_summary(df),

            "kpis": self.build_kpis(df),

            "layout": self.build_layout(df),

            "sections": {

                "executive":

                    self.executive_section(df),

                "quality":

                    self.quality_section(df),

                "distribution":

                    self.distribution_section(df),

                "relationship":

                    self.relationship_section(df),

                "time_series":

                    self.time_series_section(df),

            },

            "chart_suggestions":

                self.suggest_charts(df),

        }

        logger.info(
            "Complete dashboard generated."
        )

        return dashboard


# =====================================================
# GLOBAL INSTANCE
# =====================================================

dashboard_builder = DashboardBuilder()