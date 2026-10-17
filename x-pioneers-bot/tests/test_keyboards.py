"""Tests for inline keyboard construction and layout."""

from __future__ import annotations

import pytest
from keyboards.admin import (
    get_admin_application_action_keyboard,
    get_admin_menu_keyboard,
    get_application_review_keyboard,
    get_broadcast_confirmation_keyboard,
)
from keyboards.main_menu import get_back_to_main_keyboard, get_main_menu_keyboard
from keyboards.projects import get_project_detail_keyboard, get_projects_menu_keyboard


def test_main_menu_keyboard_has_all_required_buttons():
    kb = get_main_menu_keyboard()
    assert kb.inline_keyboard is not None

    button_texts = []
    callback_or_urls = []
    for row in kb.inline_keyboard:
        for btn in row:
            button_texts.append(btn.text)
            callback_or_urls.append(btn.callback_data or btn.url)

    # Core 6 buttons required by specification
    expected_buttons = [
        "👥 About the Team",
        "🚀 Our Projects",
        "📰 Latest News",
        "🤝 Join the Team",
        "📢 Official Channel",
        "📬 Contact Us",
    ]

    for expected in expected_buttons:
        assert any(expected in t for t in button_texts), f"Missing button: {expected}"

    # None of the buttons should have empty actions
    for action in callback_or_urls:
        assert action is not None and len(action) > 0


def test_projects_menu_keyboard():
    kb = get_projects_menu_keyboard()
    assert len(kb.inline_keyboard) >= 3

    # Check presence of flagship project MAKTAB X
    found_maktab_x = any(
        any("MAKTAB X" in btn.text for btn in row) for row in kb.inline_keyboard
    )
    assert found_maktab_x is True

    # Check back button exists
    found_back = any(
        any(btn.callback_data == "nav_back_main" for btn in row)
        for row in kb.inline_keyboard
    )
    assert found_back is True


def test_project_detail_keyboard():
    kb = get_project_detail_keyboard()
    callbacks = [btn.callback_data for row in kb.inline_keyboard for btn in row]
    assert "nav_projects" in callbacks
    assert "nav_back_main" in callbacks


def test_admin_menu_keyboard():
    kb = get_admin_menu_keyboard()
    callbacks = [btn.callback_data for row in kb.inline_keyboard for btn in row]
    assert "admin_view_apps" in callbacks
    assert "admin_publish_news" in callbacks
    assert "admin_stats" in callbacks
    assert "admin_broadcast" in callbacks
    assert "nav_back_main" in callbacks


def test_broadcast_confirmation_keyboard():
    kb = get_broadcast_confirmation_keyboard()
    callbacks = [btn.callback_data for row in kb.inline_keyboard for btn in row]
    assert "admin_broadcast_confirm" in callbacks
    assert "admin_broadcast_cancel" in callbacks


def test_application_review_keyboard():
    kb = get_application_review_keyboard()
    callbacks = [btn.callback_data for row in kb.inline_keyboard for btn in row]
    assert "app_confirm_submit" in callbacks
    assert "app_restart" in callbacks
    assert "app_cancel" in callbacks


def test_admin_application_action_keyboard():
    kb = get_admin_application_action_keyboard(app_id=42)
    callbacks = [btn.callback_data for row in kb.inline_keyboard for btn in row]
    assert "admin_app_status:42:approved" in callbacks
    assert "admin_app_status:42:rejected" in callbacks
