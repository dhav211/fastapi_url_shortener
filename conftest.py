import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.url import Base


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)      # build schema fresh
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session                          # test runs here

    session.close()
    Base.metadata.drop_all(engine)         # drop everything
    engine.dispose()