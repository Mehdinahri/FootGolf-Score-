"""
Modèle OfflineSyncRequest — Requêtes de synchronisation hors ligne.

Lorsqu'un joueur enregistre un score sans connexion, le frontend
stocke la requête localement et la renvoie au retour de la connexion.
Ce modèle gère le traitement côté serveur.
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
    String,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from app.db.base import Base


class SyncStatus(str, enum.Enum):
    """Statut de la requête de synchronisation."""

    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    CONFLICT = "CONFLICT"
    ERROR = "ERROR"


class OfflineSyncRequest(Base):
    """Table `offline_sync_requests`."""

    __tablename__ = "offline_sync_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    idempotency_key = Column(
        UUID(as_uuid=True), unique=True, nullable=False, index=True
    )
    resource_type = Column(String(50), nullable=False)  # "score"
    action = Column(String(50), nullable=False)          # "create", "update"
    payload = Column(JSONB, nullable=False)
    status = Column(
        SAEnum(SyncStatus, name="sync_status", create_constraint=True),
        nullable=False,
        default=SyncStatus.PENDING,
    )
    server_response = Column(JSONB, nullable=True)
    client_timestamp = Column(DateTime(timezone=True), nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<OfflineSyncRequest {self.resource_type}.{self.action} ({self.status.value})>"
