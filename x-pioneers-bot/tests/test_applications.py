"""Tests for application validation, submission, and status lifecycle."""

from __future__ import annotations

import pytest
from database.repository import Repository
from services.application_service import ApplicationService


def test_application_validation():
    # Name validation
    ok, err = ApplicationService.validate_name("A")
    assert not ok and err is not None

    ok, err = ApplicationService.validate_name("Kamronbek")
    assert ok and err is None

    # Interest validation
    ok, err = ApplicationService.validate_interest("no")
    assert not ok and err is not None

    ok, err = ApplicationService.validate_interest("AI & 3D Interactive Systems")
    assert ok and err is None

    # Skills validation
    ok, err = ApplicationService.validate_skills("a")
    assert not ok and err is not None

    ok, err = ApplicationService.validate_skills("Python, aiogram, React, Tailwind")
    assert ok and err is None

    # Motivation validation
    ok, err = ApplicationService.validate_motivation("ok")
    assert not ok and err is not None

    ok, err = ApplicationService.validate_motivation("I want to contribute to the MAKTAB X educational mission!")
    assert ok and err is None


@pytest.mark.asyncio
async def test_application_lifecycle(temp_repo: Repository, app_service: ApplicationService):
    data = {
        "name": "Jane Innovator",
        "interest": "EdTech & 3D Graphics",
        "skills": "Three.js, WebGL, TypeScript",
        "motivation": "Passionate about creating modern learning experiences for kids.",
    }

    # Submit application
    app_id = await app_service.submit_application(
        user_id=123456,
        username="jane_innovator",
        data=data,
    )
    assert app_id > 0

    # Retrieve application
    app = await temp_repo.get_application(app_id)
    assert app is not None
    assert app.full_name == "Jane Innovator"
    assert app.status == "pending"
    assert app.user_id == 123456
    assert app.username == "jane_innovator"

    # Admin approves
    updated = await temp_repo.update_application_status(app_id, "approved")
    assert updated is True

    app_after = await temp_repo.get_application(app_id)
    assert app_after is not None
    assert app_after.status == "approved"

    # Verify count
    count = await temp_repo.get_applications_count()
    assert count == 1
