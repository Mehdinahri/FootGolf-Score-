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

def test_score_lifecycle(client: TestClient, db_session: Session):
    admin_token, player_token, player_id = get_tokens(client, db_session)
    
    # Setup data
    course = Course(name="Score Course", hole_count=18, par_total=72, distance_total=2000)
    db_session.add(course)
    db_session.commit()

    holes = []
    for i in range(18):
        h = Hole(course_id=course.id, hole_number=i+1, par=4, distance=150, section=HoleSection.OUTWARD if i < 9 else HoleSection.INWARD)
        db_session.add(h)
        holes.append(h)
    db_session.commit()

    game = Game(
        title="Score Game",
        course_id=course.id,
        organizer_id=db_session.query(User).first().id,
        start_date=date.today(),
        status=GameStatus.IN_PROGRESS,
        registered_count=1
    )
    db_session.add(game)
    db_session.commit()

    # Player registered
    reg = GamePlayer(game_id=game.id, user_id=player_id, status=RegistrationStatus.REGISTERED, start_order=1)
    db_session.add(reg)
    db_session.commit()

    import uuid
    idemp_key1 = str(uuid.uuid4())
    idemp_key2 = str(uuid.uuid4())
    idemp_key3 = str(uuid.uuid4())
    idemp_key4 = str(uuid.uuid4())

    # 1. Create a score
    resp = client.post(
        f"/api/v1/games/{game.id}/scores",
        json={"hole_id": str(holes[0].id), "strokes": 4, "penalties": 1, "idempotency_key": idemp_key1},
        headers={"Authorization": f"Bearer {player_token}"}
    )
    assert resp.status_code == 200
    score_id = resp.json()["data"]["id"]
    assert resp.json()["data"]["total_score"] == 5

    # 2. Check scorecard updates
    resp = client.get(f"/api/v1/games/{game.id}/scorecard", headers={"Authorization": f"Bearer {player_token}"})
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["progress"]["completed_holes"] == 1
    assert data["totals"]["outward"] == 5
    assert data["totals"]["total"] == 5
    assert data["totals"]["relative_to_par"] == 1 # par is 4, total is 5

    # 3. Duplicate score on same hole should fail
    resp = client.post(
        f"/api/v1/games/{game.id}/scores",
        json={"hole_id": str(holes[0].id), "strokes": 3, "penalties": 0, "idempotency_key": idemp_key2},
        headers={"Authorization": f"Bearer {player_token}"}
    )
    assert resp.status_code == 400 or resp.status_code == 409

    # 4. Update score
    resp = client.put(
        f"/api/v1/games/{game.id}/scores/{score_id}",
        json={"strokes": 3, "idempotency_key": idemp_key3},
        headers={"Authorization": f"Bearer {player_token}"}
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["total_score"] == 4 # 3 + 1 penalty

    # 5. Validate score
    resp = client.post(f"/api/v1/games/{game.id}/scores/{score_id}/validate", headers={"Authorization": f"Bearer {player_token}"})
    assert resp.status_code == 200

    # 6. Cannot update validated score
    resp = client.put(
        f"/api/v1/games/{game.id}/scores/{score_id}",
        json={"strokes": 2, "idempotency_key": idemp_key4},
        headers={"Authorization": f"Bearer {player_token}"}
    )
    assert resp.status_code == 400
