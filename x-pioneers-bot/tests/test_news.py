"""Tests for news service and SQLite database news repository."""

from __future__ import annotations

import pytest
from database.repository import Repository
from services.news_service import NewsService


@pytest.mark.asyncio
async def test_news_empty_state_does_not_crash(news_service: NewsService):
    """Verifies clear friendly empty state when no news exists."""
    display = await news_service.get_news_display()
    assert "No announcements have been published yet" in display
    assert "MAKTAB X" in display


@pytest.mark.asyncio
async def test_publish_and_retrieve_news(temp_repo: Repository, news_service: NewsService):
    # Empty count
    count_before = await temp_repo.get_news_count()
    assert count_before == 0

    # Publish an announcement
    post_id = await news_service.publish_news(
        title="MAKTAB X Alpha Demo Announced",
        text="We are excited to share our initial 3D science simulations with our first test schools.",
        author_id=1001,
        author_name="@devazamov",
    )
    assert post_id > 0

    count_after = await temp_repo.get_news_count()
    assert count_after == 1

    # Check formatted display
    display = await news_service.get_news_display()
    assert "MAKTAB X Alpha Demo Announced" in display
    assert "@devazamov" in display
    assert "No announcements" not in display

    # Check stats
    stats = await temp_repo.get_stats()
    assert stats["total_news"] == 1
