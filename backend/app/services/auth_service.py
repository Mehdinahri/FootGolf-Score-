"""
Service d'authentification.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core import security
from app.core.exceptions import AuthenticationError, InactiveUserError, NotFoundError
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.user_repo import user_repo
from app.schemas.auth import LoginRequest, LoginResponse, RefreshRequest, RefreshResponse


class AuthService:
    """Service gérant la logique d'authentification."""

    @staticmethod
    def authenticate(db: Session, request: LoginRequest, ip_address: str | None = None, user_agent: str | None = None) -> LoginResponse:
        """Vérifie les identifiants et génère les tokens."""
        user = user_repo.get_by_email(db, email=request.email)
        if not user or not security.verify_password(request.password, user.password_hash):
            raise AuthenticationError("Email ou mot de passe incorrect.")

        if not user.is_active:
            raise InactiveUserError()

        # Mettre à jour la date de dernière connexion
        user.last_login_at = datetime.now(timezone.utc)
        db.add(user)

        return AuthService._generate_tokens(db, user, ip_address, user_agent)

    @staticmethod
    def register(db: Session, request: "RegisterRequest", ip_address: str | None = None, user_agent: str | None = None) -> LoginResponse:
        """Crée un nouvel utilisateur et le connecte immédiatement."""
        from app.schemas.auth import RegisterRequest
        from app.core.exceptions import FootGolfException
        from app.models.user import UserRole

        # Vérifier si l'email existe déjà
        existing_user = user_repo.get_by_email(db, email=request.email)
        if existing_user:
            raise FootGolfException(message="Cet email est déjà utilisé.", status_code=400)

        # Créer l'utilisateur
        new_user = User(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            password_hash=security.hash_password(request.password),
            role=UserRole.PLAYER,
            is_active=True,
            last_login_at=datetime.now(timezone.utc)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Connecter l'utilisateur
        return AuthService._generate_tokens(db, new_user, ip_address, user_agent)

    @staticmethod
    def refresh(db: Session, request: RefreshRequest, ip_address: str | None = None, user_agent: str | None = None) -> RefreshResponse:
        """Rafraîchit l'access token à partir d'un refresh token valide."""
        try:
            payload = security.decode_token(request.refresh_token)
            if payload.get("type") != "refresh":
                raise AuthenticationError("Token invalide.")
        except Exception:
            raise AuthenticationError("Token expiré ou invalide.")

        user_id = payload.get("sub")
        jti = payload.get("jti")
        
        user = user_repo.get(db, id=uuid.UUID(user_id))
        if not user or not user.is_active:
             raise AuthenticationError("Utilisateur introuvable ou désactivé.")

        # Vérifier le refresh token en DB
        token_hash = security.hash_token(request.refresh_token)
        stmt = select(RefreshToken).where(
            RefreshToken.user_id == user.id,
            RefreshToken.token_hash == token_hash,
            RefreshToken.is_revoked == False
        )
        db_token = db.scalars(stmt).first()

        if not db_token or db_token.is_expired:
             raise AuthenticationError("Token expiré ou révoqué.")

        # Révoquer l'ancien token pour la rotation
        db_token.is_revoked = True
        db.add(db_token)

        new_tokens = AuthService._generate_tokens(db, user, ip_address, user_agent)
        return RefreshResponse(**new_tokens.model_dump())

    @staticmethod
    def logout(db: Session, refresh_token: str) -> None:
        """Déconnecte l'utilisateur en révoquant son refresh token."""
        token_hash = security.hash_token(refresh_token)
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        db_token = db.scalars(stmt).first()
        if db_token:
            db_token.is_revoked = True
            db.add(db_token)
            db.commit()

    @staticmethod
    def _generate_tokens(db: Session, user: User, ip_address: str | None, user_agent: str | None) -> LoginResponse:
        from app.core.config import settings

        access_token = security.create_access_token(subject=user.id, role=user.role.value)
        refresh_token = security.create_refresh_token(subject=user.id)
        
        # Sauvegarder le refresh token en DB
        from datetime import timedelta
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        db_rt = RefreshToken(
            user_id=user.id,
            token_hash=security.hash_token(refresh_token),
            expires_at=expire,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(db_rt)
        db.commit()

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
