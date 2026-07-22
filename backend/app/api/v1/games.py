from typing import Any
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.game import GameStatus
from app.repositories.game_repo import game_repo
from app.repositories.game_player_repo import game_player_repo
from app.repositories.course_repo import course_repo
from app.services.game_status_service import GameStatusService
from app.services.registration_service import RegistrationService
from app.schemas.common import ApiResponse, success_response, paginated_response
from app.schemas.game import GameCreate, GameUpdate, GameResponse, GameBrief
from app.schemas.game_player import GamePlayerResponse
from app.core.exceptions import NotFoundError, FootGolfException

router = APIRouter()

# ── GAMES LIST & GET ───────────────────────────────────────────────

@router.get("", response_model=ApiResponse)
def list_games(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> dict:
    """Récupérer la liste des parties disponibles pour inscription ou en cours."""
    games = game_repo.get_available_games(db)
    items = []
    for g in games:
        item = GameBrief.model_validate(g).model_dump()
        # On pourrait optimiser avec un join, mais suffisant pour le moment
        course = course_repo.get(db, id=g.course_id)
        if course:
            item["course_name"] = course.name
        items.append(item)
    return paginated_response(items=items, total=len(items), page=1, page_size=100)

@router.get("/admin", response_model=ApiResponse)
def list_admin_games(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> dict:
    """[ADMIN] Récupérer toutes les parties (y compris DRAFT, FINISHED, CANCELLED)."""
    games = game_repo.get_multi(db, limit=100)
    items = []
    for g in games:
        item = GameBrief.model_validate(g).model_dump()
        course = course_repo.get(db, id=g.course_id)
        if course:
            item["course_name"] = course.name
        items.append(item)
    return paginated_response(items=items, total=len(items), page=1, page_size=100)

@router.get("/{game_id}", response_model=ApiResponse[GameResponse])
def get_game(
    game_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> dict:
    game = game_repo.get(db, id=game_id)
    if not game:
        raise NotFoundError("Partie introuvable")
    return success_response(data=GameResponse.model_validate(game).model_dump())


# ── GAMES CRUD ─────────────────────────────────────────────────────

@router.post("/admin", response_model=ApiResponse[GameResponse])
def create_game(
    game_in: GameCreate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> dict:
    """[ADMIN] Créer une partie (statut DRAFT initial)."""
    course = course_repo.get(db, id=game_in.course_id)
    if not course:
        raise NotFoundError("Parcours introuvable")
    
    data = game_in.model_dump()
    data["organizer_id"] = current_admin.id
    game = game_repo.create(db, obj_in=data)
    return success_response("Partie créée", data=GameResponse.model_validate(game).model_dump())

@router.put("/admin/{game_id}", response_model=ApiResponse[GameResponse])
def update_game(
    game_id: uuid.UUID,
    game_in: GameUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> dict:
    """[ADMIN] Mettre à jour les infos d'une partie (seulement si DRAFT ou OPEN)."""
    game = game_repo.get(db, id=game_id)
    if not game:
        raise NotFoundError("Partie introuvable")
    
    if game.status not in [GameStatus.DRAFT, GameStatus.REGISTRATION_OPEN]:
        raise FootGolfException("Impossible de modifier une partie en cours ou terminée.")
        
    game = game_repo.update(db, db_obj=game, obj_in=game_in)
    return success_response("Partie mise à jour", data=GameResponse.model_validate(game).model_dump())


# ── STATUS TRANSITIONS ─────────────────────────────────────────────

@router.post("/admin/{game_id}/open-registration", response_model=ApiResponse)
def open_registration(
    game_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> dict:
    game = GameStatusService.change_status(db, game_id, GameStatus.REGISTRATION_OPEN, current_admin)
    return success_response("Inscriptions ouvertes", data=GameResponse.model_validate(game).model_dump())

@router.post("/admin/{game_id}/start", response_model=ApiResponse)
def start_game(
    game_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> dict:
    game = GameStatusService.change_status(db, game_id, GameStatus.IN_PROGRESS, current_admin)
    return success_response("Partie démarrée", data=GameResponse.model_validate(game).model_dump())

@router.post("/admin/{game_id}/finish", response_model=ApiResponse)
def finish_game(
    game_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> dict:
    game = GameStatusService.change_status(db, game_id, GameStatus.FINISHED, current_admin)
    return success_response("Partie terminée", data=GameResponse.model_validate(game).model_dump())


# ── REGISTRATIONS ──────────────────────────────────────────────────

@router.post("/{game_id}/register", response_model=ApiResponse[GamePlayerResponse])
def register_player(
    game_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> dict:
    """S'inscrire à une partie."""
    reg = RegistrationService.register_player(db, game_id, current_user.id)
    return success_response("Inscription réussie", data=GamePlayerResponse.model_validate(reg).model_dump())

@router.delete("/{game_id}/registration", response_model=ApiResponse)
def cancel_registration(
    game_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> dict:
    """Annuler son inscription à une partie."""
    reg = RegistrationService.cancel_registration(db, game_id, current_user.id)
    return success_response("Inscription annulée", data=GamePlayerResponse.model_validate(reg).model_dump())

@router.get("/{game_id}/players", response_model=ApiResponse)
def get_game_players(
    game_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> dict:
    """Récupérer la liste des joueurs inscrits."""
    players = game_player_repo.get_by_game(db, game_id=game_id)
    items = []
    for p in players:
        # Charger le User pour la réponse
        user = db.get(User, p.user_id)
        p.user = user
        items.append(GamePlayerResponse.model_validate(p).model_dump())
    return success_response(data=items)
