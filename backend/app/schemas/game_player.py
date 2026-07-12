"""
Schémas Pydantic — Inscriptions des joueurs.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.game_player import RegistrationStatus, AttendanceStatus
from app.schemas.user import UserBrief


class GamePlayerCreate(BaseModel):
    """Création d'une inscription."""

    user_id: UUID


class GamePlayerUpdate(BaseModel):
    """Mise à jour du statut de présence ou de l'ordre de départ."""

    status: RegistrationStatus | None = None
    attendance: AttendanceStatus | None = None
    start_order: int | None = None


class GamePlayerResponse(BaseModel):
    """Inscription renvoyée par l'API."""

    id: UUID
    game_id: UUID
    user_id: UUID
    registered_at: datetime
    status: RegistrationStatus
    start_order: int | None = None
    attendance: AttendanceStatus | None = None
    cancelled_at: datetime | None = None

    # Optionnel, si l'on veut les détails du joueur
    user: UserBrief | None = None

    model_config = ConfigDict(from_attributes=True)
