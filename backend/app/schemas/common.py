"""
Schémas Pydantic communs — Format standard des réponses API.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


# ╔══════════════════════════════════════════════════════════════╗
# ║  Format standard des réponses                               ║
# ╚══════════════════════════════════════════════════════════════╝


class FieldError(BaseModel):
    """Erreur de validation sur un champ."""

    field: str
    message: str


class ApiResponse(BaseModel, Generic[T]):
    """Réponse API standard.

    Exemples :
        Succès : {"success": true, "message": "...", "data": {...}, "errors": null}
        Erreur : {"success": false, "message": "...", "data": null, "errors": [...]}
    """

    success: bool
    message: str
    data: T | None = None
    errors: list[FieldError] | None = None


class PaginatedData(BaseModel, Generic[T]):
    """Données paginées."""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Réponse paginée standard."""

    success: bool = True
    message: str = "Données récupérées avec succès"
    data: PaginatedData[T] | None = None
    errors: list[FieldError] | None = None


# ╔══════════════════════════════════════════════════════════════╗
# ║  Helpers                                                     ║
# ╚══════════════════════════════════════════════════════════════╝


def success_response(
    message: str = "Opération réussie",
    data: Any = None,
) -> dict:
    """Construit une réponse de succès."""
    return {
        "success": True,
        "message": message,
        "data": data,
        "errors": None,
    }


def error_response(
    message: str = "Une erreur est survenue",
    errors: list[dict[str, str]] | None = None,
) -> dict:
    """Construit une réponse d'erreur."""
    return {
        "success": False,
        "message": message,
        "data": None,
        "errors": errors,
    }


def paginated_response(
    items: list,
    total: int,
    page: int,
    page_size: int,
    message: str = "Données récupérées avec succès",
) -> dict:
    """Construit une réponse paginée."""
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    return {
        "success": True,
        "message": message,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        },
        "errors": None,
    }
