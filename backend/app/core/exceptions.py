"""
Exceptions métier de l'application FootGolf Score.

Chaque exception porte un `status_code` HTTP et un `message` en français.
Elles sont interceptées par le handler global dans `main.py`.
"""

from __future__ import annotations

from typing import Any


class FootGolfException(Exception):
    """Exception de base de l'application."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        errors: list[dict[str, str]] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.errors = errors
        super().__init__(self.message)


# ── Authentification / Autorisation ─────────────────────────────


class AuthenticationError(FootGolfException):
    """Échec d'authentification (identifiants invalides, token expiré…)."""

    def __init__(self, message: str = "Identifiants invalides") -> None:
        super().__init__(message=message, status_code=401)


class AuthorizationError(FootGolfException):
    """L'utilisateur n'a pas les droits requis."""

    def __init__(self, message: str = "Accès non autorisé") -> None:
        super().__init__(message=message, status_code=403)


# ── Ressources ──────────────────────────────────────────────────


class NotFoundError(FootGolfException):
    """Ressource introuvable."""

    def __init__(
        self, resource: str = "Ressource", identifier: Any = None
    ) -> None:
        msg = f"{resource} introuvable"
        if identifier is not None:
            msg = f"{resource} « {identifier} » introuvable"
        super().__init__(message=msg, status_code=404)


class ConflictError(FootGolfException):
    """Conflit (doublon, clé unique…)."""

    def __init__(self, message: str = "Conflit détecté") -> None:
        super().__init__(message=message, status_code=409)


class ValidationError(FootGolfException):
    """Données invalides."""

    def __init__(
        self,
        message: str = "Données invalides",
        errors: list[dict[str, str]] | None = None,
    ) -> None:
        super().__init__(message=message, status_code=422, errors=errors)


# ── Métier ──────────────────────────────────────────────────────


class GameStateError(FootGolfException):
    """Transition de statut de partie invalide."""

    def __init__(self, message: str = "Transition de statut invalide") -> None:
        super().__init__(message=message, status_code=400)


class RegistrationError(FootGolfException):
    """Inscription impossible (partie pleine, déjà inscrit…)."""

    def __init__(self, message: str = "Inscription impossible") -> None:
        super().__init__(message=message, status_code=400)


class ScoreError(FootGolfException):
    """Opération de score invalide."""

    def __init__(self, message: str = "Opération de score impossible") -> None:
        super().__init__(message=message, status_code=400)


class RateLimitError(FootGolfException):
    """Trop de tentatives."""

    def __init__(
        self, message: str = "Trop de tentatives. Réessayez plus tard."
    ) -> None:
        super().__init__(message=message, status_code=429)


class InactiveUserError(FootGolfException):
    """Compte utilisateur désactivé."""

    def __init__(
        self, message: str = "Ce compte est désactivé"
    ) -> None:
        super().__init__(message=message, status_code=403)
