"""
=========================================================
AI Data Analyzer Pro
Insight Generator
Author : Punit Tech Hub
Version : 2.0
=========================================================
"""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd

from components.dataset_health import dataset_health
from components.dashboard_builder import dashboard_builder

from utils.logger import get_logger
from utils.validators import validate_dataframe

logger = get_logger(__name__)


class InsightGenerator:
    """
    Enterprise Insight Generator.

    Generates business insights from datasets.

    Responsibilities
    ----------------
    • Executive Summary
    • Missing Value Insights
    • Duplicate Insights
    • Numeric Insights
    • Categorical Insights
    • Correlation Insights
    • Outlier Insights
    • Time Series Insights
    • Business Recommendations
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        logger.info(
            "InsightGenerator initialized."
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
    # EXECUTIVE SUMMARY
    # =====================================================

    def executive_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Generate executive summary.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        report = self._health_report(
            working_df
        )

        dataset = report["dataset"]

        quality_score = report["quality_score"]

        health = self._quality_label(
            quality_score
        )

        key_points = [

            f"Dataset contains {dataset['rows']} rows.",

            f"Dataset contains {dataset['columns']} columns.",

            f"Quality Score : {quality_score}/100.",

            f"Health Status : {health}.",

        ]

        if dataset["missing_cells"] == 0:

            key_points.append(
                "No missing values detected."
            )

        else:

            key_points.append(
                f"{dataset['missing_cells']} missing values detected."
            )

        if dataset["duplicate_rows"] == 0:

            key_points.append(
                "No duplicate rows detected."
            )

        else:

            key_points.append(
                f"{dataset['duplicate_rows']} duplicate rows detected."
            )

        summary = {

            "title":
                "Executive Summary",

            "overall_health":
                health,

            "quality_score":
                quality_score,

            "summary":
                (
                    f"The uploaded dataset contains "
                    f"{dataset['rows']} rows and "
                    f"{dataset['columns']} columns. "
                    f"Overall data quality is "
                    f"rated as {health}."
                ),

            "key_points":
                key_points,

        }

        logger.info(
            "Executive summary generated."
        )

        return summary
        # =====================================================
    # MISSING VALUE INSIGHTS
    # =====================================================

    def missing_insights(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Generate missing value insights.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        insights: List[str] = []

        total_rows = len(working_df)

        missing = working_df.isna().sum()

        for column, count in missing.items():

            if count == 0:

                insights.append(
                    f"{column} has no missing values."
                )

                continue

            percent = round(

                (count / total_rows) * 100,

                2,

            )

            insights.append(

                f"{column} contains {count} missing values ({percent}%)."

            )

        if not insights:

            insights.append(
                "No missing value analysis available."
            )

        logger.info(
            "Missing value insights generated."
        )

        return insights

    # =====================================================
    # DUPLICATE INSIGHTS
    # =====================================================

    def duplicate_insights(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Generate duplicate row insights.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        insights: List[str] = []

        duplicate_rows = int(

            working_df.duplicated().sum()

        )

        duplicate_percent = round(

            duplicate_rows

            / max(len(working_df), 1)

            * 100,

            2,

        )

        if duplicate_rows == 0:

            insights.append(
                "No duplicate rows detected."
            )

        else:

            insights.append(

                f"{duplicate_rows} duplicate rows detected."

            )

            insights.append(

                f"Duplicates represent {duplicate_percent}% of the dataset."

            )

            insights.append(

                "Removing duplicates is recommended before analysis."

            )

        logger.info(
            "Duplicate insights generated."
        )

        return insights

    # =====================================================
    # NUMERIC INSIGHTS
    # =====================================================

    def numeric_insights(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Generate insights for numeric columns.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        insights: List[str] = []

        numeric_columns = working_df.select_dtypes(

            include=np.number

        ).columns.tolist()

        if not numeric_columns:

            insights.append(
                "No numeric columns detected."
            )

            return insights

        for column in numeric_columns:

            series = working_df[column].dropna()

            if series.empty:

                continue

            mean = float(series.mean())

            median = float(series.median())

            std = float(series.std())

            skew = float(series.skew())

            if abs(mean - median) < 0.01:

                insights.append(

                    f"{column} appears to have a balanced distribution."

                )

            elif mean > median:

                insights.append(

                    f"{column} is positively skewed."

                )

            else:

                insights.append(

                    f"{column} is negatively skewed."

                )

            if std > abs(mean):

                insights.append(

                    f"{column} has high variability."

                )

            if skew > 1:

                insights.append(

                    f"{column} contains strong positive skewness."

                )

            elif skew < -1:

                insights.append(

                    f"{column} contains strong negative skewness."

                )

        logger.info(
            "Numeric insights generated."
        )

        return insights
        # =====================================================
    # CATEGORICAL INSIGHTS
    # =====================================================

    def categorical_insights(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Generate insights for categorical columns.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        insights: List[str] = []

        categorical_columns = working_df.select_dtypes(

            include=["object", "category", "string"]

        ).columns.tolist()

        if not categorical_columns:

            insights.append(
                "No categorical columns detected."
            )

            return insights

        for column in categorical_columns:

            series = working_df[column]

            unique_count = int(
                series.nunique(dropna=True)
            )

            insights.append(

                f"{column} contains {unique_count} unique categories."

            )

            value_counts = series.value_counts(dropna=True)

            if not value_counts.empty:

                top_category = value_counts.index[0]

                top_count = int(value_counts.iloc[0])

                top_percent = round(

                    (top_count / len(series)) * 100,

                    2,

                )

                insights.append(

                    f"{top_category} represents {top_percent}% of '{column}'."

                )

                if top_percent > 70:

                    insights.append(

                        f"{column} is highly imbalanced."

                    )

                elif top_percent < 35:

                    insights.append(

                        f"{column} has a well-balanced distribution."

                    )

        logger.info(
            "Categorical insights generated."
        )

        return insights

    # =====================================================
    # CORRELATION INSIGHTS
    # =====================================================

    def correlation_insights(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Generate correlation insights.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        insights: List[str] = []

        numeric_df = working_df.select_dtypes(
            include=np.number
        )

        if numeric_df.shape[1] < 2:

            insights.append(
                "Not enough numeric columns for correlation analysis."
            )

            return insights

        corr = numeric_df.corr().abs()

        corr = corr.mask(
          np.eye(len(corr), dtype=bool),
          0,
        )

        max_corr = corr.stack().idxmax()

        max_value = corr.stack().max()

        insights.append(

            f"Strongest correlation exists between "
            f"{max_corr[0]} and {max_corr[1]} "
            f"({round(float(max_value),2)})."

        )

        if max_value > 0.85:

            insights.append(

                "Potential multicollinearity detected."

            )

        elif max_value > 0.60:

            insights.append(

                "Moderate relationship detected."

            )

        else:

            insights.append(

                "Most numeric variables are weakly correlated."

            )

        logger.info(
            "Correlation insights generated."
        )

        return insights

    # =====================================================
    # OUTLIER INSIGHTS
    # =====================================================

    def outlier_insights(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Detect outliers using IQR.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        insights: List[str] = []

        numeric_columns = working_df.select_dtypes(

            include=np.number

        ).columns.tolist()

        for column in numeric_columns:

            series = working_df[column].dropna()

            if series.empty:

                continue

            q1 = series.quantile(0.25)

            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower = q1 - (1.5 * iqr)

            upper = q3 + (1.5 * iqr)

            outliers = int(

                ((series < lower) | (series > upper)).sum()

            )

            if outliers == 0:

                insights.append(

                    f"{column} contains no significant outliers."

                )

            else:

                insights.append(

                    f"{column} contains {outliers} outliers."

                )

        logger.info(
            "Outlier insights generated."
        )

        return insights

    # =====================================================
    # TIME SERIES INSIGHTS
    # =====================================================

    def time_series_insights(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Generate time-series insights.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        insights: List[str] = []

        datetime_columns = working_df.select_dtypes(

            include=["datetime", "datetimetz"]

        ).columns.tolist()

        if not datetime_columns:

            insights.append(
                "No datetime columns detected."
            )

            return insights

        numeric_columns = working_df.select_dtypes(

            include=np.number

        ).columns.tolist()

        for date_col in datetime_columns:

            insights.append(

                f"Datetime column detected: {date_col}."

            )

            if numeric_columns:

                insights.append(

                    f"'{date_col}' can be used for trend analysis."

                )

                insights.append(

                    f"Recommended visualization: Time Series Chart."

                )

        logger.info(
            "Time-series insights generated."
        )

        return insights
        # =====================================================
    # BUSINESS RECOMMENDATIONS
    # =====================================================

    def recommendations(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Generate business recommendations based on
        dataset quality and structure.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        report = self._health_report(
            working_df
        )

        recommendations: List[str] = []

        # ---------------------------------------------
        # Missing Values
        # ---------------------------------------------

        total_missing = report["dataset"]["missing_cells"]

        if total_missing > 0:

            recommendations.append(
                "Handle missing values before performing advanced analytics."
            )

        # ---------------------------------------------
        # Duplicates
        # ---------------------------------------------

        duplicates = report["dataset"]["duplicate_rows"]

        if duplicates > 0:

            recommendations.append(
                f"Remove {duplicates} duplicate rows to improve data quality."
            )

        # ---------------------------------------------
        # Numeric Columns
        # ---------------------------------------------

        numeric_columns = working_df.select_dtypes(
            include=np.number
        ).columns.tolist()

        if len(numeric_columns) >= 2:

            recommendations.append(
                "Perform correlation analysis before predictive modelling."
            )

        # ---------------------------------------------
        # Categorical Columns
        # ---------------------------------------------

        categorical_columns = working_df.select_dtypes(
            include=["object", "category", "string"]
        ).columns.tolist()

        if categorical_columns:

            recommendations.append(
                "Encode categorical variables before machine learning."
            )

        # ---------------------------------------------
        # Datetime Columns
        # ---------------------------------------------

        datetime_columns = working_df.select_dtypes(
            include=["datetime", "datetimetz"]
        ).columns.tolist()

        if datetime_columns:

            recommendations.append(
                "Use time-series analysis to identify trends and seasonality."
            )

        # ---------------------------------------------
        # Quality Score
        # ---------------------------------------------

        quality = report["quality_score"]

        if quality >= 90:

            recommendations.append(
                "Dataset quality is excellent and suitable for advanced analytics."
            )

        elif quality >= 75:

            recommendations.append(
                "Minor preprocessing is recommended before modelling."
            )

        else:

            recommendations.append(
                "Significant data cleaning is recommended before analysis."
            )

        logger.info(
            "Business recommendations generated."
        )

        return recommendations

    # =====================================================
    # COMPLETE INSIGHT REPORT
    # =====================================================

    def generate_insights(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Generate complete insight report.
        """

        validate_dataframe(df)

        report = {

            "executive":
                self.executive_summary(df),

            "missing":
                self.missing_insights(df),

            "duplicates":
                self.duplicate_insights(df),

            "numeric":
                self.numeric_insights(df),

            "categorical":
                self.categorical_insights(df),

            "correlation":
                self.correlation_insights(df),

            "outliers":
                self.outlier_insights(df),

            "time_series":
                self.time_series_insights(df),

            "recommendations":
                self.recommendations(df),

        }

        logger.info(
            "Complete insight report generated."
        )

        return report


# =====================================================
# GLOBAL INSTANCE
# =====================================================

insight_generator = InsightGenerator()
