"""
==========================================================
AI DATA ANALYZER PRO
Data Cleaning Workspace
Enterprise Edition
==========================================================
"""

from __future__ import annotations

import logging
import time
from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import numpy as np
import pandas as pd

import streamlit as st

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(

    page_title="Data Cleaning",

    page_icon="🧹",

    layout="wide",

    initial_sidebar_state="expanded",

)

import auth
auth.require_login()

# ==========================================================
# Logger
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s",

)

logger = logging.getLogger(__name__)

# ==========================================================
# Cleaning Operations
# ==========================================================

class CleaningOperation(Enum):

    REMOVE_DUPLICATES = "Remove Duplicates"

    HANDLE_MISSING = "Handle Missing Values"

    TEXT_CLEANING = "Text Cleaning"

    NUMERIC_CLEANING = "Numeric Cleaning"

    DATE_CLEANING = "Date Cleaning"

    COLUMN_OPERATIONS = "Column Operations"

# ==========================================================
# Cleaning Report
# ==========================================================

@dataclass
class CleaningReport:

    original_rows: int = 0

    final_rows: int = 0

    original_columns: int = 0

    final_columns: int = 0

    duplicates_removed: int = 0

    missing_fixed: int = 0

    columns_removed: int = 0

    execution_time: float = 0.0

    operations: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

# ==========================================================
# Session Initialization
# ==========================================================

