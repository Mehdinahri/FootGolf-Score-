import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import date, timedelta
import threading

from app.models.user import User, UserRole
from app.models.course import Course
from app.models.game import Game, GameStatus
from app.models.hole import Hole, HoleSection
from app.core import security

def get_tokens(client: TestClient, db_session: Session):
    admin = db_session.query(User).filter_by(email="admin@test.com").first()
    if not admin:
        admin = User(
            first_name="Admin",
            last_name="Test",
            email="admin@test.com",
            password_hash=security.hash_password("password"),
            role=UserRole.ADMIN,
        )
        db_session.add(admin)
        
    player = db_session.query(User).filter_by(email="player@test.com").first()
    if not player:
        player = User(
            first_name="Player",
            last_name="Test",
            email="player@test.com",
            password_hash=security.hash_password("password"),
            role=UserRole.PLAYER,
        )
        db_session.add(player)
    db_session.commit()
    
    a_resp = client.post("/api/v1/auth/login", json={"email": "admin@test.com", "password": "password"})
    p_resp = client.post("/api/v1/auth/login", json={"email": "player@test.com", "password": "password"})
    return a_resp.json()["data"]["access_token"], p_resp.json()["data"]["access_token"], player.id

def test_game_creation_and_registration(client: TestClient, db_session: Session):
    admin_token, player_token, player_id = get_tokens(client, db_session)
    
    # Create course
    course = Course(name="Game Course", hole_count=18, par_total=72, distance_total=2000)
    db_session.add(course)
    db_session.commit()
    
    # Create game
    game_data = {
        "title": "Test Game",
        "course_id": str(course.id),
        "start_date": (date.today() + timedelta(days=1)).isoformat(),
        "max_players": 5
    }
    resp = client.post("/api/v1/games/admin", json=game_data, headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    game_id = resp.json()["data"]["id"]

    # Player tries to register (should fail, status DRAFT)
    resp = client.post(f"/api/v1/games/{game_id}/register", headers={"Authorization": f"Bearer {player_token}"})
    assert resp.status_code == 400

    # Open registration
    resp = client.post(f"/api/v1/games/admin/{game_id}/open-registration", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200

    # Player registers successfully
    resp = client.post(f"/api/v1/games/{game_id}/register", headers={"Authorization": f"Bearer {player_token}"})
    assert resp.status_code == 200
    
    # Player lists players
    resp = client.get(f"/api/v1/games/{game_id}/players", headers={"Authorization": f"Bearer {player_token}"})
    assert len(resp.json()["data"]) == 1

def test_game_start_requires_18_holes(client: TestClient, db_session: Session):
    admin_token, player_token, player_id = get_tokens(client, db_session)
    course = Course(name="Empty Course", hole_count=18, par_total=0, distance_total=0)
    db_session.add(course)
    db_session.commit()
    
    game = Game(
        title="Start Game",
        course_id=course.id,
        organizer_id=db_session.query(User).first().id,
        start_date=date.today(),
        status=GameStatus.REGISTRATION_CLOSED,
        registered_count=1
    )
    db_session.add(game)
    db_session.commit()

    # Start without holes
    resp = client.post(f"/api/v1/games/admin/{game.id}/start", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 400
    assert "18 trous" in resp.json()["message"]

    # Add 18 holes
    for i in range(18):
        db_session.add(Hole(course_id=course.id, hole_number=i+1, par=3, distance=100, section=HoleSection.OUTWARD))
    db_session.commit()

    # Start with holes and players
    resp = client.post(f"/api/v1/games/admin/{game.id}/start", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "IN_PROGRESS"
