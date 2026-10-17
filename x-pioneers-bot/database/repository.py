"""Repository pattern for database operations."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import aiosqlite

from database.db import DatabaseManager
from database.models import BotEvent, NewsPost, TeamApplication, User


class Repository:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager

    # ---------------- USER OPERATIONS ----------------
    async def upsert_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> None:
        async with self.db.connect() as conn:
            await conn.execute(
                """
                INSERT INTO users (user_id, username, first_name, last_name, last_active_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET
                    username = excluded.username,
                    first_name = excluded.first_name,
                    last_name = excluded.last_name,
                    last_active_at = CURRENT_TIMESTAMP
                """,
                (user_id, username, first_name, last_name),
            )
            await conn.commit()

    async def get_user(self, user_id: int) -> Optional[User]:
        async with self.db.connect() as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(
                "SELECT user_id, username, first_name, last_name, joined_at, last_active_at FROM users WHERE user_id = ?",
                (user_id,),
            )
            row = await cursor.fetchone()
            if not row:
                return None
            return User(
                user_id=row["user_id"],
                username=row["username"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                joined_at=str(row["joined_at"]),
                last_active_at=str(row["last_active_at"]),
            )

    async def get_all_users(self) -> List[User]:
        async with self.db.connect() as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(
                "SELECT user_id, username, first_name, last_name, joined_at, last_active_at FROM users ORDER BY joined_at DESC"
            )
            rows = await cursor.fetchall()
            return [
                User(
                    user_id=r["user_id"],
                    username=r["username"],
                    first_name=r["first_name"],
                    last_name=r["last_name"],
                    joined_at=str(r["joined_at"]),
                    last_active_at=str(r["last_active_at"]),
                )
                for r in rows
            ]

    async def get_total_users_count(self) -> int:
        async with self.db.connect() as conn:
            cursor = await conn.execute("SELECT COUNT(*) FROM users")
            row = await cursor.fetchone()
            return row[0] if row else 0

    # ---------------- NEWS OPERATIONS ----------------
    async def add_news(
        self,
        title: str,
        text: str,
        author_id: int,
        author_name: str,
    ) -> int:
        async with self.db.connect() as conn:
            cursor = await conn.execute(
                """
                INSERT INTO news (title, text, author_id, author_name)
                VALUES (?, ?, ?, ?)
                """,
                (title.strip(), text.strip(), author_id, author_name.strip()),
            )
            await conn.commit()
            return cursor.lastrowid or 0

    async def get_latest_news(self, limit: int = 5, offset: int = 0) -> List[NewsPost]:
        async with self.db.connect() as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(
                """
                SELECT id, title, text, author_id, author_name, created_at
                FROM news
                ORDER BY created_at DESC, id DESC
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            )
            rows = await cursor.fetchall()
            return [
                NewsPost(
                    id=r["id"],
                    title=r["title"],
                    text=r["text"],
                    author_id=r["author_id"],
                    author_name=r["author_name"],
                    created_at=str(r["created_at"]),
                )
                for r in rows
            ]

    async def get_news_by_id(self, news_id: int) -> Optional[NewsPost]:
        async with self.db.connect() as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(
                "SELECT id, title, text, author_id, author_name, created_at FROM news WHERE id = ?",
                (news_id,),
            )
            row = await cursor.fetchone()
            if not row:
                return None
            return NewsPost(
                id=row["id"],
                title=row["title"],
                text=row["text"],
                author_id=row["author_id"],
                author_name=row["author_name"],
                created_at=str(row["created_at"]),
            )

    async def get_news_count(self) -> int:
        async with self.db.connect() as conn:
            cursor = await conn.execute("SELECT COUNT(*) FROM news")
            row = await cursor.fetchone()
            return row[0] if row else 0

    # ---------------- APPLICATION OPERATIONS ----------------
    async def add_application(
        self,
        user_id: int,
        username: Optional[str],
        full_name: str,
        interest: str,
        skills: str,
        motivation: str,
    ) -> int:
        async with self.db.connect() as conn:
            cursor = await conn.execute(
                """
                INSERT INTO team_applications (user_id, username, full_name, interest, skills, motivation, status)
                VALUES (?, ?, ?, ?, ?, ?, 'pending')
                """,
                (
                    user_id,
                    username,
                    full_name.strip(),
                    interest.strip(),
                    skills.strip(),
                    motivation.strip(),
                ),
            )
            await conn.commit()
            return cursor.lastrowid or 0

    async def get_application(self, application_id: int) -> Optional[TeamApplication]:
        async with self.db.connect() as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(
                """
                SELECT id, user_id, username, full_name, interest, skills, motivation, status, created_at
                FROM team_applications
                WHERE id = ?
                """,
                (application_id,),
            )
            row = await cursor.fetchone()
            if not row:
                return None
            return TeamApplication(
                id=row["id"],
                user_id=row["user_id"],
                username=row["username"],
                full_name=row["full_name"],
                interest=row["interest"],
                skills=row["skills"],
                motivation=row["motivation"],
                status=row["status"],
                created_at=str(row["created_at"]),
            )

    async def get_all_applications(self, limit: int = 20, offset: int = 0) -> List[TeamApplication]:
        async with self.db.connect() as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(
                """
                SELECT id, user_id, username, full_name, interest, skills, motivation, status, created_at
                FROM team_applications
                ORDER BY created_at DESC, id DESC
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            )
            rows = await cursor.fetchall()
            return [
                TeamApplication(
                    id=r["id"],
                    user_id=r["user_id"],
                    username=r["username"],
                    full_name=r["full_name"],
                    interest=r["interest"],
                    skills=r["skills"],
                    motivation=r["motivation"],
                    status=r["status"],
                    created_at=str(r["created_at"]),
                )
                for r in rows
            ]

    async def get_applications_count(self) -> int:
        async with self.db.connect() as conn:
            cursor = await conn.execute("SELECT COUNT(*) FROM team_applications")
            row = await cursor.fetchone()
            return row[0] if row else 0

    async def update_application_status(self, application_id: int, status: str) -> bool:
        async with self.db.connect() as conn:
            cursor = await conn.execute(
                "UPDATE team_applications SET status = ? WHERE id = ?",
                (status, application_id),
            )
            await conn.commit()
            return cursor.rowcount > 0

    # ---------------- BOT EVENTS / STATS ----------------
    async def log_event(
        self,
        event_type: str,
        user_id: Optional[int] = None,
        details: Optional[str] = None,
    ) -> None:
        async with self.db.connect() as conn:
            await conn.execute(
                "INSERT INTO bot_events (event_type, user_id, details) VALUES (?, ?, ?)",
                (event_type, user_id, details),
            )
            await conn.commit()

    async def get_stats(self) -> Dict[str, Any]:
        async with self.db.connect() as conn:
            c1 = await conn.execute("SELECT COUNT(*) FROM users")
            users_count = (await c1.fetchone())[0]

            c2 = await conn.execute("SELECT COUNT(*) FROM team_applications")
            apps_count = (await c2.fetchone())[0]

            c3 = await conn.execute("SELECT COUNT(*) FROM team_applications WHERE status = 'pending'")
            pending_apps = (await c3.fetchone())[0]

            c4 = await conn.execute("SELECT COUNT(*) FROM news")
            news_count = (await c4.fetchone())[0]

            c5 = await conn.execute("SELECT COUNT(*) FROM bot_events")
            events_count = (await c5.fetchone())[0]

            return {
                "total_users": users_count,
                "total_applications": apps_count,
                "pending_applications": pending_apps,
                "total_news": news_count,
                "total_events": events_count,
            }
