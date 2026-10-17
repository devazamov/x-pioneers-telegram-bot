"""Pytest fixtures for X PIONEERS Bot tests."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import AsyncGenerator
import pytest
import pytest_asyncio

from config import Settings
from database.db import DatabaseManager
from database.repository import Repository
from services.application_service import ApplicationService
from services.news_service import NewsService


@pytest.fixture
def test_settings() -> Settings:
    """Provides an isolated Settings instance for unit tests."""
    return Settings(
        BOT_TOKEN="123456789:TEST_MOCK_TOKEN_FOR_PYTEST",
        FOUNDER_ID=1001,
        ASSISTANT_ADMIN_ID=1002,
        EXTRA_ADMIN_IDS=[1003],
        CHANNEL_URL="https://t.me/test_channel",
        DATABASE_PATH=Path(":memory:"),
    )


@pytest_asyncio.fixture
async def temp_repo() -> AsyncGenerator[Repository, None]:
    """Provides a fresh SQLite database in a temporary file for isolated test runs."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
        temp_db_path = tf.name

    db_manager = DatabaseManager(temp_db_path)
    await db_manager.init_db()
    repo = Repository(db_manager)

    try:
        yield repo
    finally:
        if os.path.exists(temp_db_path):
            try:
                os.remove(temp_db_path)
            except OSError:
                pass


@pytest.fixture
def app_service(temp_repo: Repository) -> ApplicationService:
    return ApplicationService(temp_repo)


@pytest.fixture
def news_service(temp_repo: Repository) -> NewsService:
    return NewsService(temp_repo)
