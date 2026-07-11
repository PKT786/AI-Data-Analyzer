"""
===========================================================
AI DATA ANALYZER PRO
Dashboard Theme Engine
Version : 2.0 Enterprise
-----------------------------------------------------------

Responsible for:

    • Theme catalogue (Executive Blue/Green/Purple, Microsoft
      Fabric, Bloomberg Terminal, Dark, Light, Glass, Ocean,
      Aurora, Forest, Sunset)
    • Dynamic / random theme generation so every newly
      generated dashboard gets a fresh background colour.
    • Theme registration & validation.

Public API (see API_CONTRACT.md)

    ThemeManager.get_theme(name)
    ThemeManager.list_themes()
    ThemeManager.random_theme()
    ThemeManager.register_theme(theme)
    ThemeManager.validate_theme(theme)

Returns DashboardTheme (components/dashboard_models.py).
No Streamlit code.
===========================================================
"""

from __future__ import annotations

import logging
import random
from typing import Dict, List, Optional

from components.dashboard_models import DashboardTheme

logger = logging.getLogger(__name__)

# ==========================================================
# Built-in Premium Themes
# ==========================================================


def _theme(
    name: str,
    primary: str,
    secondary: str,
    accent: str,
    background: str,
    background_gradient: str,
    card_background: str,
    header_gradient: str,
    text_color: str,
    muted_text: str,
    header_text_color: str,
    chart_colorway: List[str],
    is_dark: bool = False,
) -> DashboardTheme:
    return DashboardTheme(
        name=name,
        primary=primary,
        secondary=secondary,
        accent=accent,
        background=background,
        background_gradient=background_gradient,
        card_background=card_background,
        header_gradient=header_gradient,
        text_color=text_color,
        muted_text=muted_text,
        header_text_color=header_text_color,
        chart_colorway=chart_colorway,
        is_dark=is_dark,
    )


