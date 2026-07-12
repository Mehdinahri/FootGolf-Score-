"""
Modèle Notification — Notifications internes.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class NotificationType(str, enum.Enum):
    """Types de notifications."""

    REGISTRATION_CONFIRMED = "REGISTRATION_CONFIRMED"
    GAME_FULL = "GAME_FULL"
    REGISTRATION_OPEN = "REGISTRATION_OPEN"
    DATE_CHANGED = "DATE_CHANGED"
    GAME_CANCELLED = "GAME_CANCELLED"
    REMINDER = "REMINDER"
    GAME_STARTED = "GAME_STARTED"
    FINAL_RANKING = "FINAL_RANKING"
    SCORE_VALIDATED = "SCORE_VALIDATED"
    SCORE_CORRECTED = "SCORE_CORRECTED"


class Notification(Base):
    """Table `notifications`."""

    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type = Column(
        SAEnum(NotificationType, name="notification_type", create_constraint=True),
        nullable=False,
    )
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    reference_id = Column(UUID(as_uuid=True), nullable=True)
    reference_type = Column(String(50), nullable=True)  # "game", "score", etc.
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    read_at = Column(DateTime(timezone=True), nullable=True)

    # ── Relations ───────────────────────────────────────────────
    user = relationship("User", back_populates="notifications")

    def __repr__(self) -> str:
        status = "lu" if self.is_read else "non lu"
        return f"<Notification {self.type.value} ({status})>"
