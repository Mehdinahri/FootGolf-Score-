import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.repositories.game_repo import game_repo
from app.services.leaderboard_service import LeaderboardService
from app.schemas.common import ApiResponse, success_response
from app.schemas.leaderboard import LeaderboardResponse
from app.core.exceptions import NotFoundError

router = APIRouter()

@router.get("/{game_id}/leaderboard", response_model=ApiResponse[LeaderboardResponse])
def get_leaderboard(
    game_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    # optionnel: protection par token (on peut imaginer que c'est public pour les spectateurs, mais on garde pour l'instant)
) -> dict:
    """Récupérer le classement d'une partie."""
    game = game_repo.get(db, id=game_id)
    if not game:
        raise NotFoundError("Partie introuvable")

    data = LeaderboardService.get_leaderboard(db, game)
    return success_response("Classement récupéré", data=data)
