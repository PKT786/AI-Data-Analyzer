"""
===========================================================
AI DATA ANALYZER PRO
Dashboard AI Engine
Version : 2.0 Enterprise
-----------------------------------------------------------

This module is responsible for:

    • Dataset Profiling
    • Business Domain Detection
    • KPI Recommendation
    • Dashboard Recommendation
    • Executive Summary
    • AI Recommendations
    • Theme Recommendation (dynamic - changes every run)
    • Dashboard Generation

Public API

    dashboard_ai = DashboardAI()
    result = dashboard_ai.analyze_dataset(df)

Returns DashboardResult only. No Streamlit code.
===========================================================
"""

from __future__ import annotations

import logging
import random
from datetime import datetime
from typing import List

import pandas as pd

from components.chart_factory import ChartFactory, profile_dataset
from components.dashboard_designer import DashboardDesigner
from components.dashboard_models import (
    BusinessDomain,
    ConfidenceScore,
    Dashboard,
    DashboardRecommendation,
    DashboardResult,
    DashboardType,
    DatasetProfile,
)
from components.dashboard_themes import ThemeManager

logger = logging.getLogger(__name__)

# ==========================================================
# Keyword banks used for lightweight business-domain detection
# ==========================================================

_DOMAIN_KEYWORDS = {
    BusinessDomain.SALES: ["sale", "revenue", "order", "customer", "product", "quantity", "discount"],
    BusinessDomain.FINANCE: ["salary", "wage", "budget", "expense", "profit", "cost", "invoice", "tax"],
    BusinessDomain.HR: ["employee", "emp", "dept", "department", "hire", "attrition", "designation", "manager"],
    BusinessDomain.MARKETING: ["campaign", "click", "impression", "lead", "conversion", "channel", "ctr"],
    BusinessDomain.OPERATIONS: ["shipment", "inventory", "supply", "logistics", "warehouse", "delivery"],
    BusinessDomain.SUPPLY_CHAIN: ["supplier", "procurement", "vendor", "stock", "sku"],
    BusinessDomain.HEALTHCARE: ["patient", "diagnosis", "treatment", "hospital", "doctor"],
    BusinessDomain.EDUCATION: ["student", "grade", "course", "school", "exam"],
    BusinessDomain.RETAIL: ["store", "branch", "region", "sku", "basket"],
    BusinessDomain.MANUFACTURING: ["machine", "production", "defect", "batch", "plant"],
}

_DOMAIN_TO_DASHBOARD = {
    BusinessDomain.SALES: DashboardType.SALES,
    BusinessDomain.RETAIL: DashboardType.SALES,
    BusinessDomain.FINANCE: DashboardType.FINANCE,
    BusinessDomain.HR: DashboardType.HR,
    BusinessDomain.MARKETING: DashboardType.MARKETING,
    BusinessDomain.OPERATIONS: DashboardType.OPERATIONS,
    BusinessDomain.SUPPLY_CHAIN: DashboardType.OPERATIONS,
    BusinessDomain.MANUFACTURING: DashboardType.OPERATIONS,
    BusinessDomain.HEALTHCARE: DashboardType.EXECUTIVE,
    BusinessDomain.EDUCATION: DashboardType.EXECUTIVE,
    BusinessDomain.GENERAL: DashboardType.EXECUTIVE,
}

_DASHBOARD_BUILDER_METHOD = {
    DashboardType.SALES: "create_sales_dashboard",
    DashboardType.FINANCE: "create_financial_dashboard",
    DashboardType.HR: "create_hr_dashboard",
    DashboardType.MARKETING: "create_marketing_dashboard",
    DashboardType.OPERATIONS: "create_operations_dashboard",
    DashboardType.EXECUTIVE: "create_executive_dashboard",
}


