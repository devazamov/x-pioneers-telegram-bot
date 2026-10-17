"""Notification and broadcast service for admins and users."""

from __future__ import annotations

import asyncio
import logging
from typing import Dict, List, Optional
from aiogram import Bot
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError

from config import settings
from database.repository import Repository

logger = logging.getLogger("xpioneers.notifications")


class NotificationService:
    def __init__(self, bot: Bot, repository: Repository) -> None:
        self.bot = bot
        self.repo = repository

    async def notify_admins_new_application(
        self,
        app_id: int,
        applicant_id: int,
        username: Optional[str],
        data: dict,
    ) -> None:
        """Sends immediate alert to founder and assistant admin when someone applies."""
        admin_ids = settings.get_all_admin_ids()
        if not admin_ids:
            logger.warning("No admin IDs configured to receive application notification.")
            return

        username_display = f"@{username}" if username else f"ID: {applicant_id}"
        message_text = (
            f"🔔 <b>New Team Application Received!</b>\n\n"
            f"<b>Application ID:</b> #{app_id}\n"
            f"<b>Applicant:</b> {data.get('name')} ({username_display})\n"
            f"<b>User ID:</b> <code>{applicant_id}</code>\n"
            f"<b>Interest:</b> {data.get('interest')}\n\n"
            f"<b>Skills:</b>\n{data.get('skills')}\n\n"
            f"<b>Motivation:</b>\n{data.get('motivation')}\n\n"
            f"<i>Review in /admin -> Applications</i>"
        )

        for admin_id in admin_ids:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=message_text,
                    parse_mode="HTML",
                )
            except Exception as e:
                logger.warning("Could not send admin notification to %s: %s", admin_id, e)

    async def broadcast_message(
        self,
        sender_id: int,
        text: str,
    ) -> Dict[str, int]:
        """Broadcasts text to all registered users safely with delay to respect rate limits."""
        users = await self.repo.get_all_users()
        sent = 0
        failed = 0

        logger.info("Admin %s initiated broadcast to %d users", sender_id, len(users))

        for user in users:
            try:
                await self.bot.send_message(
                    chat_id=user.user_id,
                    text=f"📢 <b>Announcement from X PIONEERS:</b>\n\n{text}",
                    parse_mode="HTML",
                )
                sent += 1
                await asyncio.sleep(0.05)  # Telegram rate limit buffer (~20 msgs/sec max)
            except TelegramForbiddenError:
                failed += 1
                logger.debug("User %s blocked the bot", user.user_id)
            except TelegramAPIError as e:
                failed += 1
                logger.warning("Failed to send broadcast to %s: %s", user.user_id, e)
            except Exception as e:
                failed += 1
                logger.error("Unexpected error broadcasting to %s: %s", user.user_id, e)

        await self.repo.log_event(
            event_type="broadcast_sent",
            user_id=sender_id,
            details=f"Broadcast sent: {sent} succeeded, {failed} failed",
        )

        return {"total": len(users), "sent": sent, "failed": failed}
