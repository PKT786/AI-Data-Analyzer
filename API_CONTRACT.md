# AI Data Analyzer Pro v2.0
# API CONTRACT

---

# Purpose

This document defines the ONLY public APIs that each module may expose.

Every file must follow this contract.

Never change method names without updating this document.

---

# Common Models

All modules MUST use these models.

Dashboard

DashboardWidget

DashboardMetadata

DashboardLayout

DashboardTheme

DashboardResult

DatasetProfile

DashboardRecommendation

ConfidenceScore

> **Implementation Note (v2.0 rebuild):**
> All of the models above are defined in exactly ONE file:
> `components/dashboard_models.py`. Every other dashboard
> module imports them from there — nowhere else.
>
> `DashboardTheme` is a fully-styled dataclass (colors,
> gradients, chart colorway, typography) rather than a bare
> enum, because `dashboard_themes.get_theme()` /
> `random_theme()` must hand back something rendering code
> can use directly. This was the root cause of the previous
> integration crash: `dashboard_ai.py` was importing a
> `DashboardTheme` symbol from `dashboard_themes.py` that
> didn't exist there, and three different files each defined
> their own incompatible `DatasetProfile` / theme classes.
> Both problems are fixed by routing every dashboard module
> through `dashboard_models.py`.

---

# dashboard_designer.py

Responsible for

Dashboard object management.

Public Methods

create_dashboard()

duplicate_dashboard()

delete_dashboard()

add_widget()

remove_widget()

update_widget()

move_widget()

resize_widget()

duplicate_widget()

clear_widgets()

validate_dashboard()

serialize()

deserialize()

save_layout()

load_layout()

No AI logic.

No Streamlit.

Returns Dashboard.

---

# dashboard_themes.py

Responsible for

Theme management.

Public Methods

get_theme()

list_themes()

random_theme()

register_theme()

validate_theme()

Returns DashboardTheme.

---

# chart_factory.py

Responsible for

Chart creation.

Public Methods

create_chart()

create_kpi_card()

create_sales_dashboard()

create_financial_dashboard()

create_hr_dashboard()

create_marketing_dashboard()

create_operations_dashboard()

create_executive_dashboard()

Supported Chart Types

BAR

LINE

AREA

PIE

DONUT

SCATTER

HISTOGRAM

HEATMAP

TREEMAP

FUNNEL

GAUGE

TABLE

Returns

List[DashboardWidget]

Never Dashboard.

---

# dashboard_ai.py

Responsible for

AI.

Public Methods

analyze_dataset()

analyze()

build_metadata()

build_health_report()

serialize_result()

store_result()

health_check()

debug_report()

version()

compatible_version()

is_ready()

Returns DashboardResult.

---

# dashboard_exporter.py

Responsible for

Export.

Public Methods

export_pdf()

export_png()

export_excel()

export_powerpoint()

export_html()

Input

Dashboard

Returns

Export File

---

# 4_AI_Insights.py

Responsible for

Generate Dashboard.

Public Calls

DashboardAI.analyze_dataset()

Receives

DashboardResult

Stores

st.session_state.dashboard_result

Displays

Summary

KPIs

Recommendations

Confidence

Business Domain

Never builds charts.

Never builds Dashboard.

---

# 5_Dashboard.py

Responsible for

Dashboard Rendering.

Reads

st.session_state.dashboard_result

Displays

Dashboard

Widgets

KPIs

Themes

Export Buttons

Never performs AI.

Never modifies DashboardResult.

---

# Dashboard Object

Dashboard

title

subtitle

theme

layout

widgets

kpis

summary

recommendations

metadata

---

# DashboardWidget

DashboardWidget

id

title

chart

chart_type

description

insights

position

width

height

visible

data

---

# DashboardResult

business_domain

executive_summary

confidence

dashboard

kpis

recommendations

profile

created_at

---

# DatasetProfile

row_count

column_count

numeric_columns

categorical_columns

datetime_columns

missing_values

duplicate_rows

memory_usage_mb

target_column

---

# DashboardRecommendation

business_domain

dashboard_type

confidence

reason

---

# ConfidenceScore

business_domain

dashboard_selection

overall

---

# Session Keys

dashboard_result

dashboard_ready

uploaded_dataframe

cleaned_dataframe

dataset_profile

selected_theme

selected_dashboard

---

# Rules

DashboardDesigner creates Dashboards.

ChartFactory creates Widgets.

DashboardAI creates DashboardResult.

Dashboard Page renders Dashboard.

AI Insights renders AI output.

Exporter exports Dashboard.

No module should perform another module's responsibility.

---

# Dependency Order

dashboard_designer.py

↓

dashboard_themes.py

↓

chart_factory.py

↓

dashboard_ai.py

↓

4_AI_Insights.py

↓

5_Dashboard.py

↓

dashboard_exporter.py

---

# Golden Rule

If a method is not listed in this document,

DO NOT call it.

If a property is not listed,

DO NOT use it.

Every new feature must update this document first.
