"""
===========================================================
AI DATA ANALYZER PRO
Dashboard Designer Engine
Version : 2.0 Enterprise
-----------------------------------------------------------

Responsible for Dashboard object management ONLY:

    create_dashboard, duplicate_dashboard, delete_dashboard,
    add_widget, remove_widget, update_widget, move_widget,
    resize_widget, duplicate_widget, clear_widgets,
    validate_dashboard, serialize, deserialize,
    save_layout, load_layout

No AI logic. No Streamlit. Returns Dashboard.
===========================================================
"""

from __future__ import annotations

import copy
import json
import logging
from dataclasses import asdict
from typing import Any, Dict, List, Optional

from components.dashboard_models import (
    Dashboard,
    DashboardLayout,
    DashboardMetadata,
    DashboardTheme,
    DashboardWidget,
    WidgetPosition,
)

logger = logging.getLogger(__name__)


class DashboardDesigner:
    """Pure layout/CRUD engine for Dashboard objects."""

    # ------------------------------------------------------
    # Create / Duplicate / Delete
    # ------------------------------------------------------

    def create_dashboard(
        self,
        title: str = "AI Dashboard",
        subtitle: str = "",
        theme: Optional[DashboardTheme] = None,
        layout: Optional[DashboardLayout] = None,
        dataset_name: Optional[str] = None,
    ) -> Dashboard:
        """Create a brand new, empty Dashboard."""

        dashboard = Dashboard(
            title=title,
            subtitle=subtitle,
            theme=theme or DashboardTheme(),
            layout=layout or DashboardLayout(),
            metadata=DashboardMetadata(
                title=title,
                subtitle=subtitle,
                dataset_name=dataset_name,
            ),
        )

        logger.info("Dashboard created: %s", title)
        return dashboard

    def duplicate_dashboard(self, dashboard: Dashboard) -> Dashboard:
        """Deep-copy a dashboard so it can be edited independently."""
        return copy.deepcopy(dashboard)

    def delete_dashboard(self, dashboard: Dashboard) -> Dashboard:
        """Reset a dashboard back to an empty state."""
        dashboard.widgets = []
        dashboard.kpis = []
        dashboard.summary = ""
        dashboard.recommendations = []
        return dashboard

    # ------------------------------------------------------
    # Widget Management
    # ------------------------------------------------------

    def add_widget(
        self,
        dashboard: Dashboard,
        widget: DashboardWidget,
        position: Optional[WidgetPosition] = None,
    ) -> Dashboard:
        """Append a widget to the dashboard, auto-placing it in the grid."""

        if position:
            widget.position = position
        else:
            widget.position = self._next_position(dashboard)

        widget.width = widget.position.width
        widget.height = widget.position.height

        dashboard.widgets.append(widget)
        logger.info("Widget added: %s (%s)", widget.title, widget.chart_type)
        return dashboard

    def remove_widget(self, dashboard: Dashboard, widget_id: str) -> Dashboard:
        dashboard.widgets = [w for w in dashboard.widgets if w.id != widget_id]
        return dashboard

    def update_widget(
        self,
        dashboard: Dashboard,
        widget_id: str,
        **changes: Any,
    ) -> Dashboard:
        for widget in dashboard.widgets:
            if widget.id == widget_id:
                for key, value in changes.items():
                    if hasattr(widget, key):
                        setattr(widget, key, value)
        return dashboard

    def move_widget(
        self,
        dashboard: Dashboard,
        widget_id: str,
        row: int,
        column: int,
    ) -> Dashboard:
        for widget in dashboard.widgets:
            if widget.id == widget_id:
                widget.position.row = row
                widget.position.column = column
        return dashboard

    def resize_widget(
        self,
        dashboard: Dashboard,
        widget_id: str,
        width: int,
        height: int,
    ) -> Dashboard:
        for widget in dashboard.widgets:
            if widget.id == widget_id:
                widget.position.width = width
                widget.position.height = height
                widget.width = width
                widget.height = height
        return dashboard

    def duplicate_widget(self, dashboard: Dashboard, widget_id: str) -> Dashboard:
        for widget in list(dashboard.widgets):
            if widget.id == widget_id:
                clone = copy.deepcopy(widget)
                import uuid
                clone.id = str(uuid.uuid4())[:8]
                clone.title = f"{widget.title} (copy)"
                self.add_widget(dashboard, clone)
        return dashboard

    def clear_widgets(self, dashboard: Dashboard) -> Dashboard:
        dashboard.widgets = []
        return dashboard

    # ------------------------------------------------------
    # Validation
    # ------------------------------------------------------

    def validate_dashboard(self, dashboard: Dashboard) -> bool:
        if not isinstance(dashboard, Dashboard):
            return False
        if not dashboard.title:
            return False
        for widget in dashboard.widgets:
            if not isinstance(widget, DashboardWidget):
                return False
        return True

    # ------------------------------------------------------
    # Serialization (chart/data objects are dropped - not JSON safe)
    # ------------------------------------------------------

    def serialize(self, dashboard: Dashboard) -> str:
        """Serialize a dashboard's layout/metadata to a JSON string."""

        payload: Dict[str, Any] = {
            "title": dashboard.title,
            "subtitle": dashboard.subtitle,
            "theme": asdict(dashboard.theme),
            "layout": asdict(dashboard.layout),
            "kpis": dashboard.kpis,
            "summary": dashboard.summary,
            "recommendations": dashboard.recommendations,
            "widgets": [
                {
                    "id": w.id,
                    "title": w.title,
                    "chart_type": w.chart_type.value
                    if hasattr(w.chart_type, "value")
                    else str(w.chart_type),
                    "description": w.description,
                    "insights": w.insights,
                    "position": asdict(w.position),
                    "visible": w.visible,
                }
                for w in dashboard.widgets
            ],
        }
        return json.dumps(payload, default=str, indent=2)

    def deserialize(self, payload: str) -> Dashboard:
        """Rebuild a Dashboard's layout/metadata from a JSON string.

        NOTE: chart figures are not serialized; widgets restored this
        way carry layout/metadata only and must be re-rendered by
        chart_factory.py against fresh data.
        """

        data = json.loads(payload)

        theme = DashboardTheme(**data.get("theme", {}))
        layout = DashboardLayout(**data.get("layout", {}))

        dashboard = Dashboard(
            title=data.get("title", "AI Dashboard"),
            subtitle=data.get("subtitle", ""),
            theme=theme,
            layout=layout,
            kpis=data.get("kpis", []),
            summary=data.get("summary", ""),
            recommendations=data.get("recommendations", []),
        )

        for w in data.get("widgets", []):
            position = WidgetPosition(**w.get("position", {}))
            widget = DashboardWidget(
                id=w.get("id"),
                title=w.get("title", ""),
                description=w.get("description", ""),
                insights=w.get("insights", []),
                position=position,
                width=position.width,
                height=position.height,
                visible=w.get("visible", True),
            )
            dashboard.widgets.append(widget)

        return dashboard

    def save_layout(self, dashboard: Dashboard, path: str) -> str:
        """Save the dashboard layout to a JSON file on disk."""
        content = self.serialize(dashboard)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        logger.info("Dashboard layout saved to %s", path)
        return path

    def load_layout(self, path: str) -> Dashboard:
        """Load a dashboard layout from a JSON file on disk."""
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        return self.deserialize(content)

    # ------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------

    def _next_position(self, dashboard: Dashboard, width: int = 4, height: int = 3) -> WidgetPosition:
        """Very small grid packer: fills rows left-to-right."""

        columns = dashboard.layout.columns if dashboard.layout else 12
        occupied_in_row: Dict[int, int] = {}

        for widget in dashboard.widgets:
            occupied_in_row[widget.position.row] = (
                occupied_in_row.get(widget.position.row, 0) + widget.position.width
            )

        row = 0
        while occupied_in_row.get(row, 0) + width > columns:
            row += 1

        column = occupied_in_row.get(row, 0)
        return WidgetPosition(row=row, column=column, width=width, height=height)
