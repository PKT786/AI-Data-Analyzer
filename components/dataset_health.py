"""
=========================================================
AI Data Analyzer Pro
Dataset Health Analyzer
Author : Punit Tech Hub
Version : 2.0
=========================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from utils.logger import get_logger
from utils.validators import validate_dataframe

logger = get_logger(__name__)


class DatasetHealth:
    """
    Enterprise Dataset Health Analyzer

    This class analyses the quality of a dataset.
    No cleaning is performed here.

    Responsibilities
    ----------------
    • Dataset Summary
    • Missing Analysis
    • Duplicate Analysis
    • Column Analysis
    • Numeric Analysis
    • Categorical Analysis
    • Datetime Analysis
    • Memory Analysis
    • Dataset Quality Score
    • Recommendations
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        logger.info(
            "DatasetHealth initialized."
        )

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

        validate_dataframe(df)

        return df.copy(deep=True)

    # -----------------------------------------------------

    def _numeric_columns(
        self,
        df: pd.DataFrame,
    ) -> List[str]:

        return df.select_dtypes(

            include=np.number

        ).columns.tolist()

    # -----------------------------------------------------

    def _categorical_columns(
        self,
        df: pd.DataFrame,
    ) -> List[str]:

        return df.select_dtypes(

            include=["object", "category", "string"]

        ).columns.tolist()

    # -----------------------------------------------------

    def _datetime_columns(
        self,
        df: pd.DataFrame,
    ) -> List[str]:

        return df.select_dtypes(

            include=["datetime", "datetimetz"]

        ).columns.tolist()

    # -----------------------------------------------------

    def _memory_mb(
        self,
        df: pd.DataFrame,
    ) -> float:

        return round(

            df.memory_usage(

                deep=True

            ).sum()

            / 1024

            / 1024,

            2,

        )

    # =====================================================
    # DATASET SUMMARY
    # =====================================================

    def dataset_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Return overall dataset summary.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        summary = {

            "generated_at": datetime.now(),

            "rows": len(working_df),

            "columns": len(working_df.columns),

            "shape": working_df.shape,

            "memory_mb": self._memory_mb(
                working_df
            ),

            "numeric_columns": len(
                self._numeric_columns(
                    working_df
                )
            ),

            "categorical_columns": len(
                self._categorical_columns(
                    working_df
                )
            ),

            "datetime_columns": len(
                self._datetime_columns(
                    working_df
                )
            ),

            "missing_cells": int(
                working_df.isna().sum().sum()
            ),

            "duplicate_rows": int(
                working_df.duplicated().sum()
            ),

        }

        logger.info(
            "Dataset summary generated."
        )

        return summary
        # =====================================================
    # MISSING VALUE ANALYSIS
    # =====================================================

    def missing_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Analyze missing values.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        total_missing = int(
            working_df.isna().sum().sum()
        )

        column_details = []

        for column in working_df.columns:

            missing_count = int(
                working_df[column].isna().sum()
            )

            missing_percent = round(

                (missing_count / len(working_df)) * 100,

                2,

            )

            column_details.append(

                {

                    "column": column,

                    "missing_count": missing_count,

                    "missing_percent": missing_percent,

                }

            )

        summary = {

            "total_missing": total_missing,

            "total_missing_percent": round(

                (total_missing /

                 (len(working_df) * len(working_df.columns)))

                * 100,

                2,

            ),

            "columns": column_details,

        }

        logger.info(
            "Missing value summary generated."
        )

        return summary

    # =====================================================
    # DUPLICATE ANALYSIS
    # =====================================================

    def duplicate_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Analyze duplicate rows.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        duplicate_count = int(

            working_df.duplicated().sum()

        )

        duplicate_percent = round(

            (duplicate_count / len(working_df)) * 100,

            2,

        )

        summary = {

            "duplicate_rows": duplicate_count,

            "duplicate_percent": duplicate_percent,

            "unique_rows": len(working_df) - duplicate_count,

        }

        logger.info(
            "Duplicate summary generated."
        )

        return summary

    # =====================================================
    # COLUMN SUMMARY
    # =====================================================

    def column_summary(
        self,
        df: pd.DataFrame,
    ) -> List[Dict[str, Any]]:
        """
        Analyze every column.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        result = []

        total_rows = len(working_df)

        for column in working_df.columns:

            dtype = str(

                working_df[column].dtype

            )

            missing = int(

                working_df[column].isna().sum()

            )

            missing_percent = round(

                (missing / total_rows) * 100,

                2,

            )

            unique = int(

                working_df[column].nunique(

                    dropna=True

                )

            )

            memory = round(

                working_df[column]

                .memory_usage(deep=True)

                / 1024,

                2,

            )

            column_info = {

                "column": column,

                "dtype": dtype,

                "missing": missing,

                "missing_percent": missing_percent,

                "unique": unique,

                "memory_kb": memory,

            }

            if pd.api.types.is_numeric_dtype(

                working_df[column]

            ):

                column_info.update(

                    {

                        "min": working_df[column].min(),

                        "max": working_df[column].max(),

                        "mean": round(

                            float(

                                working_df[column].mean()

                            ),

                            4,

                        )

                        if working_df[column].notna().any()

                        else None,

                        "median": round(

                            float(

                                working_df[column].median()

                            ),

                            4,

                        )

                        if working_df[column].notna().any()

                        else None,

                    }

                )

            result.append(

                column_info

            )

        logger.info(
            "Column summary generated."
        )

        return result
        # =====================================================
    # NUMERIC SUMMARY
    # =====================================================

    def numeric_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Generate summary statistics for all numeric columns.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        result: Dict[str, Dict[str, Any]] = {}

        numeric_columns = self._numeric_columns(
            working_df
        )

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

            mode = series.mode()

            result[column] = {

                "count": int(series.count()),

                "missing": int(
                    working_df[column].isna().sum()
                ),

                "mean": round(float(series.mean()), 4),

                "median": round(float(series.median()), 4),

                "mode": mode.iloc[0] if not mode.empty else None,

                "minimum": float(series.min()),

                "maximum": float(series.max()),

                "std": round(float(series.std()), 4),

                "variance": round(float(series.var()), 4),

                "skewness": round(float(series.skew()), 4),

                "kurtosis": round(float(series.kurtosis()), 4),

                "outliers": outliers,

            }

        logger.info(
            "Numeric summary generated."
        )

        return result

    # =====================================================
    # CATEGORICAL SUMMARY
    # =====================================================

    def categorical_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Generate summary statistics for categorical columns.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        result: Dict[str, Dict[str, Any]] = {}

        categorical_columns = self._categorical_columns(
            working_df
        )

        for column in categorical_columns:

            series = working_df[column]

            value_counts = series.value_counts(dropna=True)

            top_value = None

            top_frequency = 0

            if not value_counts.empty:

                top_value = value_counts.index[0]

                top_frequency = int(value_counts.iloc[0])

            result[column] = {

                "count": int(series.count()),

                "missing": int(series.isna().sum()),

                "unique": int(series.nunique(dropna=True)),

                "top_value": top_value,

                "top_frequency": top_frequency,

            }

        logger.info(
            "Categorical summary generated."
        )

        return result

    # =====================================================
    # DATETIME SUMMARY
    # =====================================================

    def datetime_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Analyze datetime columns.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        result: Dict[str, Dict[str, Any]] = {}

        datetime_columns = self._datetime_columns(
            working_df
        )

        for column in datetime_columns:

            series = working_df[column].dropna()

            if series.empty:

                continue

            result[column] = {

                "minimum": series.min(),

                "maximum": series.max(),

                "missing": int(
                    working_df[column].isna().sum()
                ),

                "unique": int(series.nunique()),

            }

        logger.info(
            "Datetime summary generated."
        )

        return result
        # =====================================================
    # MEMORY SUMMARY
    # =====================================================

    def memory_summary(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Analyze dataframe memory usage.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        per_column = {}

        for column in working_df.columns:

            per_column[column] = round(

                working_df[column]

                .memory_usage(deep=True)

                / 1024,

                2,

            )

        summary = {

            "total_memory_mb": self._memory_mb(

                working_df

            ),

            "column_memory_kb": per_column,

            "largest_column": max(

                per_column,

                key=per_column.get,

            ),

        }

        logger.info(

            "Memory summary generated."

        )

        return summary

    # =====================================================
    # QUALITY SCORE
    # =====================================================

    def quality_score(
        self,
        df: pd.DataFrame,
    ) -> int:
        """
        Dataset quality score (0-100).
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        score = 100

        total_cells = (

            len(working_df)

            * len(working_df.columns)

        )

        if total_cells > 0:

            missing_percent = (

                working_df.isna().sum().sum()

                / total_cells

            ) * 100

            score -= min(

                20,

                int(missing_percent),

            )

        duplicate_percent = (

            working_df.duplicated().sum()

            / max(len(working_df), 1)

        ) * 100

        score -= min(

            15,

            int(duplicate_percent),

        )

        object_columns = self._categorical_columns(

            working_df

        )

        if len(object_columns) > (

            len(working_df.columns) * 0.80

        ):

            score -= 10

        score = max(

            0,

            min(score, 100),

        )

        logger.info(

            "Dataset quality score calculated."

        )

        return score

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    def recommendations(
        self,
        df: pd.DataFrame,
    ) -> List[str]:
        """
        Generate recommendations.
        """

        validate_dataframe(df)

        working_df = self._copy_df(df)

        recommendations = []

        duplicate_count = int(

            working_df.duplicated().sum()

        )

        if duplicate_count:

            recommendations.append(

                f"Remove {duplicate_count} duplicate rows."

            )

        missing = working_df.isna().sum()

        for column, value in missing.items():

            if value > 0:

                recommendations.append(

                    f"Fill missing values in '{column}'."

                )

        for column in self._categorical_columns(

            working_df

        ):

            if working_df[column].nunique() < 20:

                recommendations.append(

                    f"Consider encoding '{column}'."

                )

        for column in self._datetime_columns(

            working_df

        ):

            recommendations.append(

                f"Use '{column}' for time-series analysis."

            )

        if not recommendations:

            recommendations.append(

                "Dataset quality is excellent."

            )

        logger.info(

            "Recommendations generated."

        )

        return recommendations

    # =====================================================
    # COMPLETE REPORT
    # =====================================================

    def generate_report(
        self,
        df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Generate complete dataset health report.
        """

        validate_dataframe(df)

        report = {

            "dataset": self.dataset_summary(df),

            "missing": self.missing_summary(df),

            "duplicates": self.duplicate_summary(df),

            "columns": self.column_summary(df),

            "numeric": self.numeric_summary(df),

            "categorical": self.categorical_summary(df),

            "datetime": self.datetime_summary(df),

            "memory": self.memory_summary(df),

            "quality_score": self.quality_score(df),

            "recommendations": self.recommendations(df),

        }

        logger.info(

            "Complete dataset report generated."

        )

        return report


# =====================================================
# GLOBAL INSTANCE
# =====================================================

dataset_health = DatasetHealth()