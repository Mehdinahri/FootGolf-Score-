"""
Modèle Score — Scores par trou.

Règles :
- strokes ≥ 1
- penalties ≥ 0
- total_score = strokes + penalties  (calculé côté serveur)
- Un seul score par (game, player, hole)
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class ScoreStatus(str, enum.Enum):
    """Statut d'un score."""

    DRAFT = "DRAFT"
    SAVED = "SAVED"
    VALIDATED = "VALIDATED"
    CORRECTED = "CORRECTED"


class Score(Base):
    """Table `scores`."""

    __tablename__ = "scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(
        UUID(as_uuid=True),
        ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    player_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    hole_id = Column(
        UUID(as_uuid=True),
        ForeignKey("holes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    strokes = Column(Integer, nullable=False)
    penalties = Column(Integer, nullable=False, default=0)
    total_score = Column(Integer, nullable=False)  # strokes + penalties
    status = Column(
        SAEnum(ScoreStatus, name="score_status", create_constraint=True),
        nullable=False,
        default=ScoreStatus.DRAFT,
    )
    entered_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    validated_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    comment = Column(Text, nullable=True)
    idempotency_key = Column(
        UUID(as_uuid=True), unique=True, nullable=True
    )
    entered_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    validated_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ── Relations ───────────────────────────────────────────────
    game = relationship("Game", back_populates="scores")
    player = relationship("User", foreign_keys=[player_id])
    hole = relationship("Hole", back_populates="scores")
    entered_by_user = relationship("User", foreign_keys=[entered_by])
    validated_by_user = relationship("User", foreign_keys=[validated_by])
    history = relationship(
        "ScoreHistory",
        back_populates="score",
        cascade="all, delete-orphan",
        order_by="ScoreHistory.modified_at.desc()",
    )

    # ── Contraintes ─────────────────────────────────────────────
    __table_args__ = (
        UniqueConstraint(
            "game_id", "player_id", "hole_id", name="uq_score_game_player_hole"
        ),
        CheckConstraint("strokes >= 1", name="ck_score_strokes_min"),
        CheckConstraint("penalties >= 0", name="ck_score_penalties_min"),
        CheckConstraint(
            "total_score = strokes + penalties", name="ck_score_total_formula"
        ),
    )

    def __repr__(self) -> str:
        return f"<Score game={self.game_id} player={self.player_id} total={self.total_score}>"
