"""
==========================================================
AI DATA ANALYZER PRO
Upload Data Workspace
Author : Punit Tech Hub
==========================================================
"""

from __future__ import annotations

import os
import uuid
import logging
from pathlib import Path
from datetime import datetime
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

# ==========================================================
# Logger
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s",

)

logger = logging.getLogger(__name__)

# ==========================================================
# Constants
# ==========================================================

SUPPORTED_FILES = [

    ".csv",

    ".xlsx",

    ".xls",

]

MAX_FILE_SIZE_MB = 100

UPLOAD_DIRECTORY = Path("uploaded_files")

UPLOAD_DIRECTORY.mkdir(

    exist_ok=True

)

# ==========================================================
# Dataset Metadata
# ==========================================================

@dataclass
class DatasetMetadata:

    dataset_id: str

    filename: str

    extension: str

    uploaded_at: datetime

    rows: int = 0

    columns: int = 0

    memory_mb: float = 0.0

    business_domain: Optional[str] = None

    source: str = "User Upload"

# ==========================================================
# Dataset Profile
# ==========================================================

@dataclass
class DatasetProfile:

    rows: int = 0

    columns: int = 0

    duplicate_rows: int = 0

    missing_values: int = 0

    numeric_columns: List[str] = field(default_factory=list)

    categorical_columns: List[str] = field(default_factory=list)

    datetime_columns: List[str] = field(default_factory=list)

    boolean_columns: List[str] = field(default_factory=list)

    memory_usage_mb: float = 0.0

# ==========================================================
# Upload Result
# ==========================================================

@dataclass
class UploadResult:

    success: bool

    dataframe: Optional[pd.DataFrame] = None

    metadata: Optional[DatasetMetadata] = None

    profile: Optional[DatasetProfile] = None

    message: str = ""

# ==========================================================
# Session Initialization
# ==========================================================

