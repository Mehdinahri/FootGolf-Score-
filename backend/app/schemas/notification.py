"""
Schémas Pydantic — Notifications.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.notification import NotificationType


class NotificationResponse(BaseModel):
    """Notification renvoyée par l'API."""

    id: UUID
    type: NotificationType
    title: str
    message: str
    reference_id: UUID | None = None
    reference_type: str | None = None
    is_read: bool
    created_at: datetime
    read_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
