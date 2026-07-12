import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.exceptions import FootGolfException, NotFoundError
from app.models.game import Game, GameStatus
from app.models.game_player import GamePlayer, RegistrationStatus
from app.models.user import User

class RegistrationService:
    @staticmethod
    def register_player(db: Session, game_id: uuid.UUID, user_id: uuid.UUID) -> GamePlayer:
        # Verrouillage pessimiste de la partie
        stmt = select(Game).where(Game.id == game_id).with_for_update()
        game = db.scalars(stmt).first()

        if not game:
            raise NotFoundError("Partie introuvable.")

        if game.status not in [GameStatus.REGISTRATION_OPEN, GameStatus.FULL]:
            raise FootGolfException("Les inscriptions ne sont pas ouvertes pour cette partie.")

        # Vérifier si déjà inscrit
        stmt_player = select(GamePlayer).where(
            GamePlayer.game_id == game_id,
            GamePlayer.user_id == user_id
        )
        existing_reg = db.scalars(stmt_player).first()

        if existing_reg:
            if existing_reg.status == RegistrationStatus.CANCELLED:
                # Réactivation
                if game.registered_count >= game.max_players:
                    raise FootGolfException("La partie est déjà complète.", status_code=409)
                existing_reg.status = RegistrationStatus.REGISTERED
                game.registered_count += 1
                if game.registered_count >= game.max_players:
                    game.status = GameStatus.FULL
                db.add(existing_reg)
                db.add(game)
                db.commit()
                db.refresh(existing_reg)
                return existing_reg
            else:
                raise FootGolfException("L'utilisateur est déjà inscrit à cette partie.")

        if game.registered_count >= game.max_players:
            raise FootGolfException("La partie est complète.", status_code=409)

        # Création de l'inscription
        new_reg = GamePlayer(
            game_id=game_id,
            user_id=user_id,
            status=RegistrationStatus.REGISTERED,
            start_order=game.registered_count + 1
        )
        game.registered_count += 1
        if game.registered_count >= game.max_players:
            game.status = GameStatus.FULL

        db.add(new_reg)
        db.add(game)
        db.commit()
        db.refresh(new_reg)
        return new_reg

    @staticmethod
    def cancel_registration(db: Session, game_id: uuid.UUID, user_id: uuid.UUID) -> GamePlayer:
        stmt = select(Game).where(Game.id == game_id).with_for_update()
        game = db.scalars(stmt).first()
        
        if not game:
            raise NotFoundError("Partie introuvable.")

        if game.status == GameStatus.IN_PROGRESS or game.status == GameStatus.FINISHED:
            raise FootGolfException("Impossible d'annuler l'inscription une fois la partie commencée.")

        stmt_player = select(GamePlayer).where(
            GamePlayer.game_id == game_id,
            GamePlayer.user_id == user_id,
            GamePlayer.status != RegistrationStatus.CANCELLED
        )
        existing_reg = db.scalars(stmt_player).first()

        if not existing_reg:
            raise FootGolfException("Inscription introuvable ou déjà annulée.")

        existing_reg.status = RegistrationStatus.CANCELLED
        game.registered_count = max(0, game.registered_count - 1)
        
        if game.status == GameStatus.FULL and game.registered_count < game.max_players:
            game.status = GameStatus.REGISTRATION_OPEN

        db.add(existing_reg)
        db.add(game)
        db.commit()
        db.refresh(existing_reg)
        return existing_reg
