from app.repositories.base import BaseRepository
from app.repositories.user_repo import user_repo, UserRepository
from app.repositories.course_repo import course_repo, CourseRepository
from app.repositories.hole_repo import hole_repo, HoleRepository
from app.repositories.game_repo import game_repo, GameRepository
from app.repositories.game_player_repo import game_player_repo, GamePlayerRepository

__all__ = [
    "BaseRepository",
    "UserRepository", "user_repo",
    "CourseRepository", "course_repo",
    "HoleRepository", "hole_repo",
    "GameRepository", "game_repo",
    "GamePlayerRepository", "game_player_repo",
]
