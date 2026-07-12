"""
Schémas Pydantic — Utilisateurs.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class UserCreate(BaseModel):
    """Création d'un utilisateur (admin)."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str | None = Field(None, max_length=20)
    password: str = Field(..., min_length=8, max_length=128)
    role: UserRole = UserRole.PLAYER


class UserUpdate(BaseModel):
    """Modification d'un utilisateur."""

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20)
    role: UserRole | None = None


class UserStatusUpdate(BaseModel):
    """Activation/désactivation d'un utilisateur."""

    is_active: bool


class UserProfileUpdate(BaseModel):
    """Modification du profil par le joueur lui-même."""

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    phone: str | None = Field(None, max_length=20)


class ChangePasswordRequest(BaseModel):
    """Changement de mot de passe."""

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class UserResponse(BaseModel):
    """Utilisateur renvoyé par l'API (sans mot de passe)."""

    id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserBrief(BaseModel):
    """Version allégée d'un utilisateur (pour listes, classements)."""

    id: UUID
    first_name: str
    last_name: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def initials(self) -> str:
        return f"{self.first_name[0]}{self.last_name[0]}".upper()
