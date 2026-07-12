from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.score import Score
from app.repositories.base import BaseRepository

class ScoreRepository(BaseRepository[Score]):
    def get_by_game_and_player(self, db: Session, game_id: UUID, player_id: UUID) -> List[Score]:
        stmt = select(Score).where(
            Score.game_id == game_id,
            Score.player_id == player_id
        )
        return list(db.scalars(stmt).all())
        
    def get_by_hole_player(self, db: Session, game_id: UUID, player_id: UUID, hole_id: UUID) -> Optional[Score]:
        stmt = select(Score).where(
            Score.game_id == game_id,
            Score.player_id == player_id,
            Score.hole_id == hole_id
        )
        return db.scalars(stmt).first()

score_repo = ScoreRepository(Score)
