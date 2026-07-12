from typing import Any
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.game import GameStatus
from app.models.score import Score, ScoreStatus
from app.repositories.game_repo import game_repo
from app.repositories.score_repo import score_repo
from app.repositories.hole_repo import hole_repo
from app.schemas.common import ApiResponse, success_response
from app.schemas.offline_sync import SyncRequest, SyncResponse, SyncResponseItem

router = APIRouter()

@router.post("/scores", response_model=ApiResponse[SyncResponse])
def sync_scores(
    sync_in: SyncRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> dict:
    """Synchroniser les scores saisis hors-ligne."""
    game = game_repo.get(db, id=sync_in.game_id)
    if not game:
        return success_response("Game not found", data={"results": [{"idempotency_key": s.idempotency_key, "status": "error", "error": "Game not found"} for s in sync_in.scores]})

    results = []
    
    for item in sync_in.scores:
        # Vérification idempotency key (si déjà synchronisé)
        stmt = db.query(Score).filter(Score.idempotency_key == item.idempotency_key, Score.player_id == current_user.id).first()
        if stmt:
            results.append(SyncResponseItem(idempotency_key=item.idempotency_key, status="success"))
            continue
            
        if game.status != GameStatus.IN_PROGRESS:
            results.append(SyncResponseItem(idempotency_key=item.idempotency_key, status="error", error="Game not in progress"))
            continue

        hole = hole_repo.get(db, id=item.hole_id)
        if not hole or hole.course_id != game.course_id:
            results.append(SyncResponseItem(idempotency_key=item.idempotency_key, status="error", error="Invalid hole"))
            continue

        existing_score = score_repo.get_by_hole_player(db, game.id, current_user.id, hole.id)
        if existing_score:
            results.append(SyncResponseItem(idempotency_key=item.idempotency_key, status="error", error="Score already exists for hole"))
            continue

        new_score = Score(
            game_id=game.id,
            player_id=current_user.id,
            hole_id=hole.id,
            strokes=item.strokes,
            penalties=item.penalties,
            total_score=item.strokes + item.penalties,
            status=ScoreStatus.DRAFT,
            idempotency_key=item.idempotency_key
        )
        db.add(new_score)
        
        try:
            db.commit()
            results.append(SyncResponseItem(idempotency_key=item.idempotency_key, status="success"))
        except Exception as e:
            db.rollback()
            results.append(SyncResponseItem(idempotency_key=item.idempotency_key, status="error", error=str(e)))

    # Optionnel: Broadcast de la carte des scores globale
    try:
        from app.services.broadcast_service import broadcast_service
        from app.services.leaderboard_service import LeaderboardService
        leaderboard_data = LeaderboardService.get_leaderboard(db, game)
        import asyncio
        # Run it sync because we are inside a sync endpoint
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(broadcast_service.broadcast_leaderboard(str(game.id), leaderboard_data))
        except RuntimeError:
            pass # No event loop
    except Exception:
        pass

    return success_response("Scores synchronisés", data=SyncResponse(results=results).model_dump())
