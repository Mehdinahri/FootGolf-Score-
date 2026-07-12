import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.game import Game
from app.models.user import User
from app.models.score import Score
from app.models.game_player import GamePlayer
from app.repositories.course_repo import course_repo
from app.repositories.hole_repo import hole_repo

class LeaderboardService:
    @staticmethod
    def get_leaderboard(db: Session, game: Game) -> Dict[str, Any]:
        """Calcule le classement en direct."""
        course = course_repo.get(db, id=game.course_id)
        holes = hole_repo.get_by_course(db, course_id=course.id)
        total_par = sum(h.par for h in holes)

        # Récupérer les joueurs inscrits
        stmt_players = select(GamePlayer, User).join(User).where(GamePlayer.game_id == game.id)
        players = db.execute(stmt_players).all()

        # Récupérer tous les scores
        stmt_scores = select(Score).where(Score.game_id == game.id)
        scores = db.scalars(stmt_scores).all()

        # Calculer le score de chaque joueur
        results = []
        for gp, user in players:
            player_scores = [s for s in scores if s.player_id == user.id]
            holes_completed = len(player_scores)
            
            strokes = sum(s.strokes for s in player_scores)
            penalties = sum(s.penalties for s in player_scores)
            total_score = strokes + penalties
            
            # Calcul du relative_to_par par rapport aux trous joués
            par_played = sum(h.par for h in holes if h.id in [s.hole_id for s in player_scores])
            relative_to_par = total_score - par_played if holes_completed > 0 else 0

            results.append({
                "player_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "total_score": total_score,
                "relative_to_par": relative_to_par,
                "holes_completed": holes_completed,
                "is_dnf": False # À implémenter si besoin
            })

        # Trier: plus bas score d'abord, puis plus grand nombre de trous joués
        results.sort(key=lambda x: (x["relative_to_par"], -x["holes_completed"]))

        # Assigner les positions
        for i, row in enumerate(results):
            row["position"] = i + 1

        return {
            "game_id": game.id,
            "status": game.status.value,
            "rows": results
        }
