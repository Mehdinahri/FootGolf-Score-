"""
Modèle Course — Parcours de FootGolf.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Course(Base):
    """Table `courses`."""

    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    address = Column(String(300), nullable=True)
    city = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    hole_count = Column(Integer, nullable=False, default=18)
    par_total = Column(Integer, nullable=False, default=0)
    distance_total = Column(Integer, nullable=False, default=0)  # mètres
    is_active = Column(Boolean, default=True, nullable=False)
    image_url = Column(String(500), nullable=True)
    latitude = Column(Numeric(10, 7), nullable=True)
    longitude = Column(Numeric(10, 7), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ── Relations ───────────────────────────────────────────────
    holes = relationship(
        "Hole",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Hole.hole_number",
    )
    games = relationship("Game", back_populates="course")

    def __repr__(self) -> str:
        return f"<Course {self.name} ({self.hole_count} trous)>"
