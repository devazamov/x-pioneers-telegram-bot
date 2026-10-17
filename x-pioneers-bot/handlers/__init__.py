"""Handlers package."""

from aiogram import Dispatcher

from handlers.about import router as about_router
from handlers.admin import router as admin_router
from handlers.applications import router as applications_router
from handlers.contact import router as contact_router
from handlers.news import router as news_router
from handlers.projects import router as projects_router
from handlers.start import router as start_router


def register_all_routers(dp: Dispatcher) -> None:
    """Registers all feature routers to the main aiogram Dispatcher."""
    dp.include_router(start_router)
    dp.include_router(about_router)
    dp.include_router(projects_router)
    dp.include_router(news_router)
    dp.include_router(applications_router)
    dp.include_router(contact_router)
    dp.include_router(admin_router)
