"""
=========================================================
AI Data Analyzer Pro
Enterprise Data Loader
Author : Punit Tech Hub
Version : 3.0
=========================================================
"""

from __future__ import annotations

import os
import json
import pickle
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd

from config.settings import settings
from utils.logger import get_logger
from utils.validators import validate_dataframe

logger = get_logger(__name__)


# =====================================================
# DATA LOADER
# =====================================================

class DataLoader:
    """
    Enterprise Data Loading Engine

    Features
    --------
    ✓ CSV
    ✓ Excel
    ✓ JSON
    ✓ Parquet
    ✓ Pickle

    ✓ Validation

    ✓ Dataset Information

    ✓ Preview

    ✓ Statistics

    ✓ Logging

    ✓ Reset
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        self.current_dataframe: Optional[pd.DataFrame] = None

        self.file_path: Optional[str] = None

        self.file_name: Optional[str] = None

        self.file_type: Optional[str] = None

        logger.info("DataLoader initialized.")

    # =====================================================
    # INTERNAL HELPERS
    # =====================================================

    def _copy_df(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        Return deep copy.
        """

        return df.copy(deep=True)

    # -----------------------------------------------------

    def _validate_extension(
        self,
        file_path: str,
    ) -> str:
        """
        Validate file extension.
        """

        if not os.path.exists(file_path):

            raise FileNotFoundError(
                f"File not found : {file_path}"
            )

        extension = Path(file_path).suffix.lower()

        if extension not in settings.upload.SUPPORTED_FILE_TYPES:

            raise ValueError(
                f"Unsupported file type : {extension}"
            )

        return extension

    # -----------------------------------------------------

    def _finalize_load(
        self,
        df: pd.DataFrame,
        file_path: str,
        extension: str,
    ) -> pd.DataFrame:
        """
        Store metadata after successful load.
        """

        validate_dataframe(df)

        self.current_dataframe = self._copy_df(df)

        self.file_path = file_path

        self.file_name = Path(file_path).name

        self.file_type = extension.replace(".", "")

        logger.info(
            f"Dataset loaded successfully : {self.file_name}"
        )

        return self.current_dataframe

    # =====================================================
    # MAIN LOADER
    # =====================================================

    def load(
        self,
        file_path: str,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Automatically load dataset.
        """

        extension = self._validate_extension(file_path)

        logger.info(
            f"Detected file type : {extension}"
        )

        if extension == ".csv":

            return self.load_csv(
                file_path,
                **kwargs,
            )

        elif extension in (
            ".xlsx",
            ".xls",
            ".xlsm",
        ):

            return self.load_excel(
                file_path,
                **kwargs,
            )

        elif extension == ".json":

            return self.load_json(
                file_path,
                **kwargs,
            )

        elif extension == ".parquet":

            return self.load_parquet(
                file_path,
                **kwargs,
            )

        elif extension in (
            ".pickle",
            ".pkl",
        ):

            return self.load_pickle(
                file_path,
                **kwargs,
            )

        raise ValueError(
            f"Unsupported file type : {extension}"
        )

    # =====================================================
    # CSV
    # =====================================================

    def load_csv(
        self,
        file_path: str,
        encoding: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:

        if encoding is None:

            encoding = settings.upload.DEFAULT_ENCODING

        logger.info(
            "Loading CSV dataset..."
        )

        df = pd.read_csv(

            file_path,

            encoding=encoding,

            **kwargs,

        )

        return self._finalize_load(
            df,
            file_path,
            ".csv",
        )

    # =====================================================
    # EXCEL
    # =====================================================

    def load_excel(
        self,
        file_path: str,
        sheet_name=0,
        **kwargs,
    ) -> pd.DataFrame:

        logger.info(
            "Loading Excel dataset..."
        )

        df = pd.read_excel(

            file_path,

            sheet_name=sheet_name,

            engine="openpyxl",

            **kwargs,

        )

        return self._finalize_load(
            df,
            file_path,
            Path(file_path).suffix.lower(),
        )

    # =====================================================
    # JSON
    # =====================================================

    def load_json(
        self,
        file_path: str,
        **kwargs,
    ) -> pd.DataFrame:

        logger.info(
            "Loading JSON dataset..."
        )

        df = pd.read_json(

            file_path,

            **kwargs,

        )

        return self._finalize_load(
            df,
            file_path,
            ".json",
        )
        # =====================================================
    # PARQUET
    # =====================================================

    def load_parquet(
        self,
        file_path: str,
        **kwargs,
    ) -> pd.DataFrame:

        logger.info(
            "Loading Parquet dataset..."
        )

        df = pd.read_parquet(

            file_path,

            **kwargs,

        )

        return self._finalize_load(
            df,
            file_path,
            ".parquet",
        )

    # =====================================================
    # PICKLE
    # =====================================================

    def load_pickle(
        self,
        file_path: str,
    ) -> pd.DataFrame:

        logger.info(
            "Loading Pickle dataset..."
        )

        with open(
            file_path,
            "rb",
        ) as f:

            df = pickle.load(f)

        if not isinstance(
            df,
            pd.DataFrame,
        ):

            raise TypeError(
                "Pickle does not contain a pandas DataFrame."
            )

        return self._finalize_load(
            df,
            file_path,
            ".pickle",
        )

    # =====================================================
    # DATASET INFORMATION
    # =====================================================

    def dataset_info(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        """
        Generate dataset information.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        numeric_columns = working_df.select_dtypes(

            include="number"

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

        info = {

            "rows":
                len(working_df),

            "columns":
                len(working_df.columns),

            "memory_mb":
                round(

                    working_df.memory_usage(

                        deep=True

                    ).sum()

                    / 1024
                    / 1024,

                    2,

                ),

            "file_name":
                self.file_name,

            "file_type":
                self.file_type,

            "column_names":
                working_df.columns.tolist(),

            "numeric_columns":
                numeric_columns,

            "categorical_columns":
                categorical_columns,

            "datetime_columns":
                datetime_columns,

        }

        logger.info(
            "Dataset information generated."
        )

        return info

    # =====================================================
    # PREVIEW
    # =====================================================

    def preview(
        self,
        df: pd.DataFrame,
        rows: int = 5,
    ) -> Dict[str, pd.DataFrame]:

        """
        Dataset preview.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        return {

            "head":
                working_df.head(rows),

            "tail":
                working_df.tail(rows),

            "sample":
                working_df.sample(

                    min(

                        rows,

                        len(working_df),

                    ),

                    random_state=42,

                ),

        }

    # =====================================================
    # MISSING VALUES
    # =====================================================

    def missing_values(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        Missing value summary.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        summary = pd.DataFrame({

            "Column":
                working_df.columns,

            "Missing Count":
                working_df.isna().sum().values,

            "Missing %":
                (

                    working_df.isna().mean()

                    * 100

                ).round(2).values,

        })

        summary = summary.sort_values(

            "Missing Count",

            ascending=False,

        )

        return summary

    # =====================================================
    # DATA TYPES
    # =====================================================

    def data_types(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        Column datatype summary.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        summary = pd.DataFrame({

            "Column":
                working_df.columns,

            "Data Type":
                working_df.dtypes.astype(str).values,

            "Non Null":
                working_df.notna().sum().values,

            "Null":
                working_df.isna().sum().values,

        })

        return summary
        # =====================================================
    # NUMERIC SUMMARY
    # =====================================================

    def numeric_summary(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        Summary of numeric columns.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        numeric_df = working_df.select_dtypes(
            include="number"
        )

        if numeric_df.empty:

            return pd.DataFrame()

        summary = numeric_df.describe().T

        summary["Variance"] = numeric_df.var()

        summary["Skewness"] = numeric_df.skew()

        summary["Kurtosis"] = numeric_df.kurt()

        return summary.round(3)

    # =====================================================
    # CATEGORICAL SUMMARY
    # =====================================================

    def categorical_summary(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        Summary of categorical columns.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        categorical_df = working_df.select_dtypes(

            include=[
                "object",
                "category",
                "string",
            ]

        )

        if categorical_df.empty:

            return pd.DataFrame()

        rows = []

        for column in categorical_df.columns:

            rows.append({

                "Column":
                    column,

                "Unique":
                    categorical_df[column].nunique(),

                "Most Frequent":
                    categorical_df[column].mode().iloc[0]
                    if not categorical_df[column].mode().empty
                    else None,

                "Frequency":
                    categorical_df[column]
                    .value_counts()
                    .iloc[0]
                    if not categorical_df[column].value_counts().empty
                    else 0,

            })

        return pd.DataFrame(rows)

    # =====================================================
    # DUPLICATE INFORMATION
    # =====================================================

    def duplicate_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:

        """
        Duplicate row statistics.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        duplicate_rows = working_df.duplicated()

        return {

            "duplicate_count":
                int(duplicate_rows.sum()),

            "duplicate_percentage":
                round(

                    duplicate_rows.mean() * 100,

                    2,

                ),

            "unique_rows":
                len(working_df)
                - int(duplicate_rows.sum()),

        }

    # =====================================================
    # MEMORY ANALYSIS
    # =====================================================

    def memory_analysis(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        Memory usage by column.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        memory = (

            working_df.memory_usage(

                deep=True,

            )

            / 1024

        ).round(2)

        result = pd.DataFrame({

            "Column":
                memory.index,

            "Memory (KB)":
                memory.values,

        })

        return result.sort_values(

            "Memory (KB)",

            ascending=False,

        )

    # =====================================================
    # SEARCH COLUMNS
    # =====================================================

    def search_columns(
        self,
        df: pd.DataFrame,
        keyword: str,
    ) -> list:

        """
        Search column names.
        """

        validate_dataframe(df)

        keyword = keyword.lower()

        return [

            column

            for column in df.columns

            if keyword in column.lower()

        ]

    # =====================================================
    # SELECT COLUMNS
    # =====================================================

    def select_columns(
        self,
        df: pd.DataFrame,
        columns: list,
    ) -> pd.DataFrame:

        """
        Return dataframe with selected columns.
        """

        validate_dataframe(df)

        return self._copy_df(

            df[columns]

        )

    # =====================================================
    # REMOVE EMPTY ROWS/COLUMNS
    # =====================================================

    def remove_empty(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        """
        Remove completely empty rows and columns.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        working_df = working_df.dropna(

            axis=0,

            how="all",

        )

        working_df = working_df.dropna(

            axis=1,

            how="all",

        )

        logger.info(

            "Removed empty rows and columns."

        )

        return working_df
        # =====================================================
    # RENAME COLUMNS
    # =====================================================

    def rename_columns(
        self,
        df: pd.DataFrame,
        mapping: Dict[str, str],
    ) -> pd.DataFrame:
        """
        Rename dataframe columns.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        working_df.rename(
            columns=mapping,
            inplace=True,
        )

        logger.info("Columns renamed successfully.")

        return working_df

    # =====================================================
    # FILTER DATASET
    # =====================================================

    def filter_rows(
        self,
        df: pd.DataFrame,
        column: str,
        value: Any,
    ) -> pd.DataFrame:
        """
        Filter dataframe by value.
        """

        validate_dataframe(df)

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")

        working_df = self._copy_df(df)

        return working_df[
            working_df[column] == value
        ]

    # =====================================================
    # SORT DATASET
    # =====================================================

    def sort_dataset(
        self,
        df: pd.DataFrame,
        by: str,
        ascending: bool = True,
    ) -> pd.DataFrame:
        """
        Sort dataframe.
        """

        validate_dataframe(df)

        if by not in df.columns:
            raise ValueError(f"{by} does not exist.")

        working_df = self._copy_df(df)

        return working_df.sort_values(
            by=by,
            ascending=ascending,
        )

    # =====================================================
    # RANDOM SAMPLE
    # =====================================================

    def sample(
        self,
        df: pd.DataFrame,
        rows: int = 10,
    ) -> pd.DataFrame:
        """
        Random sample.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        rows = min(
            rows,
            len(working_df),
        )

        return working_df.sample(
            rows,
            random_state=42,
        )

    # =====================================================
    # EXPORT DATASET
    # =====================================================

    def export_csv(
        self,
        df: pd.DataFrame,
        output_file: str,
    ):
        """
        Export dataframe to CSV.
        """

        validate_dataframe(df)

        df.to_csv(
            output_file,
            index=False,
        )

        logger.info(
            f"CSV exported : {output_file}"
        )

    # -----------------------------------------------------

    def export_excel(
        self,
        df: pd.DataFrame,
        output_file: str,
    ):
        """
        Export dataframe to Excel.
        """

        validate_dataframe(df)

        df.to_excel(
            output_file,
            index=False,
        )

        logger.info(
            f"Excel exported : {output_file}"
        )

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):
        """
        Reset loader.
        """

        self.current_dataframe = None

        self.file_name = None

        self.file_path = None

        self.file_type = None

        logger.info(
            "Loader reset."
        )

    # =====================================================
    # GET METADATA
    # =====================================================

    def metadata(self) -> Dict[str, Any]:
        """
        Return current metadata.
        """

        return {

            "file_name":
                self.file_name,

            "file_path":
                self.file_path,

            "file_type":
                self.file_type,

            "loaded":
                self.current_dataframe is not None,

        }

    # =====================================================
    # SHAPE
    # =====================================================

    def shape(
        self,
        df: pd.DataFrame,
    ) -> tuple:
        """
        Dataset shape.
        """

        validate_dataframe(df)

        return df.shape

    # =====================================================
    # COLUMN LIST
    # =====================================================

    def columns(
        self,
        df: pd.DataFrame,
    ) -> list:
        """
        Return column names.
        """

        validate_dataframe(df)

        return df.columns.tolist()

    # =====================================================
    # DATA TYPES
    # =====================================================

    def dtypes(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, str]:
        """
        Return datatype dictionary.
        """

        validate_dataframe(df)

        return {

            column: str(dtype)

            for column, dtype

            in df.dtypes.items()

        }

    # =====================================================
    # IS LOADED
    # =====================================================

    @property
    def is_loaded(self) -> bool:
        """
        Check dataset loaded.
        """

        return self.current_dataframe is not None
        # =====================================================
    # CORRELATION MATRIX
    # =====================================================

    def correlation_matrix(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate correlation matrix.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        numeric_df = working_df.select_dtypes(
            include="number"
        )

        if numeric_df.empty:
            return pd.DataFrame()

        return numeric_df.corr(numeric_only=True)

    # =====================================================
    # UNIQUE VALUE SUMMARY
    # =====================================================

    def unique_values(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Unique values per column.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        result = pd.DataFrame({

            "Column":
                working_df.columns,

            "Unique Values":
                [

                    working_df[col].nunique()

                    for col in working_df.columns

                ],

        })

        return result

    # =====================================================
    # NULL PERCENTAGE
    # =====================================================

    def null_percentage(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Null percentage by column.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        result = pd.DataFrame({

            "Column":
                working_df.columns,

            "Null %":
                (

                    working_df.isna().mean()

                    * 100

                ).round(2).values,

        })

        return result.sort_values(

            "Null %",

            ascending=False,

        )

    # =====================================================
    # DATASET QUALITY REPORT
    # =====================================================

    def quality_report(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Complete dataset quality summary.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        report = {

            "rows":
                len(working_df),

            "columns":
                len(working_df.columns),

            "duplicates":
                int(
                    working_df.duplicated().sum()
                ),

            "missing_cells":
                int(
                    working_df.isna().sum().sum()
                ),

            "missing_percentage":
                round(

                    (

                        working_df.isna()

                        .sum()

                        .sum()

                        /

                        (

                            working_df.shape[0]

                            * working_df.shape[1]

                        )

                    )

                    * 100,

                    2,

                ),

            "memory_mb":
                round(

                    working_df.memory_usage(

                        deep=True,

                    ).sum()

                    / 1024

                    / 1024,

                    2,

                ),

        }

        return report

    # =====================================================
    # CURRENT DATAFRAME
    # =====================================================

    def get_dataframe(
        self,
    ) -> Optional[pd.DataFrame]:
        """
        Return currently loaded dataframe.
        """

        return self.current_dataframe

    # -----------------------------------------------------

    def has_dataframe(
        self,
    ) -> bool:
        """
        Check dataframe availability.
        """

        return self.current_dataframe is not None

    # =====================================================
    # STRING REPRESENTATION
    # =====================================================

    def __repr__(self):

        return (

            f"DataLoader("

            f"file='{self.file_name}', "

            f"type='{self.file_type}', "

            f"loaded={self.has_dataframe()}"

            f")"

        )


# =====================================================
# GLOBAL SINGLETON INSTANCE
# =====================================================

data_loader = DataLoader()
