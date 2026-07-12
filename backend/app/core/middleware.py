"""
Middleware de l'application.

- CORS
- Logging des requêtes
- Header de sécurité
"""

from __future__ import annotations

import time
import logging
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

logger = logging.getLogger("footgolf")


def setup_middleware(app: FastAPI) -> None:
    """Configure tous les middleware de l'application."""

    # ── CORS ────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Logging & Timing ───────────────────────────────────────
    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        response: Response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "%s %s → %s (%.1f ms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response

    # ── Security headers ───────────────────────────────────────
    @app.middleware("http")
    async def add_security_headers(
        request: Request, call_next: Callable
    ) -> Response:
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response
