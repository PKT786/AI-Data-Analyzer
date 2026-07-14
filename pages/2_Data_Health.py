"""
==========================================================
AI DATA ANALYZER PRO
Data Health Workspace
Enterprise Edition
==========================================================
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List
from typing import Optional
from typing import Any

import numpy as np
import pandas as pd

import streamlit as st

# ==========================================================
# Page Configuration
# ==========================================================

import auth
auth.require_login()
auth.render_account_bar()

# ==========================================================
# Logger
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s",

)

logger = logging.getLogger(__name__)

# ==========================================================
# Health Report Model
# ==========================================================

@dataclass
class HealthReport:

    overall_score: float = 0.0

    total_rows: int = 0

    total_columns: int = 0

    duplicate_rows: int = 0

    missing_values: int = 0

    duplicate_columns: int = 0

    memory_usage_mb: float = 0.0

    numeric_columns: int = 0

    categorical_columns: int = 0

    datetime_columns: int = 0

    issues: List[str] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)

# ==========================================================
# Session Initialization
# ==========================================================

def initialize_session() -> None:
    """
    Initialize required session variables.
    Compatible with Upload page.
    """

    defaults = {

        "dataset": None,

        "cleaned_df": None,

        "profile": None,

        "metadata": None,

        "health_report": None,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value

# ==========================================================
# Dataset Loader
# ==========================================================

def get_dataset() -> Optional[pd.DataFrame]:
    """
    Return cleaned dataframe if available,
    otherwise return original dataset.
    """

    initialize_session()

    if st.session_state.cleaned_df is not None:

        return st.session_state.cleaned_df

    return st.session_state.dataset

# ==========================================================
# Validation
# ==========================================================

def validate_dataset() -> Optional[pd.DataFrame]:
    """
    Validate dataset exists.
    """

    df = get_dataset()

    if df is None:

        st.warning(
            """
No dataset available.

