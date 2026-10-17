"""About the Team handlers."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from config import settings
from keyboards.main_menu import get_back_to_main_keyboard

router = Router(name="about_router")

ABOUT_TEXT = (
    f"👥 <b>About {settings.BOT_NAME}</b>\n\n"
    f"💡 <b>Slogan:</b> <i>{settings.SLOGAN}</i>\n\n"
    f"🎯 <b>Mission & Vision:</b>\n"
    f"{settings.MISSION}\n\n"
    "🛠 <b>Main Technology Areas:</b>\n"
    "• <b>AI & Machine Learning:</b> Developing intelligent assistants, agents, and automated tools.\n"
    "• <b>Software Engineering:</b> Full-stack systems, Telegram bots, APIs, and scalable backends.\n"
    "• <b>Educational Technology (EdTech):</b> Interactive, gamified, and 3D learning platforms.\n"
    "• <b>Future Technologies:</b> Exploratory robotics, decentralized tech, and youth innovation.\n\n"
    "🏆 <b>Flagship Project:</b>\n"
    "• <b>MAKTAB X</b> — Interactive educational platform & 3D learning world.\n\n"
    "👑 <b>Leadership:</b>\n"
    f"• <b>Founder & Admin:</b> {settings.FOUNDER_USERNAME}\n"
    f"• <b>Assistant Admin:</b> {settings.ASSISTANT_USERNAME}\n"
)


@router.message(Command("about"))
async def command_about(message: Message) -> None:
    await message.answer(
        text=ABOUT_TEXT,
        parse_mode="HTML",
        reply_markup=get_back_to_main_keyboard(),
    )


@router.callback_query(F.data == "nav_about")
async def callback_about(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message:
        await callback.message.edit_text(
            text=ABOUT_TEXT,
            parse_mode="HTML",
            reply_markup=get_back_to_main_keyboard(),
        )