BUILT_IN_THEMES: Dict[str, DashboardTheme] = {

    "Executive Blue": _theme(
        "Executive Blue", "#2563EB", "#1D4ED8", "#38BDF8",
        "#F5F7FB", "linear-gradient(135deg,#eef2ff 0%,#f5f7fb 55%,#dbeafe 100%)",
        "#FFFFFF", "linear-gradient(90deg,#1E3A8A 0%,#2563EB 55%,#38BDF8 100%)",
        "#0F172A", "#64748B", "#FFFFFF",
        ["#2563EB", "#38BDF8", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4", "#F97316"],
    ),
    "Executive Green": _theme(
        "Executive Green", "#059669", "#047857", "#34D399",
        "#F3FBF7", "linear-gradient(135deg,#ecfdf5 0%,#f3fbf7 55%,#d1fae5 100%)",
        "#FFFFFF", "linear-gradient(90deg,#065F46 0%,#059669 55%,#34D399 100%)",
        "#0F172A", "#64748B", "#FFFFFF",
        ["#059669", "#34D399", "#2563EB", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4", "#84CC16"],
    ),
    "Executive Purple": _theme(
        "Executive Purple", "#7C3AED", "#6D28D9", "#C4B5FD",
        "#F8F6FE", "linear-gradient(135deg,#f5f3ff 0%,#f8f6fe 55%,#ede9fe 100%)",
        "#FFFFFF", "linear-gradient(90deg,#4C1D95 0%,#7C3AED 55%,#C4B5FD 100%)",
        "#1E1B29", "#6B6478", "#FFFFFF",
        ["#7C3AED", "#C4B5FD", "#EC4899", "#F59E0B", "#10B981", "#06B6D4", "#EF4444", "#3B82F6"],
    ),
    "Microsoft Fabric": _theme(
        "Microsoft Fabric", "#0F6CBD", "#0C4A78", "#50E6FF",
        "#F5FAFF", "linear-gradient(135deg,#eff6ff 0%,#f5faff 55%,#dbeafe 100%)",
        "#FFFFFF", "linear-gradient(90deg,#0C4A78 0%,#0F6CBD 55%,#50E6FF 100%)",
        "#0B1F33", "#5B7183", "#FFFFFF",
        ["#0F6CBD", "#50E6FF", "#F2C811", "#8764B8", "#107C10", "#E74856", "#00B7C3", "#FFB900"],
    ),
    "Bloomberg Terminal": _theme(
        "Bloomberg Terminal", "#FF8000", "#191919", "#00E676",
        "#0B0B0B", "linear-gradient(135deg,#111111 0%,#050505 60%,#1a1a1a 100%)",
        "#161616", "linear-gradient(90deg,#000000 0%,#1a1a1a 55%,#FF8000 130%)",
        "#F5F5F5", "#9CA3AF", "#FFFFFF",
        ["#FF8000", "#00E676", "#FFEA00", "#00B0FF", "#FF3D00", "#E040FB", "#69F0AE", "#FF6E40"],
        is_dark=True,
    ),
    "Dark": _theme(
        "Dark", "#6366F1", "#4338CA", "#A5B4FC",
        "#0F172A", "linear-gradient(135deg,#111827 0%,#0f172a 55%,#1e293b 100%)",
        "#1E293B", "linear-gradient(90deg,#111827 0%,#312E81 55%,#4338CA 100%)",
        "#F1F5F9", "#94A3B8", "#FFFFFF",
        ["#6366F1", "#22D3EE", "#34D399", "#FBBF24", "#F87171", "#E879F9", "#60A5FA", "#FB923C"],
        is_dark=True,
    ),
    "Light": _theme(
        "Light", "#334155", "#1E293B", "#64748B",
        "#FFFFFF", "linear-gradient(135deg,#ffffff 0%,#f8fafc 55%,#f1f5f9 100%)",
        "#F8FAFC", "linear-gradient(90deg,#475569 0%,#334155 100%)",
        "#0F172A", "#64748B", "#FFFFFF",
        ["#334155", "#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4", "#F97316"],
    ),
    "Glass": _theme(
        "Glass", "#8B5CF6", "#6D28D9", "#F472B6",
        "#F4F1FE", "linear-gradient(135deg,#faf5ff 0%,#f4f1fe 40%,#fce7f3 100%)",
        "rgba(255,255,255,0.65)", "linear-gradient(90deg,#8B5CF6 0%,#F472B6 100%)",
        "#241C3B", "#6B6478", "#FFFFFF",
        ["#8B5CF6", "#F472B6", "#38BDF8", "#34D399", "#FBBF24", "#FB7185", "#22D3EE", "#A78BFA"],
    ),
    "Ocean": _theme(
        "Ocean", "#0891B2", "#0E7490", "#67E8F9",
        "#F0FBFD", "linear-gradient(135deg,#ecfeff 0%,#f0fbfd 55%,#cffafe 100%)",
        "#FFFFFF", "linear-gradient(90deg,#155E75 0%,#0891B2 55%,#67E8F9 100%)",
        "#0B2530", "#57727A", "#FFFFFF",
        ["#0891B2", "#67E8F9", "#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#14B8A6"],
    ),
    "Aurora": _theme(
        "Aurora", "#22D3EE", "#A78BFA", "#34D399",
        "#0B1226", "linear-gradient(135deg,#0b1226 0%,#111a3d 45%,#1c1440 100%)",
        "#161F3E", "linear-gradient(90deg,#22D3EE 0%,#A78BFA 55%,#34D399 100%)",
        "#F1F5F9", "#A3ADC2", "#0B1226",
        ["#22D3EE", "#A78BFA", "#34D399", "#F472B6", "#FBBF24", "#60A5FA", "#F87171", "#4ADE80"],
        is_dark=True,
    ),
    "Forest": _theme(
        "Forest", "#15803D", "#166534", "#84CC16",
        "#F5FAF2", "linear-gradient(135deg,#f0fdf4 0%,#f5faf2 55%,#dcfce7 100%)",
        "#FFFFFF", "linear-gradient(90deg,#14532D 0%,#15803D 55%,#84CC16 100%)",
        "#132A18", "#5B6E5E", "#FFFFFF",
        ["#15803D", "#84CC16", "#CA8A04", "#0891B2", "#EF4444", "#7C3AED", "#F97316", "#22C55E"],
    ),
    "Sunset": _theme(
        "Sunset", "#EA580C", "#C2410C", "#FBBF24",
        "#FFF8F1", "linear-gradient(135deg,#fff7ed 0%,#fff8f1 45%,#ffe4e6 100%)",
        "#FFFFFF", "linear-gradient(90deg,#9D174D 0%,#EA580C 55%,#FBBF24 100%)",
        "#2B1608", "#8A6A55", "#FFFFFF",
        ["#EA580C", "#FBBF24", "#DB2777", "#7C3AED", "#0891B2", "#16A34A", "#F43F5E", "#F97316"],
    ),
}


# ==========================================================
# Theme Manager
# ==========================================================


class ThemeManager:
    """Owns the theme catalogue and hands out DashboardTheme objects."""

    def __init__(self) -> None:
        self._themes: Dict[str, DashboardTheme] = dict(BUILT_IN_THEMES)
        logger.info("ThemeManager initialised with %d themes.", len(self._themes))

    # ------------------------------------------------------
    def list_themes(self) -> List[str]:
        """Return the names of all registered themes."""
        return list(self._themes.keys())

    # ------------------------------------------------------
    def get_theme(self, name: Optional[str]) -> DashboardTheme:
        """
        Return a DashboardTheme by name.
        Falls back to 'Executive Blue' if the name is unknown.
        """
        if not name:
            return self._themes["Executive Blue"]
        return self._themes.get(name, self._themes["Executive Blue"])

    # ------------------------------------------------------
    def random_theme(self, exclude: Optional[str] = None) -> DashboardTheme:
        """
        Pick a random built-in theme. This is what makes the
        dashboard background dynamically change every time a
        new dashboard is generated.
        """
        names = [n for n in self._themes if n != exclude] or list(self._themes)
        choice = random.choice(names)
        logger.info("Random theme selected: %s", choice)
        return self._themes[choice]

    # ------------------------------------------------------
    def register_theme(self, theme: DashboardTheme) -> DashboardTheme:
        """Register (or overwrite) a custom theme."""
        if not self.validate_theme(theme):
            raise ValueError(f"Invalid theme: {theme}")
        self._themes[theme.name] = theme
        return theme

    # ------------------------------------------------------
    def validate_theme(self, theme: DashboardTheme) -> bool:
        """Basic structural validation of a DashboardTheme."""
        if not isinstance(theme, DashboardTheme):
            return False
        required = [theme.name, theme.primary, theme.background, theme.text_color]
        return all(bool(v) for v in required)


# ==========================================================
# Module-level convenience functions (API_CONTRACT.md)
# ==========================================================

_manager = ThemeManager()


def get_theme(name: Optional[str] = None) -> DashboardTheme:
    return _manager.get_theme(name)


def list_themes() -> List[str]:
    return _manager.list_themes()


def random_theme(exclude: Optional[str] = None) -> DashboardTheme:
    return _manager.random_theme(exclude=exclude)


def register_theme(theme: DashboardTheme) -> DashboardTheme:
    return _manager.register_theme(theme)


def validate_theme(theme: DashboardTheme) -> bool:
    return _manager.validate_theme(theme)
