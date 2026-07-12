"""
Export de tous les schémas.
"""

from app.schemas.common import ApiResponse, PaginatedResponse, PaginatedData, FieldError, success_response, error_response, paginated_response
from app.schemas.auth import LoginRequest, LoginResponse, RefreshRequest, RefreshResponse, ForgotPasswordRequest, ResetPasswordRequest, TokenPayload
from app.schemas.user import UserCreate, UserUpdate, UserStatusUpdate, UserProfileUpdate, ChangePasswordRequest, UserResponse, UserBrief
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse, CourseBrief
from app.schemas.hole import HoleCreate, HoleBulkCreate, HoleUpdate, HoleResponse
from app.schemas.game import GameCreate, GameUpdate, GameResponse, GameBrief
from app.schemas.game_player import GamePlayerCreate, GamePlayerUpdate, GamePlayerResponse
from app.schemas.score import ScoreCreate, ScoreUpdate, ScoreCorrection, ScoreResponse
from app.schemas.leaderboard import LeaderboardRow, LeaderboardResponse
from app.schemas.notification import NotificationResponse

__all__ = [
    "ApiResponse", "PaginatedResponse", "PaginatedData", "FieldError", "success_response", "error_response", "paginated_response",
    "LoginRequest", "LoginResponse", "RefreshRequest", "RefreshResponse", "ForgotPasswordRequest", "ResetPasswordRequest", "TokenPayload",
    "UserCreate", "UserUpdate", "UserStatusUpdate", "UserProfileUpdate", "ChangePasswordRequest", "UserResponse", "UserBrief",
    "CourseCreate", "CourseUpdate", "CourseResponse", "CourseBrief",
    "HoleCreate", "HoleBulkCreate", "HoleUpdate", "HoleResponse",
    "GameCreate", "GameUpdate", "GameResponse", "GameBrief",
    "GamePlayerCreate", "GamePlayerUpdate", "GamePlayerResponse",
    "ScoreCreate", "ScoreUpdate", "ScoreCorrection", "ScoreResponse",
    "LeaderboardRow", "LeaderboardResponse",
    "NotificationResponse",
]
