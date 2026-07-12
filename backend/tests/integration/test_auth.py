import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core import security
from app.models.user import User, UserRole

def test_login_success(client: TestClient, db_session: Session):
    # Setup un utilisateur
    user = User(
        first_name="Test",
        last_name="User",
        email="test@footgolf.com",
        password_hash=security.hash_password("password123"),
        role=UserRole.PLAYER,
    )
    db_session.add(user)
    db_session.commit()

    # Tentative de login
    response = client.post(
        "/api/auth/login",
        json={"email": "test@footgolf.com", "password": "password123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]

def test_login_invalid_password(client: TestClient, db_session: Session):
    user = User(
        first_name="Test",
        last_name="User",
        email="test2@footgolf.com",
        password_hash=security.hash_password("password123"),
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/auth/login",
        json={"email": "test2@footgolf.com", "password": "wrongpassword"}
    )
    
    assert response.status_code == 401
    assert response.json()["success"] is False
    assert "Identifiants invalides" in response.json()["message"]

def test_login_inactive_user(client: TestClient, db_session: Session):
    user = User(
        first_name="Inactive",
        last_name="User",
        email="inactive@footgolf.com",
        password_hash=security.hash_password("password123"),
        is_active=False
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/auth/login",
        json={"email": "inactive@footgolf.com", "password": "password123"}
    )
    
    assert response.status_code == 403
    assert response.json()["success"] is False

def test_get_me(client: TestClient, db_session: Session):
    user = User(
        first_name="Me",
        last_name="User",
        email="me@footgolf.com",
        password_hash=security.hash_password("password123"),
    )
    db_session.add(user)
    db_session.commit()

    # Login to get token
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "me@footgolf.com", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]

    # Call /me
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["email"] == "me@footgolf.com"
    assert data["first_name"] == "Me"
