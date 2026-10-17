"""Asynchronous SQLite connection manager and schema initialization."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional
import aiosqlite

logger = logging.getLogger("xpioneers.database")


SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    author_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS team_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    full_name TEXT NOT NULL,
    interest TEXT NOT NULL,
    skills TEXT NOT NULL,
    motivation TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bot_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    user_id INTEGER,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_last_active ON users(last_active_at);
CREATE INDEX IF NOT EXISTS idx_news_created ON news(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_applications_user ON team_applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON team_applications(status);
"""


class DatabaseManager:
    """Manages asynchronous database connection pooling and schema initialization."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)

    async def init_db(self) -> None:
        """Create tables and indexes if they do not exist."""
        # Ensure parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info("Initializing SQLite database at %s", self.db_path)

        async with aiosqlite.connect(self.db_path) as conn:
            await conn.executescript(SCHEMA_SQL)
            await conn.commit()
        logger.info("Database schema initialized successfully.")

    def connect(self) -> aiosqlite.Connection:
        """Returns an async connection context manager."""
        return aiosqlite.connect(self.db_path)
