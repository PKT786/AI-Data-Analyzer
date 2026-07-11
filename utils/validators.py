"""
=========================================================
AI Data Analyzer Pro
Validation Utilities
=========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

from config.settings import settings


# ==========================================================
# DATAFRAME VALIDATION
# ==========================================================

def validate_dataframe(df: Optional[pd.DataFrame]) -> bool:
    """
    Validate a pandas DataFrame.

    Raises
    ------
    ValueError
        If dataframe is invalid.
    """

    if df is None:
        raise ValueError("DataFrame cannot be None.")

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    if df.empty:
        raise ValueError("DataFrame is empty.")

    if len(df) > settings.upload.MAX_ROWS:
        raise ValueError(
            f"Maximum supported rows: {settings.upload.MAX_ROWS:,}"
        )

    if len(df.columns) > settings.upload.MAX_COLUMNS:
        raise ValueError(
            f"Maximum supported columns: {settings.upload.MAX_COLUMNS}"
        )

    return True


# ==========================================================
# COLUMN VALIDATION
# ==========================================================

def validate_column_exists(
    df: pd.DataFrame,
    column: str,
) -> bool:
    """
    Ensure column exists.
    """

    validate_dataframe(df)

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' not found."
        )

    return True


def validate_columns_exist(
    df: pd.DataFrame,
    columns: Iterable[str],
) -> bool:
    """
    Ensure multiple columns exist.
    """

    validate_dataframe(df)

    missing = [

        col

        for col in columns

        if col not in df.columns

    ]

    if missing:

        raise ValueError(

            f"Columns not found: {missing}"

        )

    return True


# ==========================================================
# NUMERIC COLUMN VALIDATION
# ==========================================================

def validate_numeric_column(
    df: pd.DataFrame,
    column: str,
) -> bool:
    """
    Ensure column is numeric.
    """

    validate_column_exists(df, column)

    if not pd.api.types.is_numeric_dtype(

        df[column]

    ):

        raise ValueError(

            f"'{column}' is not numeric."

        )

    return True


# ==========================================================
# FILE VALIDATION
# ==========================================================

def validate_file_extension(
    filename: str,
) -> bool:
    """
    Validate uploaded file extension.
    """

    extension = (

        Path(filename)

        .suffix

        .lower()

        .replace(".", "")

    )

    if extension not in settings.upload.SUPPORTED_FILE_TYPES:

        raise ValueError(

            f"Unsupported file type: {extension}"

        )

    return True


# ==========================================================
# CHART VALIDATION
# ==========================================================

def validate_chart_columns(
    df: pd.DataFrame,
    x_column: str,
    y_column: Optional[str] = None,
) -> bool:
    """
    Validate chart columns.
    """

    validate_column_exists(df, x_column)

    if y_column is not None:

        validate_column_exists(

            df,

            y_column,

        )

    return True


# ==========================================================
# VALUE VALIDATION
# ==========================================================

def validate_not_empty(
    value,
    name: str = "Value",
) -> bool:
    """
    Ensure value is not empty.
    """

    if value is None:

        raise ValueError(

            f"{name} cannot be None."

        )

    if isinstance(value, str):

        if value.strip() == "":

            raise ValueError(

                f"{name} cannot be empty."

            )

    return True


# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [

    "validate_dataframe",

    "validate_column_exists",

    "validate_columns_exist",

    "validate_numeric_column",

    "validate_file_extension",

    "validate_chart_columns",

    "validate_not_empty",

]
