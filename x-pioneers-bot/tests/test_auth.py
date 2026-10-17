"""Tests for numeric ID role-based authorization."""

from __future__ import annotations

from config import Settings, _parse_id, _parse_id_list


def test_admin_authorization_rules(test_settings: Settings):
    founder_id = 1001
    assistant_id = 1002
    extra_id = 1003
    regular_user_id = 9999

    assert test_settings.is_admin(founder_id) is True
    assert test_settings.is_founder(founder_id) is True

    assert test_settings.is_admin(assistant_id) is True
    assert test_settings.is_founder(assistant_id) is False

    assert test_settings.is_admin(extra_id) is True
    assert test_settings.is_founder(extra_id) is False

    # Regular user must be blocked from admin privileges
    assert test_settings.is_admin(regular_user_id) is False
    assert test_settings.is_founder(regular_user_id) is False

    # None check
    assert test_settings.is_admin(None) is False
    assert test_settings.is_founder(None) is False


def test_id_parsers():
    assert _parse_id("12345") == 12345
    assert _parse_id("  98765  ") == 98765
    assert _parse_id("not_a_number") is None
    assert _parse_id("") is None
    assert _parse_id(None) is None

    assert _parse_id_list("101, 102, 103") == [101, 102, 103]
    assert _parse_id_list("101, invalid, 202") == [101, 202]
    assert _parse_id_list("") == []
    assert _parse_id_list(None) == []


def test_runtime_validation():
    # Placeholder should raise error
    invalid_settings = Settings(BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE")
    import pytest
    with pytest.raises(ValueError):
        invalid_settings.validate_runtime()

    # Empty token should raise error
    empty_settings = Settings(BOT_TOKEN="")
    with pytest.raises(ValueError):
        empty_settings.validate_runtime()
