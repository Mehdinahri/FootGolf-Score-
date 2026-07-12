"""
Modèle User — Utilisateurs de l'application.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SAEnum,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class UserRole(str, enum.Enum):
    """Rôles possibles d'un utilisateur."""

    ADMIN = "ADMIN"
    PLAYER = "PLAYER"
    MARKER = "MARKER"


class User(Base):
    """Table `users`."""

    __tablename__ = "users"

    # ── Colonnes ────────────────────────────────────────────────
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        SAEnum(UserRole, name="user_role", create_constraint=True),
        nullable=False,
        default=UserRole.PLAYER,
    )
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # ── Relations ───────────────────────────────────────────────
    organized_games = relationship(
        "Game", back_populates="organizer", foreign_keys="Game.organizer_id"
    )
    marked_games = relationship(
        "Game", back_populates="marker", foreign_keys="Game.marker_id"
    )
    game_registrations = relationship("GamePlayer", back_populates="user")
    refresh_tokens = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )
    notifications = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan"
    )

    # ── Propriétés ──────────────────────────────────────────────
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def initials(self) -> str:
        return f"{self.first_name[0]}{self.last_name[0]}".upper()

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role.value})>"
