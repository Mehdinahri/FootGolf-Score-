"""
Modèle ScoreHistory — Historique des modifications de scores.

Chaque correction d'un score génère une entrée dans cette table
avec l'ancien et le nouveau score, ainsi que le motif.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class ScoreHistory(Base):
    """Table `score_histories`."""

    __tablename__ = "score_histories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    score_id = Column(
        UUID(as_uuid=True),
        ForeignKey("scores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    modified_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    old_strokes = Column(Integer, nullable=False)
    old_penalties = Column(Integer, nullable=False)
    old_total = Column(Integer, nullable=False)
    new_strokes = Column(Integer, nullable=False)
    new_penalties = Column(Integer, nullable=False)
    new_total = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)
    modified_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # ── Relations ───────────────────────────────────────────────
    score = relationship("Score", back_populates="history")
    modifier = relationship("User", foreign_keys=[modified_by])

    def __repr__(self) -> str:
        return f"<ScoreHistory score={self.score_id} {self.old_total}→{self.new_total}>"
