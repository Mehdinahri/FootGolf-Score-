import uuid
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.exceptions import FootGolfException, NotFoundError
from app.models.game import Game, GameStatus, VALID_TRANSITIONS
from app.models.user import User

class GameStatusService:
    @staticmethod
    def change_status(db: Session, game_id: uuid.UUID, new_status: GameStatus, user: User) -> Game:
        # On vérifie que le jeu existe
        game = db.get(Game, game_id)
        if not game:
            raise NotFoundError("Partie introuvable.")
        
        # On vérifie l'autorisation (seulement ADMIN ou l'organisateur)
        if user.role.value != "ADMIN" and game.organizer_id != user.id:
            raise FootGolfException("Non autorisé à modifier le statut de cette partie.", status_code=403)
            
        current_status = game.status
        if new_status not in VALID_TRANSITIONS.get(current_status, []):
            raise FootGolfException(f"Transition invalide de {current_status.value} à {new_status.value}.")

        # Règles spécifiques
        if new_status == GameStatus.IN_PROGRESS:
            # Vérifier s'il y a des joueurs
            if game.registered_count == 0:
                raise FootGolfException("Impossible de démarrer une partie sans joueurs.")
            
            # Vérifier si le parcours a au moins 1 trou
            from app.models.hole import Hole
            stmt = select(Hole).where(Hole.course_id == game.course_id)
            holes = db.scalars(stmt).all()
            if len(holes) == 0:
                raise FootGolfException("Impossible de démarrer la partie : le parcours doit avoir au moins 1 trou configuré.")

        game.status = new_status
        db.add(game)
        db.commit()
        db.refresh(game)
        return game
