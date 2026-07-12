"""
Configuration de la session SQLAlchemy.

Fournit :
- `engine` : moteur de connexion PostgreSQL
- `SessionLocal` : factory de sessions
- `get_db` : dépendance FastAPI injectant une session par requête
"""

from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Dépendance FastAPI : ouvre une session DB et la ferme après la requête."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
