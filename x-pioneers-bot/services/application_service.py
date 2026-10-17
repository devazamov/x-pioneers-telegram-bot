"""Service layer for team applications validation and processing."""

from __future__ import annotations

from typing import Optional, Tuple
from database.models import TeamApplication
from database.repository import Repository


class ApplicationService:
    def __init__(self, repository: Repository) -> None:
        self.repo = repository

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, Optional[str]]:
        clean = name.strip()
        if len(clean) < 2:
            return False, "Please enter a valid name (at least 2 characters)."
        if len(clean) > 80:
            return False, "Name is too long (maximum 80 characters)."
        return True, None

    @staticmethod
    def validate_interest(interest: str) -> Tuple[bool, Optional[str]]:
        clean = interest.strip()
        if len(clean) < 3:
            return False, "Please provide a little more detail about your area of interest (at least 3 characters)."
        if len(clean) > 200:
            return False, "Interest text is too long (maximum 200 characters)."
        return True, None

    @staticmethod
    def validate_skills(skills: str) -> Tuple[bool, Optional[str]]:
        clean = skills.strip()
        if len(clean) < 3:
            return False, "Please share some of your skills, tech stack, or experience (at least 3 characters)."
        if len(clean) > 500:
            return False, "Skills description is too long (maximum 500 characters)."
        return True, None

    @staticmethod
    def validate_motivation(motivation: str) -> Tuple[bool, Optional[str]]:
        clean = motivation.strip()
        if len(clean) < 5:
            return False, "Please explain briefly why you want to join X PIONEERS (at least 5 characters)."
        if len(clean) > 1000:
            return False, "Motivation is too long (maximum 1000 characters)."
        return True, None

    @staticmethod
    def format_review(data: dict) -> str:
        """Formats application data for the applicant review screen."""
        return (
            "📋 <b>Review Your Application:</b>\n\n"
            f"👤 <b>Name:</b> {data.get('name', 'N/A')}\n"
            f"🎯 <b>Area of Interest:</b> {data.get('interest', 'N/A')}\n"
            f"🛠 <b>Skills & Experience:</b>\n{data.get('skills', 'N/A')}\n\n"
            f"💡 <b>Why X PIONEERS:</b>\n{data.get('motivation', 'N/A')}\n\n"
            "<i>Please review your information carefully before submitting.</i>"
        )

    async def submit_application(
        self,
        user_id: int,
        username: Optional[str],
        data: dict,
    ) -> int:
        """Saves a validated application to the database."""
        app_id = await self.repo.add_application(
            user_id=user_id,
            username=username,
            full_name=data["name"],
            interest=data["interest"],
            skills=data["skills"],
            motivation=data["motivation"],
        )
        await self.repo.log_event(
            event_type="application_submitted",
            user_id=user_id,
            details=f"App ID {app_id} submitted by @{username or user_id}",
        )
        return app_id
