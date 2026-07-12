"""
Repository pour l'utilisateur.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository pour User."""

    def get_by_email(self, db: Session, *, email: str) -> User | None:
        """Récupère un utilisateur par son email."""
        stmt = select(User).where(User.email == email)
        return db.scalars(stmt).first()


user_repo = UserRepository(User)
