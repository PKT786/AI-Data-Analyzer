"""
=========================================================
AI Data Analyzer Pro
Enterprise Data Cleaning Engine

Author : Punit Tech Hub
Version : 4.0 Enterprise
=========================================================
"""

from __future__ import annotations

import copy
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from sklearn.preprocessing import (
    LabelEncoder,
    MinMaxScaler,
    StandardScaler,
)

from utils.logger import get_logger
from utils.validators import (
    validate_dataframe,
    validate_column_exists,
    validate_columns_exist,
)

logger = get_logger(__name__)


# ==========================================================
# ENTERPRISE DATA CLEANER
# ==========================================================

class DataCleaner:
    """
    Enterprise Data Cleaning Engine

    Features
    --------
    ✓ Remove Duplicates

    ✓ Remove Empty Rows

    ✓ Handle Missing Values

    ✓ Trim Text

    ✓ Standardize Column Names

    ✓ Convert Data Types

    ✓ Optimize Memory

    ✓ Encode Columns

    ✓ Scale Data

    ✓ Outlier Removal

    ✓ Auto Cleaning

    ✓ Cleaning Pipeline

    ✓ Undo

    ✓ Cleaning History

    Original dataframe is NEVER modified.
    """

    # ======================================================
    # INITIALIZATION
    # ======================================================

    def __init__(self):

        self._history: List[Dict[str, Any]] = []

        self._snapshots: List[pd.DataFrame] = []

        self._label_encoders: Dict[str, LabelEncoder] = {}

        logger.info(
            "Enterprise DataCleaner initialized."
        )

    # ======================================================
    # INTERNAL COPY
    # ======================================================

    def _copy_df(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        return df.copy(deep=True)

    # ======================================================
    # HISTORY
    # ======================================================

    def _add_history(
        self,
        operation: str,
        details: Dict[str, Any],
    ):

        self._history.append({

            "timestamp":
                datetime.now(),

            "operation":
                operation,

            "details":
                details,

        })

    # ======================================================
    # SNAPSHOT
    # ======================================================

    def _save_snapshot(
        self,
        df: pd.DataFrame,
    ):

        self._snapshots.append(
            self._copy_df(df)
        )

    # ======================================================
    # VALIDATION HELPERS
    # ======================================================

    def validate_column(
        self,
        df: pd.DataFrame,
        column: str,
    ):

        validate_column_exists(
            df,
            column,
        )

    def validate_columns(
        self,
        df: pd.DataFrame,
        columns: List[str],
    ):

        validate_columns_exist(
            df,
            columns,
        )

    # ======================================================
    # RESET HISTORY
    # ======================================================

    def clear_history(self):

        self._history.clear()

        self._snapshots.clear()

        logger.info(
            "Cleaning history cleared."
        )

    # ======================================================
    # RETURN HISTORY
    # ======================================================

    @property
    def history(self):

        return self._history
        # ======================================================
    # REMOVE DUPLICATE ROWS
    # ======================================================

    def remove_duplicate_rows(
        self,
        df: pd.DataFrame,
        keep: str = "first",
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        before = len(working_df)

        working_df = working_df.drop_duplicates(
            keep=keep
        ).reset_index(drop=True)

        removed = before - len(working_df)

        self._add_history(
            "Remove Duplicate Rows",
            {
                "rows_removed": removed
            }
        )

        logger.info(
            f"Removed {removed} duplicate rows."
        )

        return working_df

    # ======================================================
    # REMOVE EMPTY ROWS
    # ======================================================

    def remove_empty_rows(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        before = len(working_df)

        working_df = working_df.dropna(
            how="all"
        ).reset_index(drop=True)

        removed = before - len(working_df)

        self._add_history(
            "Remove Empty Rows",
            {
                "rows_removed": removed
            }
        )

        logger.info(
            f"Removed {removed} empty rows."
        )

        return working_df

    # ======================================================
    # REMOVE EMPTY COLUMNS
    # ======================================================

    def remove_empty_columns(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        before = len(working_df.columns)

        working_df = working_df.dropna(
            axis=1,
            how="all"
        )

        removed = before - len(working_df.columns)

        self._add_history(
            "Remove Empty Columns",
            {
                "columns_removed": removed
            }
        )

        logger.info(
            f"Removed {removed} empty columns."
        )

        return working_df

    # ======================================================
    # STANDARDIZE COLUMN NAMES
    # ======================================================

    def standardize_column_names(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        working_df.columns = (

            working_df.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace("-", "_", regex=False)
            .str.replace("/", "_", regex=False)
            .str.replace(r"[^a-zA-Z0-9_]", "", regex=True)

        )

        self._add_history(
            "Standardize Column Names",
            {}
        )

        logger.info(
            "Column names standardized."
        )

        return working_df

    # ======================================================
    # TRIM TEXT COLUMNS
    # ======================================================

    def trim_text_columns(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        if columns is None:

            columns = working_df.select_dtypes(
                include=["object", "string"]
            ).columns.tolist()

        for column in columns:

            if column not in working_df.columns:
                continue

            working_df[column] = (
                working_df[column]
                .astype(str)
                .str.strip()
            )

        self._add_history(
            "Trim Text Columns",
            {
                "columns": columns
            }
        )

        logger.info(
            "Text columns trimmed."
        )

        return working_df
        # ======================================================
    # HANDLE MISSING VALUES
    # ======================================================

    def handle_missing_values(
        self,
        df: pd.DataFrame,
        strategy: str = "median",
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        numeric_cols = working_df.select_dtypes(
            include=np.number
        ).columns

        categorical_cols = working_df.select_dtypes(
            include=["object", "category", "string"]
        ).columns

        for col in numeric_cols:

            if working_df[col].isna().sum() == 0:
                continue

            if strategy == "mean":

                value = working_df[col].mean()

            elif strategy == "median":

                value = working_df[col].median()

            elif strategy == "zero":

                value = 0

            else:

                value = working_df[col].median()

            working_df[col] = working_df[col].fillna(value)

        for col in categorical_cols:

            if working_df[col].isna().sum() == 0:
                continue

            mode = working_df[col].mode()

            if len(mode):

                working_df[col] = working_df[col].fillna(mode.iloc[0])

            else:

                working_df[col] = working_df[col].fillna("Unknown")

        self._add_history(

            "Handle Missing Values",

            {

                "strategy": strategy

            },

        )

        logger.info("Missing values handled.")

        return working_df

    # ======================================================
    # CONVERT DATA TYPES
    # ======================================================

    def convert_data_types(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        for column in working_df.columns:

            if working_df[column].dtype == object:

                try:

                    working_df[column] = pd.to_datetime(
                        working_df[column]
                    )

                    continue

                except Exception:

                    pass

                try:

                    working_df[column] = pd.to_numeric(
                        working_df[column]
                    )

                    continue

                except Exception:

                    pass

        self._add_history(

            "Convert Data Types",

            {},

        )

        logger.info("Data type conversion completed.")

        return working_df

    # ======================================================
    # OPTIMIZE MEMORY
    # ======================================================

    def optimize_memory(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        before = (

            working_df.memory_usage(
                deep=True
            ).sum()

            / 1024
            / 1024

        )

        for column in working_df.select_dtypes(

            include=["int"]

        ).columns:

            working_df[column] = pd.to_numeric(

                working_df[column],

                downcast="integer",

            )

        for column in working_df.select_dtypes(

            include=["float"]

        ).columns:

            working_df[column] = pd.to_numeric(

                working_df[column],

                downcast="float",

            )

        after = (

            working_df.memory_usage(
                deep=True
            ).sum()

            / 1024
            / 1024

        )

        self._add_history(

            "Optimize Memory",

            {

                "before_mb": round(before, 2),

                "after_mb": round(after, 2),

            },

        )

        logger.info(

            f"Memory optimized {before:.2f}MB -> {after:.2f}MB"

        )

        return working_df

    # ======================================================
    # CLEAN TEXT
    # ======================================================

    def clean_text(
        self,
        df: pd.DataFrame,
        columns: List[str],
    ) -> pd.DataFrame:

        self.validate_columns(df, columns)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        for col in columns:

            working_df[col] = (

                working_df[col]

                .astype(str)

                .str.replace(
                    r"\s+",
                    " ",
                    regex=True,
                )

                .str.strip()

            )

        self._add_history(

            "Clean Text",

            {

                "columns": columns

            },

        )

        logger.info("Text cleaned.")

        return working_df

    # ======================================================
    # NORMALIZE TEXT
    # ======================================================

    def normalize_text(
        self,
        df: pd.DataFrame,
        columns: List[str],
    ) -> pd.DataFrame:

        self.validate_columns(df, columns)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        for col in columns:

            working_df[col] = (

                working_df[col]

                .astype(str)

                .str.lower()

                .str.strip()

            )

        self._add_history(

            "Normalize Text",

            {

                "columns": columns

            },

        )

        logger.info("Text normalized.")

        return working_df
        # ======================================================
    # REMOVE OUTLIERS (IQR)
    # ======================================================

    def remove_outliers(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        multiplier: float = 1.5,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        if columns is None:

            columns = working_df.select_dtypes(
                include=np.number
            ).columns.tolist()

        for col in columns:

            if col not in working_df.columns:
                continue

            q1 = working_df[col].quantile(0.25)

            q3 = working_df[col].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - multiplier * iqr

            upper = q3 + multiplier * iqr

            working_df = working_df[
                (working_df[col] >= lower)
                &
                (working_df[col] <= upper)
            ]

        working_df = working_df.reset_index(drop=True)

        self._add_history(

            "Remove Outliers",

            {

                "columns": columns,

            },

        )

        logger.info("Outliers removed.")

        return working_df

    # ======================================================
    # LABEL ENCODING
    # ======================================================

    def label_encode(
        self,
        df: pd.DataFrame,
        columns: List[str],
    ) -> pd.DataFrame:

        self.validate_columns(df, columns)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        for col in columns:

            encoder = LabelEncoder()

            working_df[col] = encoder.fit_transform(

                working_df[col].astype(str)

            )

            self._label_encoders[col] = encoder

        self._add_history(

            "Label Encoding",

            {

                "columns": columns

            },

        )

        logger.info("Label encoding completed.")

        return working_df

    # ======================================================
    # ONE HOT ENCODING
    # ======================================================

    def one_hot_encode(
        self,
        df: pd.DataFrame,
        columns: List[str],
    ) -> pd.DataFrame:

        self.validate_columns(df, columns)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        working_df = pd.get_dummies(

            working_df,

            columns=columns,

            drop_first=False,

        )

        self._add_history(

            "One Hot Encoding",

            {

                "columns": columns

            },

        )

        logger.info("One-hot encoding completed.")

        return working_df

    # ======================================================
    # STANDARD SCALER
    # ======================================================

    def standard_scale(
        self,
        df: pd.DataFrame,
        columns: List[str],
    ) -> pd.DataFrame:

        self.validate_columns(df, columns)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        scaler = StandardScaler()

        working_df[columns] = scaler.fit_transform(

            working_df[columns]

        )

        self._add_history(

            "Standard Scaling",

            {

                "columns": columns

            },

        )

        logger.info("Standard scaling completed.")

        return working_df

    # ======================================================
    # MIN MAX SCALER
    # ======================================================

    def minmax_scale(
        self,
        df: pd.DataFrame,
        columns: List[str],
    ) -> pd.DataFrame:

        self.validate_columns(df, columns)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        scaler = MinMaxScaler()

        working_df[columns] = scaler.fit_transform(

            working_df[columns]

        )

        self._add_history(

            "MinMax Scaling",

            {

                "columns": columns

            },

        )

        logger.info("MinMax scaling completed.")

        return working_df

    # ======================================================
    # BOOLEAN CONVERSION
    # ======================================================

    def convert_boolean(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        mapping = {

            "true": True,

            "false": False,

            "yes": True,

            "no": False,

            "1": True,

            "0": False,

        }

        for col in working_df.select_dtypes(

            include=["object", "string"]

        ).columns:

            values = (

                working_df[col]

                .astype(str)

                .str.lower()

            )

            if values.isin(mapping.keys()).all():

                working_df[col] = values.map(mapping)

        self._add_history(

            "Boolean Conversion",

            {}

        )

        logger.info("Boolean conversion completed.")

        return working_df

    # ======================================================
    # DATE STANDARDIZATION
    # ======================================================

    def standardize_dates(
        self,
        df: pd.DataFrame,
        columns: List[str],
    ) -> pd.DataFrame:

        self.validate_columns(df, columns)

        working_df = self._copy_df(df)

        self._save_snapshot(working_df)

        for col in columns:

            working_df[col] = pd.to_datetime(

                working_df[col],

                errors="coerce",

            )

        self._add_history(

            "Standardize Dates",

            {

                "columns": columns

            },

        )

        logger.info("Date standardization completed.")

        return working_df
        # ======================================================
    # RUN CLEANING PIPELINE
    # ======================================================

    def run_pipeline(
        self,
        df: pd.DataFrame,
        config: Dict[str, Any],
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        logger.info("Running cleaning pipeline...")

        if config.get("remove_duplicates", False):
            working_df = self.remove_duplicate_rows(
                working_df
            )

        if config.get("remove_empty_rows", False):
            working_df = self.remove_empty_rows(
                working_df
            )

        if config.get("remove_empty_columns", False):
            working_df = self.remove_empty_columns(
                working_df
            )

        if config.get("handle_missing", False):
            strategy = config.get(
                "missing_strategy",
                "median",
            )

            working_df = self.handle_missing_values(
                working_df,
                strategy=strategy,
            )

        if config.get("standardize_columns", False):
            working_df = self.standardize_column_names(
                working_df
            )

        if config.get("trim_text", False):
            working_df = self.trim_text_columns(
                working_df
            )

        if config.get("convert_types", False):
            working_df = self.convert_data_types(
                working_df
            )

        if config.get("optimize_memory", False):
            working_df = self.optimize_memory(
                working_df
            )

        if config.get("remove_outliers", False):
            working_df = self.remove_outliers(
                working_df
            )

        logger.info(
            "Cleaning pipeline completed."
        )

        return working_df

    # ======================================================
    # AUTO CLEAN
    # ======================================================

    def auto_clean(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        config = {

            "remove_duplicates": True,

            "remove_empty_rows": True,

            "remove_empty_columns": True,

            "handle_missing": True,

            "missing_strategy": "median",

            "standardize_columns": True,

            "trim_text": True,

            "convert_types": True,

            "optimize_memory": True,

        }

        return self.run_pipeline(
            df,
            config,
        )

    # ======================================================
    # UNDO LAST OPERATION
    # ======================================================

    def undo(
        self,
    ) -> Optional[pd.DataFrame]:

        if not self._snapshots:

            logger.warning(
                "Nothing to undo."
            )

            return None

        snapshot = self._snapshots.pop()

        if self._history:

            self._history.pop()

        logger.info(
            "Undo successful."
        )

        return snapshot

    # ======================================================
    # RESET
    # ======================================================

    def reset(self):

        self._history.clear()

        self._snapshots.clear()

        self._label_encoders.clear()

        logger.info(
            "Cleaner reset."
        )

    # ======================================================
    # EXPORT CLEANING REPORT
    # ======================================================

    def export_cleaning_report(
        self,
    ) -> Dict[str, Any]:

        return {

            "operations":

                len(self._history),

            "history":

                self._history,

        }

    # ======================================================
    # INVERSE LABEL ENCODING
    # ======================================================

    def inverse_label_encode(
        self,
        df: pd.DataFrame,
        column: str,
    ) -> pd.DataFrame:

        validate_dataframe(df)

        working_df = self._copy_df(df)

        if column not in self._label_encoders:

            return working_df

        encoder = self._label_encoders[column]

        working_df[column] = encoder.inverse_transform(

            working_df[column]

        )

        return working_df

    # ======================================================
    # CLASS INFO
    # ======================================================

    @property
    def version(self):

        return "4.0 Enterprise"

    def __repr__(self):

        return (

            f"DataCleaner("

            f"version='{self.version}')"

        )


# ======================================================
# GLOBAL INSTANCE
# ======================================================

cleaning_operations = DataCleaner()
