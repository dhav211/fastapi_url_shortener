from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.url import Url


def test_shorten(client: TestClient, monkeypatch: pytest.MonkeyPatch, db_session: Session):
    url_to_shorten = "https://docs.sqlalchemy.org/en/20/orm/quickstart.html"
    monkeypatch.setattr("src.routes.urls.create_short_code", lambda: "abcd1234")
    expected_url = Url(full=url_to_shorten, short="abcd1234", creation_date=date.today(), expiration_date=date.today())
    response = client.post("/api/v1/urls/", params= {"url_shorten": url_to_shorten})

    saved_url = db_session.query(Url).filter(Url.short == "abcd1234").first()
    
    assert response.status_code == 200
    assert response.json()["short"] == expected_url.short
    assert saved_url is not None

def test_full_address_already_in_db(client: TestClient):
    used_address = "https://fastapi.tiangolo.com/tutorial/query-params/"
    response = client.post("/api/v1/urls/", params= {"url_shorten": used_address})

    assert response.status_code == 409

def test_short_code_already_in_db(client: TestClient, db_session: Session, monkeypatch: pytest.MonkeyPatch):
    url_to_shorten = "https://developer.apple.com/documentation/uikit/uitableview"

    call_count = 0

    def fake_create_short_code():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return "a2df55sa"   # collides with existing row -> triggers retry
        return "b33f0ad8"      # unique -> loop exits

    monkeypatch.setattr("src.routes.urls.create_short_code", fake_create_short_code)    
    response = client.post("/api/v1/urls/", params= {"url_shorten": url_to_shorten})

    saved_url = db_session.query(Url).filter_by(full= "developer.apple.com/documentation/uikit/uitableview").first()

    assert saved_url is not None
    assert response.status_code == 200
    assert saved_url.short == "b33f0ad8"

def test_invalid_url(monkeypatch: pytest.MonkeyPatch, client: TestClient):
    bad_url = "http://asdfgasfgasdfaserjkljvu.com"
    monkeypatch.setattr("src.routes.urls.create_short_code", lambda: "abcd1234")
    response = client.post("/api/v1/urls/", params= {"url_shorten": bad_url})

    
    assert response.status_code == 400