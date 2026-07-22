"""
Router pour la gestion des utilisateurs.
"""

from typing import Any
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_current_admin, get_current_active_user
from app.core.exceptions import NotFoundError, AuthorizationError
from app.db.session import get_db
from app.models.user import User, UserRole
from app.models.game import Game
from app.models.game_player import GamePlayer, RegistrationStatus
from app.repositories.user_repo import user_repo
from app.schemas.common import PaginatedResponse, paginated_response, success_response, ApiResponse
from app.schemas.user import UserResponse, UserHistoryItem

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[UserResponse])
def get_users(
    page: int = 1,
    size: int = 50,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Any:
    """
    Récupère la liste de tous les utilisateurs (Admin seulement).
    """
    skip = (page - 1) * size
    limit = size
    
    users = user_repo.get_multi(db, skip=skip, limit=limit)
    
    from sqlalchemy import func
    total = db.scalar(select(func.count(User.id)))
    
    return paginated_response(
        items=users,
        total=total,
        page=page,
        page_size=size,
    )

@router.get("/{user_id}", response_model=ApiResponse[UserResponse])
def get_user_profile(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Récupère le profil d'un utilisateur.
    Accessible par l'admin ou par l'utilisateur lui-même.
    """
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise AuthorizationError("Vous ne pouvez consulter que votre propre profil.")
        
    user = user_repo.get(db, id=user_id)
    if not user:
        raise NotFoundError("Utilisateur introuvable.")
    return success_response(data=user)

@router.get("/{user_id}/history", response_model=ApiResponse[list[UserHistoryItem]])
def get_user_history(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Récupère l'historique des parties d'un utilisateur.
    Accessible par l'admin ou par l'utilisateur lui-même.
    """
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise AuthorizationError("Vous ne pouvez consulter que votre propre historique.")
        
    user = user_repo.get(db, id=user_id)
    if not user:
        raise NotFoundError("Utilisateur introuvable.")
        
    stmt = (
        select(GamePlayer, Game)
        .join(Game, GamePlayer.game_id == Game.id)
        .where(GamePlayer.user_id == user_id)
        .order_by(Game.start_date.desc().nullslast(), GamePlayer.registered_at.desc())
    )
    results = db.execute(stmt).all()
    
    history = []
    # On importe LeaderboardService ici pour éviter des imports circulaires si nécessaire
    from app.services.leaderboard_service import LeaderboardService
    
    for game_player, game in results:
        # Extraire score/position seulement si la partie est terminée ou en cours
        total_score = None
        relative_to_par = None
        position = None
        
        # Pour récupérer le classement global et la position du joueur:
        if game.status.value in ["IN_PROGRESS", "FINISHED"]:
            lb_data = LeaderboardService.get_leaderboard(db, game)
            for row in lb_data["rows"]:
                if row["player_id"] == str(user_id):
                    total_score = row.get("total_score")
                    relative_to_par = row.get("relative_to_par")
                    position = row.get("position")
                    break

        # On utilise le `course_name` depuis l'objet course lié s'il est préchargé ou on le recupère:
        from app.repositories.course_repo import course_repo
        course = course_repo.get(db, id=game.course_id)
        
        history.append({
            "game_id": game.id,
            "title": game.title,
            "course_name": course.name if course else "Parcours inconnu",
            "start_date": game.start_date,
            "status": game.status.value,
            "registered_at": game_player.registered_at,
            "attendance": game_player.attendance.value if game_player.attendance else None,
            "total_score": total_score,
            "relative_to_par": relative_to_par,
            "position": position
        })
        
    return success_response(data=history)