def initialize_session() -> None:
    """
    Initialize session variables.
    Compatible with previous pages.
    """

    defaults = {

        "dataset": None,

        "cleaned_df": None,

        "profile": None,

        "metadata": None,

        "health_report": None,

        "cleaning_report": None,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value

# ==========================================================
# Dataset Loader
# ==========================================================

def get_dataset() -> Optional[pd.DataFrame]:
    """
    Return latest dataframe.

    If cleaned dataframe exists,
    continue cleaning from it.
    """

    initialize_session()

    if st.session_state.cleaned_df is not None:

        return st.session_state.cleaned_df.copy()

    if st.session_state.dataset is not None:

        return st.session_state.dataset.copy()

    return None

# ==========================================================
# Validation
# ==========================================================

def validate_dataset() -> pd.DataFrame:
    """
    Ensure dataset exists.
    """

    dataframe = get_dataset()

    if dataframe is None:

        st.warning(
            """
No dataset found.

Please upload your dataset from
**1️⃣ Upload Data**
before continuing.
"""
        )

        st.stop()

    return dataframe

# ==========================================================
# Enterprise Cleaning Engine
# ==========================================================

class DataCleaningEngine:
    """
    Enterprise Data Cleaning Engine.

    Responsibilities

    • Missing Value Handling

    • Duplicate Removal

    • Text Cleaning

    • Numeric Cleaning

    • Date Cleaning

    • Column Operations

    • Cleaning Report

    • Session Integration
    """

    def __init__(self):

        self.original_df = validate_dataset()

        self.df = self.original_df.copy()

        self.report = CleaningReport(

            original_rows=len(self.df),

            original_columns=len(self.df.columns),

        )

        self.start_time = time.time()

        logger.info(
            "Data Cleaning Engine initialized."
        )
# ==========================================================
# Remove Duplicate Rows
# ==========================================================

    def remove_duplicate_rows(self) -> None:
        """
        Remove duplicate records.
        """

        before = len(self.df)

        self.df = self.df.drop_duplicates()

        removed = before - len(self.df)

        self.report.duplicates_removed += removed

        if removed > 0:

            self.report.operations.append(
                f"Removed {removed} duplicate rows."
            )

# ==========================================================
# Remove Duplicate Columns
# ==========================================================

    def remove_duplicate_columns(self) -> None:
        """
        Remove duplicate column names.
        """

        before = len(self.df.columns)

        self.df = self.df.loc[
            :,
            ~self.df.columns.duplicated()
        ]

        removed = before - len(self.df.columns)

        self.report.columns_removed += removed

        if removed > 0:

            self.report.operations.append(
                f"Removed {removed} duplicate columns."
            )

# ==========================================================
# Remove Empty Rows
# ==========================================================

    def remove_empty_rows(self) -> None:
        """
        Remove rows where every value is missing/blank.
        """

        before = len(self.df)

        self.df = self.df.dropna(how="all")

        removed = before - len(self.df)

        if removed > 0:

            self.report.operations.append(
                f"Removed {removed} fully empty rows."
            )

# ==========================================================
# Remove Empty Columns
# ==========================================================

    def remove_empty_columns(self) -> None:
        """
        Remove columns where every value is missing/blank.
        """

        before = len(self.df.columns)

        self.df = self.df.dropna(axis=1, how="all")

        removed = before - len(self.df.columns)

        self.report.columns_removed += removed

        if removed > 0:

            self.report.operations.append(
                f"Removed {removed} fully empty columns."
            )

# ==========================================================
# Standardize Column Names
# ==========================================================

    def standardize_column_names(self) -> None:
        """
        Convert column names to a consistent snake_case format:
        lowercase, spaces/special characters replaced with underscores.
        """

        import re as _re

        new_columns = {}

        for col in self.df.columns:

            cleaned = _re.sub(r"[^0-9a-zA-Z]+", "_", str(col).strip())

            cleaned = _re.sub(r"_+", "_", cleaned).strip("_").lower()

            new_columns[col] = cleaned or col

        self.df.rename(columns=new_columns, inplace=True)

        self.report.operations.append(
            "Standardized column names to snake_case."
        )

# ==========================================================
# Remove Outliers
# ==========================================================

    def remove_outliers(
        self,
        columns: Optional[List[str]] = None,
        method: str = "iqr",
        factor: float = 1.5,
    ) -> None:
        """
        Remove rows containing statistical outliers in numeric columns.

        method="iqr"    -> values outside [Q1 - factor*IQR, Q3 + factor*IQR]
        method="zscore" -> values with |z-score| > factor (factor used as
                            the z-score threshold, typically 3)
        """

        numeric_columns = columns or list(
            self.df.select_dtypes(include=["number"]).columns
        )

        if not numeric_columns:
            return

        before = len(self.df)
        mask = pd.Series(True, index=self.df.index)

        for col in numeric_columns:

            series = self.df[col]

            if method == "zscore":

                std = series.std()

                if not std or pd.isna(std):
                    continue

                z_scores = (series - series.mean()) / std

                mask &= z_scores.abs().le(factor) | series.isna()

            else:  # iqr (default)

                q1 = series.quantile(0.25)
                q3 = series.quantile(0.75)
                iqr = q3 - q1

                if pd.isna(iqr) or iqr == 0:
                    continue

                lower = q1 - factor * iqr
                upper = q3 + factor * iqr

                mask &= series.between(lower, upper) | series.isna()

        self.df = self.df[mask]

        removed = before - len(self.df)

        if removed > 0:

            self.report.operations.append(
                f"Removed {removed} rows containing outliers "
                f"({method.upper()} method)."
            )

# ==========================================================
# Handle Missing Values
# ==========================================================

    def handle_missing_values(
        self,
        strategy: str = "mean",
        custom_value: Any = None,
    ) -> None:
        """
        Handle missing values.
        """

        before = int(
            self.df.isna().sum().sum()
        )

        if before == 0:

            return

        if strategy == "drop_rows":

            self.df = self.df.dropna()

        elif strategy == "drop_columns":

            self.df = self.df.dropna(
                axis=1
            )

        elif strategy == "mean":

            for col in self.df.select_dtypes(
                include=["number"]
            ).columns:

                self.df[col] = self.df[col].fillna(
                    self.df[col].mean()
                )

        elif strategy == "median":

            for col in self.df.select_dtypes(
                include=["number"]
            ).columns:

                self.df[col] = self.df[col].fillna(
                    self.df[col].median()
                )

        elif strategy == "mode":

            for col in self.df.columns:

                mode = self.df[col].mode()

                if not mode.empty:

                    self.df[col] = self.df[col].fillna(
                        mode.iloc[0]
                    )

        elif strategy == "ffill":

            self.df = self.df.ffill()

        elif strategy == "bfill":

            self.df = self.df.bfill()

        elif strategy == "custom":

            self.df = self.df.fillna(
                custom_value
            )

        after = int(
            self.df.isna().sum().sum()
        )

        fixed = before - after

        self.report.missing_fixed += fixed

        self.report.operations.append(
            f"Handled missing values using '{strategy}'."
        )

# ==========================================================
# Finish Cleaning
# ==========================================================

    def finalize(self) -> None:
        """
        Finalize cleaning process.
        """

        self.report.final_rows = len(
            self.df
        )

        self.report.final_columns = len(
            self.df.columns
        )

        self.report.execution_time = round(

            time.time() - self.start_time,

            2,

        )
# ==========================================================
# Text Cleaning
# ==========================================================

    def clean_text_columns(
        self,
        trim: bool = True,
        lower: bool = False,
        upper: bool = False,
        title: bool = False,
        remove_special: bool = False,
    ) -> None:
        """
        Clean text columns.
        """

        text_columns = self.df.select_dtypes(
            include=["object", "category"]
        ).columns

        for col in text_columns:

            series = self.df[col].astype(str)

            if trim:

                series = series.str.strip()

            if lower:

                series = series.str.lower()

            if upper:

                series = series.str.upper()

            if title:

                series = series.str.title()

            if remove_special:

                series = series.str.replace(
                    r"[^A-Za-z0-9 ]",
                    "",
                    regex=True,
                )

            self.df[col] = series

        self.report.operations.append(
            "Text cleaning completed."
        )


# ==========================================================
# Numeric Cleaning
# ==========================================================

    def clean_numeric_columns(
        self,
        round_digits: Optional[int] = None,
        absolute_values: bool = False,
    ) -> None:
        """
        Clean numeric columns.
        """

        numeric_columns = self.df.select_dtypes(
            include=["number"]
        ).columns

        for col in numeric_columns:

            if absolute_values:

                self.df[col] = self.df[col].abs()

            if round_digits is not None:

                self.df[col] = self.df[col].round(
                    round_digits
                )

        self.report.operations.append(
            "Numeric cleaning completed."
        )


# ==========================================================
# Date Cleaning
# ==========================================================

    def clean_date_columns(
        self,
        infer_dates: bool = True,
    ) -> None:
        """
        Convert date columns.
        """

        for column in self.df.columns:

            if infer_dates:

                try:

                    converted = pd.to_datetime(
                        self.df[column],
                        errors="ignore",
                    )

                    self.df[column] = converted

                except Exception:

                    continue

        self.report.operations.append(
            "Date cleaning completed."
        )


# ==========================================================
# Column Operations
# ==========================================================

    def rename_columns(
        self,
        mapping: Dict[str, str],
    ) -> None:
        """
        Rename columns.
        """

        self.df.rename(
            columns=mapping,
            inplace=True,
        )

        self.report.operations.append(
            "Columns renamed."
        )


    def drop_columns(
        self,
        columns: List[str],
    ) -> None:
        """
        Drop selected columns.
        """

        existing = [

            col

            for col in columns

            if col in self.df.columns

        ]

        if existing:

            self.df.drop(

                columns=existing,

                inplace=True,

            )

            self.report.columns_removed += len(
                existing
            )

            self.report.operations.append(

                f"Removed {len(existing)} columns."

            )


# ==========================================================
# Get Clean Data
# ==========================================================

    def get_dataframe(
        self,
    ) -> pd.DataFrame:
        """
        Return cleaned dataframe.
        """

        return self.df.copy()
# ==========================================================
# Cleaning Summary Cards
# ==========================================================

def show_cleaning_summary(
    report: CleaningReport,
) -> None:
    """
    Display cleaning summary cards.
    """

    st.subheader("🧹 Cleaning Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Original Rows",
            f"{report.original_rows:,}"
        )

    with c2:
        st.metric(
            "Current Rows",
            f"{report.final_rows:,}"
        )

    with c3:
        st.metric(
            "Duplicates Removed",
            report.duplicates_removed
        )

    with c4:
        st.metric(
            "Missing Fixed",
            report.missing_fixed
        )

    c5, c6, c7 = st.columns(3)

    with c5:
        st.metric(
            "Columns Removed",
            report.columns_removed
        )

    with c6:
        st.metric(
            "Execution Time",
            f"{report.execution_time:.2f}s"
        )

    with c7:
        st.metric(
            "Operations",
            len(report.operations)
        )


# ==========================================================
# Before / After Preview
# ==========================================================

def show_dataset_preview(
    original_df: pd.DataFrame,
    cleaned_df: pd.DataFrame,
) -> None:
    """
    Show before/after preview.
    """

    st.subheader("👀 Dataset Preview")

    tab1, tab2 = st.tabs(
        [
            "Original Dataset",
            "Cleaned Dataset",
        ]
    )

    with tab1:

        st.dataframe(
            original_df.head(20),
            use_container_width=True,
            hide_index=True,
        )

    with tab2:

        st.dataframe(
            cleaned_df.head(20),
            use_container_width=True,
            hide_index=True,
        )


# ==========================================================
# Cleaning Controls
# ==========================================================

def show_cleaning_controls():
    """
    Cleaning options.
    """

    st.subheader("⚙ Cleaning Options")

    options = {}

    dataframe = get_dataset()
    all_columns = list(dataframe.columns) if dataframe is not None else []
    numeric_columns = (
        list(dataframe.select_dtypes(include=["number"]).columns)
        if dataframe is not None else []
    )

    # ------------------------------------------------------
    # Basic Cleaning
    # ------------------------------------------------------
    with st.expander("🧺 Basic Cleaning", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            options["remove_duplicates"] = st.checkbox(
                "Remove Duplicate Rows",
                value=True,
            )

            options["remove_duplicate_columns"] = st.checkbox(
                "Remove Duplicate Columns",
                value=True,
            )

            options["remove_empty_rows"] = st.checkbox(
                "Remove Fully Empty Rows",
                value=True,
            )

            options["remove_empty_columns"] = st.checkbox(
                "Remove Fully Empty Columns",
                value=True,
            )

        with col2:

            options["handle_missing"] = st.selectbox(
                "Handle Missing Values",
                [
                    "None",
                    "mean",
                    "median",
                    "mode",
                    "ffill",
                    "bfill",
                    "custom",
                    "drop_rows",
                    "drop_columns",
                ],
            )

            options["missing_custom_value"] = ""

            if options["handle_missing"] == "custom":

                options["missing_custom_value"] = st.text_input(
                    "Fill missing values with",
                    value="N/A",
                )

            options["round_numbers"] = st.checkbox(
                "Round Numeric Values (2 decimals)"
            )

            options["convert_dates"] = st.checkbox(
                "Convert Date Columns",
                value=True,
            )

    # ------------------------------------------------------
    # Text Cleaning
    # ------------------------------------------------------
    with st.expander("🔤 Text Cleaning", expanded=False):

        col1, col2 = st.columns(2)

        with col1:

            options["trim_text"] = st.checkbox(
                "Trim Extra Spaces",
                value=True,
            )

            text_case = st.radio(
                "Text Case",
                ["No Change", "lowercase", "UPPERCASE", "Title Case"],
                horizontal=True,
            )
            options["lower_case"] = text_case == "lowercase"
            options["upper_case"] = text_case == "UPPERCASE"
            options["title_case"] = text_case == "Title Case"

        with col2:

            options["remove_special_chars"] = st.checkbox(
                "Remove Special Characters from Text",
                help="Strips punctuation/symbols from text columns, "
                     "keeping only letters, numbers and spaces.",
            )

    # ------------------------------------------------------
    # Column Management
    # ------------------------------------------------------
    with st.expander("🏷️ Column Management", expanded=False):

        options["standardize_columns"] = st.checkbox(
            "Standardize Column Names (snake_case)",
            help="e.g. 'Customer Name!' -> 'customer_name'",
        )

        options["drop_columns"] = st.multiselect(
            "Drop Selected Columns",
            all_columns,
            help="Columns picked here are removed entirely from the dataset.",
        )

    # ------------------------------------------------------
    # Advanced Cleaning
    # ------------------------------------------------------
    with st.expander("🎯 Advanced Cleaning (Outliers)", expanded=False):

        options["remove_outliers"] = st.checkbox(
            "Remove Statistical Outliers",
            help="Removes rows with extreme numeric values that can "
                 "distort charts, KPIs and AI insights.",
        )

        options["outlier_method"] = "iqr"
        options["outlier_columns"] = []
        options["outlier_factor"] = 1.5

        if options["remove_outliers"] and numeric_columns:

            oc1, oc2 = st.columns(2)

            with oc1:

                options["outlier_method"] = st.selectbox(
                    "Detection Method",
                    ["iqr", "zscore"],
                    format_func=lambda m: "IQR (Interquartile Range)" if m == "iqr" else "Z-Score",
                )

            with oc2:

                options["outlier_factor"] = st.slider(
                    "Sensitivity",
                    min_value=1.0,
                    max_value=4.0,
                    value=1.5 if options["outlier_method"] == "iqr" else 3.0,
                    step=0.5,
                    help="Lower = stricter (removes more rows). "
                         "IQR typically uses 1.5, Z-Score typically uses 3.0.",
                )

            options["outlier_columns"] = st.multiselect(
                "Apply to columns (default: all numeric columns)",
                numeric_columns,
            )

        elif options["remove_outliers"] and not numeric_columns:

            st.info("No numeric columns available for outlier detection.")

    return options


# ==========================================================
# Cleaning History
# ==========================================================

def show_cleaning_history(
    report: CleaningReport,
) -> None:
    """
    Display cleaning log.
    """

    st.subheader("📜 Cleaning History")

    if len(report.operations) == 0:

        st.info(
            "No cleaning operations performed."
        )

        return

    for operation in report.operations:

        st.success(operation)


# ==========================================================
# Warnings
# ==========================================================

def show_cleaning_warnings(
    report: CleaningReport,
) -> None:
    """
    Display warnings.
    """

    if len(report.warnings) == 0:

        return

    st.subheader("⚠ Warnings")

    for warning in report.warnings:

        st.warning(warning)
# ==========================================================
# Save Clean Dataset
# ==========================================================

def save_clean_dataset(
    engine: DataCleaningEngine,
) -> None:
    """
    Save cleaned dataframe into session state.
    """

    cleaned_df = engine.get_dataframe()

    st.session_state.cleaned_df = cleaned_df

    st.session_state.cleaning_report = engine.report

    logger.info(
        "Clean dataset stored in session state."
    )


# ==========================================================
# Download Clean Dataset
# ==========================================================

def download_clean_dataset(
    dataframe: pd.DataFrame,
) -> None:
    """
    Download cleaned dataset.
    """

    csv = dataframe.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="⬇ Download Clean Dataset",

        data=csv,

        file_name="clean_dataset.csv",

        mime="text/csv",

        use_container_width=True,

    )


# ==========================================================
# Execute Cleaning
# ==========================================================

def execute_cleaning(
    engine: DataCleaningEngine,
    options: dict,
) -> None:
    """
    Execute selected cleaning operations.
    """

    if options["remove_duplicates"]:

        engine.remove_duplicate_rows()

    if options["remove_duplicate_columns"]:

        engine.remove_duplicate_columns()

    if options.get("remove_empty_rows"):

        engine.remove_empty_rows()

    if options.get("remove_empty_columns"):

        engine.remove_empty_columns()

    if options.get("drop_columns"):

        engine.drop_columns(options["drop_columns"])

    if options.get("standardize_columns"):

        engine.standardize_column_names()

    if options["handle_missing"] != "None":

        engine.handle_missing_values(
            strategy=options["handle_missing"],
            custom_value=options.get("missing_custom_value"),
        )

    engine.clean_text_columns(

        trim=options["trim_text"],

        lower=options.get("lower_case", False),

        upper=options.get("upper_case", False),

        title=options.get("title_case", False),

        remove_special=options.get("remove_special_chars", False),

    )

    if options["round_numbers"]:

        engine.clean_numeric_columns(
            round_digits=2
        )

    if options.get("remove_outliers"):

        engine.remove_outliers(
            columns=options.get("outlier_columns") or None,
            method=options.get("outlier_method", "iqr"),
            factor=options.get("outlier_factor", 1.5),
        )

    if options["convert_dates"]:

        engine.clean_date_columns()

    engine.finalize()

    save_clean_dataset(engine)


# ==========================================================
# Footer
# ==========================================================

def show_footer():

    st.divider()

    st.caption(
        "AI Data Analyzer Pro | Enterprise Cleaning Workspace"
    )

    st.caption(
        "© 2026 Punit Tech Hub"
    )


# ==========================================================
# Main
# ==========================================================

def main():

    st.title(
        "🧹 Data Cleaning Workspace"
    )

    st.markdown(
        """
Prepare your dataset for

✔ AI Insights

✔ Premium Dashboard

✔ Reporting
"""
    )

    engine = DataCleaningEngine()

    options = show_cleaning_controls()

    if st.button(

        "🚀 Apply Cleaning",

        use_container_width=True,

    ):

        with st.spinner(
            "Cleaning dataset..."
        ):

            execute_cleaning(
                engine,
                options,
            )

        st.success(
            "Cleaning completed successfully."
        )

    report = engine.report

    if report.final_rows == 0:

        report.final_rows = report.original_rows

        report.final_columns = report.original_columns

    show_cleaning_summary(
        report
    )

    show_dataset_preview(

        engine.original_df,

        engine.get_dataframe(),

    )

    show_cleaning_history(
        report
    )

    show_cleaning_warnings(
        report
    )

    download_clean_dataset(
        engine.get_dataframe()
    )

    show_footer()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    try:

        main()

    except Exception as ex:

        logger.exception(ex)

        st.error(
            "Data Cleaning module failed."
        )

        st.exception(ex)
