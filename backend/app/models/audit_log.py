"""
Modèle AuditLog — Journal d'audit.

Enregistre toutes les actions sensibles avec l'ancien et
le nouveau contenu au format JSON.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from app.db.base import Base


class AuditLog(Base):
    """Table `audit_logs`."""

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    old_value = Column(JSONB, nullable=True)
    new_value = Column(JSONB, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<AuditLog {self.action} {self.resource_type}>"
