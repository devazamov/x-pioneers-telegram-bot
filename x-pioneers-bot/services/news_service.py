"""News and announcement service."""

from __future__ import annotations

from typing import List, Optional
from database.models import NewsPost
from database.repository import Repository


class NewsService:
    def __init__(self, repository: Repository) -> None:
        self.repo = repository

    async def get_news_display(self, limit: int = 5, offset: int = 0) -> str:
        """Returns formatted string of latest announcements or friendly empty state."""
        news_items = await self.repo.get_latest_news(limit=limit, offset=offset)

        if not news_items:
            return (
                "📰 <b>Latest News & Announcements</b>\n\n"
                "<i>No announcements have been published yet.</i>\n\n"
                "Our team is actively building MAKTAB X and core AI initiatives. "
                "Official updates and milestones will be announced right here! 🚀"
            )

        total_count = await self.repo.get_news_count()
        parts = [
            f"📰 <b>Latest News & Announcements</b> <i>({min(len(news_items), total_count)} of {total_count})</i>\n"
        ]

        for item in news_items:
            date_str = item.created_at[:16] if item.created_at else "Recently"
            parts.append(
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"📌 <b>{item.title}</b>\n"
                f"📅 <i>{date_str}</i> | ✍️ <i>{item.author_name}</i>\n\n"
                f"{item.text}\n"
            )

        return "\n".join(parts)

    async def publish_news(
        self,
        title: str,
        text: str,
        author_id: int,
        author_name: str,
    ) -> int:
        post_id = await self.repo.add_news(
            title=title,
            text=text,
            author_id=author_id,
            author_name=author_name,
        )
        await self.repo.log_event(
            event_type="news_published",
            user_id=author_id,
            details=f"News ID {post_id}: '{title[:40]}'",
        )
        return post_id
