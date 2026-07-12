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
from app.services.score_calculation_service import ScoreCalculationService
from app.schemas.common import ApiResponse, success_response
from app.schemas.score import ScoreCreate, ScoreUpdate, ScoreCorrection, ScoreResponse, ScorecardResponse
from app.core.exceptions import NotFoundError, FootGolfException

router = APIRouter()

# ── SCORECARD ───────────────────────────────────────────────────────

@router.get("/{game_id}/scorecard", response_model=ApiResponse[ScorecardResponse])
def get_scorecard(
    game_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> dict:
    """Récupérer la carte de score pour un joueur."""
    data = ScoreCalculationService.calculate_scorecard(db, game_id, current_user)
    if not data:
        raise NotFoundError("Partie introuvable")
    return success_response("Carte de score récupérée", data=data)

# ── SCORES CRUD ─────────────────────────────────────────────────────

@router.post("/{game_id}/scores", response_model=ApiResponse[ScoreResponse])
def create_score(
    game_id: uuid.UUID,
    score_in: ScoreCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> dict:
    """Saisir un score."""
    game = game_repo.get(db, id=game_id)
    if not game:
        raise NotFoundError("Partie introuvable")
        
    if game.status != GameStatus.IN_PROGRESS:
        raise FootGolfException("La saisie des scores est autorisée uniquement pendant la partie.")
        
    hole = hole_repo.get(db, id=score_in.hole_id)
    if not hole or hole.course_id != game.course_id:
        raise FootGolfException("Ce trou n'appartient pas au parcours de cette partie.")

    # Vérification d'unicité
    existing_score = score_repo.get_by_hole_player(db, game_id, current_user.id, hole.id)
    if existing_score:
        raise FootGolfException("Un score existe déjà pour ce trou.", status_code=409)

    score_total = score_in.strokes + score_in.penalties

    new_score = Score(
        game_id=game_id,
        player_id=current_user.id,
        hole_id=hole.id,
        strokes=score_in.strokes,
        penalties=score_in.penalties,
        total_score=score_total,
        status=ScoreStatus.DRAFT,
        idempotency_key=score_in.idempotency_key
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    
    return success_response("Score enregistré", data=ScoreResponse.model_validate(new_score).model_dump())

@router.put("/{game_id}/scores/{score_id}", response_model=ApiResponse[ScoreResponse])
def update_score(
    game_id: uuid.UUID,
    score_id: uuid.UUID,
    score_in: ScoreUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> dict:
    """Modifier un score non validé."""
    score = score_repo.get(db, id=score_id)
    if not score or score.game_id != game_id or score.player_id != current_user.id:
        raise NotFoundError("Score introuvable ou non autorisé.")
        
    if score.status == ScoreStatus.VALIDATED:
        raise FootGolfException("Impossible de modifier un score validé.")

    game = game_repo.get(db, id=game_id)
    if game.status != GameStatus.IN_PROGRESS:
        raise FootGolfException("La saisie des scores est autorisée uniquement pendant la partie.")

    if score_in.strokes is not None:
        score.strokes = score_in.strokes
    if score_in.penalties is not None:
        score.penalties = score_in.penalties
        
    score.total_score = score.strokes + score.penalties
    score.idempotency_key = score_in.idempotency_key
    
    db.add(score)
    db.commit()
    db.refresh(score)
    
    return success_response("Score mis à jour", data=ScoreResponse.model_validate(score).model_dump())

@router.post("/{game_id}/scores/{score_id}/validate", response_model=ApiResponse)
async def validate_score(
    game_id: uuid.UUID,
    score_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> dict:
    """Valider un score."""
    score = score_repo.get(db, id=score_id)
    if not score or score.game_id != game_id or score.player_id != current_user.id:
        raise NotFoundError("Score introuvable ou non autorisé.")

    score.status = ScoreStatus.VALIDATED
    db.add(score)
    db.commit()
    
    # Broadcast WS Update
    from app.services.broadcast_service import broadcast_service
    from app.services.leaderboard_service import LeaderboardService
    game = game_repo.get(db, id=game_id)
    leaderboard_data = LeaderboardService.get_leaderboard(db, game)
    await broadcast_service.broadcast_leaderboard(str(game_id), leaderboard_data)
    
    return success_response("Score validé")

@router.post("/admin/{game_id}/scores/{score_id}/correct", response_model=ApiResponse)
def admin_correct_score(
    game_id: uuid.UUID,
    score_id: uuid.UUID,
    correction: ScoreCorrection,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> dict:
    """[ADMIN] Corriger un score, même validé."""
    score = score_repo.get(db, id=score_id)
    if not score or score.game_id != game_id:
        raise NotFoundError("Score introuvable.")

    # Historisation à implémenter (ScoreHistory)
    score.strokes = correction.strokes
    score.penalties = correction.penalties
    score.total_score = correction.strokes + correction.penalties
    
    db.add(score)
    db.commit()
    
    return success_response("Score corrigé par l'administrateur")
