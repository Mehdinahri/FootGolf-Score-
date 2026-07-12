"""
Base déclarative SQLAlchemy.

Tous les modèles ORM héritent de `Base`.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Classe de base pour tous les modèles SQLAlchemy."""
    pass
