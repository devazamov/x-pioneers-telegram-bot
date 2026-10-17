"""Projects section handlers and dynamic catalog views."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from config import PROJECTS_CATALOG
from keyboards.projects import get_project_detail_keyboard, get_projects_menu_keyboard

router = Router(name="projects_router")

PROJECTS_INTRO = (
    "🚀 <b>X PIONEERS Projects</b>\n\n"
    "We believe in building impactful, working technologies that empower students "
    "and developers. Here are our current initiatives and active tracks:\n\n"
    "Select any project below to view its details and development status:"
)


@router.message(Command("projects"))
async def command_projects(message: Message) -> None:
    await message.answer(
        text=PROJECTS_INTRO,
        parse_mode="HTML",
        reply_markup=get_projects_menu_keyboard(),
    )


@router.callback_query(F.data == "nav_projects")
async def callback_projects_menu(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message:
        await callback.message.edit_text(
            text=PROJECTS_INTRO,
            parse_mode="HTML",
            reply_markup=get_projects_menu_keyboard(),
        )


@router.callback_query(F.data.startswith("proj_view:"))
async def callback_project_detail(callback: CallbackQuery) -> None:
    await callback.answer()
    if not callback.data:
        return

    project_id = callback.data.split(":", 1)[1]
    project = next((p for p in PROJECTS_CATALOG if p.id == project_id), None)

    if not project:
        if callback.message:
            await callback.message.edit_text(
                "⚠️ <i>Project not found or moved.</i>",
                reply_markup=get_projects_menu_keyboard(),
            )
        return

    features_str = "\n".join(f"• {f}" for f in project.key_features)
    text = (
        f"🚀 <b>{project.name}</b>\n"
        f"<i>{project.tagline}</i>\n\n"
        f"📊 <b>Status:</b> <code>{project.status}</code>\n\n"
        f"📝 <b>Overview:</b>\n{project.description}\n\n"
        f"✨ <b>Key Highlights:</b>\n{features_str}\n"
    )

    if callback.message:
        await callback.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=get_project_detail_keyboard(),
        )
