"""
Dépendances FastAPI (Injection).
Gère la récupération de la session DB, de l'utilisateur actuel et de ses permissions.
"""

from __future__ import annotations

import uuid
from typing import Generator

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core import security
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories.user_repo import user_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Récupère l'utilisateur à partir du JWT access token."""
    try:
        payload = security.decode_token(token)
        if payload.get("type") != "access":
            raise AuthenticationError("Type de token invalide.")
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthenticationError("Token invalide.")
    except Exception:
        raise AuthenticationError("Non authentifié ou token expiré.")

    user = user_repo.get(db, id=uuid.UUID(user_id))
    if not user:
        raise AuthenticationError("Utilisateur introuvable.")
    if not user.is_active:
        raise AuthenticationError("Compte désactivé.")
        
    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Vérifie que l'utilisateur est un ADMIN."""
    if current_user.role != UserRole.ADMIN:
        raise AuthorizationError("Droits administrateur requis.")
    return current_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Vérifie que l'utilisateur est actif (déjà fait dans get_current_user)."""
    return current_user
