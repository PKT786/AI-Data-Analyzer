"""
auth.py
-------
Authentication layer for AI Data Analyzer Pro.

Responsibilities:
    * User storage (SQLite file DB) - signup / login / duplicate-email check
    * Password hashing (PBKDF2-SHA256, salted - never stores plaintext)
    * Google & Facebook OAuth2 "Sign in with..." (no signup form needed -
      a verified email from the provider is trusted automatically)
    * Admin notification (email + SMS) on every signup and every login,
      containing the user's name, email and mobile number

--------------------------------------------------------------------
SETUP REQUIRED (see .streamlit/secrets.toml.example)
--------------------------------------------------------------------
Nothing here works "for free" - Google/Facebook login and the admin
email/SMS alerts all need credentials that only you can create. Until
you add them to `.streamlit/secrets.toml`, local email/password
signup & login still work fully; the social buttons and notifications
simply no-op (log a warning) instead of crashing the app.

Required secrets (all optional individually - each feature degrades
gracefully if its keys are missing):

    [google]
    client_id     = "xxxx.apps.googleusercontent.com"
    client_secret = "xxxx"
    redirect_uri  = "https://your-app-url.streamlit.app"

    [facebook]
    app_id        = "xxxx"
    app_secret    = "xxxx"
    redirect_uri  = "https://your-app-url.streamlit.app"

    [smtp]
    email         = "your-sending-address@gmail.com"
    app_password  = "xxxx xxxx xxxx xxxx"   # Gmail App Password
    admin_email   = "punitkr.786@gmail.com"

    [sms]
    provider      = "twilio"
    account_sid   = "ACxxxx"
    auth_token    = "xxxx"
    from_number   = "+1xxxxxxxxxx"
    admin_mobile  = "+919145480345"
--------------------------------------------------------------------
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import re
import smtplib
import sqlite3
import ssl
import time
import uuid
from contextlib import closing
from email.mime.text import MIMEText

import requests
import streamlit as st
import streamlit.components.v1 as components

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "users.db")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

DEFAULT_ADMIN_EMAIL = "punitkr.786@gmail.com"
DEFAULT_ADMIN_MOBILE = "+919145480345"
APP_LABEL = "AI Data Analyzer Pro"


# ================================================================== DB =====

def _get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id            TEXT PRIMARY KEY,
            name          TEXT NOT NULL,
            email         TEXT NOT NULL UNIQUE,
            mobile        TEXT,
            password_hash TEXT,
            auth_provider TEXT NOT NULL DEFAULT 'local',
            created_at    REAL NOT NULL,
            last_login_at REAL
        )
        """
    )
    conn.commit()
    return conn


def _normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def find_user_by_email(email: str) -> dict | None:
    email = _normalize_email(email)
    with closing(_get_conn()) as conn:
        row = conn.execute(
            "SELECT id, name, email, mobile, password_hash, auth_provider, created_at, last_login_at "
            "FROM users WHERE email = ?",
            (email,),
        ).fetchone()
    if not row:
        return None
    keys = ["id", "name", "email", "mobile", "password_hash", "auth_provider", "created_at", "last_login_at"]
    return dict(zip(keys, row))


# ============================================================ PASSWORDS ====

def _hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return f"{salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, digest_hex = stored.split("$", 1)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
        return hmac.compare_digest(candidate, expected)
    except Exception:
        return False


# ================================================================ VALIDATION

def validate_signup(name: str, email: str, mobile: str, password: str) -> str | None:
    """Return an error message, or None if everything looks valid."""
    if not name or not name.strip():
        return "Please enter your name."
    if not email or not EMAIL_RE.match(email.strip()):
        return "Please enter a valid email address."
    if not mobile or len(re.sub(r"\D", "", mobile)) < 10:
        return "Please enter a valid mobile number (at least 10 digits)."
    if not password or len(password) < 6:
        return "Password must be at least 6 characters."
    return None


# ============================================================== SIGN UP ====

def signup_user(name: str, email: str, mobile: str, password: str) -> tuple[bool, str]:
    """
    Create a new local account.
    Returns (success, message). If the email already exists, success is
    False and the message tells the user to log in instead.
    """
    error = validate_signup(name, email, mobile, password)
    if error:
        return False, error

    email = _normalize_email(email)

    if find_user_by_email(email):
        return False, "You have already signed up with this email id. Please log in instead."

    user_id = str(uuid.uuid4())
    now = time.time()
    with closing(_get_conn()) as conn:
        conn.execute(
            "INSERT INTO users (id, name, email, mobile, password_hash, auth_provider, created_at) "
            "VALUES (?, ?, ?, ?, ?, 'local', ?)",
            (user_id, name.strip(), email, mobile.strip(), _hash_password(password), now),
        )
        conn.commit()

    notify_admin(name.strip(), email, mobile.strip(), event="New Sign Up")
    return True, "Signup successful! You can now log in with your email and password."


# ================================================================ LOG IN ====

