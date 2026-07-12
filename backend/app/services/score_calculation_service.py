import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.models.score import Score, ScoreStatus
from app.models.hole import HoleSection
from app.repositories.score_repo import score_repo
from app.repositories.hole_repo import hole_repo
from app.repositories.game_repo import game_repo
from app.repositories.course_repo import course_repo
from app.models.user import User

class ScoreCalculationService:
    @staticmethod
    def calculate_scorecard(db: Session, game_id: uuid.UUID, player_user: User) -> Dict[str, Any]:
        game = game_repo.get(db, id=game_id)
        if not game:
            return {}
            
        course = course_repo.get(db, id=game.course_id)
        holes = hole_repo.get_by_course(db, course_id=course.id)
        scores = score_repo.get_by_game_and_player(db, game_id=game_id, player_id=player_user.id)
        
        scores_by_hole = {s.hole_id: s for s in scores}
        
        outward_total = 0
        return_total = 0
        par_played = 0
        strokes_played = 0
        completed_holes = 0
        current_hole = 1
        
        holes_dto = []
        
        for h in holes:
            score = scores_by_hole.get(h.id)
            score_data = {
                "id": None,
                "strokes": None,
                "penalties": 0,
                "total": None,
                "status": None,
                "sync_status": None
            }
            
            if score:
                score_total = score.strokes + score.penalties
                score_data = {
                    "id": str(score.id),
                    "strokes": score.strokes,
                    "penalties": score.penalties,
                    "total": score_total,
                    "status": score.status.value
                }
                
                if h.section == HoleSection.OUTWARD:
                    outward_total += score_total
                else:
                    return_total += score_total
                    
                strokes_played += score_total
                par_played += h.par
                completed_holes += 1
            elif current_hole == completed_holes + 1:
                # C'est le trou actuel
                current_hole = h.hole_number

            holes_dto.append({
                "id": str(h.id),
                "hole_number": h.hole_number,
                "distance": h.distance,
                "par": h.par,
                "section": h.section.value,
                "score": score_data
            })
            
        total = outward_total + return_total
        relative_to_par = total - par_played if completed_holes > 0 else 0
        
        if completed_holes == len(holes):
            current_hole = len(holes)

        return {
            "game": {
                "id": str(game.id),
                "title": game.title,
                "status": game.status.value
            },
            "course": {
                "id": str(course.id),
                "name": course.name,
                "total_par": course.par_total
            },
            "player": {
                "id": str(player_user.id),
                "first_name": player_user.first_name,
                "last_name": player_user.last_name
            },
            "progress": {
                "completed_holes": completed_holes,
                "current_hole": current_hole,
                "total_holes": len(holes)
            },
            "totals": {
                "outward": outward_total,
                "return": return_total,
                "total": total,
                "relative_to_par": relative_to_par
            },
            "holes": holes_dto
        }
