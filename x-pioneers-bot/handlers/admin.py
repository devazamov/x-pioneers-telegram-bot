"""Role-based Admin dashboard and management handlers."""

from __future__ import annotations

import logging
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import settings
from database.repository import Repository
from keyboards.admin import (
    get_admin_application_action_keyboard,
    get_admin_menu_keyboard,
    get_broadcast_confirmation_keyboard,
)
from keyboards.main_menu import get_back_to_main_keyboard
from services.news_service import NewsService
from services.notification_service import NotificationService
from states.admin_states import BroadcastSG, PublishNewsSG

logger = logging.getLogger("xpioneers.handlers.admin")
router = Router(name="admin_router")


def _get_admin_role_title(user_id: int) -> str:
    if settings.is_founder(user_id):
        return "👑 Founder & Admin"
    if user_id == settings.ASSISTANT_ADMIN_ID:
        return "🛡 Assistant Admin"
    return "⚡ Authorized Administrator"


# ---------------- DASHBOARD ACCESS ----------------

@router.message(Command("admin"))
async def command_admin(message: Message, repository: Repository) -> None:
    user = message.from_user
    if not user or not settings.is_admin(user.id):
        await message.answer(
            "⛔ <b>Access Denied</b>\n\n"
            "This command is restricted to authorized X PIONEERS administrators.",
            parse_mode="HTML",
        )
        return

    stats = await repository.get_stats()
    role_title = _get_admin_role_title(user.id)

    text = (
        f"⚙️ <b>X PIONEERS Administration Panel</b>\n"
        f"<b>Role:</b> {role_title}\n"
        f"<b>User ID:</b> <code>{user.id}</code>\n\n"
        f"📊 <b>System Overview:</b>\n"
        f"• Registered Users: <b>{stats['total_users']}</b>\n"
        f"• Total Applications: <b>{stats['total_applications']}</b> (Pending: <b>{stats['pending_applications']}</b>)\n"
        f"• News Posts: <b>{stats['total_news']}</b>\n\n"
        "Choose an administrative action below:"
    )

    await message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=get_admin_menu_keyboard(),
    )


@router.callback_query(F.data == "admin_menu")
async def callback_admin_menu(callback: CallbackQuery, repository: Repository) -> None:
    user = callback.from_user
    if not user or not settings.is_admin(user.id):
        await callback.answer("Access denied.", show_alert=True)
        return

    await callback.answer()
    stats = await repository.get_stats()
    role_title = _get_admin_role_title(user.id)

    text = (
        f"⚙️ <b>X PIONEERS Administration Panel</b>\n"
        f"<b>Role:</b> {role_title}\n"
        f"<b>User ID:</b> <code>{user.id}</code>\n\n"
        f"📊 <b>System Overview:</b>\n"
        f"• Registered Users: <b>{stats['total_users']}</b>\n"
        f"• Total Applications: <b>{stats['total_applications']}</b> (Pending: <b>{stats['pending_applications']}</b>)\n"
        f"• News Posts: <b>{stats['total_news']}</b>\n\n"
        "Choose an administrative action below:"
    )

    if callback.message:
        await callback.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=get_admin_menu_keyboard(),
        )


# ---------------- BOT STATISTICS ----------------

@router.callback_query(F.data == "admin_stats")
async def callback_admin_stats(callback: CallbackQuery, repository: Repository) -> None:
    user = callback.from_user
    if not user or not settings.is_admin(user.id):
        await callback.answer("Access denied.", show_alert=True)
        return

    await callback.answer()
    stats = await repository.get_stats()

    text = (
        "📊 <b>X PIONEERS Bot Statistics</b>\n\n"
        f"👥 <b>Total Users in Database:</b> {stats['total_users']}\n"
        f"📥 <b>Total Applications Received:</b> {stats['total_applications']}\n"
        f"⏳ <b>Pending Applications:</b> {stats['pending_applications']}\n"
        f"📰 <b>Published Announcements:</b> {stats['total_news']}\n"
        f"⚡ <b>Recorded Audit Events:</b> {stats['total_events']}\n\n"
        f"📁 <i>Database location: {settings.DATABASE_PATH.name}</i>"
    )

    if callback.message:
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        b = InlineKeyboardBuilder()
        b.row(InlineKeyboardButton(text="⬅️ Back to Admin", callback_data="admin_menu"))
        await callback.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=b.as_markup(),
        )


# ---------------- VIEW APPLICATIONS ----------------

