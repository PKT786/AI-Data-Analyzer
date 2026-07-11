"""
=========================================================
AI Data Analyzer Pro
Enterprise Report Builder

Author : Punit Tech Hub
Version : 3.0
=========================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import numpy as np

from utils.logger import get_logger
from utils.validators import validate_dataframe

logger = get_logger(__name__)


# =========================================================
# REPORT BUILDER
# =========================================================

class ReportBuilder:
    """
    Enterprise Report Builder

    Generates

    ✓ Executive Summary

    ✓ Dataset Overview

    ✓ Data Quality Report

    ✓ Business Insights

    ✓ KPI Summary

    ✓ Recommendations

    ✓ Exportable Report

    Every report is returned as a dictionary.
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        logger.info(
            "ReportBuilder initialized."
        )

    # =====================================================
    # INTERNAL COPY
    # =====================================================

    def _copy_df(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        return df.copy(deep=True)

    # =====================================================
    # REPORT METADATA
    # =====================================================

    def report_metadata(
        self,
    ) -> Dict[str, Any]:

        return {

            "title":
                "AI Data Analyzer Report",

            "version":
                "3.0 Enterprise",

            "generated_on":
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),

            "generated_by":
                "AI Data Analyzer Pro",

        }

    # =====================================================
    # DATASET OVERVIEW
    # =====================================================

    def dataset_overview(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        numeric_columns = working_df.select_dtypes(

            include=np.number

        ).columns.tolist()

        categorical_columns = working_df.select_dtypes(

            include=[
                "object",
                "category",
                "string",
            ]

        ).columns.tolist()

        datetime_columns = working_df.select_dtypes(

            include=[
                "datetime",
                "datetimetz",
            ]

        ).columns.tolist()

        return {

            "rows":
                len(working_df),

            "columns":
                len(working_df.columns),

            "numeric_columns":
                len(numeric_columns),

            "categorical_columns":
                len(categorical_columns),

            "datetime_columns":
                len(datetime_columns),

            "memory_mb":
                round(

                    working_df.memory_usage(
                        deep=True
                    ).sum()

                    / 1024
                    / 1024,

                    2,

                ),

            "duplicates":
                int(
                    working_df.duplicated().sum()
                ),

            "missing_cells":
                int(
                    working_df.isna().sum().sum()
                ),

        }

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    def executive_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        validate_dataframe(df)

        overview = self.dataset_overview(df)

        summary_text = (

            f"The uploaded dataset contains "

            f"{overview['rows']} rows and "

            f"{overview['columns']} columns. "

            f"It includes "

            f"{overview['numeric_columns']} numeric columns, "

            f"{overview['categorical_columns']} categorical columns "

            f"and "

            f"{overview['datetime_columns']} datetime columns. "

            f"There are "

            f"{overview['duplicates']} duplicate rows "

            f"and "

            f"{overview['missing_cells']} missing values."

        )

        return {

            "summary_text":
                summary_text,

            "dataset_overview":
                overview,

        }

    # =====================================================
    # BASIC REPORT
    # =====================================================

    def basic_report(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        validate_dataframe(df)

        report = {

            "metadata":
                self.report_metadata(),

            "executive_summary":
                self.executive_summary(df),

        }

        logger.info(
            "Basic report generated."
        )

        return report
        # =====================================================
    # DATA QUALITY REPORT
    # =====================================================

    def data_quality_report(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        total_cells = (
            working_df.shape[0]
            * working_df.shape[1]
        )

        missing_cells = int(
            working_df.isna().sum().sum()
        )

        duplicate_rows = int(
            working_df.duplicated().sum()
        )

        return {

            "total_rows":
                len(working_df),

            "total_columns":
                len(working_df.columns),

            "missing_cells":
                missing_cells,

            "missing_percentage":
                round(

                    (missing_cells / total_cells) * 100,

                    2,

                ) if total_cells else 0,

            "duplicate_rows":
                duplicate_rows,

            "duplicate_percentage":
                round(

                    duplicate_rows

                    / len(working_df)

                    * 100,

                    2,

                ) if len(working_df) else 0,

        }

    # =====================================================
    # MISSING VALUE REPORT
    # =====================================================

    def missing_value_report(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        report = pd.DataFrame({

            "Column":
                working_df.columns,

            "Missing Count":
                working_df.isna().sum().values,

            "Missing Percentage":
                (

                    working_df.isna().mean()

                    * 100

                ).round(2).values,

        })

        report = report.sort_values(

            "Missing Count",

            ascending=False,

        )

        return report

    # =====================================================
    # DUPLICATE REPORT
    # =====================================================

    def duplicate_report(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        duplicate_rows = working_df[
            working_df.duplicated()
        ]

        return {

            "duplicate_count":
                len(duplicate_rows),

            "duplicate_percentage":
                round(

                    len(duplicate_rows)

                    / len(working_df)

                    * 100,

                    2,

                ) if len(working_df) else 0,

            "duplicates":
                duplicate_rows,

        }

    # =====================================================
    # DATA TYPE SUMMARY
    # =====================================================

    def datatype_summary(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        summary = pd.DataFrame({

            "Column":
                working_df.columns,

            "Data Type":
                working_df.dtypes.astype(str).values,

            "Missing":
                working_df.isna().sum().values,

            "Unique":
                working_df.nunique().values,

        })

        return summary

    # =====================================================
    # NUMERIC SUMMARY
    # =====================================================

    def numeric_summary(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        numeric_df = working_df.select_dtypes(

            include=np.number

        )

        if numeric_df.empty:

            return pd.DataFrame()

        summary = numeric_df.describe().T

        summary["missing"] = (

            numeric_df.isna().sum()

        )

        summary["variance"] = (

            numeric_df.var()

        )

        summary["skewness"] = (

            numeric_df.skew()

        )

        summary["kurtosis"] = (

            numeric_df.kurt()

        )

        return summary.round(2)

    # =====================================================
    # CATEGORICAL SUMMARY
    # =====================================================

    def categorical_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        categorical = working_df.select_dtypes(

            include=[

                "object",

                "category",

                "string",

            ]

        )

        results = {}

        for column in categorical.columns:

            value_counts = categorical[column].value_counts(

                dropna=False

            )

            results[column] = {

                "unique_values":

                    int(

                        categorical[column].nunique()

                    ),

                "top_value":

                    value_counts.index[0]

                    if len(value_counts)

                    else None,

                "top_count":

                    int(value_counts.iloc[0])

                    if len(value_counts)

                    else 0,

            }

        return results
        # =====================================================
    # CORRELATION REPORT
    # =====================================================

    def correlation_report(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        numeric_df = working_df.select_dtypes(
            include=np.number
        )

        if numeric_df.shape[1] < 2:
            return pd.DataFrame()

        corr = numeric_df.corr()

        return corr.round(3)

    # =====================================================
    # DISTRIBUTION SUMMARY
    # =====================================================

    def distribution_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        numeric_df = working_df.select_dtypes(
            include=np.number
        )

        results = {}

        for column in numeric_df.columns:

            results[column] = {

                "minimum":
                    float(numeric_df[column].min()),

                "maximum":
                    float(numeric_df[column].max()),

                "mean":
                    float(numeric_df[column].mean()),

                "median":
                    float(numeric_df[column].median()),

                "std":
                    float(numeric_df[column].std()),

                "variance":
                    float(numeric_df[column].var()),

                "skewness":
                    float(numeric_df[column].skew()),

                "kurtosis":
                    float(numeric_df[column].kurt()),

            }

        return results

    # =====================================================
    # OUTLIER SUMMARY
    # =====================================================

    def outlier_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, int]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        numeric_df = working_df.select_dtypes(
            include=np.number
        )

        results = {}

        for column in numeric_df.columns:

            q1 = numeric_df[column].quantile(0.25)

            q3 = numeric_df[column].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - (1.5 * iqr)

            upper = q3 + (1.5 * iqr)

            outliers = numeric_df[
                (numeric_df[column] < lower)
                |
                (numeric_df[column] > upper)
            ]

            results[column] = len(outliers)

        return results

    # =====================================================
    # COLUMN STATISTICS
    # =====================================================

    def column_statistics(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        results = {}

        for column in working_df.columns:

            results[column] = {

                "dtype":
                    str(working_df[column].dtype),

                "unique":
                    int(
                        working_df[column].nunique()
                    ),

                "missing":
                    int(
                        working_df[column].isna().sum()
                    ),

                "memory_bytes":
                    int(
                        working_df[column]
                        .memory_usage(
                            deep=True
                        )
                    ),

            }

        return results

    # =====================================================
    # DATASET HEALTH SCORE
    # =====================================================

    def dataset_health_score(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        total_cells = (
            working_df.shape[0]
            * working_df.shape[1]
        )

        missing = int(
            working_df.isna().sum().sum()
        )

        duplicates = int(
            working_df.duplicated().sum()
        )

        score = 100

        if total_cells > 0:

            score -= (
                missing
                / total_cells
            ) * 40

        if len(working_df) > 0:

            score -= (
                duplicates
                / len(working_df)
            ) * 30

        score = max(0, min(100, round(score, 2)))

        if score >= 90:
            status = "Excellent"

        elif score >= 75:
            status = "Good"

        elif score >= 60:
            status = "Average"

        else:
            status = "Poor"

        return {

            "score": score,

            "status": status,

        }

    # =====================================================
    # STATISTICAL OVERVIEW
    # =====================================================

    def statistical_overview(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        validate_dataframe(df)

        return {

            "numeric_summary":
                self.numeric_summary(df),

            "categorical_summary":
                self.categorical_summary(df),

            "distribution":
                self.distribution_summary(df),

            "outliers":
                self.outlier_summary(df),

            "health":
                self.dataset_health_score(df),

        }
        # =====================================================
    # KPI SUMMARY
    # =====================================================

    def kpi_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        numeric = working_df.select_dtypes(
            include=np.number
        )

        return {

            "total_records":
                len(working_df),

            "total_columns":
                len(working_df.columns),

            "numeric_columns":
                len(numeric.columns),

            "missing_values":
                int(
                    working_df.isna().sum().sum()
                ),

            "duplicate_rows":
                int(
                    working_df.duplicated().sum()
                ),

            "memory_mb":
                round(

                    working_df.memory_usage(
                        deep=True
                    ).sum()

                    / 1024
                    / 1024,

                    2,

                ),

        }

    # =====================================================
    # BUSINESS INSIGHTS
    # =====================================================

    def business_insights(
        self,
        df: pd.DataFrame,
    ) -> List[str]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        insights = []

        if working_df.isna().sum().sum() > 0:

            insights.append(
                "Dataset contains missing values that should be cleaned before modelling."
            )

        if working_df.duplicated().sum() > 0:

            insights.append(
                "Duplicate records detected. Removing duplicates may improve data quality."
            )

        numeric = working_df.select_dtypes(
            include=np.number
        )

        if len(numeric.columns) > 0:

            insights.append(
                f"Dataset contains {len(numeric.columns)} numeric features suitable for machine learning."
            )

        categorical = working_df.select_dtypes(
            include=["object", "category"]
        )

        if len(categorical.columns) > 0:

            insights.append(
                f"{len(categorical.columns)} categorical columns may require encoding."
            )

        if not insights:

            insights.append(
                "Dataset appears clean and ready for analysis."
            )

        return insights

    # =====================================================
    # RISK ANALYSIS
    # =====================================================

    def risk_analysis(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, str]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        risks = {}

        missing = working_df.isna().sum().sum()

        duplicates = working_df.duplicated().sum()

        if missing > 0:

            risks["Missing Values"] = "Medium"

        else:

            risks["Missing Values"] = "Low"

        if duplicates > 0:

            risks["Duplicate Records"] = "Medium"

        else:

            risks["Duplicate Records"] = "Low"

        numeric = working_df.select_dtypes(
            include=np.number
        )

        if len(numeric.columns) == 0:

            risks["Machine Learning Readiness"] = "High"

        else:

            risks["Machine Learning Readiness"] = "Low"

        return risks

    # =====================================================
    # DATA QUALITY RECOMMENDATIONS
    # =====================================================

    def recommendations(
        self,
        df: pd.DataFrame,
    ) -> List[str]:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        rec = []

        if working_df.isna().sum().sum():

            rec.append(
                "Handle missing values using Mean, Median or Mode."
            )

        if working_df.duplicated().sum():

            rec.append(
                "Remove duplicate rows."
            )

        numeric = working_df.select_dtypes(
            include=np.number
        )

        if len(numeric.columns):

            rec.append(
                "Check numeric columns for outliers."
            )

        categorical = working_df.select_dtypes(
            include=["object", "category"]
        )

        if len(categorical.columns):

            rec.append(
                "Encode categorical variables before machine learning."
            )

        rec.append(
            "Validate data before building dashboards."
        )

        return rec

    # =====================================================
    # EXECUTIVE RECOMMENDATION
    # =====================================================

    def executive_recommendation(
        self,
        df: pd.DataFrame,
    ) -> str:

        score = self.dataset_health_score(df)

        if score["score"] >= 90:

            return (
                "Dataset is production ready."
            )

        if score["score"] >= 75:

            return (
                "Minor cleaning recommended before analytics."
            )

        if score["score"] >= 60:

            return (
                "Moderate data cleaning required before reporting."
            )

        return (
            "Extensive data cleaning is recommended before analysis."
        )

    # =====================================================
    # ACTION ITEMS
    # =====================================================

    def action_items(
        self,
        df: pd.DataFrame,
    ) -> List[str]:

        return [

            "Review missing values",

            "Remove duplicates",

            "Detect outliers",

            "Validate data types",

            "Generate dashboard",

            "Generate AI insights",

            "Export cleaned dataset",

        ]

    # =====================================================
    # FINAL CONCLUSION
    # =====================================================

    def final_conclusion(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        return {

            "health":
                self.dataset_health_score(df),

            "recommendation":
                self.executive_recommendation(df),

            "business_insights":
                self.business_insights(df),

            "action_items":
                self.action_items(df),

        }
        # =====================================================
    # BUILD COMPLETE REPORT
    # =====================================================

    def build_complete_report(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Generate complete enterprise report.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        report = {

            "metadata":
                self.report_metadata(),

            "executive_summary":
                self.executive_summary(
                    working_df
                ),

            "dataset_overview":
                self.dataset_overview(
                    working_df
                ),

            "data_quality":
                self.data_quality_report(
                    working_df
                ),

            "datatype_summary":
                self.datatype_summary(
                    working_df
                ),

            "numeric_summary":
                self.numeric_summary(
                    working_df
                ),

            "categorical_summary":
                self.categorical_summary(
                    working_df
                ),

            "correlation":
                self.correlation_report(
                    working_df
                ),

            "statistics":
                self.statistical_overview(
                    working_df
                ),

            "kpi_summary":
                self.kpi_summary(
                    working_df
                ),

            "risk_analysis":
                self.risk_analysis(
                    working_df
                ),

            "recommendations":
                self.recommendations(
                    working_df
                ),

            "business_insights":
                self.business_insights(
                    working_df
                ),

            "conclusion":
                self.final_conclusion(
                    working_df
                ),

        }

        logger.info(
            "Complete report generated."
        )

        return report

    # =====================================================
    # EXPORT JSON
    # =====================================================

    def export_json(
        self,
        report: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        JSON ready report.
        """

        return report

    # =====================================================
    # EXPORT MARKDOWN
    # =====================================================

    def export_markdown(
        self,
        report: Dict[str, Any],
    ) -> str:

        md = "# AI Data Analyzer Report\n\n"

        md += "## Executive Summary\n\n"

        md += report["executive_summary"][
            "summary_text"
        ]

        md += "\n\n"

        md += "## Dataset Overview\n\n"

        overview = report["dataset_overview"]

        for key, value in overview.items():

            md += f"- **{key}** : {value}\n"

        md += "\n"

        md += "## Recommendations\n\n"

        for item in report["recommendations"]:

            md += f"- {item}\n"

        return md

    # =====================================================
    # EXPORT HTML
    # =====================================================

    def export_html(
        self,
        report: Dict[str, Any],
    ) -> str:

        html = f"""

        <html>

        <head>

        <title>

        AI Data Analyzer Report

        </title>

        </head>

        <body>

        <h1>

        AI Data Analyzer Report

        </h1>

        <h2>

        Executive Summary

        </h2>

        <p>

        {report["executive_summary"]["summary_text"]}

        </p>

        </body>

        </html>

        """

        return html

    # =====================================================
    # SIMPLE TEXT REPORT
    # =====================================================

    def export_text(
        self,
        report: Dict[str, Any],
    ) -> str:

        text = ""

        text += "AI DATA ANALYZER REPORT\n"

        text += "=" * 50 + "\n\n"

        text += report["executive_summary"][
            "summary_text"
        ]

        text += "\n\n"

        text += "Recommendations\n"

        text += "-" * 30 + "\n"

        for item in report["recommendations"]:

            text += f"• {item}\n"

        return text

    # =====================================================
    # REPORT INFO
    # =====================================================

    @property
    def version(self):

        return "3.0 Enterprise"

    def __repr__(self):

        return (

            f"ReportBuilder("

            f"version='{self.version}')"

        )


# =====================================================
# GLOBAL INSTANCE
# =====================================================

report_builder = ReportBuilder()
