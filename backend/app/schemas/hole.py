"""
Schémas Pydantic — Trous.
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.hole import HoleSection


class HoleCreate(BaseModel):
    """Création d'un trou."""

    hole_number: int = Field(..., ge=1, le=18)
    distance: int = Field(..., gt=0, description="Distance en mètres")
    par: int = Field(..., gt=0)
    description: str | None = None
    difficulty: int | None = Field(None, ge=1, le=18)


class HoleBulkCreate(BaseModel):
    """Création en lot de tous les trous d'un parcours."""

    holes: list[HoleCreate] = Field(..., min_length=1, max_length=18)


class HoleUpdate(BaseModel):
    """Modification d'un trou."""

    distance: int | None = Field(None, gt=0)
    par: int | None = Field(None, gt=0)
    description: str | None = None
    difficulty: int | None = Field(None, ge=1, le=18)
    is_active: bool | None = None


class HoleResponse(BaseModel):
    """Trou renvoyé par l'API."""

    id: UUID
    course_id: UUID
    hole_number: int
    distance: int
    par: int
    section: HoleSection
    description: str | None = None
    difficulty: int | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