@router.callback_query(F.data == "admin_view_apps")
async def callback_admin_view_apps(callback: CallbackQuery, repository: Repository) -> None:
    user = callback.from_user
    if not user or not settings.is_admin(user.id):
        await callback.answer("Access denied.", show_alert=True)
        return

    await callback.answer()
    apps = await repository.get_all_applications(limit=10)

    if not apps:
        text = "📥 <b>Applications</b>\n\n<i>No team applications submitted yet.</i>"
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        b = InlineKeyboardBuilder()
        b.row(InlineKeyboardButton(text="⬅️ Back to Admin", callback_data="admin_menu"))
        if callback.message:
            await callback.message.edit_text(text=text, parse_mode="HTML", reply_markup=b.as_markup())
        return

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    b = InlineKeyboardBuilder()

    lines = ["📥 <b>Recent Team Applications:</b>\n"]
    for app in apps:
        status_icon = "⏳" if app.status == "pending" else ("✅" if app.status == "approved" else "❌")
        username_part = f"@{app.username}" if app.username else f"ID:{app.user_id}"
        lines.append(f"{status_icon} <b>#{app.id}</b> {app.full_name} ({username_part}) — <i>{app.interest}</i>")
        b.row(InlineKeyboardButton(text=f"View Application #{app.id} ({app.full_name[:15]})", callback_data=f"admin_app_detail:{app.id}"))

    b.row(InlineKeyboardButton(text="⬅️ Back to Admin", callback_data="admin_menu"))

    if callback.message:
        await callback.message.edit_text(
            text="\n".join(lines),
            parse_mode="HTML",
            reply_markup=b.as_markup(),
        )


@router.callback_query(F.data.startswith("admin_app_detail:"))
async def callback_admin_app_detail(callback: CallbackQuery, repository: Repository) -> None:
    user = callback.from_user
    if not user or not settings.is_admin(user.id):
        await callback.answer("Access denied.", show_alert=True)
        return

    await callback.answer()
    app_id = int(callback.data.split(":")[1])
    app = await repository.get_application(app_id)

    if not app:
        await callback.answer("Application not found.", show_alert=True)
        return

    status_badge = {
        "pending": "⏳ Pending Review",
        "approved": "✅ Approved",
        "rejected": "❌ Rejected",
    }.get(app.status, app.status)

    text = (
        f"📋 <b>Application #{app.id} Details</b>\n"
        f"<b>Status:</b> {status_badge}\n"
        f"<b>Date:</b> {app.created_at}\n\n"
        f"👤 <b>Name:</b> {app.full_name}\n"
        f"🆔 <b>User ID:</b> <code>{app.user_id}</code>\n"
        f"💬 <b>Telegram:</b> @{app.username or 'No username'}\n"
        f"🎯 <b>Interest:</b> {app.interest}\n\n"
        f"🛠 <b>Skills & Tech:</b>\n{app.skills}\n\n"
        f"💡 <b>Motivation:</b>\n{app.motivation}\n"
    )

    if callback.message:
        await callback.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=get_admin_application_action_keyboard(app.id),
        )


@router.callback_query(F.data.startswith("admin_app_status:"))
async def callback_admin_change_app_status(callback: CallbackQuery, repository: Repository) -> None:
    user = callback.from_user
    if not user or not settings.is_admin(user.id):
        await callback.answer("Access denied.", show_alert=True)
        return

    parts = callback.data.split(":")
    app_id = int(parts[1])
    new_status = parts[2]

    success = await repository.update_application_status(app_id, new_status)
    if success:
        await callback.answer(f"Application #{app_id} marked as {new_status}!", show_alert=True)
        await repository.log_event(
            "admin_status_change",
            user.id,
            f"Admin {user.id} updated app #{app_id} status to {new_status}",
        )
        # Refresh detail screen
        app = await repository.get_application(app_id)
        if app and callback.message:
            status_badge = "✅ Approved" if new_status == "approved" else "❌ Rejected"
            text = (
                f"📋 <b>Application #{app.id} Details</b>\n"
                f"<b>Status:</b> {status_badge}\n"
                f"<b>Date:</b> {app.created_at}\n\n"
                f"👤 <b>Name:</b> {app.full_name}\n"
                f"🆔 <b>User ID:</b> <code>{app.user_id}</code>\n"
                f"💬 <b>Telegram:</b> @{app.username or 'No username'}\n"
                f"🎯 <b>Interest:</b> {app.interest}\n\n"
                f"🛠 <b>Skills & Tech:</b>\n{app.skills}\n\n"
                f"💡 <b>Motivation:</b>\n{app.motivation}\n"
            )
            await callback.message.edit_text(
                text=text,
                parse_mode="HTML",
                reply_markup=get_admin_application_action_keyboard(app.id),
            )
    else:
        await callback.answer("Failed to update status.", show_alert=True)


# ---------------- PUBLISH NEWS FSM ----------------

@router.callback_query(F.data == "admin_publish_news")
async def callback_start_publish_news(callback: CallbackQuery, state: FSMContext) -> None:
    user = callback.from_user
    if not user or not settings.is_admin(user.id):
        await callback.answer("Access denied.", show_alert=True)
        return

    await callback.answer()
    await state.clear()
    await state.set_state(PublishNewsSG.waiting_for_title)

    if callback.message:
        await callback.message.edit_text(
            "📢 <b>Publish Official Announcement</b>\n\n"
            "Step 1/2: Please send the <b>headline / title</b> for the announcement:\n"
            "<i>(Type /cancel to abort at any time)</i>",
            parse_mode="HTML",
        )


