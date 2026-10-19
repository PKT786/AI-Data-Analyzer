"""
db.py
-----
Storage for user accounts (and anything else that must survive a restart).

WHY THIS EXISTS
    Streamlit Community Cloud wipes the app's local disk every time the
    app restarts, sleeps, or is redeployed. A SQLite file (data/users.db)
    therefore loses every account - users get asked to sign up again.

HOW IT WORKS
    * If secrets.toml has a [database] section with a `url`, all data is
      stored in that PostgreSQL database (permanent, free tiers exist -
      see SETUP_DATABASE.md).
    * If it does not, a local SQLite file is used. That is fine for
      running on your own computer, but it is NOT permanent on
      Streamlit Cloud.
    * If a `url` IS configured but the connection fails, we raise a clear
      error. We deliberately do NOT fall back to SQLite in that case,
      because that would silently put accounts on the disk that gets wiped.

Callers use plain `?` placeholders; they are translated for PostgreSQL.
"""

from __future__ import annotations

import logging
import os
import sqlite3

import streamlit as st

logger = logging.getLogger(__name__)

SQLITE_PATH = os.path.join(os.path.dirname(__file__), "data", "users.db")

_SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id            TEXT PRIMARY KEY,
        name          TEXT NOT NULL,
        email         TEXT NOT NULL UNIQUE,
        mobile        TEXT,
        password_hash TEXT,
        auth_provider TEXT NOT NULL DEFAULT 'local',
        created_at    DOUBLE PRECISION NOT NULL,
        last_login_at DOUBLE PRECISION,
        dashboard_credits_remaining INTEGER NOT NULL DEFAULT 2
    )
    """,
]

_schema_ready = {"sqlite": False, "postgres": False}


def database_url() -> str | None:
    try:
        url = st.secrets["database"]["url"]
    except Exception:
        return None
    url = (url or "").strip()
    return url or None


def backend() -> str:
    return "postgres" if database_url() else "sqlite"


def is_persistent() -> bool:
    """True when data is kept in an external database (survives restarts)."""
    return backend() == "postgres"


class _Conn:
    """Tiny wrapper so auth.py can use the same calls for both databases."""

    def __init__(self, raw, kind: str):
        self._raw = raw
        self._kind = kind

    def execute(self, sql: str, params=()):
        if self._kind == "postgres":
            cur = self._raw.cursor()
            cur.execute(sql.replace("?", "%s"), tuple(params))
            return cur
        return self._raw.execute(sql, tuple(params))

    def commit(self):
        self._raw.commit()

    def rollback(self):
        self._raw.rollback()

    def close(self):
        self._raw.close()


def _connect_postgres(url: str):
    try:
        import psycopg2
    except ImportError as ex:  # pragma: no cover
        raise RuntimeError(
            "A [database] url is configured but the 'psycopg2-binary' package "
            "is not installed. Add it to requirements.txt."
        ) from ex
    try:
        return psycopg2.connect(url, connect_timeout=10)
    except Exception as ex:
        raise RuntimeError(
            "Could not connect to the configured database "
            f"({type(ex).__name__}). Check the [database] url in your secrets "
            "(see SETUP_DATABASE.md). Accounts are NOT being saved right now."
        ) from ex


def _ensure_schema(conn: _Conn, kind: str) -> None:
    if kind == "postgres" and _schema_ready[kind]:
        return  # remote DB: check once per process
    for ddl in _SCHEMA:
        conn.execute(ddl)
    # Columns added after the first release, for databases created earlier.
    if kind == "postgres":
        conn.execute(
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS "
            "dashboard_credits_remaining INTEGER NOT NULL DEFAULT 2"
        )
    else:
        try:
            conn.execute(
                "ALTER TABLE users ADD COLUMN dashboard_credits_remaining "
                "INTEGER NOT NULL DEFAULT 2"
            )
        except sqlite3.OperationalError:
            pass  # column already exists
    conn.commit()
    _schema_ready[kind] = True


def get_conn() -> _Conn:
    url = database_url()
    if url:
        conn = _Conn(_connect_postgres(url), "postgres")
        _ensure_schema(conn, "postgres")
        return conn

    os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
    conn = _Conn(sqlite3.connect(SQLITE_PATH), "sqlite")
    _ensure_schema(conn, "sqlite")
    return conn
