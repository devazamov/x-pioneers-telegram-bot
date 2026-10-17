"""Configuration module for X PIONEERS Telegram Bot.

Loads environment variables, project definitions, and role authorizations.
All sensitive credentials are read strictly from the environment.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load .env file from project root
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _parse_id(val: Optional[str]) -> Optional[int]:
    if not val:
        return None
    try:
        return int(val.strip())
    except ValueError:
        return None


def _parse_id_list(val: Optional[str]) -> List[int]:
    if not val:
        return []
    ids: List[int] = []
    for item in val.split(","):
        cleaned = item.strip()
        if cleaned.isdigit():
            ids.append(int(cleaned))
    return ids


@dataclass(frozen=True)
class ProjectInfo:
    id: str
    name: str
    tagline: str
    status: str
    description: str
    key_features: List[str]


# Static project catalog - can be updated without rewriting handlers
PROJECTS_CATALOG: List[ProjectInfo] = [
    ProjectInfo(
        id="maktab_x",
        name="MAKTAB X",
        tagline="Interactive Educational Platform & 3D Learning World",
        status="In development",
        description=(
            "MAKTAB X is the flagship initiative of X PIONEERS. It bridges modern 3D "
            "gamification with core school curricula, empowering students to visualize "
            "abstract science and math concepts in an immersive spatial environment."
        ),
        key_features=[
            "Interactive 3D science & physics lab simulations",
            "Gamified progress tracking & mastery quests",
            "Adaptive digital textbook integration",
            "Designed for accessibility on low-spec hardware",
        ],
    ),
    ProjectInfo(
        id="ai_dev",
        name="AI & Software Development",
        tagline="Intelligent Tools, Automation & Applied ML",
        status="Active research & prototyping",
        description=(
            "Research and engineering group building practical software solutions, "
            "intelligent developer tools, and open-source utilities tailored for "
            "modern development workflows."
        ),
        key_features=[
            "Practical AI assistant integrations",
            "Internal workflow automations",
            "Open-source utilities and bot infrastructure",
            "Collaborative engineering standards",
        ],
    ),
    ProjectInfo(
        id="future_projects",
        name="Future Projects",
        tagline="Next-Gen Technology Initiatives",
        status="Planned / Conceptual",
        description=(
            "Long-term exploratory tracks assessing robotics, decentralized computing, "
            "and cross-platform student collaboration tools."
        ),
        key_features=[
            "Hardware & IoT experimentation",
            "Community hackathon initiatives",
            "Mentorship & incubation for young innovators",
        ],
    ),
]


@dataclass
class Settings:
    # Bot identity
    BOT_NAME: str = "X PIONEERS | Official"
    BOT_USERNAME: str = "@XPioneersOfficialBot"
    FOUNDER_USERNAME: str = "@devazamov"
    ASSISTANT_USERNAME: str = "@xvoid11"
    SLOGAN: str = "One Team. One Vision. A Bigger Future."
    MISSION: str = (
        "Build a professional technology community focused on AI, "
        "software development, educational technology, and innovative projects."
    )

    # API and Environment
    BOT_TOKEN: str = field(default_factory=lambda: os.getenv("BOT_TOKEN", "").strip())
    FOUNDER_ID: Optional[int] = field(default_factory=lambda: _parse_id(os.getenv("FOUNDER_ID")))
    ASSISTANT_ADMIN_ID: Optional[int] = field(default_factory=lambda: _parse_id(os.getenv("ASSISTANT_ADMIN_ID")))
    EXTRA_ADMIN_IDS: List[int] = field(default_factory=lambda: _parse_id_list(os.getenv("EXTRA_ADMIN_IDS")))

    # Official channel (None if not provided or empty)
    CHANNEL_URL: Optional[str] = field(
        default_factory=lambda: (os.getenv("CHANNEL_URL") or "").strip() or None
    )

    # Database
    DATABASE_PATH: Path = field(
        default_factory=lambda: BASE_DIR / (os.getenv("DATABASE_FILE", "xpioneers.db").strip())
    )

    def get_all_admin_ids(self) -> List[int]:
        """Returns unique list of authorized admin IDs."""
        admins: List[int] = []
        if self.FOUNDER_ID is not None:
            admins.append(self.FOUNDER_ID)
        if self.ASSISTANT_ADMIN_ID is not None:
            admins.append(self.ASSISTANT_ADMIN_ID)
        for extra in self.EXTRA_ADMIN_IDS:
            if extra not in admins:
                admins.append(extra)
        return admins

    def is_admin(self, user_id: Optional[int]) -> bool:
        """Role-based authorization by Telegram numeric ID."""
        if user_id is None:
            return False
        return user_id in self.get_all_admin_ids()

    def is_founder(self, user_id: Optional[int]) -> bool:
        if user_id is None:
            return False
        return user_id == self.FOUNDER_ID

    def validate_runtime(self) -> None:
        """Validate required configuration before running bot polling."""
        if not self.BOT_TOKEN or self.BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
            raise ValueError(
                "BOT_TOKEN is missing or has default placeholder in .env file! "
                "Please obtain a token from @BotFather and set BOT_TOKEN=... in your .env file."
            )
        if self.FOUNDER_ID is None:
            import logging
            logging.getLogger("xpioneers").warning(
                "FOUNDER_ID is not configured in .env. Admin commands will be locked until set."
            )


settings = Settings()
