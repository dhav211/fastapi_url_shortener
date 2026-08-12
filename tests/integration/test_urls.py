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

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

SEED_DATA = [
    ("fastapi.tiangolo.com/tutorial/query-params", "a2df55sa"),
    ("github.com/dhav211/fastapi_url_shortener", "04bba14a"),
    ("boredpanda.com/most-destructive-thing-cat-ever-done", "99fbc123"),
]

@pytest.fixture
def preloaded_db(db_session):
    for full, short in SEED_DATA:
        db_session.add(
            Url(
                full=full,
                short=short,
                creation_date=date.today(),
                expiration_date=date.today(),
            )
        )
    db_session.commit()
    return SEED_DATA

def test_shorten(client, monkeypatch):
    url_to_shorten = "https://docs.sqlalchemy.org/en/20/orm/quickstart.html"
    monkeypatch.setattr("src.routes.urls.create_short_code", lambda: "abcd1234")
    expected_url = Url(full=url_to_shorten, short="abcd1234", creation_date=date.today(), expiration_date=date.today())
    response = client.post(f"/api/v1/urls/{url_to_shorten}")

    db = TestingSessionLocal()
    saved_url = db.query(Url).filter(Url.short == "abcd1234").first()
    db.close()
    
    assert response.status_code == 200
    assert response.json()["short"] == expected_url.short
    assert saved_url is not None

def test_full_address_already_in_db(client, preloaded_db):
    used_address = "https://fastapi.tiangolo.com/tutorial/query-params/"
    response = client.post(f"/api/v1/urls/{used_address}")

    assert response.status_code == 409

def test_short_code_already_in_db(client, monkeypatch, preloaded_db):
    url_to_shorten = "https://developer.apple.com/documentation/uikit/uitableview"

    call_count = 0

    def fake_create_short_code():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return "a2df55sa"   # collides with existing row -> triggers retry
        return "b33f0ad8"      # unique -> loop exits

    monkeypatch.setattr("src.routes.urls.create_short_code", fake_create_short_code)    
    response = client.post(f"/api/v1/urls/{url_to_shorten}")

    db = TestingSessionLocal()
    saved_url = db.query(Url).filter_by(full= "developer.apple.com/documentation/uikit/uitableview").first()
    db.close()
    
    assert response.status_code == 200
    assert saved_url.short == "b33f0ad8"
