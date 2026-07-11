"""
=========================================================
AI Data Analyzer Pro
Application Settings
Author : Punit Tech Hub
Version : 2.0
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

# =====================================================
# PROJECT PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_DIR = PROJECT_ROOT / "config"

COMPONENTS_DIR = PROJECT_ROOT / "components"

PAGES_DIR = PROJECT_ROOT / "pages"

UTILS_DIR = PROJECT_ROOT / "utils"

ASSETS_DIR = PROJECT_ROOT / "assets"

LOGS_DIR = PROJECT_ROOT / "logs"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"


# =====================================================
# APPLICATION SETTINGS
# =====================================================

@dataclass(frozen=True)
class ApplicationSettings:
    """
    General application information.
    """

    APP_NAME: str = "AI Data Analyzer Pro"

    APP_VERSION: str = "2.0"

    AUTHOR: str = "Punit Tech Hub"

    COMPANY: str = "Punit Tech Hub"

    WEBSITE: str = "https://punittechhub.com"

    DEFAULT_LANGUAGE: str = "en"

    DEFAULT_TIMEZONE: str = "Asia/Kolkata"

    COPYRIGHT: str = "© 2026 Punit Tech Hub"


# =====================================================
# UPLOAD SETTINGS
# =====================================================

@dataclass(frozen=True)
class UploadSettings:
    """
    Dataset upload configuration.
    """

    SUPPORTED_FILE_TYPES: List[str] = (

        ".csv",
        ".xlsx",
        ".xls",
       ".xlsm",
       ".json",
       ".parquet",
       ".pickle",
       ".pkl",

    )

    MAX_FILE_SIZE_MB: int = 200

    MAX_ROWS: int = 5_000_000

    MAX_COLUMNS: int = 500

    DEFAULT_ENCODING: str = "utf-8"

    READ_SAMPLE_ROWS: int = 1000
# =====================================================
# CLEANING SETTINGS
# =====================================================

@dataclass(frozen=True)
class CleaningSettings:
    """
    Data cleaning configuration.
    """

    DUPLICATE_THRESHOLD: float = 0.95

    MISSING_VALUE_THRESHOLD: float = 0.40

    ENABLE_OUTLIER_DETECTION: bool = True

    AUTO_TRIM_STRINGS: bool = True

    AUTO_STANDARDIZE_COLUMNS: bool = True

    AUTO_REMOVE_EMPTY_ROWS: bool = True

    AUTO_REMOVE_EMPTY_COLUMNS: bool = True

    DEFAULT_NUMERIC_FILL: float = 0.0

    DEFAULT_TEXT_FILL: str = "Unknown"

    DEFAULT_DATE_FILL: str = "1970-01-01"


# =====================================================
# AI SETTINGS
# =====================================================

@dataclass(frozen=True)
class AISettings:
    """
    AI engine configuration.
    """

    ENABLE_AI: bool = True

    MAX_INSIGHTS: int = 25

    MAX_RECOMMENDATIONS: int = 15

    SUMMARY_MAX_LENGTH: int = 500

    INSIGHT_CONFIDENCE_THRESHOLD: float = 0.75

    TEMPERATURE: float = 0.2

    TOP_K: int = 40

    RANDOM_SEED: int = 42


# =====================================================
# DASHBOARD SETTINGS
# =====================================================

@dataclass(frozen=True)
class DashboardSettings:
    """
    Dashboard configuration.
    """

    MAX_CHARTS: int = 20

    CHARTS_PER_ROW: int = 2

    DEFAULT_CHART_HEIGHT: int = 420

    RESPONSIVE_LAYOUT: bool = True

    DEFAULT_THEME: str = "Modern"

    ENABLE_DOWNLOAD: bool = True

    SHOW_TOOLBAR: bool = True

    DEFAULT_COLOR_PALETTE: str = "ElectricBlue"


# =====================================================
# REPORT SETTINGS
# =====================================================

@dataclass(frozen=True)
class ReportSettings:
    """
    Report generation configuration.
    """

    DEFAULT_TEMPLATE: str = "Business"

    SUPPORTED_FORMATS: List[str] = (
        "PDF",
        "Word",
        "Excel",
        "HTML",
        "Text",
    )

    INCLUDE_EXECUTIVE_SUMMARY: bool = True

    INCLUDE_AI_INSIGHTS: bool = True

    INCLUDE_DASHBOARD: bool = True

    INCLUDE_DATA_HEALTH: bool = True

    INCLUDE_CLEANING_SUMMARY: bool = True

    MAX_REPORT_PAGES: int = 100
# =====================================================
# THEME SETTINGS
# =====================================================

@dataclass(frozen=True)
class ThemeSettings:
    """
    UI theme configuration.
    """

    PRIMARY_COLOR: str = "#00A8FF"

    BACKGROUND_COLOR: str = "#1E1E1E"

    SECONDARY_BACKGROUND: str = "#2A2A2A"

    TEXT_COLOR: str = "#FFFFFF"

    FONT: str = "sans-serif"

    BORDER_RADIUS: int = 8

    CARD_BACKGROUND: str = "#2F2F2F"


# =====================================================
# LOGGING SETTINGS
# =====================================================

@dataclass(frozen=True)
class LoggingSettings:
    """
    Logging configuration.
    """

    LOG_LEVEL: str = "INFO"

    LOG_DIRECTORY: Path = LOGS_DIR

    LOG_FILE: str = "application.log"

    MAX_LOG_SIZE_MB: int = 20

    BACKUP_COUNT: int = 10

    LOG_FORMAT: str = (
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    )


# =====================================================
# MASTER SETTINGS
# =====================================================

@dataclass(frozen=True)
class Settings:
    """
    Master application settings.
    """

    app: ApplicationSettings = ApplicationSettings()

    upload: UploadSettings = UploadSettings()

    cleaning: CleaningSettings = CleaningSettings()

    ai: AISettings = AISettings()

    dashboard: DashboardSettings = DashboardSettings()

    report: ReportSettings = ReportSettings()

    theme: ThemeSettings = ThemeSettings()

    logging: LoggingSettings = LoggingSettings()


# =====================================================
# GLOBAL SETTINGS OBJECT
# =====================================================

settings = Settings()


# =====================================================
# EXPORTED CONSTANTS
# =====================================================

APP_NAME = settings.app.APP_NAME

APP_VERSION = settings.app.APP_VERSION

AUTHOR = settings.app.AUTHOR

COMPANY = settings.app.COMPANY

WEBSITE = settings.app.WEBSITE

DEFAULT_LANGUAGE = settings.app.DEFAULT_LANGUAGE

DEFAULT_TIMEZONE = settings.app.DEFAULT_TIMEZONE
