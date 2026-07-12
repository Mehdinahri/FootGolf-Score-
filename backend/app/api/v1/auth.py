"""
Routeur d'authentification.
"""

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.auth import LoginRequest, LoginResponse, RefreshRequest, RefreshResponse
from app.schemas.common import ApiResponse, success_response
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter()


@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(
    request: Request,
    payload: LoginRequest,
    db: Session = Depends(deps.get_db),
) -> dict:
    """Connexion (email + mot de passe)."""
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    
    tokens = AuthService.authenticate(db, payload, ip_address=ip, user_agent=ua)
    return success_response("Connexion réussie", data=tokens.model_dump())


@router.post("/refresh", response_model=ApiResponse[RefreshResponse])
def refresh_token(
    request: Request,
    payload: RefreshRequest,
    db: Session = Depends(deps.get_db),
) -> dict:
    """Rafraîchir le token d'accès."""
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    
    tokens = AuthService.refresh(db, payload, ip_address=ip, user_agent=ua)
    return success_response("Token rafraîchi", data=tokens.model_dump())


@router.post("/logout", response_model=ApiResponse[None])
def logout(
    payload: RefreshRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """Déconnexion."""
    AuthService.logout(db, payload.refresh_token)
    return success_response("Déconnexion réussie")


@router.get("/me", response_model=ApiResponse[UserResponse])
def get_me(
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """Récupérer le profil de l'utilisateur connecté."""
    return success_response("Profil récupéré", data=current_user)
