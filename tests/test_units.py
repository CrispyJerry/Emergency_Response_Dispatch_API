import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def fresh_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_unit():
    response = client.post("/api/units", json={"unit_type": "Ambulance", "station_location": "Dublin"})
    assert response.status_code == 201
    assert response.json()["callsign"] == "AMB-1"
    assert response.json()["status"] == "available"


def test_get_missing_unit_returns_404():
    response = client.get("/api/units/999")
    assert response.status_code == 404


def test_invalid_unit_type_returns_422():
    response = client.post("/api/units", json={"unit_type": "banana", "station_location": "Dublin"})
    assert response.status_code == 422


def test_invalid_status_transition_returns_400():
    unit_id = client.post("/api/units", json={"unit_type": "Ambulance", "station_location": "Dublin"}).json()["unit_id"]
    response = client.patch(f"/api/units/{unit_id}/status", json={"status": "arrived"})
    assert response.status_code == 400


def test_cannot_delete_active_unit():
    unit_id = client.post("/api/units", json={"unit_type": "Ambulance", "station_location": "Dublin"}).json()["unit_id"]
    client.patch(f"/api/units/{unit_id}/status", json={"status": "en_route"})
    response = client.delete(f"/api/units/{unit_id}")
    assert response.status_code == 409