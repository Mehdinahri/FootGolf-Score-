"""
Package models — Importe tous les modèles ORM.

Cet import centralisé est nécessaire pour que :
- Alembic détecte toutes les tables
- SQLAlchemy résout toutes les relations
"""

from app.models.user import User, UserRole  # noqa: F401
from app.models.course import Course  # noqa: F401
from app.models.hole import Hole, HoleSection  # noqa: F401
from app.models.game import Game, GameStatus, TiebreakerRule, VALID_TRANSITIONS  # noqa: F401
from app.models.game_player import GamePlayer, RegistrationStatus, AttendanceStatus  # noqa: F401
from app.models.score import Score, ScoreStatus  # noqa: F401
from app.models.score_history import ScoreHistory  # noqa: F401
from app.models.refresh_token import RefreshToken  # noqa: F401
from app.models.notification import Notification, NotificationType  # noqa: F401
from app.models.audit_log import AuditLog  # noqa: F401
from app.models.offline_sync import OfflineSyncRequest, SyncStatus  # noqa: F401

__all__ = [
    "User", "UserRole",
    "Course",
    "Hole", "HoleSection",
    "Game", "GameStatus", "TiebreakerRule", "VALID_TRANSITIONS",
    "GamePlayer", "RegistrationStatus", "AttendanceStatus",
    "Score", "ScoreStatus",
    "ScoreHistory",
    "RefreshToken",
    "Notification", "NotificationType",
    "AuditLog",
    "OfflineSyncRequest", "SyncStatus",
]
