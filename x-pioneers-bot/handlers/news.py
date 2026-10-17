"""Latest news handlers."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards.main_menu import get_back_to_main_keyboard
from services.news_service import NewsService

router = Router(name="news_router")


@router.message(Command("news"))
async def command_news(message: Message, news_service: NewsService) -> None:
    text = await news_service.get_news_display()
    await message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=get_back_to_main_keyboard(),
    )


@router.callback_query(F.data == "nav_news")
async def callback_news(callback: CallbackQuery, news_service: NewsService) -> None:
    await callback.answer()
    text = await news_service.get_news_display()
    if callback.message:
        await callback.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=get_back_to_main_keyboard(),
        )
