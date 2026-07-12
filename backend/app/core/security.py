"""
Utilitaires de sécurité.

- Hachage de mots de passe (bcrypt, cost factor 12)
- Création / décodage de tokens JWT (PyJWT)
- Hachage de refresh tokens pour stockage en base
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from app.core.config import settings


# ╔══════════════════════════════════════════════════════════════╗
# ║  Password hashing                                          ║
# ╚══════════════════════════════════════════════════════════════╝


def hash_password(password: str) -> str:
    """Hache un mot de passe avec bcrypt (cost=12)."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe en clair contre son hash bcrypt."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ╔══════════════════════════════════════════════════════════════╗
# ║  JWT tokens                                                 ║
# ╚══════════════════════════════════════════════════════════════╝


def create_access_token(
    subject: str | uuid.UUID,
    role: str,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Crée un JWT access token.

    Args:
        subject: Identifiant de l'utilisateur (UUID).
        role: Rôle de l'utilisateur (ADMIN, PLAYER, MARKER).
        expires_delta: Durée de validité personnalisée.
        extra_claims: Claims supplémentaires à inclure.

    Returns:
        Token JWT encodé.
    """
    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta
        or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload: dict[str, Any] = {
        "sub": str(subject),
        "role": role,
        "type": "access",
        "iat": now,
        "exp": expire,
    }
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(
    subject: str | uuid.UUID,
    expires_delta: timedelta | None = None,
) -> str:
    """Crée un JWT refresh token avec un identifiant unique (jti).

    Args:
        subject: Identifiant de l'utilisateur (UUID).
        expires_delta: Durée de validité personnalisée.

    Returns:
        Token JWT encodé.
    """
    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta
        or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": "refresh",
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """Décode et valide un token JWT.

    Raises:
        jwt.ExpiredSignatureError: Token expiré.
        jwt.InvalidTokenError: Token invalide.
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )


def hash_token(token: str) -> str:
    """Hache un token (SHA-256) pour stockage sécurisé en base."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
