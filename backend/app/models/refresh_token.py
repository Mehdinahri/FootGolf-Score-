"""
Modèle RefreshToken — Tokens de rafraîchissement.

Stocke les hashes SHA-256 des refresh tokens pour permettre
la révocation et la rotation.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class RefreshToken(Base):
    """Table `refresh_tokens`."""

    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash = Column(String(64), nullable=False, index=True)  # SHA-256 hex
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    ip_address = Column(String(45), nullable=True)  # IPv4 ou IPv6
    user_agent = Column(String(500), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # ── Relations ───────────────────────────────────────────────
    user = relationship("User", back_populates="refresh_tokens")

    @property
    def is_expired(self) -> bool:
        from datetime import timezone as tz
        return datetime.now(tz.utc) > self.expires_at

    @property
    def is_valid(self) -> bool:
        return not self.is_revoked and not self.is_expired

    def __repr__(self) -> str:
        status = "valid" if self.is_valid else "invalid"
        return f"<RefreshToken user={self.user_id} ({status})>"
