"""
===========================================================
AI DATA ANALYZER PRO
Dashboard Shared Models
-----------------------------------------------------------

Purpose
-------
This is the ONLY place where the shared dashboard data
models are defined.

Per ARCHITECTURE.md / API_CONTRACT.md "Compatibility Rule":

    Every file must use exactly the same
    Dashboard, DashboardWidget, DashboardMetadata,
    DashboardTheme, DashboardLayout ...

    No duplicate models. No duplicate classes.
    No adapters. One model shared across the project.

Every other dashboard module (dashboard_designer.py,
dashboard_themes.py, chart_factory.py, dashboard_ai.py,
dashboard_exporter.py, pages/4_AI_Insights.py,
pages/5_Dashboard.py) imports these models from here.

No Streamlit code lives in this file.
===========================================================
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# ==========================================================
# Chart Types (chart_factory.py contract)
# ==========================================================


class ChartType(str, Enum):
    """Supported chart types (see API_CONTRACT.md)."""

    BAR = "BAR"
    LINE = "LINE"
    AREA = "AREA"
    PIE = "PIE"
    DONUT = "DONUT"
    SCATTER = "SCATTER"
    HISTOGRAM = "HISTOGRAM"
    HEATMAP = "HEATMAP"
    TREEMAP = "TREEMAP"
    FUNNEL = "FUNNEL"
    GAUGE = "GAUGE"
    TABLE = "TABLE"
    KPI = "KPI"


# ==========================================================
# Business Domain / Dashboard Type
# ==========================================================


class BusinessDomain(str, Enum):
    SALES = "Sales"
    FINANCE = "Finance"
    HR = "Human Resources"
    MARKETING = "Marketing"
    OPERATIONS = "Operations"
    SUPPLY_CHAIN = "Supply Chain"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    RETAIL = "Retail"
    MANUFACTURING = "Manufacturing"
    GENERAL = "General"


class DashboardType(str, Enum):
    SALES = "Sales Dashboard"
    FINANCE = "Finance Dashboard"
    HR = "HR Dashboard"
    MARKETING = "Marketing Dashboard"
    OPERATIONS = "Operations Dashboard"
    EXECUTIVE = "Executive Dashboard"
    CUSTOM = "Custom Dashboard"


# ==========================================================
# Dashboard Theme
# ==========================================================
#
# NOTE: DashboardTheme is a fully-styled theme object (colors,
# gradient, chart colorway, typography) rather than a bare
# enum. dashboard_themes.py owns the catalogue of built-in
# DashboardTheme instances and hands them out via get_theme(),
# list_themes() and random_theme(). Every module renders using
# the *same* DashboardTheme object attached to Dashboard.theme.


@dataclass
class DashboardTheme:
    """A complete, self-contained visual theme for a dashboard."""

    name: str = "Executive Blue"

    # Core palette
    primary: str = "#2563EB"
    secondary: str = "#1D4ED8"
    accent: str = "#38BDF8"

    # Surfaces
    background: str = "#F5F7FA"
    background_gradient: str = (
        "linear-gradient(135deg, #eef2ff 0%, #f5f7fa 60%, #e0e7ff 100%)"
    )
    card_background: str = "#FFFFFF"
    header_gradient: str = (
        "linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%)"
    )

    # Text
    text_color: str = "#0F172A"
    muted_text: str = "#64748B"
    header_text_color: str = "#FFFFFF"

    # Semantic
    success: str = "#10B981"
    warning: str = "#F59E0B"
    danger: str = "#EF4444"
    info: str = "#06B6D4"

    border_color: str = "#E2E8F0"
    border_radius: int = 14
    font_family: str = "Segoe UI, -apple-system, sans-serif"
    is_dark: bool = False

    # Ordered colour list used for chart series / pie slices
    chart_colorway: List[str] = field(
        default_factory=lambda: [
            "#2563EB", "#10B981", "#F59E0B", "#EF4444",
            "#8B5CF6", "#06B6D4", "#F97316", "#84CC16",
        ]
    )


# ==========================================================
# Widget Position / Layout
# ==========================================================


@dataclass
class WidgetPosition:
    row: int = 0
    column: int = 0
    width: int = 4
    height: int = 3


@dataclass
class DashboardLayout:
    """Grid layout configuration for a dashboard."""

    template: str = "Executive"
    columns: int = 12
    row_height: int = 130
    gap: int = 16
    responsive: bool = True


# ==========================================================
# Dashboard Widget
# ==========================================================


@dataclass
class DashboardWidget:
    """A single chart / KPI / table placed on a dashboard."""

    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    chart_type: ChartType = ChartType.BAR
    chart: Optional[Any] = None  # plotly Figure
    data: Optional[Any] = None  # underlying pandas DataFrame / Series
    description: str = ""
    insights: List[str] = field(default_factory=list)
    position: WidgetPosition = field(default_factory=WidgetPosition)
    width: int = 4
    height: int = 3
    visible: bool = True


# ==========================================================
# Dashboard Metadata
# ==========================================================


@dataclass
class DashboardMetadata:
    title: str = "AI Dashboard"
    subtitle: str = ""
    created_by: str = "AI Data Analyzer Pro"
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    version: str = "2.0"
    dataset_name: Optional[str] = None
    description: str = ""


# ==========================================================
# Dashboard
# ==========================================================


@dataclass
class Dashboard:
    """The complete dashboard object rendered by 5_Dashboard.py."""

    title: str = "AI Dashboard"
    subtitle: str = ""
    theme: DashboardTheme = field(default_factory=DashboardTheme)
    layout: DashboardLayout = field(default_factory=DashboardLayout)
    widgets: List[DashboardWidget] = field(default_factory=list)
    kpis: List[Dict[str, Any]] = field(default_factory=list)
    summary: str = ""
    recommendations: List[str] = field(default_factory=list)
    metadata: DashboardMetadata = field(default_factory=DashboardMetadata)


# ==========================================================
# Dataset Profile
# ==========================================================


@dataclass
class DatasetProfile:
    row_count: int = 0
    column_count: int = 0
    numeric_columns: List[str] = field(default_factory=list)
    categorical_columns: List[str] = field(default_factory=list)
    datetime_columns: List[str] = field(default_factory=list)
    missing_values: int = 0
    duplicate_rows: int = 0
    memory_usage_mb: float = 0.0
    target_column: Optional[str] = None


# ==========================================================
# Dashboard Recommendation / Confidence
# ==========================================================


@dataclass
class DashboardRecommendation:
    business_domain: BusinessDomain
    dashboard_type: DashboardType
    confidence: float
    reason: str


@dataclass
class ConfidenceScore:
    business_domain: float = 0.0
    dashboard_selection: float = 0.0
    overall: float = 0.0


# ==========================================================
# Dashboard Result (output of dashboard_ai.py)
# ==========================================================


@dataclass
class DashboardResult:
    business_domain: BusinessDomain
    executive_summary: str
    confidence: ConfidenceScore
    dashboard: Dashboard
    kpis: List[Any] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    profile: Optional[DatasetProfile] = None
    created_at: datetime = field(default_factory=datetime.now)
