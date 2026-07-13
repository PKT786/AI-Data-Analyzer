"""
=========================================================
AI Data Analyzer Pro
Main Application Entry Point
Author : Punit Tech Hub
Version : 2.1
=========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import streamlit as st

from config.settings import settings

from components.ai_engine import ai_engine

from utils.logger import get_logger
from utils.session_manager import session_manager

import auth

logger = get_logger(__name__)

# =====================================================
# APPLICATION CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Data Analyzer Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_NAME = "AI Data Analyzer Pro"
APP_VERSION = "2.1"
PROJECT_ROOT = Path(__file__).resolve().parent


def horizontal_space(lines: int = 1) -> None:
    """Adds vertical spacing in the Streamlit app."""
    for _ in range(lines):
        st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# PREMIUM STYLING
# =====================================================

def inject_premium_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        h1, h2, h3, .pth-font-poppins { font-family: 'Poppins', sans-serif; }

        .pth-hero-wrap {
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 16px 40px rgba(9,14,32,0.35);
            margin-bottom: 6px;
        }
        .pth-hero-wrap img { display: block; width: 100%; }

        .pth-badge-row {
            display: flex; flex-wrap: wrap; gap: 10px;
            justify-content: center; margin: 18px 0 6px;
        }
        .pth-badge {
            background: linear-gradient(90deg, #1C2D60, #483A96);
            color: #F5F0E6; padding: 7px 16px; border-radius: 999px;
            font-size: 13px; font-weight: 600; letter-spacing: .02em;
            border: 1px solid rgba(201,168,119,0.5);
        }

        .pth-section-title {
            font-family: 'Poppins', sans-serif; font-weight: 700;
            font-size: 28px; text-align: center; margin: 8px 0 2px;
            color: #0F172A;
        }
        .pth-section-sub {
            text-align: center; color: #64748B; font-size: 15px;
            margin-bottom: 28px;
        }

        .pth-feature-card {
            background: #FFFFFF; border: 1px solid #E7EAF0;
            border-radius: 16px; padding: 22px 20px; height: 100%;
            box-shadow: 0 4px 14px rgba(13,27,42,0.06);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .pth-feature-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 26px rgba(13,27,42,0.12);
        }
        .pth-feature-icon {
            width: 46px; height: 46px; border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; margin-bottom: 12px;
            background: linear-gradient(135deg, #1C2D60, #483A96);
        }
        .pth-feature-title {
            font-family: 'Poppins', sans-serif; font-weight: 600;
            font-size: 16.5px; color: #0F172A; margin-bottom: 6px;
        }
        .pth-feature-desc { color: #5B6478; font-size: 13.8px; line-height: 1.5; }

        .pth-stat-card {
            background: linear-gradient(135deg, #0D1B2A, #1C2D60);
            border-radius: 16px; padding: 20px 10px; text-align: center;
            color: #F5F0E6;
        }
        .pth-stat-value {
            font-family: 'Poppins', sans-serif; font-weight: 800;
            font-size: 26px; color: #E7C48E;
        }
        .pth-stat-label { font-size: 12.5px; opacity: 0.85; margin-top: 4px; }

        .pth-step-card {
            background: #FFFFFF; border: 1px solid #E7EAF0; border-radius: 14px;
            padding: 16px 18px; display: flex; align-items: center; gap: 14px;
            box-shadow: 0 3px 10px rgba(13,27,42,0.05); margin-bottom: 10px;
        }
        .pth-step-num {
            min-width: 34px; height: 34px; border-radius: 50%;
            background: linear-gradient(135deg, #1C2D60, #483A96);
            color: white; display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-family: 'Poppins', sans-serif; font-size: 14px;
        }
        .pth-step-text { font-size: 14.5px; color: #1F2937; font-weight: 500; }

        .pth-account-bar {
            background: #F4F6FB; border: 1px solid #E7EAF0; border-radius: 12px;
            padding: 10px 16px; margin-bottom: 18px;
            display: flex; align-items: center; justify-content: space-between;
        }

        .pth-cta-card {
            background: linear-gradient(120deg, #0D1B2A, #1C2D60 55%, #483A96);
            border-radius: 20px; padding: 34px 30px; text-align: center;
            color: #F5F0E6; margin: 10px 0 26px;
        }
        .pth-cta-title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 24px; }
        .pth-cta-sub { opacity: 0.85; font-size: 14.5px; margin-top: 6px; }

        .pth-auth-feature-list { margin-top: 18px; }
        .pth-auth-feature-item {
            display: flex; align-items: flex-start; gap: 12px;
            margin-bottom: 14px;
        }
        .pth-auth-feature-icon {
            width: 34px; height: 34px; min-width: 34px; border-radius: 10px;
            background: linear-gradient(135deg, #1C2D60, #483A96);
            display: flex; align-items: center; justify-content: center;
            font-size: 16px;
        }
        .pth-auth-feature-title {
            font-family: 'Poppins', sans-serif; font-weight: 600;
            font-size: 14.5px; color: #0F172A;
        }
        .pth-auth-feature-desc { font-size: 12.8px; color: #64748B; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =====================================================
# AUTHENTICATION
# =====================================================

def _complete_oauth_callback() -> None:
    """If Google/Facebook just redirected back here with ?code=&state=,
    finish the login and clear the URL before rendering anything else."""
    if st.session_state.get("auth_user"):
        return

    params = st.query_params
    code = params.get("code")
    state = params.get("state")
    if not code or state not in ("google", "facebook"):
        return

    profile = auth.complete_google_login(code) if state == "google" else auth.complete_facebook_login(code)
    st.query_params.clear()

    if profile and profile.get("email"):
        user = auth.login_or_signup_via_social(profile["name"], profile["email"], provider=state)
        st.session_state["auth_user"] = user
        st.session_state["auth_flash"] = f"Signed in with {state.title()} as {profile['email']}."
    else:
        st.session_state["auth_error"] = f"{state.title()} sign-in failed or was cancelled. Please try again."

    st.rerun()


def _render_social_buttons(context: str) -> None:
    col1, col2 = st.columns(2)
    google_url = auth.build_google_auth_url()
    facebook_url = auth.build_facebook_auth_url()

    with col1:
        if google_url:
            st.link_button("🔵 Continue with Google", google_url, use_container_width=True,
                            key=f"google_btn_{context}")
        else:
            st.button("🔵 Continue with Google", disabled=True, use_container_width=True,
                       key=f"google_btn_disabled_{context}",
                       help="Add [google] client_id/client_secret/redirect_uri to secrets.toml to enable this.")
    with col2:
        if facebook_url:
            st.link_button("🔷 Continue with Facebook", facebook_url, use_container_width=True,
                            key=f"facebook_btn_{context}")
        else:
            st.button("🔷 Continue with Facebook", disabled=True, use_container_width=True,
                       key=f"facebook_btn_disabled_{context}",
                       help="Add [facebook] app_id/app_secret/redirect_uri to secrets.toml to enable this.")


def render_auth_gate() -> None:
    """Split-screen Login / Sign up gate shown before the platform unlocks.
    Left: brand hero panel. Right: login/signup form."""

    left, right = st.columns([1, 1], gap="large")

    with left:
        assets = Path(__file__).parent / "assets"
        auth_hero_path = assets / "images" / "auth_hero.png"
        if auth_hero_path.exists():
            st.markdown('<div class="pth-hero-wrap">', unsafe_allow_html=True)
            st.image(str(auth_hero_path), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            logo_path = assets / "logo" / "logo.png"
            if logo_path.exists():
                st.image(str(logo_path), width=110)
            st.markdown(
                "<div class='pth-section-title' style='text-align:left;'>"
                "Turn Raw Data Into Decisions</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='pth-section-sub' style='text-align:left;'>"
                "AI cleaning &bull; dashboards &bull; insights &bull; reports</div>",
                unsafe_allow_html=True,
            )

        auth_features = [
            ("🧹", "Smart Data Cleaning", "One-click duplicate, missing-value and outlier cleanup."),
            ("🩺", "Data Health Check", "Instant data quality score before you analyze anything."),
            ("🤖", "AI-Powered Analysis", "Automatic business insights and an executive summary."),
            ("📊", "Dynamic Dashboards", "Premium, themeable dashboards generated in seconds."),
            ("📈", "Chart Creation", "Bar, line, pie, scatter, heatmap and more, one click away."),
            ("📄", "One-Click Reports", "Export polished PDF, Word, Excel and HTML reports."),
        ]
        feature_items = "".join(
            f"""
            <div class="pth-auth-feature-item">
                <div class="pth-auth-feature-icon">{icon}</div>
                <div>
                    <div class="pth-auth-feature-title">{title}</div>
                    <div class="pth-auth-feature-desc">{desc}</div>
                </div>
            </div>
            """
            for icon, title, desc in auth_features
        )
        st.markdown(
            f'<div class="pth-auth-feature-list">{feature_items}</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="pth-cta-card" style="margin-top:0;">
                <div class="pth-cta-title">Welcome to AI Data Analyzer Pro</div>
                <div class="pth-cta-sub">Log in or create a free account to get started.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.get("auth_flash"):
            st.success(st.session_state.pop("auth_flash"))
        if st.session_state.get("auth_error"):
            st.error(st.session_state.pop("auth_error"))

        tab_login, tab_signup = st.tabs(["🔐 Log In", "📝 Sign Up"])

        with tab_login:
            with st.form("login_form"):
                login_email = st.text_input("Email (User ID)", key="login_email")
                login_password = st.text_input("Password", type="password", key="login_password")
                submitted = st.form_submit_button("Log In", type="primary", use_container_width=True)
            if submitted:
                success, message, user = auth.login_user(login_email, login_password)
                if success:
                    st.session_state["auth_user"] = user
                    st.session_state["auth_flash"] = f"Welcome back, {user['name']}!"
                    st.rerun()
                else:
                    st.error(message)

            st.caption("or continue with")
            _render_social_buttons("login")

        with tab_signup:
            with st.form("signup_form"):
                su_name = st.text_input("Full Name", key="signup_name")
                su_email = st.text_input("Email (User ID)", key="signup_email")
                su_mobile = st.text_input("Mobile Number", key="signup_mobile")
                su_password = st.text_input("Create Password", type="password", key="signup_password")
                submitted_su = st.form_submit_button("Sign Up", type="primary", use_container_width=True)
            if submitted_su:
                success, message = auth.signup_user(su_name, su_email, su_mobile, su_password)
                if success:
                    st.success(message)
                else:
                    # Includes the "already signed up with this email id" case
                    st.warning(message)

            st.caption("or sign up with")
            _render_social_buttons("signup")


def render_account_bar() -> None:
    user = st.session_state["auth_user"]
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown(
            f"""<div class="pth-account-bar">
                <span>👋 Logged in as <b>{user['name']}</b> &nbsp;•&nbsp; {user['email']}</span>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        if st.button("Log Out", use_container_width=True):
            st.session_state.pop("auth_user", None)
            st.rerun()


