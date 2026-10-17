"""Data models for X PIONEERS SQLite Database."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    joined_at: str
    last_active_at: str


@dataclass
class NewsPost:
    id: int
    title: str
    text: str
    author_id: int
    author_name: str
    created_at: str


@dataclass
class TeamApplication:
    id: int
    user_id: int
    username: Optional[str]
    full_name: str
    interest: str
    skills: str
    motivation: str
    status: str  # 'pending', 'approved', 'rejected'
    created_at: str


@dataclass
class BotEvent:
    id: int
    event_type: str
    user_id: Optional[int]
    details: Optional[str]
    created_at: str
