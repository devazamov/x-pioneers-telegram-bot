"""Tests for callback payload routing, project catalog, and repository safety."""

from __future__ import annotations

import pytest
from config import PROJECTS_CATALOG
from database.repository import Repository


def test_project_catalog_integrity():
    assert len(PROJECTS_CATALOG) >= 3

    project_ids = [p.id for p in PROJECTS_CATALOG]
    assert "maktab_x" in project_ids
    assert "ai_dev" in project_ids
    assert "future_projects" in project_ids

    maktab = next(p for p in PROJECTS_CATALOG if p.id == "maktab_x")
    assert maktab.name == "MAKTAB X"
    assert maktab.status == "In development"
    assert len(maktab.key_features) > 0


def test_unknown_project_id_lookup_safety():
    unknown_id = "non_existent_project_id_999"
    project = next((p for p in PROJECTS_CATALOG if p.id == unknown_id), None)
    assert project is None


@pytest.mark.asyncio
async def test_user_upsert_and_event_logging(temp_repo: Repository):
    # Upsert new user
    await temp_repo.upsert_user(
        user_id=8888,
        username="dev_member",
        first_name="Member",
        last_name="One",
    )

    user = await temp_repo.get_user(8888)
    assert user is not None
    assert user.username == "dev_member"
    assert user.first_name == "Member"

    # Upsert same user with updated name
    await temp_repo.upsert_user(
        user_id=8888,
        username="dev_member_updated",
        first_name="MemberPrime",
    )
    updated_user = await temp_repo.get_user(8888)
    assert updated_user is not None
    assert updated_user.username == "dev_member_updated"
    assert updated_user.first_name == "MemberPrime"

    # Log event
    await temp_repo.log_event("test_event", 8888, "Test event details")
    stats = await temp_repo.get_stats()
    assert stats["total_events"] == 1
    assert stats["total_users"] == 1