class DashboardAI:
    """AI orchestration engine that produces a DashboardResult."""

    def __init__(self) -> None:
        self.designer = DashboardDesigner()
        self.chart_factory = ChartFactory()
        self.theme_manager = ThemeManager()
        self._version = "2.0"

    # ------------------------------------------------------
    # Public API (API_CONTRACT.md)
    # ------------------------------------------------------

    def analyze_dataset(self, df: pd.DataFrame, dataset_name: str | None = None) -> DashboardResult:
        """Full pipeline: profile -> detect domain -> build dashboard."""
        return self.analyze(df, dataset_name=dataset_name)

    def analyze(self, df: pd.DataFrame, dataset_name: str | None = None) -> DashboardResult:
        if df is None or df.empty:
            raise ValueError("Cannot analyze an empty dataset.")

        profile = self.build_metadata(df)
        domain, domain_confidence = self._detect_business_domain(df)
        dashboard_type = _DOMAIN_TO_DASHBOARD.get(domain, DashboardType.EXECUTIVE)

        # Dynamic theme: every generation gets a fresh, random premium
        # theme so the dashboard background colour visibly changes.
        theme = self.theme_manager.random_theme()

        dashboard = self.designer.create_dashboard(
            title=f"{dashboard_type.value}",
            subtitle=f"AI-generated for {domain.value} • {datetime.now().strftime('%d %b %Y, %H:%M')}",
            theme=theme,
            dataset_name=dataset_name,
        )

        builder_name = _DASHBOARD_BUILDER_METHOD.get(dashboard_type, "create_executive_dashboard")
        widgets = getattr(self.chart_factory, builder_name)(df, theme=theme)
        for widget in widgets:
            self.designer.add_widget(dashboard, widget)

        kpis = self._build_kpis(df, profile)
        dashboard.kpis = kpis

        summary = self._build_summary(domain, dashboard_type, profile, kpis)
        recommendations = self._build_recommendations(profile, domain)

        dashboard.summary = summary
        dashboard.recommendations = recommendations

        confidence = ConfidenceScore(
            business_domain=domain_confidence,
            dashboard_selection=domain_confidence,
            overall=round((domain_confidence + 0.9) / 2, 2),
        )

        result = DashboardResult(
            business_domain=domain,
            executive_summary=summary,
            confidence=confidence,
            dashboard=dashboard,
            kpis=kpis,
            recommendations=recommendations,
            profile=profile,
        )

        logger.info(
            "Dashboard generated: domain=%s type=%s theme=%s widgets=%d",
            domain.value, dashboard_type.value, theme.name, len(dashboard.widgets),
        )
        return result

    # ------------------------------------------------------
    # Profiling
    # ------------------------------------------------------

    def build_metadata(self, df: pd.DataFrame) -> DatasetProfile:
        return profile_dataset(df)

    def build_health_report(self, df: pd.DataFrame) -> dict:
        profile = profile_dataset(df)
        completeness = 1 - (profile.missing_values / max(profile.row_count * profile.column_count, 1))
        return {
            "row_count": profile.row_count,
            "column_count": profile.column_count,
            "missing_values": profile.missing_values,
            "duplicate_rows": profile.duplicate_rows,
            "completeness_score": round(completeness * 100, 1),
        }

    # ------------------------------------------------------
    # Business domain detection
    # ------------------------------------------------------

    def _detect_business_domain(self, df: pd.DataFrame) -> tuple[BusinessDomain, float]:
        columns_text = " ".join(str(c).lower() for c in df.columns)

        scores = {}
        for domain, keywords in _DOMAIN_KEYWORDS.items():
            hits = sum(1 for kw in keywords if kw in columns_text)
            if hits:
                scores[domain] = hits

        if not scores:
            return BusinessDomain.GENERAL, 0.55

        best_domain = max(scores, key=scores.get)
        total_keywords = len(_DOMAIN_KEYWORDS[best_domain])
        confidence = min(0.55 + (scores[best_domain] / max(total_keywords, 1)) * 0.4, 0.97)
        return best_domain, round(confidence, 2)

    # ------------------------------------------------------
    # KPI generation
    # ------------------------------------------------------

    def _build_kpis(self, df: pd.DataFrame, profile: DatasetProfile) -> List[dict]:
        kpis = []
        numeric_cols = profile.numeric_columns[:4]

        for col in numeric_cols:
            kpis.append(self.chart_factory.create_kpi_card(df, col, agg="sum"))

        kpis.append({
            "label": "Total Records",
            "value": f"{profile.row_count:,}",
            "raw_value": profile.row_count,
            "delta": None,
        })

        if not numeric_cols:
            kpis.append({
                "label": "Columns",
                "value": str(profile.column_count),
                "raw_value": profile.column_count,
                "delta": None,
            })

        return kpis[:6]

    # ------------------------------------------------------
    # Executive summary & recommendations
    # ------------------------------------------------------

    def _build_summary(self, domain, dashboard_type, profile: DatasetProfile, kpis: List[dict]) -> str:
        lead_kpi = kpis[0]["label"] if kpis else "key metrics"
        return (
            f"This {dashboard_type.value.lower()} was generated for the "
            f"{domain.value} domain, covering {profile.row_count:,} records across "
            f"{profile.column_count} columns. The dataset contains "
            f"{len(profile.numeric_columns)} numeric and {len(profile.categorical_columns)} "
            f"categorical fields, with {lead_kpi} as the leading metric."
        )

    def _build_recommendations(self, profile: DatasetProfile, domain: BusinessDomain) -> List[str]:
        recs = []

        if profile.missing_values > 0:
            recs.append(
                f"Clean {profile.missing_values} missing values before deeper analysis for more reliable KPIs."
            )
        if profile.duplicate_rows > 0:
            recs.append(f"Remove {profile.duplicate_rows} duplicate rows to avoid double-counting metrics.")
        if profile.datetime_columns:
            recs.append("Add a time-series view to track trends across the detected date columns.")
        if len(profile.numeric_columns) >= 2:
            recs.append("Explore correlations between numeric fields using the heatmap widget.")
        if not recs:
            recs.append("Dataset looks healthy — consider adding more charts to explore relationships.")

        recs.append(f"Consider a dedicated {domain.value} deep-dive dashboard for more granular insight.")
        return recs[:5]

    # ------------------------------------------------------
    # Misc / diagnostics (API_CONTRACT.md)
    # ------------------------------------------------------

    def serialize_result(self, result: DashboardResult) -> str:
        return self.designer.serialize(result.dashboard)

    def store_result(self, result: DashboardResult, session_state) -> None:
        session_state["dashboard_result"] = result
        session_state["dashboard_ready"] = True

    def health_check(self) -> dict:
        return {"status": "ok", "version": self._version}

    def debug_report(self) -> dict:
        return {
            "themes": self.theme_manager.list_themes(),
            "version": self._version,
        }

    def version(self) -> str:
        return self._version

    def compatible_version(self, other: str) -> bool:
        return other.split(".")[0] == self._version.split(".")[0]

    def is_ready(self) -> bool:
        return True
