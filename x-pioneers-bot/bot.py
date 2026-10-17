"""Main entry point for X PIONEERS Official Telegram Bot.

Runs polling with aiogram 3.x, sets up dependency injection,
initializes SQLite tables, registers bot commands, and handles graceful shutdown.
"""

from __future__ import annotations

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import settings
from database.db import DatabaseManager
from database.repository import Repository
from handlers import register_all_routers
from services.application_service import ApplicationService
from services.news_service import NewsService
from services.notification_service import NotificationService

# Configure clean logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("xpioneers")


async def setup_bot_commands(bot: Bot) -> None:
    """Registers standard bot commands with the Telegram API."""
    commands = [
        BotCommand(command="start", description="🚀 Open main interactive menu"),
        BotCommand(command="about", description="👥 Team mission, tech stack & leadership"),
        BotCommand(command="projects", description="🚀 Discover MAKTAB X & active tracks"),
        BotCommand(command="news", description="📰 Read official announcements"),
        BotCommand(command="join", description="🤝 Apply to join X PIONEERS"),
        BotCommand(command="contact", description="📬 Contact founder and admins"),
        BotCommand(command="cancel", description="❌ Cancel current conversation or form"),
        BotCommand(command="help", description="ℹ️ Show help and command overview"),
    ]
    try:
        await bot.set_my_commands(commands)
        logger.info("Bot commands successfully registered with Telegram.")
    except Exception as e:
        logger.warning("Could not set bot commands: %s", e)


async def main() -> None:
    """Initializes and runs the bot."""
    logger.info("Starting %s (%s)...", settings.BOT_NAME, settings.BOT_USERNAME)

    # Validate settings before attempting to connect
    try:
        settings.validate_runtime()
    except ValueError as err:
        logger.critical("Configuration Error: %s", err)
        sys.exit(1)

    # Initialize SQLite Database
    db_manager = DatabaseManager(settings.DATABASE_PATH)
    await db_manager.init_db()

    # Initialize Repositories and Services
    repository = Repository(db_manager)
    application_service = ApplicationService(repository)
    news_service = NewsService(repository)

    # Initialize Bot & Dispatcher
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    notification_service = NotificationService(bot=bot, repository=repository)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Provide services to handlers via workflow data (dependency injection)
    dp["repository"] = repository
    dp["application_service"] = application_service
    dp["news_service"] = news_service
    dp["notification_service"] = notification_service

    # Register handlers
    register_all_routers(dp)

    # Setup command suggestions
    await setup_bot_commands(bot)

    logger.info("Bot is ready. Starting polling loop...")
    try:
        # Drop pending updates so old messages while offline don't cause spam
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot session closed. Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user.")