def initialize_session() -> None:
    """
    Initialize every session variable required
    by the application.
    """

    defaults = {

        "dataset": None,

        "cleaned_df": None,

        "metadata": None,

        "profile": None,

        "dashboard_result": None,

        "ai_insights": [],

        "health_report": {},

        "cleaning_report": {},

        "report_history": [],

        "generated_dashboard": None,

        "uploaded_file_name": None,

        "business_domain": None,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value

# ==========================================================
# Upload Workspace
# ==========================================================

class UploadWorkspace:

    """
    Enterprise Upload Workspace.

    Responsibilities

    • Upload Dataset
    • Validate File
    • Read Dataset
    • Create Metadata
    • Profile Dataset
    • Save Session
    """

    def __init__(self):

        initialize_session()

        logger.info(

            "Upload Workspace initialized."

        )
# ==========================================================
# Upload Interface
# ==========================================================

    def render_upload_section(self):
        """
        Render upload UI.
        """

        st.title("📂 Upload Dataset")

        st.markdown(
            """
Upload Excel or CSV files to begin your AI-powered analysis.

Supported formats

• CSV

• XLSX

• XLS

Maximum Size : 100 MB
"""
        )

        uploaded_file = st.file_uploader(

            "Choose Dataset",

            type=["csv", "xlsx", "xls"],

            accept_multiple_files=False,

            help="Drag & Drop or Browse",

        )

        if uploaded_file is None:

            return None

        result = self.process_upload(uploaded_file)

        if result.success:

            st.success(result.message)

        else:

            st.error(result.message)

        return result

# ==========================================================
# Upload Processor
# ==========================================================

    def process_upload(
        self,
        uploaded_file,
    ) -> UploadResult:

        try:

            self.validate_file(uploaded_file)

            dataframe = self.read_dataframe(
                uploaded_file
            )

            metadata = self.create_metadata(

                uploaded_file,

                dataframe,

            )

            profile = self.create_profile(
                dataframe
            )

            return UploadResult(

                success=True,

                dataframe=dataframe,

                metadata=metadata,

                profile=profile,

                message="Dataset uploaded successfully.",

            )

        except Exception as ex:

            logger.exception(ex)

            return UploadResult(

                success=False,

                message=str(ex),

            )

# ==========================================================
# Validation
# ==========================================================

    def validate_file(
        self,
        uploaded_file,
    ):

        extension = Path(
            uploaded_file.name
        ).suffix.lower()

        if extension not in SUPPORTED_FILES:

            raise ValueError(

                f"Unsupported file : {extension}"

            )

        size_mb = (
            uploaded_file.size
            / 1024
            / 1024
        )

        if size_mb > MAX_FILE_SIZE_MB:

            raise ValueError(

                "File exceeds maximum allowed size."

            )

# ==========================================================
# Read DataFrame
# ==========================================================

    def read_dataframe(
        self,
        uploaded_file,
    ) -> pd.DataFrame:

        extension = Path(
            uploaded_file.name
        ).suffix.lower()

        with st.spinner(

            "Reading dataset..."

        ):

            if extension == ".csv":

                dataframe = pd.read_csv(
                    uploaded_file
                )

            else:

                dataframe = pd.read_excel(
                    uploaded_file
                )

        if dataframe.empty:

            raise ValueError(
                "Dataset is empty."
            )

        dataframe.columns = [

            str(col).strip()

            for col in dataframe.columns

        ]

        return dataframe

# ==========================================================
# Metadata Builder
# ==========================================================

    def create_metadata(
        self,
        uploaded_file,
        dataframe: pd.DataFrame,
    ) -> DatasetMetadata:

        return DatasetMetadata(

            dataset_id=str(uuid.uuid4()),

            filename=uploaded_file.name,

            extension=Path(
                uploaded_file.name
            ).suffix,

            uploaded_at=datetime.now(),

            rows=len(dataframe),

            columns=len(dataframe.columns),

            memory_mb=round(

                dataframe.memory_usage(
                    deep=True
                ).sum()
                / 1024
                / 1024,
                2,
            ),

        )
# ==========================================================
# Dataset Profiler
# ==========================================================

    def create_profile(
        self,
        dataframe: pd.DataFrame,
    ) -> DatasetProfile:
        """
        Generate dataset profile.
        """

        profile = DatasetProfile()

        profile.rows = len(dataframe)

        profile.columns = len(dataframe.columns)

        profile.duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        profile.missing_values = int(
            dataframe.isna().sum().sum()
        )

        profile.numeric_columns = list(
            dataframe.select_dtypes(
                include=["number"]
            ).columns
        )

        profile.categorical_columns = list(
            dataframe.select_dtypes(
                include=["object", "category"]
            ).columns
        )

        profile.datetime_columns = list(
            dataframe.select_dtypes(
                include=["datetime", "datetimetz"]
            ).columns
        )

        profile.boolean_columns = list(
            dataframe.select_dtypes(
                include=["bool"]
            ).columns
        )

        profile.memory_usage_mb = round(

            dataframe.memory_usage(
                deep=True
            ).sum()
            / 1024
            / 1024,

            2,

        )

        return profile


# ==========================================================
# Save Session State
# ==========================================================

    def save_session(
        self,
        result: UploadResult,
    ) -> None:
        """
        Store uploaded dataset for all pages.
        """

        st.session_state.dataset = result.dataframe

        # Initial cleaned dataframe

        st.session_state.cleaned_df = (
            result.dataframe.copy()
        )

        st.session_state.metadata = result.metadata

        st.session_state.profile = result.profile

        st.session_state.uploaded_file_name = (
            result.metadata.filename
        )

        # Reset downstream pages

        st.session_state.dashboard_result = None

        st.session_state.generated_dashboard = None

        st.session_state.ai_insights = []

        st.session_state.health_report = {}

        st.session_state.cleaning_report = {}

        logger.info(
            "Dataset stored in session state."
        )


# ==========================================================
# Dataset Preview
# ==========================================================

    def show_preview(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Preview uploaded dataset.
        """

        st.subheader("👀 Dataset Preview")

        st.dataframe(

            dataframe.head(20),

            use_container_width=True,

            hide_index=True,

        )


# ==========================================================
# Upload Summary
# ==========================================================

    def show_upload_summary(
        self,
        metadata: DatasetMetadata,
        profile: DatasetProfile,
    ) -> None:
        """
        Dataset summary cards.
        """

        st.subheader("📊 Dataset Summary")

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Rows",
                f"{profile.rows:,}"
            )

        with c2:

            st.metric(
                "Columns",
                profile.columns
            )

        with c3:

            st.metric(
                "Duplicates",
                profile.duplicate_rows
            )

        with c4:

            st.metric(
                "Missing Values",
                profile.missing_values
            )

        c5, c6, c7, c8 = st.columns(4)

        with c5:

            st.metric(
                "Numeric",
                len(profile.numeric_columns)
            )

        with c6:

            st.metric(
                "Categorical",
                len(profile.categorical_columns)
            )

        with c7:

            st.metric(
                "Datetime",
                len(profile.datetime_columns)
            )

        with c8:

            st.metric(
                "Memory",
                f"{profile.memory_usage_mb:.2f} MB"
            )
# ==========================================================
# Business Domain Detection
# ==========================================================

    def detect_business_domain(
        self,
        dataframe: pd.DataFrame,
    ) -> str:
        """
        Simple business domain detection based on column names.
        """

        columns = [
            str(col).lower()
            for col in dataframe.columns
        ]

        keywords = {

            "Sales": [
                "sales",
                "revenue",
                "profit",
                "customer",
                "product",
                "order",
                "invoice",
            ],

            "Finance": [
                "expense",
                "budget",
                "amount",
                "payment",
                "cost",
                "balance",
            ],

            "HR": [
                "employee",
                "salary",
                "department",
                "joining",
                "designation",
                "manager",
            ],

            "Marketing": [
                "campaign",
                "click",
                "impression",
                "lead",
                "conversion",
            ],

            "Operations": [
                "inventory",
                "warehouse",
                "stock",
                "shipment",
                "vendor",
            ],

        }

        scores = {}

        for domain, words in keywords.items():

            score = 0

            for word in words:

                score += sum(
                    word in column
                    for column in columns
                )

            scores[domain] = score

        best_domain = max(
            scores,
            key=scores.get,
        )

        if scores[best_domain] == 0:

            return "General"

        return best_domain


# ==========================================================
# File Information
# ==========================================================

    def show_file_information(
        self,
        metadata: DatasetMetadata,
    ) -> None:
        """
        Display uploaded file information.
        """

        st.subheader("📁 File Information")

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                f"**Filename:** {metadata.filename}"
            )

            st.write(
                f"**Extension:** {metadata.extension}"
            )

            st.write(
                f"**Rows:** {metadata.rows:,}"
            )

        with c2:

            st.write(
                f"**Columns:** {metadata.columns}"
            )

            st.write(
                f"**Memory:** {metadata.memory_mb:.2f} MB"
            )

            st.write(
                f"**Uploaded:** {metadata.uploaded_at.strftime('%d %b %Y %H:%M')}"
            )


# ==========================================================
# Success Banner
# ==========================================================

    def show_success_banner(self) -> None:
        """
        Display completion message.
        """

        st.success(
            """
✅ Dataset uploaded successfully.

Your dataset is now available for:

✔ Data Health

✔ Data Cleaning

✔ AI Insights

✔ Premium Dashboard

✔ Reports
"""
        )


# ==========================================================
# Main Upload Workflow
# ==========================================================

    def run(self) -> None:
        """
        Execute upload workflow.
        """

        result = self.render_upload_section()

        if result is None:

            return

        if not result.success:

            return

        business_domain = self.detect_business_domain(
            result.dataframe
        )

        result.metadata.business_domain = (
            business_domain
        )

        st.session_state.business_domain = (
            business_domain
        )

        self.save_session(result)

        self.show_success_banner()

        self.show_file_information(
            result.metadata
        )

        self.show_upload_summary(
            result.metadata,
            result.profile,
        )

        self.show_preview(
            result.dataframe
        )

        st.info(
            f"🤖 Detected Business Domain: **{business_domain}**"
        )
# ==========================================================
# Navigation Status
# ==========================================================

def show_navigation_status() -> None:
    """
    Display application workflow status.
    """

    st.divider()

    st.subheader("🚀 Application Workflow")

    dataset_ready = st.session_state.dataset is not None

    cleaning_ready = st.session_state.cleaned_df is not None

    ai_ready = st.session_state.dashboard_result is not None

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:

        st.success("✅ Upload")

    with c2:

        if dataset_ready:

            st.success("✅ Health")

        else:

            st.info("⏳ Health")

    with c3:

        if cleaning_ready:

            st.success("✅ Cleaning")

        else:

            st.info("⏳ Cleaning")

    with c4:

        if ai_ready:

            st.success("✅ AI")

        else:

            st.info("⏳ AI")

    with c5:

        if ai_ready:

            st.success("✅ Dashboard")

        else:

            st.info("⏳ Dashboard")

    with c6:

        if ai_ready:

            st.success("✅ Reports")

        else:

            st.info("⏳ Reports")


# ==========================================================
# Footer
# ==========================================================

def show_footer() -> None:

    st.divider()

    st.caption(
        "AI Data Analyzer Pro | Enterprise Edition"
    )

    st.caption(
        "© 2026 Punit Tech Hub"
    )


# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    Upload Data Workspace
    """

    workspace = UploadWorkspace()

    workspace.run()

    if st.session_state.dataset is not None:

        show_navigation_status()

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
            "Upload page failed to load."
        )

        st.exception(ex)
