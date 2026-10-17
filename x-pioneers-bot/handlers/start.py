"""Start, Help, and Navigation callback handlers."""

from __future__ import annotations

import logging
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import settings
from database.repository import Repository
from keyboards.main_menu import get_back_to_main_keyboard, get_main_menu_keyboard

logger = logging.getLogger("xpioneers.handlers.start")
router = Router(name="start_router")


WELCOME_TEXT = (
    "🚀 <b>Welcome to X PIONEERS!</b>\n\n"
    "We are a team of young innovators exploring AI, software development, "
    "educational technology, and future technologies.\n\n"
    "💡 <i>One Team. One Vision. A Bigger Future.</i>\n\n"
    "Explore our community, projects, and latest updates below:"
)

HELP_TEXT = (
    "ℹ️ <b>X PIONEERS Bot Commands</b>\n\n"
    "/start — Open the main interactive menu\n"
    "/about — Learn about our team, vision, and leadership\n"
    "/projects — Discover our projects including MAKTAB X\n"
    "/news — Read latest announcements and team milestones\n"
    "/cancel — Cancel any active form or conversation\n"
    "/help — Show this help message\n\n"
    "<i>Authorized administrators can access /admin</i>"
)


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext, repository: Repository) -> None:
    """Handles the /start command."""
    await state.clear()

    user = message.from_user
    if user:
        await repository.upsert_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        await repository.log_event("command_start", user.id, f"User {user.id} opened bot")

    await message.answer(
        text=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard(),
    )


@router.message(Command("help"))
async def command_help(message: Message) -> None:
    """Handles the /help command."""
    await message.answer(
        text=HELP_TEXT,
        parse_mode="HTML",
        reply_markup=get_back_to_main_keyboard(),
    )


@router.callback_query(F.data == "nav_back_main")
async def callback_back_to_main(callback: CallbackQuery, state: FSMContext) -> None:
    """Returns the user to the main menu from any section."""
    await state.clear()
    await callback.answer()

    if callback.message:
        try:
            await callback.message.edit_text(
                text=WELCOME_TEXT,
                parse_mode="HTML",
                reply_markup=get_main_menu_keyboard(),
            )
        except Exception:
            # If message cannot be edited (e.g. content identical), re-send
            await callback.message.answer(
                text=WELCOME_TEXT,
                parse_mode="HTML",
                reply_markup=get_main_menu_keyboard(),
            )


@router.callback_query(F.data == "nav_channel_info")
async def callback_channel_info(callback: CallbackQuery) -> None:
    """Shown when official channel URL is not yet configured."""
    await callback.answer(
        text="Channel link coming soon! The official channel is currently being prepared.",
        show_alert=True,
    )
