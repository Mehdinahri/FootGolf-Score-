"""
Modèle Hole — Trous d'un parcours.

Chaque parcours a 18 trous :
- trous 1→9  : OUTWARD (aller)
- trous 10→18 : INWARD (retour)
"""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class HoleSection(str, enum.Enum):
    """Section du parcours."""

    OUTWARD = "OUTWARD"  # Aller (trous 1–9)
    INWARD = "INWARD"    # Retour (trous 10–18)


class Hole(Base):
    """Table `holes`."""

    __tablename__ = "holes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    hole_number = Column(Integer, nullable=False)  # 1–18
    distance = Column(Integer, nullable=False)       # mètres
    par = Column(Integer, nullable=False)
    section = Column(
        SAEnum(HoleSection, name="hole_section", create_constraint=True),
        nullable=False,
    )
    description = Column(Text, nullable=True)
    difficulty = Column(Integer, nullable=True)  # 1 (facile) → 18 (difficile)
    is_active = Column(Boolean, default=True, nullable=False)

    # ── Relations ───────────────────────────────────────────────
    course = relationship("Course", back_populates="holes")
    scores = relationship("Score", back_populates="hole")

    # ── Contraintes ─────────────────────────────────────────────
    __table_args__ = (
        UniqueConstraint("course_id", "hole_number", name="uq_hole_course_number"),
        CheckConstraint("hole_number >= 1 AND hole_number <= 18", name="ck_hole_number_range"),
        CheckConstraint("par > 0", name="ck_hole_par_positive"),
        CheckConstraint("distance > 0", name="ck_hole_distance_positive"),
    )

    def __repr__(self) -> str:
        return f"<Hole #{self.hole_number} PAR {self.par}>"
