"""
=========================================================
AI Data Analyzer Pro
AI Engine
Author : Punit Tech Hub
Version : 2.0
=========================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

import copy
import pandas as pd

from components.data_loader import data_loader

from components.cleaning_operations import cleaning_operations
from components.dataset_health import dataset_health
from components.dashboard_builder import dashboard_builder
from components.insight_generator import insight_generator
from components.report_builder import report_builder

from utils.logger import get_logger
from utils.validators import validate_dataframe

logger = get_logger(__name__)


class AIEngine:
    """
    Enterprise AI Engine.

    Central orchestration layer for the application.

    Responsibilities
    ----------------
    • Dataset Loading
    • Cleaning Pipeline
    • Dataset Health
    • Dashboard Generation
    • Insight Generation
    • Report Generation
    • Complete AI Analysis
    • Result Caching
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        self.cache: Dict[str, Any] = {}

        self.pipeline_log = []

        self.current_dataframe: Optional[pd.DataFrame] = None

        self.cleaned_dataframe: Optional[pd.DataFrame] = None

        logger.info(
            "AIEngine initialized."
        )

    # =====================================================
    # INTERNAL HELPERS
    # =====================================================

    def _copy_df(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Create safe dataframe copy.
        """

        validate_dataframe(df)

        return copy.deepcopy(df)

    # -----------------------------------------------------

    def _log_step(
        self,
        step: str,
    ) -> None:
        """
        Record pipeline execution step.
        """

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        self.pipeline_log.append(
            {
                "time": timestamp,
                "step": step,
            }
        )

        logger.info(step)

    # -----------------------------------------------------

    def _cache(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store object in cache.
        """

        self.cache[key] = value

    # -----------------------------------------------------

    def _get_cache(
        self,
        key: str,
    ) -> Any:
        """
        Retrieve cached object.
        """

        return self.cache.get(key)

    # -----------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset engine state.
        """

        self.cache.clear()

        self.pipeline_log.clear()

        self.current_dataframe = None

        self.cleaned_dataframe = None

        logger.info(
            "AI Engine reset completed."
        )
            # =====================================================
    # DATASET LOADING
    # =====================================================

    def load_dataset(
        self,
        file_path: str,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Load dataset using the enterprise DataLoader.
        """

        logger.info(
            f"Loading dataset: {file_path}"
        )

        df = data_loader.load(
            file_path,
            **kwargs,
        )

        validate_dataframe(df)

        self.current_dataframe = self._copy_df(df)

        self._cache(
            "original_dataframe",
            self.current_dataframe,
        )

        self._cache(
            "source_file",
            file_path,
        )

        self._log_step(
            "Dataset Loaded"
        )

        return self.current_dataframe

    # =====================================================
    # DATA CLEANING
    # =====================================================

    def clean_dataset(
        self,
        df: Optional[pd.DataFrame] = None,
    ) -> pd.DataFrame:
        """
        Execute the enterprise cleaning pipeline.
        """

        if df is None:

            if self.current_dataframe is None:

                raise ValueError(
                    "No dataset available for cleaning."
                )

            df = self.current_dataframe

        validate_dataframe(df)

        working_df = self._copy_df(df)

        # Execute the standardized cleaning pipeline
        #
        # NOTE:
        # This method assumes cleaning_operations.py
        # exposes run_pipeline(df).
        # If your final implementation uses another
        # public method (for example clean_dataframe()),
        # only this single call needs updating.
        #
        cleaned_df = cleaning_operations.run_pipeline(
            working_df
        )

        self.cleaned_dataframe = self._copy_df(
            cleaned_df
        )

        self._cache(
            "cleaned_dataframe",
            self.cleaned_dataframe,
        )

        self._log_step(
            "Cleaning Completed"
        )

        return self.cleaned_dataframe

    # =====================================================
    # DATASET HEALTH
    # =====================================================

    def dataset_health(
        self,
        df: Optional[pd.DataFrame] = None,
    ) -> Dict[str, Any]:
        """
        Generate dataset health report.
        """

        if df is None:

            if self.cleaned_dataframe is not None:

                df = self.cleaned_dataframe

            elif self.current_dataframe is not None:

                df = self.current_dataframe

            else:

                raise ValueError(
                    "No dataset available."
                )

        validate_dataframe(df)

        working_df = self._copy_df(df)

        report = dataset_health.generate_report(
            working_df
        )

        self._cache(
            "dataset_health",
            report,
        )

        self._log_step(
            "Dataset Health Generated"
        )

        return report
        # =====================================================
    # DASHBOARD GENERATION
    # =====================================================

    def build_dashboard(
        self,
        df: Optional[pd.DataFrame] = None,
    ) -> Dict[str, Any]:
        """
        Build interactive dashboard configuration.
        """

        if df is None:

            if self.cleaned_dataframe is not None:

                df = self.cleaned_dataframe

            elif self.current_dataframe is not None:

                df = self.current_dataframe

            else:

                raise ValueError(
                    "No dataset available."
                )

        validate_dataframe(df)

        working_df = self._copy_df(df)

        dashboard = dashboard_builder.build_dashboard(
            working_df
        )

        self._cache(
            "dashboard",
            dashboard,
        )

        self._log_step(
            "Dashboard Built"
        )

        return dashboard

    # =====================================================
    # INSIGHT GENERATION
    # =====================================================

    def generate_insights(
        self,
        df: Optional[pd.DataFrame] = None,
    ) -> Dict[str, Any]:
        """
        Generate business insights.
        """

        if df is None:

            if self.cleaned_dataframe is not None:

                df = self.cleaned_dataframe

            elif self.current_dataframe is not None:

                df = self.current_dataframe

            else:

                raise ValueError(
                    "No dataset available."
                )

        validate_dataframe(df)

        working_df = self._copy_df(df)

        insights = insight_generator.generate_insights(
            working_df
        )

        self._cache(
            "insights",
            insights,
        )

        self._log_step(
            "Insights Generated"
        )

        return insights

    # =====================================================
    # REPORT GENERATION
    # =====================================================

    def build_report(
        self,
        df: Optional[pd.DataFrame] = None,
    ) -> Dict[str, Any]:
        """
        Generate complete enterprise report.
        """

        if df is None:

            if self.cleaned_dataframe is not None:

                df = self.cleaned_dataframe

            elif self.current_dataframe is not None:

                df = self.current_dataframe

            else:

                raise ValueError(
                    "No dataset available."
                )

        validate_dataframe(df)

        working_df = self._copy_df(df)

        report = report_builder.build_complete_report(
            working_df
        )

        self._cache(
            "report",
            report,
        )

        self._log_step(
            "Report Generated"
        )

        return report
        # =====================================================
    # DATASET ANALYSIS
    # =====================================================

    def analyze_dataset(
        self,
        df: Optional[pd.DataFrame] = None,
    ) -> Dict[str, Any]:
        """
        Execute complete dataset analysis without
        reloading the dataset.

        Returns
        -------
        Dictionary containing health,
        dashboard, insights and report.
        """

        if df is None:

            if self.cleaned_dataframe is not None:

                df = self.cleaned_dataframe

            elif self.current_dataframe is not None:

                df = self.current_dataframe

            else:

                raise ValueError(
                    "No dataset available."
                )

        validate_dataframe(df)

        working_df = self._copy_df(df)

        health = self.dataset_health(
            working_df
        )

        dashboard = self.build_dashboard(
            working_df
        )

        insights = self.generate_insights(
            working_df
        )

        report = self.build_report(
            working_df
        )

        results = {

            "health": health,

            "dashboard": dashboard,

            "insights": insights,

            "report": report,

        }

        self._cache(
            "analysis_results",
            results,
        )

        self._log_step(
            "Dataset Analysis Completed"
        )

        return results

    # =====================================================
    # COMPLETE AI ANALYSIS PIPELINE
    # =====================================================

    def analyze(
        self,
        file_path: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Complete AI analysis pipeline.

        Pipeline

        Load Dataset
            ↓
        Clean Dataset
            ↓
        Dataset Health
            ↓
        Dashboard
            ↓
        Insights
            ↓
        Report
        """

        logger.info(
            "Starting complete AI analysis."
        )

        self.reset()

        original_df = self.load_dataset(
            file_path,
            **kwargs,
        )

        cleaned_df = self.clean_dataset(
            original_df
        )

        health = self.dataset_health(
            cleaned_df
        )

        dashboard = self.build_dashboard(
            cleaned_df
        )

        insights = self.generate_insights(
            cleaned_df
        )

        report = self.build_report(
            cleaned_df
        )

        results = {

            "original_dataframe":
                original_df,

            "cleaned_dataframe":
                cleaned_df,

            "health":
                health,

            "dashboard":
                dashboard,

            "insights":
                insights,

            "report":
                report,

            "pipeline_log":
                self.pipeline_log,

        }

        self._cache(
            "complete_analysis",
            results,
        )

        self._log_step(
            "Complete AI Analysis Finished"
        )

        logger.info(
            "AI analysis completed successfully."
        )

        return results
        # =====================================================
    # CACHE MANAGEMENT
    # =====================================================

    def cache_results(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a value in the AI Engine cache.

        Parameters
        ----------
        key : Cache key
        value : Object to cache
        """

        self._cache(
            key,
            value,
        )

        logger.info(
            f"Cached result: {key}"
        )

    # -----------------------------------------------------

    def get_cached_result(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve cached object.

        Parameters
        ----------
        key : Cache key

        Returns
        -------
        Cached object if available,
        otherwise default.
        """

        value = self.cache.get(
            key,
            default,
        )

        logger.info(
            f"Retrieved cached result: {key}"
        )

        return value

    # =====================================================
    # CURRENT ENGINE STATE
    # =====================================================

    def current_state(
        self,
    ) -> Dict[str, Any]:
        """
        Return current AI Engine state.
        """

        state = {

            "dataset_loaded":
                self.current_dataframe is not None,

            "dataset_cleaned":
                self.cleaned_dataframe is not None,

            "cached_objects":
                list(self.cache.keys()),

            "pipeline_steps":
                len(self.pipeline_log),

            "pipeline_log":
                self.pipeline_log,

            "rows":
                (
                    len(self.cleaned_dataframe)
                    if self.cleaned_dataframe is not None
                    else (
                        len(self.current_dataframe)
                        if self.current_dataframe is not None
                        else 0
                    )
                ),

            "columns":
                (
                    len(self.cleaned_dataframe.columns)
                    if self.cleaned_dataframe is not None
                    else (
                        len(self.current_dataframe.columns)
                        if self.current_dataframe is not None
                        else 0
                    )
                ),

        }

        logger.info(
            "AI Engine state requested."
        )

        return state


# =====================================================
# GLOBAL INSTANCE
# =====================================================

ai_engine = AIEngine()
