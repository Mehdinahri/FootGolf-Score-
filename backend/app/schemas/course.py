"""
Schémas Pydantic — Parcours.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    """Création d'un parcours."""

    name: str = Field(..., min_length=1, max_length=200)
    address: str | None = Field(None, max_length=300)
    city: str | None = Field(None, max_length=100)
    description: str | None = None
    hole_count: int = Field(default=18, ge=1, le=18)
    image_url: str | None = Field(None, max_length=500)
    latitude: Decimal | None = None
    longitude: Decimal | None = None


class CourseUpdate(BaseModel):
    """Modification d'un parcours."""

    name: str | None = Field(None, min_length=1, max_length=200)
    address: str | None = Field(None, max_length=300)
    city: str | None = Field(None, max_length=100)
    description: str | None = None
    image_url: str | None = Field(None, max_length=500)
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    is_active: bool | None = None


class CourseResponse(BaseModel):
    """Parcours renvoyé par l'API."""

    id: UUID
    name: str
    address: str | None = None
    city: str | None = None
    description: str | None = None
    hole_count: int
    par_total: int
    distance_total: int
    is_active: bool
    image_url: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CourseBrief(BaseModel):
    """Version allégée d'un parcours."""

    id: UUID
    name: str
    city: str | None = None
    par_total: int
    hole_count: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
