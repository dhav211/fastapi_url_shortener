from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.main import app
from src.models.url import Url

TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)

@

def test_shorten(client, monkeypatch):
    url_to_shorten = "fastapi.tiangolo.com/tutorial/query-params/"
    monkeypatch.setattr("src.routes.urls.create_short_code", lambda: "abcd1234")
    expected_url = Url(full=url_to_shorten, short="abcd1234", creation_date=date.today(), expiration_date=date.today())
    response = client.post(f"/api/v1/urls/{url_to_shorten}")

    db = TestingSessionLocal()
    saved_url = db.query(Url).filter(Url.short == "abcd1234").first()
    db.close()
    
    assert response.status_code == 200
    assert response.json()["short"] == expected_url.short
    assert saved_url is not None