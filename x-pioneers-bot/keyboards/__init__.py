"""Keyboards package."""

from keyboards.admin import (
    get_admin_application_action_keyboard,
    get_admin_menu_keyboard,
    get_application_review_keyboard,
    get_broadcast_confirmation_keyboard,
)
from keyboards.main_menu import (
    get_back_to_main_keyboard,
    get_contact_keyboard,
    get_main_menu_keyboard,
)
from keyboards.projects import (
    get_project_detail_keyboard,
    get_projects_menu_keyboard,
)

__all__ = [
    "get_main_menu_keyboard",
    "get_back_to_main_keyboard",
    "get_contact_keyboard",
    "get_projects_menu_keyboard",
    "get_project_detail_keyboard",
    "get_admin_menu_keyboard",
    "get_broadcast_confirmation_keyboard",
    "get_application_review_keyboard",
    "get_admin_application_action_keyboard",
]
