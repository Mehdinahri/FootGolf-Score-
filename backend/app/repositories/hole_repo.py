from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.hole import Hole
from app.repositories.base import BaseRepository

class HoleRepository(BaseRepository[Hole]):
    def get_by_course(self, db: Session, course_id: UUID) -> List[Hole]:
        stmt = select(Hole).where(Hole.course_id == course_id).order_by(Hole.hole_number)
        return list(db.scalars(stmt).all())

hole_repo = HoleRepository(Hole)
