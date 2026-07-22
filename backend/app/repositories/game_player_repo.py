from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.game_player import GamePlayer
from app.repositories.base import BaseRepository

class GamePlayerRepository(BaseRepository[GamePlayer]):
    def get_by_game_and_user(self, db: Session, game_id: UUID, user_id: UUID) -> Optional[GamePlayer]:
        stmt = select(GamePlayer).where(
            GamePlayer.game_id == game_id,
            GamePlayer.user_id == user_id
        )
        return db.scalars(stmt).first()

    def get_by_game(self, db: Session, game_id: UUID) -> List[GamePlayer]:
        from app.models.game_player import RegistrationStatus
        stmt = select(GamePlayer).where(
            GamePlayer.game_id == game_id,
            GamePlayer.status != RegistrationStatus.CANCELLED
        ).order_by(GamePlayer.registered_at)
        return list(db.scalars(stmt).all())

game_player_repo = GamePlayerRepository(GamePlayer)