def login_user(email: str, password: str) -> tuple[bool, str, dict | None]:
    """Returns (success, message, user_dict_or_None)."""
    email = _normalize_email(email)
    if not email or not password:
        return False, "Please enter both your email and password.", None

    user = find_user_by_email(email)
    if not user:
        return False, "No account found with this email. Please sign up first.", None

    if user["auth_provider"] != "local" or not user["password_hash"]:
        return False, (
            f"This email is registered via {user['auth_provider'].title()} sign-in. "
            f"Please use the '{user['auth_provider'].title()}' button instead."
        ), None

    if not _verify_password(password, user["password_hash"]):
        return False, "Incorrect password. Please try again.", None

    _touch_last_login(user["id"])
    notify_admin(user["name"], user["email"], user.get("mobile") or "N/A", event="Login")
    return True, "Logged in successfully!", user


def _touch_last_login(user_id: str) -> None:
    with closing(_get_conn()) as conn:
        conn.execute("UPDATE users SET last_login_at = ? WHERE id = ?", (time.time(), user_id))
        conn.commit()


# ========================================================= OAUTH (SOCIAL) ==

def _secret(section: str, key: str) -> str | None:
    try:
        return st.secrets[section][key]
    except Exception:
        return None


def oauth_configured(provider: str) -> bool:
    if provider == "google":
        return bool(_secret("google", "client_id") and _secret("google", "client_secret"))
    if provider == "facebook":
        return bool(_secret("facebook", "app_id") and _secret("facebook", "app_secret"))
    return False


def build_google_auth_url() -> str | None:
    client_id = _secret("google", "client_id")
    redirect_uri = _secret("google", "redirect_uri")
    if not client_id or not redirect_uri:
        return None
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "prompt": "select_account",
        "state": "google",
    }
    query = "&".join(f"{k}={requests.utils.quote(v)}" for k, v in params.items())
    return f"https://accounts.google.com/o/oauth2/v2/auth?{query}"


def build_facebook_auth_url() -> str | None:
    app_id = _secret("facebook", "app_id")
    redirect_uri = _secret("facebook", "redirect_uri")
    if not app_id or not redirect_uri:
        return None
    params = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "email,public_profile",
        "state": "facebook",
    }
    query = "&".join(f"{k}={requests.utils.quote(v)}" for k, v in params.items())
    return f"https://www.facebook.com/v19.0/dialog/oauth?{query}"


def complete_google_login(code: str) -> dict | None:
    """Exchange an OAuth code for the user's verified Google profile."""
    client_id = _secret("google", "client_id")
    client_secret = _secret("google", "client_secret")
    redirect_uri = _secret("google", "redirect_uri")
    if not all([client_id, client_secret, redirect_uri]):
        return None

    try:
        token_resp = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
            timeout=10,
        )
        token_resp.raise_for_status()
        access_token = token_resp.json()["access_token"]

        profile_resp = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        profile_resp.raise_for_status()
        profile = profile_resp.json()

        if not profile.get("email_verified", True):
            return None

        return {"name": profile.get("name") or profile.get("email"), "email": profile.get("email")}
    except Exception as ex:
        logger.warning("Google OAuth exchange failed: %s", ex)
        return None


def complete_facebook_login(code: str) -> dict | None:
    """Exchange an OAuth code for the user's verified Facebook profile."""
    app_id = _secret("facebook", "app_id")
    app_secret = _secret("facebook", "app_secret")
    redirect_uri = _secret("facebook", "redirect_uri")
    if not all([app_id, app_secret, redirect_uri]):
        return None

    try:
        token_resp = requests.get(
            "https://graph.facebook.com/v19.0/oauth/access_token",
            params={
                "client_id": app_id,
                "client_secret": app_secret,
                "redirect_uri": redirect_uri,
                "code": code,
            },
            timeout=10,
        )
        token_resp.raise_for_status()
        access_token = token_resp.json()["access_token"]

        profile_resp = requests.get(
            "https://graph.facebook.com/me",
            params={"fields": "id,name,email", "access_token": access_token},
            timeout=10,
        )
        profile_resp.raise_for_status()
        profile = profile_resp.json()

        if not profile.get("email"):
            return None

        return {"name": profile.get("name") or profile.get("email"), "email": profile.get("email")}
    except Exception as ex:
        logger.warning("Facebook OAuth exchange failed: %s", ex)
        return None


def login_or_signup_via_social(name: str, email: str, provider: str) -> dict:
    """
    A verified email from Google/Facebook is trusted automatically -
    no signup form needed. If the email is new, an account is created
    on the fly (mobile number left blank, can be added later); if it
    already exists, this is treated as a normal login.
    """
    email = _normalize_email(email)
    existing = find_user_by_email(email)

    if existing:
        _touch_last_login(existing["id"])
        notify_admin(existing["name"], existing["email"], existing.get("mobile") or "N/A",
                     event=f"Login via {provider.title()}")
        return existing

    user_id = str(uuid.uuid4())
    now = time.time()
    with closing(_get_conn()) as conn:
        conn.execute(
            "INSERT INTO users (id, name, email, mobile, password_hash, auth_provider, created_at, last_login_at) "
            "VALUES (?, ?, ?, NULL, NULL, ?, ?, ?)",
            (user_id, name, email, provider, now, now),
        )
        conn.commit()

    notify_admin(name, email, "N/A", event=f"New Sign Up via {provider.title()}")
    return find_user_by_email(email)


