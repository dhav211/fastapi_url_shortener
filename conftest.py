from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import get_db
from src.main import app
from src.models.url import Base, Url


SEED_DATA = [
    ("fastapi.tiangolo.com/tutorial/query-params", "a2df55sa"),
    ("github.com/dhav211/fastapi_url_shortener", "04bba14a"),
    ("boredpanda.com/most-destructive-thing-cat-ever-done", "99fbc123"),
]

@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    for full, short in SEED_DATA:
        session.add(
            Url(
                full=full,
                short=short,
                creation_date=date.today(),
                expiration_date=date.today(),
            )
        )
    session.commit()

    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
