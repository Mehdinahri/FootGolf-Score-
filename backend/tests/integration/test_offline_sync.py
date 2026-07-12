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
    player = db_session.query(User).filter_by(email="player_sync@test.com").first()
    if not player:
        player = User(
            first_name="PlayerSync",
            last_name="Test",
            email="player_sync@test.com",
            password_hash=security.hash_password("password"),
            role=UserRole.PLAYER,
        )
        db_session.add(player)
        db_session.commit()
    
    p_resp = client.post("/api/v1/auth/login", json={"email": "player_sync@test.com", "password": "password"})
    return p_resp.json()["data"]["access_token"], player

def test_offline_sync(client: TestClient, db_session: Session):
    token, player = get_tokens(client, db_session)
    
    course = Course(name="Sync Course", hole_count=18, par_total=72, distance_total=2000)
    db_session.add(course)
    db_session.commit()

    holes = []
    for i in range(18):
        h = Hole(course_id=course.id, hole_number=i+1, par=4, distance=150, section=HoleSection.OUTWARD if i < 9 else HoleSection.INWARD)
        db_session.add(h)
        holes.append(h)
    db_session.commit()

    game = Game(
        title="Sync Game",
        course_id=course.id,
        organizer_id=player.id,
        start_date=date.today(),
        status=GameStatus.IN_PROGRESS,
        registered_count=1
    )
    db_session.add(game)
    db_session.commit()

    db_session.add(GamePlayer(game_id=game.id, user_id=player.id, status=RegistrationStatus.REGISTERED, start_order=1))
    db_session.commit()

    idemp_key1 = str(uuid.uuid4())
    idemp_key2 = str(uuid.uuid4())

    payload = {
        "game_id": str(game.id),
        "scores": [
            {
                "hole_id": str(holes[0].id),
                "strokes": 4,
                "penalties": 0,
                "idempotency_key": idemp_key1
            },
            {
                "hole_id": str(holes[1].id),
                "strokes": 5,
                "penalties": 1,
                "idempotency_key": idemp_key2
            }
        ]
    }

    resp = client.post(
        "/api/v1/offline-sync/scores",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert resp.status_code == 200
    data = resp.json()["data"]["results"]
    assert len(data) == 2
    assert data[0]["status"] == "success"
    assert data[1]["status"] == "success"

    # Verify scores in db
    scores = db_session.query(Score).filter_by(game_id=game.id, player_id=player.id).all()
    assert len(scores) == 2

    # Resync with same keys should be idempotent
    resp = client.post(
        "/api/v1/offline-sync/scores",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.json()["data"]["results"]
    assert len(data) == 2
    assert data[0]["status"] == "success" # treated as success because already handled
    
    # Verify no duplication
    scores = db_session.query(Score).filter_by(game_id=game.id, player_id=player.id).all()
    assert len(scores) == 2
