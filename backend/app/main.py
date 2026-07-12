"""
Point d'entrée de l'application FastAPI.
"""

import logging
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import FootGolfException
from app.core.middleware import setup_middleware
from app.schemas.common import error_response

# ── Logging ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("footgolf")

# ── Application ─────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

# ── Middleware ──────────────────────────────────────────────────
setup_middleware(app)

# ── Exception Handlers ──────────────────────────────────────────

@app.exception_handler(FootGolfException)
async def footgolf_exception_handler(request: Request, exc: FootGolfException) -> JSONResponse:
    """Gère nos exceptions métier."""
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=exc.message, errors=exc.errors),
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Gère les erreurs de validation Pydantic de façon formatée."""
    errors = []
    for err in exc.errors():
        field = ".".join(str(x) for x in err["loc"] if x != "body")
        errors.append({"field": field or "body", "message": err["msg"]})
        
    return JSONResponse(
        status_code=422,
        content=error_response(message="Erreur de validation", errors=errors),
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Fallback pour les erreurs non gérées."""
    logger.exception(f"Erreur inattendue: {exc}")
    return JSONResponse(
        status_code=500,
        content=error_response(message="Une erreur interne est survenue."),
    )

# ── Routers ─────────────────────────────────────────────────────
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

from app.api.ws import leaderboard as ws_leaderboard
app.include_router(ws_leaderboard.router, prefix="/ws")


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
