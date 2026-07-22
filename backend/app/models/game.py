"""
Modèle Game — Parties de FootGolf.

Machine à états :
    DRAFT → REGISTRATION_OPEN → FULL | REGISTRATION_CLOSED → IN_PROGRESS → FINISHED
    (tout sauf FINISHED/CANCELLED → CANCELLED)
"""

from __future__ import annotations

import enum
import uuid
from datetime import date, datetime, time

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class GameStatus(str, enum.Enum):
    """Statuts possibles d'une partie."""

    DRAFT = "DRAFT"
    REGISTRATION_OPEN = "REGISTRATION_OPEN"
    FULL = "FULL"
    REGISTRATION_CLOSED = "REGISTRATION_CLOSED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"


class TiebreakerRule(str, enum.Enum):
    """Règles de départage."""

    STANDARD = "STANDARD"  # retour → 6 derniers → 3 derniers → trou 18


# Transitions autorisées : {état_actuel: [états_possibles]}
VALID_TRANSITIONS: dict[GameStatus, list[GameStatus]] = {
    GameStatus.DRAFT: [GameStatus.REGISTRATION_OPEN, GameStatus.CANCELLED],
    GameStatus.REGISTRATION_OPEN: [
        GameStatus.FULL,
        GameStatus.REGISTRATION_CLOSED,
        GameStatus.IN_PROGRESS,
        GameStatus.CANCELLED,
    ],
    GameStatus.FULL: [
        GameStatus.REGISTRATION_CLOSED,
        GameStatus.IN_PROGRESS,
        GameStatus.CANCELLED
    ],
    GameStatus.REGISTRATION_CLOSED: [GameStatus.IN_PROGRESS, GameStatus.CANCELLED],
    GameStatus.IN_PROGRESS: [GameStatus.FINISHED, GameStatus.CANCELLED],
    GameStatus.FINISHED: [],
    GameStatus.CANCELLED: [],
}


class Game(Base):
    """Table `games`."""

    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    course_id = Column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="RESTRICT"),
        nullable=False,
    )
    organizer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    marker_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    start_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=True)
    max_players = Column(Integer, nullable=False, default=5)
    registered_count = Column(Integer, nullable=False, default=0)
    status = Column(
        SAEnum(GameStatus, name="game_status", create_constraint=True),
        nullable=False,
        default=GameStatus.DRAFT,
        index=True,
    )
    description = Column(Text, nullable=True)
    tiebreaker_rule = Column(
        SAEnum(TiebreakerRule, name="tiebreaker_rule", create_constraint=True),
        nullable=False,
        default=TiebreakerRule.STANDARD,
    )
    registration_open_at = Column(DateTime(timezone=True), nullable=True)
    registration_close_at = Column(DateTime(timezone=True), nullable=True)
    actual_start_at = Column(DateTime(timezone=True), nullable=True)
    actual_end_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ── Relations ───────────────────────────────────────────────
    course = relationship("Course", back_populates="games")
    organizer = relationship(
        "User", back_populates="organized_games", foreign_keys=[organizer_id]
    )
    marker = relationship(
        "User", back_populates="marked_games", foreign_keys=[marker_id]
    )
    players = relationship(
        "GamePlayer", back_populates="game", cascade="all, delete-orphan"
    )
    scores = relationship("Score", back_populates="game", cascade="all, delete-orphan")

    # ── Contraintes ─────────────────────────────────────────────
    __table_args__ = (
        CheckConstraint(
            "max_players >= 1 AND max_players <= 5",
            name="ck_game_max_players_range",
        ),
        CheckConstraint(
            "registered_count >= 0 AND registered_count <= max_players",
            name="ck_game_registered_count_range",
        ),
    )

    # ── Helpers ─────────────────────────────────────────────────

    def can_transition_to(self, new_status: GameStatus) -> bool:
        """Vérifie si la transition de statut est autorisée."""
        return new_status in VALID_TRANSITIONS.get(self.status, [])

    @property
    def is_registration_open(self) -> bool:
        return self.status == GameStatus.REGISTRATION_OPEN

    @property
    def is_full(self) -> bool:
        return self.registered_count >= self.max_players

    @property
    def is_in_progress(self) -> bool:
        return self.status == GameStatus.IN_PROGRESS

    @property
    def is_finished(self) -> bool:
        return self.status == GameStatus.FINISHED

    @property
    def available_spots(self) -> int:
        return max(0, self.max_players - self.registered_count)

    def __repr__(self) -> str:
        return f"<Game {self.title} ({self.status.value})>"
