"""Main menu and general navigation inline keyboards."""

from __future__ import annotations

from typing import Optional
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import settings


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Builds the 6-button main menu inline keyboard."""
    builder = InlineKeyboardBuilder()

    # 1. 👥 About the Team & 🚀 Our Projects
    builder.row(
        InlineKeyboardButton(text="👥 About the Team", callback_data="nav_about"),
        InlineKeyboardButton(text="🚀 Our Projects", callback_data="nav_projects"),
    )

    # 2. 📰 Latest News & 🤝 Join the Team
    builder.row(
        InlineKeyboardButton(text="📰 Latest News", callback_data="nav_news"),
        InlineKeyboardButton(text="🤝 Join the Team", callback_data="nav_join"),
    )

    # 3. 📢 Official Channel & 📬 Contact Us
    # If a real channel URL is provided, open directly; otherwise show informational callback
    if settings.CHANNEL_URL and settings.CHANNEL_URL.startswith("http"):
        channel_btn = InlineKeyboardButton(text="📢 Official Channel", url=settings.CHANNEL_URL)
    else:
        channel_btn = InlineKeyboardButton(text="📢 Official Channel", callback_data="nav_channel_info")

    builder.row(
        channel_btn,
        InlineKeyboardButton(text="📬 Contact Us", callback_data="nav_contact"),
    )

    return builder.as_markup()


def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    """Standard back button to return to the main menu."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 Back to Main Menu", callback_data="nav_back_main")
    return builder.as_markup()


def get_contact_keyboard() -> InlineKeyboardMarkup:
    """Contact keyboard with direct Telegram link to founder."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="💬 Message Founder (@devazamov)",
            url="https://t.me/devazamov",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="💬 Message Assistant (@xvoid11)",
            url="https://t.me/xvoid11",
        )
    )
    builder.row(
        InlineKeyboardButton(text="🏠 Back to Main Menu", callback_data="nav_back_main")
    )
    return builder.as_markup()
