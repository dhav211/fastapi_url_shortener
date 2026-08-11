from datetime import date
import pytest

from src.models.url import Url


@pytest.fixture()
def default_urls(db_session):
    urls = [
        Url(full="https://docs.sqlalchemy.org/en/20/orm/quickstart.html", short="5aa32bhh", creation_date=date.today(), expiration_date=date.today()),
        Url(full="https://github.com/dhav211/fastapi_url_shortener", short="82sg543s", creation_date=date.today(), expiration_date=date.today()),
        Url(full="https://www.boredpanda.com/most-destructive-thing-cat-ever-done/", short="al0sf8sf", creation_date=date.today(), expiration_date=date.today())
    ]
    db_session.add_all(urls)
    db_session.commit()


def test_remove_url_by_short(default_urls, db_session):
    url = db_session.query(Url).filter_by(short="82sg543s").first()

    if url:
        db_session.delete(url)
        db_session.commit()

    assert db_session.query(Url).count() == 2

def test_get_all_urls(default_urls, db_session):
    assert db_session.query(Url).count() == 3

def test_get_by_short(default_urls, db_session):
    url = db_session.query(Url).filter_by(short="82sg543s").first()
    assert url.short == "82sg543s"
