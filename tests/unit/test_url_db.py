from datetime import date

from src.models.url import Url


def test_create_url(db_session):
    url = Url(full="https://docs.sqlalchemy.org/en/20/orm/quickstart.html", short="5aa32bhh", creation_date=date.today(), expiration_date=date.today())
    db_session.add(url)
    db_session.commit()
    assert db_session.query(Url).count() == 1