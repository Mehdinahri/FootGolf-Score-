"""
Configuration de l'application.

Charge les variables d'environnement depuis le fichier .env
et les expose via l'objet singleton `settings`.
"""

import logging
from pydantic_settings import BaseSettings

logger = logging.getLogger("footgolf")

_INSECURE_SECRET_KEYS = {
    "change-this-secret-key-in-production",
    "dev-secret-key-change-in-production-use-openssl-rand-hex-32",
}


class Settings(BaseSettings):
    """Paramètres globaux de l'application FootGolf Score."""

    # ── Application ─────────────────────────────────────────────
    APP_NAME: str = "FootGolf Score"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # ── Database ────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql://footgolf:footgolf_secret@localhost:5432/footgolf_db"
    DATABASE_TEST_URL: str = "postgresql://footgolf:footgolf_secret@localhost:5432/footgolf_test_db"
    DB_ECHO: bool = False

    # ── JWT ─────────────────────────────────────────────────────
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── CORS ────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # ── Rate limiting ───────────────────────────────────────────
    LOGIN_RATE_LIMIT_ATTEMPTS: int = 5
    LOGIN_RATE_LIMIT_MINUTES: int = 15

    # ── Admin initial ───────────────────────────────────────────
    ADMIN_EMAIL: str = "admin@footgolf.com"
    ADMIN_PASSWORD: str = "Admin123!"
    ADMIN_FIRST_NAME: str = "Admin"
    ADMIN_LAST_NAME: str = "FootGolf"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore",
    }


settings = Settings()

# ── Startup Security Checks ────────────────────────────────────
if settings.SECRET_KEY in _INSECURE_SECRET_KEYS:
    if not settings.DEBUG:
        logger.critical(
            "🔴 CRITICAL: SECRET_KEY is set to an insecure default value! "
            "Generate a secure key with: python -c \"import secrets; print(secrets.token_hex(32))\" "
            "and set it in your .env file. The application should NOT run in production with this key."
        )
    else:
        logger.warning(
            "⚠️  SECRET_KEY is using a development default. "
            "Remember to change it before deploying to production."
        )

