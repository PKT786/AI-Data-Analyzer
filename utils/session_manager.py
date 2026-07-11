"""
utils/session_manager.py

Centralized Streamlit Session State Manager
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import pandas as pd
import streamlit as st

# =====================================================
# SESSION KEYS
# =====================================================

SESSION_ORIGINAL_DF = "original_dataframe"
SESSION_CLEAN_DF = "clean_dataframe"

SESSION_PROFILE = "dataset_profile"
SESSION_HEALTH = "dataset_health"

SESSION_INSIGHTS = "ai_insights"

SESSION_CHART = "dashboard_charts"

SESSION_REPORT = "generated_report"

SESSION_HISTORY = "cleaning_history"

SESSION_FILENAME = "uploaded_filename"

SESSION_FILETYPE = "uploaded_filetype"


# =====================================================
# SESSION MANAGER
# =====================================================


class SessionManager:
    """
    Wrapper around Streamlit Session State.
    """

    def __init__(self):
        pass

    # -------------------------------------------------
    # Basic Operations
    # -------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        return st.session_state.get(key, default)

    def set(self, key: str, value: Any) -> None:
        st.session_state[key] = value

    def exists(self, key: str) -> bool:
        return key in st.session_state

    def delete(self, key: str) -> None:
        if key in st.session_state:
            del st.session_state[key]

    def clear(self) -> None:
        st.session_state.clear()

    # -------------------------------------------------
    # DataFrames
    # -------------------------------------------------

    def set_original_dataframe(self, df: pd.DataFrame):
        self.set(SESSION_ORIGINAL_DF, df)

    def get_original_dataframe(self) -> Optional[pd.DataFrame]:
        return self.get(SESSION_ORIGINAL_DF)

    def set_clean_dataframe(self, df: pd.DataFrame):
        self.set(SESSION_CLEAN_DF, df)

    def get_clean_dataframe(self) -> Optional[pd.DataFrame]:
        return self.get(SESSION_CLEAN_DF)

    # -------------------------------------------------
    # Dataset Health
    # -------------------------------------------------

    def set_health(self, health: Dict):
        self.set(SESSION_HEALTH, health)

    def get_health(self):
        return self.get(SESSION_HEALTH)

    # -------------------------------------------------
    # Profile
    # -------------------------------------------------

    def set_profile(self, profile: Dict):
        self.set(SESSION_PROFILE, profile)

    def get_profile(self):
        return self.get(SESSION_PROFILE)

    # -------------------------------------------------
    # AI Insights
    # -------------------------------------------------

    def set_insights(self, insights):
        self.set(SESSION_INSIGHTS, insights)

    def get_insights(self):
        return self.get(SESSION_INSIGHTS)

    # -------------------------------------------------
    # Dashboard
    # -------------------------------------------------

    def set_dashboard(self, dashboard):
        self.set(SESSION_CHART, dashboard)

    def get_dashboard(self):
        return self.get(SESSION_CHART)

    # -------------------------------------------------
    # Reports
    # -------------------------------------------------

    def set_report(self, report):
        self.set(SESSION_REPORT, report)

    def get_report(self):
        return self.get(SESSION_REPORT)

    # -------------------------------------------------
    # Cleaning History
    # -------------------------------------------------

    def set_history(self, history):
        self.set(SESSION_HISTORY, history)

    def get_history(self):
        return self.get(SESSION_HISTORY)

    # -------------------------------------------------
    # Uploaded File Info
    # -------------------------------------------------

    def set_filename(self, filename: str):
        self.set(SESSION_FILENAME, filename)

    def get_filename(self):
        return self.get(SESSION_FILENAME)

    def set_filetype(self, filetype: str):
        self.set(SESSION_FILETYPE, filetype)

    def get_filetype(self):
        return self.get(SESSION_FILETYPE)

    # -------------------------------------------------
    # Reset Data Session
    # -------------------------------------------------

    def reset_dataset(self):
        keys = [
            SESSION_ORIGINAL_DF,
            SESSION_CLEAN_DF,
            SESSION_PROFILE,
            SESSION_HEALTH,
            SESSION_INSIGHTS,
            SESSION_CHART,
            SESSION_REPORT,
            SESSION_HISTORY,
            SESSION_FILENAME,
            SESSION_FILETYPE,
        ]

        for key in keys:
            self.delete(key)


# =====================================================
# GLOBAL INSTANCE
# =====================================================

session_manager = SessionManager()
