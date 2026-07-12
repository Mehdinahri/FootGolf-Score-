from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.game import Game, GameStatus
from app.repositories.base import BaseRepository

class GameRepository(BaseRepository[Game]):
    def get_available_games(self, db: Session) -> List[Game]:
        """Récupère les parties ouvertes ou en cours pour le dashboard."""
        stmt = select(Game).where(
            Game.status.in_([GameStatus.REGISTRATION_OPEN, GameStatus.IN_PROGRESS, GameStatus.FULL])
        ).order_by(Game.start_date.asc())
        return list(db.scalars(stmt).all())

game_repo = GameRepository(Game)
