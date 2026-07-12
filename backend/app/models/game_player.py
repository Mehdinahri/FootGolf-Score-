"""
Modèle GamePlayer — Inscriptions des joueurs aux parties.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class RegistrationStatus(str, enum.Enum):
    """Statut de l'inscription d'un joueur."""

    REGISTERED = "REGISTERED"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    FINISHED = "FINISHED"


class AttendanceStatus(str, enum.Enum):
    """Statut de présence."""

    PRESENT = "PRESENT"
    ABSENT = "ABSENT"


class GamePlayer(Base):
    """Table `game_players`."""

    __tablename__ = "game_players"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(
        UUID(as_uuid=True),
        ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    registered_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    status = Column(
        SAEnum(RegistrationStatus, name="registration_status", create_constraint=True),
        nullable=False,
        default=RegistrationStatus.REGISTERED,
    )
    start_order = Column(Integer, nullable=True)
    attendance = Column(
        SAEnum(AttendanceStatus, name="attendance_status", create_constraint=True),
        nullable=True,
    )
    cancelled_at = Column(DateTime(timezone=True), nullable=True)

    # ── Relations ───────────────────────────────────────────────
    game = relationship("Game", back_populates="players")
    user = relationship("User", back_populates="game_registrations")

    # ── Contraintes ─────────────────────────────────────────────
    __table_args__ = (
        UniqueConstraint("game_id", "user_id", name="uq_game_player"),
    )

    @property
    def is_active(self) -> bool:
        """L'inscription est active (non annulée)."""
        return self.status not in (
            RegistrationStatus.CANCELLED,
            RegistrationStatus.ABSENT,
        )

    def __repr__(self) -> str:
        return f"<GamePlayer game={self.game_id} user={self.user_id} ({self.status.value})>"
