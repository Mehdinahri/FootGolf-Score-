"""
Schémas Pydantic — Authentification.
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class LoginRequest(BaseModel):
    """Requête de connexion."""

    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class LoginResponse(BaseModel):
    """Réponse de connexion réussie."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # secondes

    model_config = ConfigDict(from_attributes=True)


class RefreshRequest(BaseModel):
    """Requête de rafraîchissement du token."""

    refresh_token: str


class RefreshResponse(BaseModel):
    """Réponse de rafraîchissement."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class ForgotPasswordRequest(BaseModel):
    """Requête de mot de passe oublié."""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Requête de réinitialisation du mot de passe."""

    token: str
    new_password: str = Field(..., min_length=8, max_length=128)


class TokenPayload(BaseModel):
    """Payload décodé d'un JWT."""

    sub: str
    role: str
    type: str  # "access" ou "refresh"
    jti: str | None = None  # Uniquement pour refresh
    exp: int
    iat: int
