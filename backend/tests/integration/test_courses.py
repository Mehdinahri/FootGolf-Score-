import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid

from app.models.user import User, UserRole
from app.models.course import Course
from app.core import security

def get_admin_token(client: TestClient, db_session: Session) -> str:
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
        db_session.commit()
        resp = client.post("/api/v1/auth/login", json={"email": "admin@test.com", "password": "password"})
        if resp.status_code != 200:
            print("LOGIN FAILED:", resp.json())
        return resp.json()["data"]["access_token"]
    
    resp = client.post("/api/v1/auth/login", json={"email": "admin@test.com", "password": "password"})
    return resp.json()["data"]["access_token"]

def test_create_course(client: TestClient, db_session: Session):
    token = get_admin_token(client, db_session)
    resp = client.post(
        "/api/v1/courses/admin",
        json={
            "name": "Test Course",
            "city": "Paris",
            "hole_count": 18
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["name"] == "Test Course"
    assert "id" in data

def test_bulk_create_holes(client: TestClient, db_session: Session):
    token = get_admin_token(client, db_session)
    # Create course first
    course = Course(name="Holes Course", hole_count=18, par_total=0, distance_total=0)
    db_session.add(course)
    db_session.commit()

    holes = []
    for i in range(1, 19):
        holes.append({"hole_number": i, "distance": 100, "par": 3})

    resp = client.post(
        f"/api/v1/courses/admin/{course.id}/holes/bulk",
        json={"holes": holes},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    
    # Check if they are retrieved
    resp_get = client.get(f"/api/v1/courses/{course.id}/holes")
    assert len(resp_get.json()["data"]) == 18

def test_bulk_create_holes_invalid_count(client: TestClient, db_session: Session):
    token = get_admin_token(client, db_session)
    course = Course(name="Holes Course 2", hole_count=18, par_total=0, distance_total=0)
    db_session.add(course)
    db_session.commit()

    holes = [{"hole_number": i, "distance": 100, "par": 3} for i in range(1, 10)] # Only 9 holes

    resp = client.post(
        f"/api/v1/courses/admin/{course.id}/holes/bulk",
        json={"holes": holes},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 400
