from typing import Any
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.repositories.course_repo import course_repo
from app.repositories.hole_repo import hole_repo
from app.schemas.common import ApiResponse, success_response, paginated_response
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse, CourseBrief
from app.schemas.hole import HoleCreate, HoleBulkCreate, HoleUpdate, HoleResponse
from app.core.exceptions import NotFoundError, FootGolfException

router = APIRouter()

# ── COURSES ─────────────────────────────────────────────────────────

@router.get("", response_model=ApiResponse)
def list_courses(db: Session = Depends(deps.get_db)) -> dict:
    """Récupérer la liste des parcours actifs."""
    courses = course_repo.get_multi(db, limit=100)
    # Dans une vraie app on pourrait filtrer sur is_active=True pour les joueurs
    items = [CourseBrief.model_validate(c).model_dump() for c in courses]
    return paginated_response(items=items, total=len(items), page=1, page_size=100)

@router.get("/{course_id}", response_model=ApiResponse[CourseResponse])
def get_course(course_id: uuid.UUID, db: Session = Depends(deps.get_db)) -> dict:
    course = course_repo.get(db, id=course_id)
    if not course:
        raise NotFoundError("Parcours introuvable")
    return success_response(data=CourseResponse.model_validate(course).model_dump())

@router.post("/admin", response_model=ApiResponse[CourseResponse])
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> dict:
    """[ADMIN] Créer un parcours."""
    course = course_repo.create(db, obj_in=course_in)
    return success_response("Parcours créé avec succès", data=CourseResponse.model_validate(course).model_dump())

@router.put("/admin/{course_id}", response_model=ApiResponse[CourseResponse])
def update_course(
    course_id: uuid.UUID,
    course_in: CourseUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> dict:
    """[ADMIN] Modifier un parcours."""
    course = course_repo.get(db, id=course_id)
    if not course:
        raise NotFoundError("Parcours introuvable")
    course = course_repo.update(db, db_obj=course, obj_in=course_in)
    return success_response("Parcours modifié avec succès", data=CourseResponse.model_validate(course).model_dump())

@router.delete("/admin/{course_id}", response_model=ApiResponse[None])
def delete_course(
    course_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> dict:
    """[ADMIN] Supprimer un parcours."""
    course = course_repo.delete(db, id=course_id)
    if not course:
        raise NotFoundError("Parcours introuvable")
    return success_response("Parcours supprimé avec succès")


# ── HOLES ───────────────────────────────────────────────────────────

@router.get("/{course_id}/holes", response_model=ApiResponse)
def get_course_holes(course_id: uuid.UUID, db: Session = Depends(deps.get_db)) -> dict:
    """Récupérer les trous d'un parcours."""
    course = course_repo.get(db, id=course_id)
    if not course:
        raise NotFoundError("Parcours introuvable")
    holes = hole_repo.get_by_course(db, course_id=course_id)
    items = [HoleResponse.model_validate(h).model_dump() for h in holes]
    return success_response(data=items)

@router.post("/admin/{course_id}/holes/bulk", response_model=ApiResponse)
def bulk_create_holes(
    course_id: uuid.UUID,
    holes_in: HoleBulkCreate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin),
) -> dict:
    """[ADMIN] Créer en lot les trous pour un parcours (exactement 1 à 18)."""
    course = course_repo.get(db, id=course_id)
    if not course:
        raise NotFoundError("Parcours introuvable")
        
    if len(holes_in.holes) != 18:
        raise FootGolfException("Il faut exactement 18 trous.")

    # Vérification que les numéros 1 à 18 sont présents exactement une fois
    numbers = set(h.hole_number for h in holes_in.holes)
    if len(numbers) != 18 or min(numbers) != 1 or max(numbers) != 18:
        raise FootGolfException("Les numéros de trous doivent aller de 1 à 18 sans doublons.")

    # On supprime d'abord les trous existants pour ce parcours si on refait le bulk
    existing_holes = hole_repo.get_by_course(db, course_id=course_id)
    for h in existing_holes:
        db.delete(h)
    db.commit()

    created_holes = []
    from app.models.hole import HoleSection, Hole
    for h_in in holes_in.holes:
        section = HoleSection.OUTWARD if h_in.hole_number <= 9 else HoleSection.INWARD
        new_hole = Hole(
            course_id=course_id,
            hole_number=h_in.hole_number,
            distance=h_in.distance,
            par=h_in.par,
            description=h_in.description,
            difficulty=h_in.difficulty,
            section=section
        )
        db.add(new_hole)
        created_holes.append(new_hole)
    
    db.commit()
    return success_response("Trous créés avec succès")
