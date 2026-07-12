import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import date
import uuid

from app.models.user import User, UserRole
from app.models.course import Course
from app.models.hole import Hole, HoleSection
from app.models.game import Game, GameStatus
from app.models.game_player import GamePlayer, RegistrationStatus
from app.models.score import Score, ScoreStatus
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
        
    p1 = db_session.query(User).filter_by(email="p1@test.com").first()
    if not p1:
        p1 = User(first_name="Player1", last_name="One", email="p1@test.com", password_hash=security.hash_password("password"), role=UserRole.PLAYER)
        db_session.add(p1)

    p2 = db_session.query(User).filter_by(email="p2@test.com").first()
    if not p2:
        p2 = User(first_name="Player2", last_name="Two", email="p2@test.com", password_hash=security.hash_password("password"), role=UserRole.PLAYER)
        db_session.add(p2)
        
    db_session.commit()
    
    a_resp = client.post("/api/v1/auth/login", json={"email": "admin@test.com", "password": "password"})
    return a_resp.json()["data"]["access_token"], p1, p2

def test_leaderboard(client: TestClient, db_session: Session):
    admin_token, p1, p2 = get_tokens(client, db_session)
    
    course = Course(name="Leaderboard Course", hole_count=18, par_total=72, distance_total=2000)
    db_session.add(course)
    db_session.commit()

    holes = []
    for i in range(18):
        h = Hole(course_id=course.id, hole_number=i+1, par=4, distance=150, section=HoleSection.OUTWARD if i < 9 else HoleSection.INWARD)
        db_session.add(h)
        holes.append(h)
    db_session.commit()

    game = Game(
        title="Leaderboard Game",
        course_id=course.id,
        organizer_id=p1.id,
        start_date=date.today(),
        status=GameStatus.IN_PROGRESS,
        registered_count=2
    )
    db_session.add(game)
    db_session.commit()

    db_session.add(GamePlayer(game_id=game.id, user_id=p1.id, status=RegistrationStatus.REGISTERED, start_order=1))
    db_session.add(GamePlayer(game_id=game.id, user_id=p2.id, status=RegistrationStatus.REGISTERED, start_order=2))
    db_session.commit()

    # Scores
    s1 = Score(game_id=game.id, player_id=p1.id, hole_id=holes[0].id, strokes=5, penalties=0, total_score=5, status=ScoreStatus.VALIDATED)
    s2 = Score(game_id=game.id, player_id=p2.id, hole_id=holes[0].id, strokes=3, penalties=0, total_score=3, status=ScoreStatus.VALIDATED)
    db_session.add(s1)
    db_session.add(s2)
    db_session.commit()

    resp = client.get(f"/api/v1/games/{game.id}/leaderboard")
    assert resp.status_code == 200
    rows = resp.json()["data"]["rows"]
    
    assert len(rows) == 2
    # Player 2 should be first because 3 < 5
    assert rows[0]["player_id"] == str(p2.id)
    assert rows[0]["position"] == 1
    assert rows[0]["relative_to_par"] == -1  # 3 - 4 = -1
    
    assert rows[1]["player_id"] == str(p1.id)
    assert rows[1]["position"] == 2
    assert rows[1]["relative_to_par"] == 1   # 5 - 4 = 1

    # WebSocket connection test
    with client.websocket_connect(f"/ws/games/{game.id}/leaderboard") as websocket:
        data = websocket.receive_json()
        assert data["type"] == "LEADERBOARD_UPDATE"
        assert len(data["data"]["rows"]) == 2