# =====================================================
# HERO SECTION
# =====================================================

def show_branding() -> None:
    """Display application logo and hero banner."""

    assets = Path(__file__).parent / "assets"
    hero_path = assets / "images" / "hero_banner.png"

    if hero_path.exists():
        st.markdown('<div class="pth-hero-wrap">', unsafe_allow_html=True)
        st.image(str(hero_path), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Hero image not found.")

    st.markdown(
        """
        <div class="pth-badge-row">
            <div class="pth-badge">🧹 Smart Data Cleaning</div>
            <div class="pth-badge">📊 Interactive Dashboards</div>
            <div class="pth-badge">🤖 AI-Generated Insights</div>
            <div class="pth-badge">📄 One-Click Reports</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# SESSION INITIALIZATION
# =====================================================

def initialize_session() -> None:
    """Initialize application session state."""

    defaults = {
        "current_dataframe": None,
        "cleaned_dataframe": None,
        "dataset_info": None,
        "analysis_results": None,
        "insights": None,
        "dashboard": None,
        "generated_report": None,
        "dashboard_theme": "Modern",
        "cleaning_completed": False,
        "pipeline_log": [],
    }

    for key, value in defaults.items():
        if session_manager.get(key) is None:
            session_manager.set(key, value)

    logger.info("Session initialized.")


# =====================================================
# LOAD APPLICATION SETTINGS
# =====================================================

def load_configuration() -> Dict:
    """Load application configuration."""
    logger.info("Loading application configuration.")
    return settings


# =====================================================
# ENVIRONMENT VALIDATION
# =====================================================

def validate_environment() -> bool:
    """Validate required project folders."""

    logger.info("Validating project structure.")

    required_folders = [
        "config", "components", "pages", "utils", "logs", "outputs", "assets",
    ]

    for folder in required_folders:
        folder_path = PROJECT_ROOT / folder
        if not folder_path.exists():
            Path(folder).mkdir(parents=True, exist_ok=True)

    logger.info("Project structure validated.")
    return True


# =====================================================
# AI ENGINE INITIALIZATION
# =====================================================

def initialize_ai() -> bool:
    """Initialize AI Engine."""

    try:
        logger.info("Initializing AI Engine.")
        session_manager.set("ai_engine_ready", True)
        logger.info("AI Engine initialized.")
        return True

    except Exception as ex:
        logger.exception(ex)
        st.error("Unable to initialize AI Engine.")
        session_manager.set("ai_engine_ready", False)
        return False


# =====================================================
# STARTUP VALIDATION
# =====================================================

def startup_checks() -> bool:
    """Execute application startup checks."""
    if not validate_environment():
        return False
    if not initialize_ai():
        return False
    logger.info("Startup validation completed.")
    return True


# =====================================================
# HOMEPAGE
# =====================================================

def show_homepage() -> None:
    """Render application homepage intro."""

    st.markdown(
        "<div class='pth-section-title'>AI-Powered Data Analytics Platform</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='pth-section-sub'>
        Upload any spreadsheet or CSV and let AI Data Analyzer Pro clean it,
        understand it, visualize it, and explain it back to you — in minutes,
        not days.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =====================================================
# WHAT IS THIS WEBSITE FOR
# =====================================================

def show_purpose() -> None:
    """Explain the purpose of the platform in plain language."""

    st.markdown(
        "<div class='pth-section-title'>What Is AI Data Analyzer Pro?</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='pth-section-sub'>
        A single workspace that takes you from a messy raw file to a
        boardroom-ready dashboard and report — without writing a line of
        code or wrestling with spreadsheet formulas.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="pth-feature-card">
                <div class="pth-feature-icon">📂</div>
                <div class="pth-feature-title">1. Upload Anything</div>
                <div class="pth-feature-desc">
                CSV, Excel or JSON — drag in your raw dataset and AI Data
                Analyzer Pro instantly profiles rows, columns and data types.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="pth-feature-card">
                <div class="pth-feature-icon">🧠</div>
                <div class="pth-feature-title">2. Let AI Do the Work</div>
                <div class="pth-feature-desc">
                Automated cleaning, business-domain detection, KPI discovery
                and a written executive summary — generated for you.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="pth-feature-card">
                <div class="pth-feature-icon">📊</div>
                <div class="pth-feature-title">3. Present With Confidence</div>
                <div class="pth-feature-desc">
                A premium, themeable dashboard plus one-click PDF, PPT, Excel
                and HTML exports — ready to share or present.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    horizontal_space()


# =====================================================
# FEATURE CARDS
# =====================================================

FEATURES = [
    ("🧹", "Smart Data Cleaning",
     "Remove duplicates & empty rows/columns, fix missing values, trim & "
     "recase text, standardize column names, strip outliers with IQR/Z-score, "
     "and more — all with one click."),
    ("📈", "Data Health Check",
     "Instant quality score covering completeness, duplicates, data types "
     "and structural issues before you analyze anything."),
    ("🤖", "AI-Generated Insights",
     "Automatic business-domain detection, KPI recommendations and a "
     "plain-English executive summary of what your data is telling you."),
    ("📊", "Interactive Chart Builder",
     "Bar, line, area, pie, donut, scatter, histogram, heatmap, treemap, "
     "funnel, gauge and table charts generated straight from your columns."),
    ("🎨", "Premium Dashboards",
     "A polished, KPI-driven dashboard with 12 built-in premium themes — "
     "shuffle colors for a fresh look every time you generate one."),
    ("📄", "One-Click Reports",
     "Export your dashboard as PDF, PNG, Excel (with an embedded dashboard "
     "view), PowerPoint or a self-contained HTML file."),
]


def show_features() -> None:
    """Display application features as premium cards."""

    st.markdown(
        "<div class='pth-section-title'>Everything You Need, In One Platform</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='pth-section-sub'>Six modules, one seamless workflow.</div>",
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(FEATURES):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="pth-feature-card">
                    <div class="pth-feature-icon">{icon}</div>
                    <div class="pth-feature-title">{title}</div>
                    <div class="pth-feature-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)

    horizontal_space()


# =====================================================
# CAPABILITY STATS
# =====================================================

def show_capability_stats() -> None:
    """Highlight platform capabilities (not fabricated user counts)."""

    stats = [
        ("12+", "Chart Types"),
        ("12", "Premium Themes"),
        ("5", "Export Formats"),
        ("6", "AI-Powered Modules"),
    ]

    cols = st.columns(4)
    for col, (value, label) in zip(cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="pth-stat-card">
                    <div class="pth-stat-value">{value}</div>
                    <div class="pth-stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    horizontal_space()


# =====================================================
# WORKFLOW / HOW IT WORKS
# =====================================================

def show_workflow() -> None:
    """Step-by-step workflow, restyled as a premium timeline."""

    st.markdown(
        "<div class='pth-section-title'>How It Works</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='pth-section-sub'>Six steps from raw file to finished report.</div>",
        unsafe_allow_html=True,
    )

    workflow = [
        "📂 Upload your dataset (CSV / Excel / JSON)",
        "🩺 Run an automated data health check",
        "🧹 Clean your data with one-click, AI-assisted tools",
        "🤖 Generate AI insights, KPIs and an executive summary",
        "📊 Build a premium, interactive dashboard",
        "📄 Export a polished business report",
    ]

    left, right = st.columns(2)
    for i, step in enumerate(workflow):
        target = left if i % 2 == 0 else right
        with target:
            st.markdown(
                f"""
                <div class="pth-step-card">
                    <div class="pth-step-num">{i + 1}</div>
                    <div class="pth-step-text">{step}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()


# =====================================================
# APPLICATION STATUS
# =====================================================

def show_application_status() -> None:
    """Display application status."""

    st.header("Application Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Logger", "✅ Ready")

    with col2:
        ai_status = session_manager.get("ai_engine_ready", False)
        st.metric("AI Engine", "✅ Ready" if ai_status else "❌ Not Ready")

    with col3:
        st.metric("Session", "✅ Active")

    horizontal_space()


# =====================================================
# SIDEBAR
# =====================================================

def render_sidebar() -> None:
    """Render sidebar branding/status. Page links themselves are handled
    by st.navigation() in main(), based on login state."""

    with st.sidebar:
        st.title(APP_NAME)

        if st.session_state.get("auth_user"):
            user = st.session_state["auth_user"]
            st.success(f"👤 {user['name']}")

        st.markdown("---")
        st.subheader("Application")
        st.write(f"Version : {APP_VERSION}")
        st.write("Environment : Production")

        st.markdown("---")
        if session_manager.get("ai_engine_ready", False):
            st.success("AI Engine Ready")
        else:
            st.warning("AI Engine Not Initialized")


# =====================================================
# FOOTER
# =====================================================

def render_footer() -> None:
    """Render application footer."""

    st.divider()
    st.markdown(
        """
        <div style="text-align:center; color:#64748B; font-size:13px;">
        © 2026 <b>Punit Tech Hub</b> &nbsp;|&nbsp; AI Data Analyzer Pro<br>
        Professional AI-Powered Data Analytics Platform
        </div>
        """,
        unsafe_allow_html=True,
    )


# =====================================================
# HOME PAGES (registered via st.navigation below)
# =====================================================

def render_logged_out_home() -> None:
    """Home content shown before login: split-screen hero + auth form.
    No workflow pages exist in the sidebar at this point."""

    render_auth_gate()
    render_footer()


def render_logged_in_home() -> None:
    """Home content shown after login: full-width hero + platform intro."""

    render_account_bar()
    show_branding()

    show_homepage()
    show_purpose()
    show_capability_stats()
    show_features()
    show_workflow()
    show_application_status()

    st.header("Quick Start")
    st.success(
        """
        Your account is ready.

        Start by opening **Upload Data**
        from the navigation panel on the left.
        """
    )
    st.info(
        """
        Recommended workflow

        1. Upload Dataset
        2. Data Health Check
        3. Data Cleaning
        4. AI Insights
        5. Dashboard
        6. Reports
        """
    )

    render_footer()


# =====================================================
# MAIN APPLICATION
# =====================================================

def main() -> None:
    """Main application. Uses st.navigation() so the workflow pages
    (Upload Data, Data Health, ...) only appear in the sidebar once the
    user is logged in - before that, only Home is reachable."""

    logger.info("Starting AI Data Analyzer Pro.")

    inject_premium_css()
    initialize_session()
    load_configuration()

    if not startup_checks():
        st.stop()

    _complete_oauth_callback()
    render_sidebar()

    if st.session_state.get("auth_user"):
        pages = [
            st.Page(render_logged_in_home, title="Home", icon="🏠", default=True),
            st.Page("pages/1_Upload_Data.py", title="Upload Data", icon="📂"),
            st.Page("pages/2_Data_Health.py", title="Data Health", icon="🩺"),
            st.Page("pages/3_Data_Cleaning.py", title="Data Cleaning", icon="🧹"),
            st.Page("pages/4_AI_Insights.py", title="AI Insights", icon="🧠"),
            st.Page("pages/5_Dashboard.py", title="Dashboard", icon="📊"),
            st.Page("pages/6_Reports.py", title="Reports", icon="📄"),
        ]
    else:
        pages = [
            st.Page(render_logged_out_home, title="Home", icon="🏠", default=True),
        ]

    navigation = st.navigation(pages, position="sidebar")
    navigation.run()


# =====================================================
# APPLICATION EXECUTION
# =====================================================

if __name__ == "__main__":
    try:
        logger.info("Launching application.")
        main()
        logger.info("Application loaded successfully.")

    except Exception as ex:
        logger.exception(ex)
        st.error("Unexpected application error.")
        st.exception(ex)

