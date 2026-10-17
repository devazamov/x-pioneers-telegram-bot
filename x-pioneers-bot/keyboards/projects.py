"""Projects inline keyboards."""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import PROJECTS_CATALOG


def get_projects_menu_keyboard() -> InlineKeyboardMarkup:
    """Builds project selection list from the static catalog."""
    builder = InlineKeyboardBuilder()

    for project in PROJECTS_CATALOG:
        builder.row(
            InlineKeyboardButton(
                text=f"🔹 {project.name}",
                callback_data=f"proj_view:{project.id}",
            )
        )

    builder.row(
        InlineKeyboardButton(text="🏠 Back to Main Menu", callback_data="nav_back_main")
    )
    return builder.as_markup()


def get_project_detail_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for an individual project detail screen."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️ Back to Projects", callback_data="nav_projects"),
        InlineKeyboardButton(text="🏠 Main Menu", callback_data="nav_back_main"),
    )
    return builder.as_markup()