# ========================================================= NOTIFICATIONS ===

def notify_admin(name: str, email: str, mobile: str, event: str) -> None:
    """Best-effort: emails + texts the admin. Never raises - a failed
    notification must never block a user's signup/login."""
    try:
        _send_admin_email(name, email, mobile, event)
    except Exception as ex:
        logger.warning("Admin email notification failed: %s", ex)

    try:
        _send_admin_sms(name, email, mobile, event)
    except Exception as ex:
        logger.warning("Admin SMS notification failed: %s", ex)


def _send_admin_email(name: str, email: str, mobile: str, event: str) -> None:
    sender = _secret("smtp", "email")
    app_password = _secret("smtp", "app_password")
    admin_email = _secret("smtp", "admin_email") or DEFAULT_ADMIN_EMAIL

    if not sender or not app_password:
        logger.info("SMTP not configured - skipping admin email for '%s'.", event)
        return

    body = (
        f"Event: {event}\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Mobile: {mobile}\n"
        f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    msg = MIMEText(body)
    msg["Subject"] = f"[{APP_LABEL}] {event}: {name}"
    msg["From"] = sender
    msg["To"] = admin_email

    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
        server.starttls(context=context)
        server.login(sender, app_password)
        server.sendmail(sender, [admin_email], msg.as_string())


def _send_admin_sms(name: str, email: str, mobile: str, event: str) -> None:
    account_sid = _secret("sms", "account_sid")
    auth_token = _secret("sms", "auth_token")
    from_number = _secret("sms", "from_number")
    admin_mobile = _secret("sms", "admin_mobile") or DEFAULT_ADMIN_MOBILE

    if not all([account_sid, auth_token, from_number]):
        logger.info("SMS provider not configured - skipping admin SMS for '%s'.", event)
        return

    body = f"[{APP_LABEL}] {event}: {name} ({email}, {mobile})"

    # Twilio REST API (swap this block out if you use a different SMS provider)
    resp = requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json",
        data={"To": admin_mobile, "From": from_number, "Body": body},
        auth=(account_sid, auth_token),
        timeout=10,
    )
    resp.raise_for_status()


# =========================================================== PAGE GUARD ====

def require_login() -> None:
    """
    Call this at the top of every page (right after st.set_page_config)
    to make sure a page can't be reached by typing/clicking its URL
    directly without logging in first via the home page.
    """
    if st.session_state.get("auth_user"):
        return

    st.warning(
        "🔒 Please log in from the **Home** page (first item in the left "
        "sidebar navigation) to use AI Data Analyzer Pro."
    )
    st.stop()


# ======================================================= SHARED ACCOUNT BAR

def render_account_bar() -> None:
    """
    Shared "Logged in as ... | Log Out" bar. Call this on every page
    (right after require_login()) so a logged-in user can log out from
    anywhere, without going back to Home. The bar is pinned (sticky) to
    the top of the content area so it stays visible while scrolling.
    """
    user = st.session_state.get("auth_user")
    if not user:
        return

    st.markdown(
        """
        <style>
        .st-key-pth_account_bar {
            position: fixed !important;
            top: 60px;
            left: 0;
            right: 0;
            z-index: 500;
            background: #F4F6FB;
            border-bottom: 1px solid #E7EAF0;
            padding: 10px 24px;
            box-sizing: border-box;
            transition: left 0.15s ease;
        }
        .st-key-pth_account_bar div[data-testid="stMarkdownContainer"] p {
            margin-bottom: 0;
            font-size: 14px;
        }
        [data-testid="stMain"] .block-container {
            padding-top: 7.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # The bar is fixed to the viewport (so it truly stays put while
    # scrolling), which means it no longer follows the sidebar's flex
    # layout. This tiny script keeps its left edge/width lined up with
    # the actual main content area - so its text always starts to the
    # right of the sidebar, whether the sidebar is expanded, collapsed,
    # or resized.
    components.html(
        """
        <script>
        function pthAlignAccountBar() {
            const doc = window.parent.document;
            const main = doc.querySelector('[data-testid="stMain"]');
            const bar = doc.querySelector('.st-key-pth_account_bar');
            if (main && bar) {
                const rect = main.getBoundingClientRect();
                bar.style.left = rect.left + 'px';
                bar.style.width = rect.width + 'px';
            }
        }
        pthAlignAccountBar();
        window.parent.addEventListener('resize', pthAlignAccountBar);
        setInterval(pthAlignAccountBar, 400);
        </script>
        """,
        height=0,
    )

    with st.container(key="pth_account_bar"):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(
                f"👋 Logged in as **{user['name']}**  •  {user['email']}"
            )
        with col2:
            if st.button("Log Out", key="pth_logout_btn", use_container_width=True):
                st.session_state.pop("auth_user", None)
                st.rerun()

