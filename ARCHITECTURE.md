# AI Data Analyzer Pro v2.0
## Enterprise Architecture

---

# Vision

AI Data Analyzer Pro is an enterprise-grade Data Analytics platform inspired by

- Microsoft Fabric
- Power BI
- Tableau
- Bloomberg Terminal
- ChatGPT

Users should be able to upload datasets and instantly receive AI-powered insights, KPIs, charts and professional dashboards.

---

# Product Goals

The application must allow users to

✅ Upload Excel / CSV

✅ AI understands business domain

✅ Generate AI insights

✅ Generate KPIs

✅ Generate multiple charts

✅ Build multiple dashboards

✅ Change dashboard themes dynamically

✅ Download dashboards

✅ Save dashboards

---

# Overall Workflow

Upload Dataset
        │
        ▼
Data Health
        │
        ▼
Data Cleaning
        │
        ▼
AI Insight Engine
        │
        ▼
Business Domain Detection
        │
        ▼
KPI Generator
        │
        ▼
Chart Recommendation
        │
        ▼
Chart Generator
        │
        ▼
Dashboard Builder
        │
        ▼
Theme Engine
        │
        ▼
Dashboard Export

---

# Repository Structure

components/

    dashboard_ai.py

    dashboard_designer.py

    chart_factory.py

    dashboard_themes.py

    dashboard_exporter.py

pages/

    1_Upload.py

    2_Data_Health.py

    3_Data_Cleaning.py

    4_AI_Insights.py

    5_Dashboard.py

core/

    session_manager.py

    config.py

assets/

templates/

themes/

exports/

---

# Dashboard Model

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

# Widget Model

DashboardWidget

id

title

chart

chart_type

data

description

insights

position

width

height

visible

---

# Dashboard Themes

Executive Blue

Executive Green

Executive Purple

Microsoft Fabric

Bloomberg Terminal

Dark

Light

Glass

Ocean

Aurora

Forest

Sunset

Random AI Theme

---

# Dashboard Templates

Executive Dashboard

Sales Dashboard

Finance Dashboard

HR Dashboard

Marketing Dashboard

Operations Dashboard

Custom Dashboard

---

# Supported Charts

Bar

Line

Area

Pie

Donut

Scatter

Histogram

Heatmap

Treemap

Waterfall

Gauge

KPI Cards

Funnel

Table

---

# AI Responsibilities

dashboard_ai.py

Business Domain Detection

Dataset Profiling

Theme Recommendation

Dashboard Recommendation

KPI Recommendation

Executive Summary

Recommendations

Dashboard Generation

Returns DashboardResult only.

No Streamlit code.

---

# Chart Factory Responsibilities

chart_factory.py

Generate widgets.

Input

DataFrame

Chart Type

Output

DashboardWidget

Never Dashboard.

---

# Dashboard Designer Responsibilities

dashboard_designer.py

Create Dashboard

Add Widget

Remove Widget

Update Widget

Move Widget

Resize Widget

Duplicate Widget

Duplicate Dashboard

Save Layout

Load Layout

Serialize

Deserialize

No AI logic.

---

# Dashboard Page Responsibilities

5_Dashboard.py

Render Dashboard

Render KPIs

Render Widgets

Theme Selector

Export

No AI calculations.

---

# AI Insights Responsibilities

4_AI_Insights.py

Generate Dashboard

Display Summary

Display Recommendations

Display KPIs

Store DashboardResult in Session

---

# Export

dashboard_exporter.py

Export PDF

Export PNG

Export PPT

Export Excel

Future

HTML

---

# Development Order

1.

dashboard_designer.py

↓

2.

dashboard_themes.py

↓

3.

chart_factory.py

↓

4.

dashboard_ai.py

↓

5.

4_AI_Insights.py

↓

6.

5_Dashboard.py

↓

7.

dashboard_exporter.py

---

# Compatibility Rule

Every file must use exactly the same

Dashboard

DashboardWidget

DashboardMetadata

DashboardTheme

DashboardLayout

No duplicate models.

No duplicate classes.

No adapters.

One model shared across the project.

> **Implementation Note (v2.0 rebuild):** enforced via a single
> `components/dashboard_models.py` module. Every dashboard
> file (`dashboard_designer.py`, `dashboard_themes.py`,
> `chart_factory.py`, `dashboard_ai.py`, `dashboard_exporter.py`,
> `pages/4_AI_Insights.py`, `pages/5_Dashboard.py`) imports
> `Dashboard`, `DashboardWidget`, `DashboardMetadata`,
> `DashboardTheme`, `DashboardLayout`, `DatasetProfile`,
> `DashboardRecommendation`, `ConfidenceScore` and
> `DashboardResult` from that one file only.

---

# Coding Standards

Python 3.14

Type Hints

Dataclasses

Logging

Docstrings

SOLID Principles

Enterprise Architecture

No duplicate code.

Backward compatible with existing repository whenever possible.

---

# Final Goal

Power BI + Microsoft Fabric quality dashboard generation with AI.