@router.message(PublishNewsSG.waiting_for_title)
async def process_news_title(message: Message, state: FSMContext) -> None:
    title = (message.text or "").strip()
    if len(title) < 3 or len(title) > 120:
        await message.answer("⚠️ Title must be between 3 and 120 characters. Please try again:")
        return

    await state.update_data(title=title)
    await state.set_state(PublishNewsSG.waiting_for_text)
    await message.answer(
        f"Title set: <b>{title}</b>\n\n"
        "Step 2/2: Now enter the full announcement body text:",
        parse_mode="HTML",
    )


@router.message(PublishNewsSG.waiting_for_text)
async def process_news_text(
    message: Message,
    state: FSMContext,
    news_service: NewsService,
) -> None:
    text = (message.text or "").strip()
    if len(text) < 5:
        await message.answer("⚠️ Announcement text must be at least 5 characters. Please try again:")
        return

    data = await state.get_data()
    title = data["title"]
    user = message.from_user
    author_name = user.first_name if user else "Admin"

    post_id = await news_service.publish_news(
        title=title,
        text=text,
        author_id=user.id if user else 0,
        author_name=author_name,
    )
    await state.clear()

    await message.answer(
        f"✅ <b>Announcement Published!</b>\n\n"
        f"<b>Post ID:</b> #{post_id}\n"
        f"<b>Title:</b> {title}\n\n"
        "It is now live in the /news section for all community members.",
        parse_mode="HTML",
        reply_markup=get_admin_menu_keyboard(),
    )


# ---------------- BROADCAST MESSAGE (WITH 2-STEP CONFIRMATION) ----------------

@router.callback_query(F.data == "admin_broadcast")
async def callback_start_broadcast(callback: CallbackQuery, state: FSMContext, repository: Repository) -> None:
    user = callback.from_user
    if not user or not settings.is_admin(user.id):
        await callback.answer("Access denied.", show_alert=True)
        return

    await callback.answer()
    users_count = await repository.get_total_users_count()
    await state.clear()
    await state.set_state(BroadcastSG.waiting_for_text)

    text = (
        f"📨 <b>Broadcast to All Users</b>\n\n"
        f"There are currently <b>{users_count}</b> registered user(s) in the database.\n\n"
        "Please type the message you would like to broadcast to everyone:\n"
        "<i>(Type /cancel to abort at any time)</i>"
    )

    if callback.message:
        await callback.message.edit_text(text=text, parse_mode="HTML")


@router.message(BroadcastSG.waiting_for_text)
async def process_broadcast_text(message: Message, state: FSMContext, repository: Repository) -> None:
    broadcast_text = (message.text or "").strip()
    if len(broadcast_text) < 5:
        await message.answer("⚠️ Broadcast message must be at least 5 characters. Try again:")
        return

    users_count = await repository.get_total_users_count()
    await state.update_data(text=broadcast_text)
    await state.set_state(BroadcastSG.confirming)

    preview_text = (
        "⚠️ <b>CONFIRM BROADCAST</b>\n\n"
        f"Recipient count: <b>{users_count}</b> user(s)\n\n"
        "<b>Message Preview:</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"{broadcast_text}\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "Are you absolutely sure you want to broadcast this message now?"
    )

    await message.answer(
        text=preview_text,
        parse_mode="HTML",
        reply_markup=get_broadcast_confirmation_keyboard(),
    )


@router.callback_query(F.data == "admin_broadcast_cancel", BroadcastSG.confirming)
async def callback_cancel_broadcast(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer("Broadcast cancelled.", show_alert=False)
    if callback.message:
        await callback.message.edit_text(
            "❌ Broadcast cancelled. No messages were sent.",
            reply_markup=get_admin_menu_keyboard(),
        )


@router.callback_query(F.data == "admin_broadcast_confirm", BroadcastSG.confirming)
async def callback_confirm_broadcast(
    callback: CallbackQuery,
    state: FSMContext,
    notification_service: NotificationService,
) -> None:
    user = callback.from_user
    if not user or not settings.is_admin(user.id):
        await callback.answer("Access denied.", show_alert=True)
        return

    data = await state.get_data()
    broadcast_text = data.get("text", "")
    await state.clear()

    await callback.answer("Broadcasting in progress...", show_alert=False)

    if callback.message:
        await callback.message.edit_text("⏳ <i>Sending broadcast... Please wait...</i>", parse_mode="HTML")

    result = await notification_service.broadcast_message(
        sender_id=user.id,
        text=broadcast_text,
    )

    report_text = (
        "✅ <b>Broadcast Completed!</b>\n\n"
        f"• Total Targets: {result['total']}\n"
        f"• Successfully Delivered: <b>{result['sent']}</b>\n"
        f"• Failed/Blocked: <b>{result['failed']}</b>\n"
    )

    if callback.message:
        await callback.message.edit_text(
            text=report_text,
            parse_mode="HTML",
            reply_markup=get_admin_menu_keyboard(),
        )
