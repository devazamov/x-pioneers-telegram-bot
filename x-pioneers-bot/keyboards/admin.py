"""Admin keyboards and application review keyboards."""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_menu_keyboard() -> InlineKeyboardMarkup:
    """Builds the main admin dashboard inline keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="📥 View Applications", callback_data="admin_view_apps"),
        InlineKeyboardButton(text="📢 Publish News", callback_data="admin_publish_news"),
    )
    builder.row(
        InlineKeyboardButton(text="📊 Bot Statistics", callback_data="admin_stats"),
        InlineKeyboardButton(text="📨 Broadcast Message", callback_data="admin_broadcast"),
    )
    builder.row(
        InlineKeyboardButton(text="🏠 Return to Main Menu", callback_data="nav_back_main")
    )
    return builder.as_markup()


def get_broadcast_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Explicit confirmation keyboard for message broadcasting."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Yes, Send Broadcast", callback_data="admin_broadcast_confirm"),
        InlineKeyboardButton(text="❌ Cancel Broadcast", callback_data="admin_broadcast_cancel"),
    )
    return builder.as_markup()


def get_application_review_keyboard() -> InlineKeyboardMarkup:
    """Applicant review screen keyboard before final submission."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Confirm & Submit", callback_data="app_confirm_submit"),
        InlineKeyboardButton(text="🔄 Restart Form", callback_data="app_restart"),
    )
    builder.row(
        InlineKeyboardButton(text="❌ Cancel Application", callback_data="app_cancel"),
    )
    return builder.as_markup()


def get_admin_application_action_keyboard(app_id: int) -> InlineKeyboardMarkup:
    """Actions an authorized admin can take on a submitted application."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Approve", callback_data=f"admin_app_status:{app_id}:approved"),
        InlineKeyboardButton(text="❌ Reject", callback_data=f"admin_app_status:{app_id}:rejected"),
    )
    builder.row(
        InlineKeyboardButton(text="⬅️ Back to Applications", callback_data="admin_view_apps"),
        InlineKeyboardButton(text="⚙️ Admin Menu", callback_data="admin_menu"),
    )
    return builder.as_markup()