Please upload a dataset first from
**1️⃣ Upload Data**.
"""
        )

        st.stop()

    return df

# ==========================================================
# Data Health Analyzer
# ==========================================================

class DataHealthAnalyzer:
    """
    Enterprise Data Health Engine.

    Responsibilities

    • Dataset Validation

    • Missing Value Analysis

    • Duplicate Detection

    • Memory Analysis

    • Data Type Analysis

    • Health Score Calculation

    • Recommendation Generation
    """

    def __init__(self):

        self.df = validate_dataset()

        logger.info(
            "Data Health Analyzer initialized."
        )
# ==========================================================
# Generate Health Report
# ==========================================================

    def analyze(self) -> HealthReport:
        """
        Perform complete health analysis.
        """

        report = HealthReport()

        report.total_rows = len(self.df)

        report.total_columns = len(self.df.columns)

        report.duplicate_rows = int(
            self.df.duplicated().sum()
        )

        report.missing_values = int(
            self.df.isna().sum().sum()
        )

        report.memory_usage_mb = round(

            self.df.memory_usage(
                deep=True
            ).sum()
            / 1024
            / 1024,

            2,

        )

        report.numeric_columns = len(

            self.df.select_dtypes(
                include=["number"]
            ).columns

        )

        report.categorical_columns = len(

            self.df.select_dtypes(
                include=["object", "category"]
            ).columns

        )

        report.datetime_columns = len(

            self.df.select_dtypes(
                include=["datetime", "datetimetz"]
            ).columns

        )

        report.duplicate_columns = (
            self._duplicate_columns()
        )

        return report


# ==========================================================
# Duplicate Columns
# ==========================================================

    def _duplicate_columns(self) -> int:
        """
        Count duplicate column names.
        """

        return int(

            pd.Index(
                self.df.columns
            ).duplicated().sum()

        )


# ==========================================================
# Missing Values
# ==========================================================

    def missing_summary(self) -> pd.DataFrame:
        """
        Missing value summary.
        """

        summary = pd.DataFrame({

            "Column": self.df.columns,

            "Missing": self.df.isna().sum().values,

            "Missing %": (

                self.df.isna().mean()

                * 100

            ).round(2),

        })

        return summary.sort_values(

            "Missing",

            ascending=False,

        )


# ==========================================================
# Duplicate Rows
# ==========================================================

    def duplicate_rows(self) -> pd.DataFrame:
        """
        Return duplicated rows.
        """

        return self.df[
            self.df.duplicated()
        ]


# ==========================================================
# Data Types
# ==========================================================

    def datatype_summary(self) -> pd.DataFrame:
        """
        Column datatype summary.
        """

        summary = pd.DataFrame({

            "Column": self.df.columns,

            "Datatype": self.df.dtypes.astype(str),

            "Unique Values": [

                self.df[c].nunique()

                for c in self.df.columns

            ],

        })

        return summary


# ==========================================================
# Memory Analysis
# ==========================================================

    def memory_summary(self) -> pd.DataFrame:
        """
        Memory usage per column.
        """

        memory = (

            self.df.memory_usage(
                deep=True
            )

            / 1024

        ).round(2)

        return pd.DataFrame({

            "Column": memory.index,

            "Memory (KB)": memory.values,

        })
# ==========================================================
# Health Score Calculation
# ==========================================================

    def calculate_health_score(
        self,
        report: HealthReport,
    ) -> float:
        """
        Calculate overall dataset health score.
        """

        score = 100.0


        # Missing values impact

        if report.missing_values > 0:

            missing_percentage = (

                report.missing_values

                /

                (
                    report.total_rows
                    *
                    report.total_columns
                )

            ) * 100


            if missing_percentage > 30:

                score -= 30

            elif missing_percentage > 15:

                score -= 20

            elif missing_percentage > 5:

                score -= 10

            else:

                score -= 5


        # Duplicate rows impact

        if report.duplicate_rows > 0:

            duplicate_percentage = (

                report.duplicate_rows

                /

                report.total_rows

            ) * 100


            if duplicate_percentage > 20:

                score -= 20

            elif duplicate_percentage > 5:

                score -= 10

            else:

                score -= 5


        # Duplicate columns

        if report.duplicate_columns > 0:

            score -= 10


        return max(
            round(score, 2),
            0
        )


# ==========================================================
# Issue Detection
# ==========================================================

    def detect_issues(
        self,
        report: HealthReport,
    ) -> List[str]:
        """
        Identify dataset quality issues.
        """

        issues = []


        if report.missing_values > 0:

            issues.append(

                f"{report.missing_values} missing values detected."

            )


        if report.duplicate_rows > 0:

            issues.append(

                f"{report.duplicate_rows} duplicate rows detected."

            )


        if report.duplicate_columns > 0:

            issues.append(

                "Duplicate column names detected."

            )



        if report.total_rows < 100:

            issues.append(

                "Dataset size is small. Insights may have limited accuracy."

            )


        if not issues:

            issues.append(

                "No major data quality issues detected."

            )


        return issues


# ==========================================================
# Recommendation Engine
# ==========================================================

    def generate_recommendations(
        self,
        report: HealthReport,
    ) -> List[str]:
        """
        Generate improvement recommendations.
        """

        recommendations = []


        if report.missing_values > 0:

            recommendations.append(

                "Review missing values and apply suitable imputation methods."

            )

        if report.categorical_columns > 0:

            recommendations.append(

                "Categorical columns require encoding or validation before ML analysis."

            )

        if report.duplicate_rows > 0:

            recommendations.append(

                "Remove duplicate records before dashboard generation."

            )


        if report.categorical_columns > 0:

            recommendations.append(

                "Review categorical columns for consistency and standardization."

            )


        if report.memory_usage_mb > 500:

            recommendations.append(

                "Consider optimizing data types to reduce memory usage."

            )


        if not recommendations:

            recommendations.append(

                "Dataset quality is good. Ready for AI analysis."

            )


        return recommendations


# ==========================================================
# Complete Analysis Pipeline
# ==========================================================

    def generate_health_report(self) -> HealthReport:
        """
        Generate final health report.
        """

        report = self.analyze()


        report.overall_score = (
            self.calculate_health_score(
                report
            )
        )


        report.issues = (
            self.detect_issues(
                report
            )
        )


        report.recommendations = (
            self.generate_recommendations(
                report
            )
        )


        return report


# ==========================================================
# Save Health Report
# ==========================================================

    def save_report(
        self,
        report: HealthReport,
    ) -> None:
        """
        Store health report globally.
        """

        st.session_state.health_report = report

        logger.info(
            "Health report saved successfully."
        )
# ==========================================================
# Health Score Status
# ==========================================================

def get_health_status(
    score: float,
) -> str:
    """
    Convert score into status.
    """

    if score >= 90:

        return "Excellent 🟢"

    elif score >= 75:

        return "Good 🟡"

    elif score >= 50:

        return "Fair 🟠"

    else:

        return "Poor 🔴"


# ==========================================================
# Executive Health Cards
# ==========================================================

def show_health_summary(
    report: HealthReport,
) -> None:
    """
    Display premium KPI cards.
    """

    st.subheader(
        "🩺 Dataset Health Overview"
    )


    status = get_health_status(
        report.overall_score
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(

            "Health Score",

            f"{report.overall_score}/100"

        )


    with c2:

        st.metric(

            "Status",

            status

        )


    with c3:

        st.metric(

            "Rows",

            f"{report.total_rows:,}"

        )


    with c4:

        st.metric(

            "Columns",

            report.total_columns

        )


    c5, c6, c7, c8 = st.columns(4)


    with c5:

        st.metric(

            "Missing Values",

            report.missing_values

        )


    with c6:

        st.metric(

            "Duplicates",

            report.duplicate_rows

        )


    with c7:

        st.metric(

            "Memory",

            f"{report.memory_usage_mb:.2f} MB"

        )


    with c8:

        st.metric(

            "Data Types",

            (
                report.numeric_columns
                +
                report.categorical_columns
                +
                report.datetime_columns
            )

        )


# ==========================================================
# Issue Section
# ==========================================================

def show_health_issues(
    report: HealthReport,
) -> None:
    """
    Display detected issues.
    """

    st.subheader(
        "⚠️ Data Quality Issues"
    )


    if report.issues:

        for issue in report.issues:

            st.warning(issue)

    else:

        st.success(
            "No issues detected."
        )


# ==========================================================
# Recommendations Section
# ==========================================================

def show_recommendations(
    report: HealthReport,
) -> None:
    """
    Display recommendations.
    """

    st.subheader(
        "💡 Recommendations"
    )


    for item in report.recommendations:

        st.info(item)


# ==========================================================
# Missing Value Analysis
# ==========================================================

def show_missing_analysis(
    analyzer: DataHealthAnalyzer,
) -> None:
    """
    Missing value table.
    """

    st.subheader(
        "📌 Missing Value Analysis"
    )


    missing_df = (
        analyzer.missing_summary()
    )


    st.dataframe(

        missing_df,

        use_container_width=True,

        hide_index=True,

    )


# ==========================================================
# Data Type Analysis
# ==========================================================

def show_datatype_analysis(
    analyzer: DataHealthAnalyzer,
) -> None:
    """
    Display datatype summary.
    """

    st.subheader(
        "🔍 Column Data Types"
    )


    datatype_df = (
        analyzer.datatype_summary()
    )


    st.dataframe(

        datatype_df,

        use_container_width=True,

        hide_index=True,

    )


# ==========================================================
# Duplicate Analysis
# ==========================================================

def show_duplicate_analysis(
    analyzer: DataHealthAnalyzer,
) -> None:
    """
    Duplicate records.
    """

    st.subheader(
        "♻️ Duplicate Records"
    )


    duplicates = (
        analyzer.duplicate_rows()
    )


    if len(duplicates) > 0:

        st.dataframe(

            duplicates.head(100),

            use_container_width=True,

            hide_index=True,

        )

    else:

        st.success(
            "No duplicate records found."
        )


# ==========================================================
# Memory Analysis
# ==========================================================

def show_memory_analysis(
    analyzer: DataHealthAnalyzer,
) -> None:
    """
    Memory consumption.
    """

    st.subheader(
        "💾 Memory Usage"
    )


    memory_df = (
        analyzer.memory_summary()
    )


    st.dataframe(

        memory_df,

        use_container_width=True,

        hide_index=True,

    )
# ==========================================================
# Footer
# ==========================================================

def show_footer():

    st.divider()

    st.caption("AI Data Analyzer Pro")

    st.caption("© 2026 Punit Tech Hub")


# ==========================================================
# Main
# ==========================================================

def main():

    initialize_session()

    st.title("🩺 Data Health")

    analyzer = DataHealthAnalyzer()

    report = analyzer.generate_health_report()

    analyzer.save_report(report)

    show_health_summary(report)

    st.divider()

    show_health_issues(report)

    st.divider()

    show_recommendations(report)

    st.divider()

    show_missing_analysis(analyzer)

    st.divider()

    show_datatype_analysis(analyzer)

    st.divider()

    show_duplicate_analysis(analyzer)

    st.divider()

    show_memory_analysis(analyzer)

    show_footer()


# ==========================================================
# Execute
# ==========================================================

main()
