"""
Repository générique de base.
Fournit les opérations CRUD communes pour tous les modèles SQLAlchemy.
"""

from __future__ import annotations

from typing import Any, Generic, Type, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Repository de base."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType | None:
        """Récupère un objet par son ID."""
        return db.get(self.model, id)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        """Récupère plusieurs objets (paginés)."""
        stmt = select(self.model).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def create(self, db: Session, *, obj_in: dict[str, Any] | BaseModel) -> ModelType:
        """Crée un nouvel objet."""
        obj_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: dict[str, Any] | BaseModel
    ) -> ModelType:
        """Met à jour un objet existant."""
        obj_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: Any) -> ModelType | None:
        """Supprime un objet par son ID."""
        obj = db.get(self.model, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    from pydantic import BaseModel # Imported here to fix typing issue locally within the class
