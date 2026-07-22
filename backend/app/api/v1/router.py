from fastapi import APIRouter

from app.api.v1 import auth, courses, games, scores, leaderboard, offline_sync, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(games.router, prefix="/games", tags=["games"])
api_router.include_router(scores.router, prefix="/games", tags=["scores"])
api_router.include_router(leaderboard.router, prefix="/games", tags=["leaderboard"])
api_router.include_router(offline_sync.router, prefix="/offline-sync", tags=["offline-sync"])
