"""Contact section handlers."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from config import settings
from keyboards.main_menu import get_contact_keyboard

router = Router(name="contact_router")

CONTACT_TEXT = (
    f"📬 <b>Contact X PIONEERS Leadership</b>\n\n"
    "Have questions, partnership inquiries, or ideas you would like to discuss with our team? "
    "Reach out directly to our leadership:\n\n"
    f"👑 <b>Founder & Lead:</b> {settings.FOUNDER_USERNAME}\n"
    f"🛡 <b>Assistant Admin:</b> {settings.ASSISTANT_USERNAME}\n\n"
    "Tap the buttons below to open a direct chat on Telegram:"
)


@router.message(Command("contact"))
async def command_contact(message: Message) -> None:
    await message.answer(
        text=CONTACT_TEXT,
        parse_mode="HTML",
        reply_markup=get_contact_keyboard(),
    )


@router.callback_query(F.data == "nav_contact")
async def callback_contact(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message:
        await callback.message.edit_text(
            text=CONTACT_TEXT,
            parse_mode="HTML",
            reply_markup=get_contact_keyboard(),
        )
