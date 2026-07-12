from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.course import Course
from app.repositories.base import BaseRepository

class CourseRepository(BaseRepository[Course]):
    pass

course_repo = CourseRepository(Course)
