"""
Schémas Pydantic — Parties.
"""

from __future__ import annotations

from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.game import GameStatus, TiebreakerRule
from app.schemas.course import CourseBrief
from app.schemas.user import UserBrief


class GameCreate(BaseModel):
    """Création d'une partie."""

    title: str = Field(..., min_length=1, max_length=200)
    course_id: UUID
    start_date: date
    start_time: time | None = None
    max_players: int = Field(default=5, ge=1, le=5)
    description: str | None = None
    marker_id: UUID | None = None
    tiebreaker_rule: TiebreakerRule = TiebreakerRule.STANDARD


class GameUpdate(BaseModel):
    """Modification d'une partie (DRAFT ou REGISTRATION_OPEN)."""

    title: str | None = Field(None, min_length=1, max_length=200)
    start_date: date | None = None
    start_time: time | None = None
    description: str | None = None
    marker_id: UUID | None = None
    max_players: int | None = Field(None, ge=1, le=5)


class GameResponse(BaseModel):
    """Partie renvoyée par l'API."""

    id: UUID
    title: str
    course_id: UUID
    organizer_id: UUID
    marker_id: UUID | None = None
    start_date: date
    start_time: time | None = None
    max_players: int
    registered_count: int
    status: GameStatus
    description: str | None = None
    tiebreaker_rule: TiebreakerRule
    registration_open_at: datetime | None = None
    registration_close_at: datetime | None = None
    actual_start_at: datetime | None = None
    actual_end_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    # Relations optionnelles (populées si demandées)
    course: CourseBrief | None = None
    organizer: UserBrief | None = None

    model_config = ConfigDict(from_attributes=True)


class GameBrief(BaseModel):
    """Version allégée d'une partie pour les listes."""

    id: UUID
    title: str
    start_date: date
    start_time: time | None = None
    status: GameStatus
    registered_count: int
    max_players: int
    course_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
