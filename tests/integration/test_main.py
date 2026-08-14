from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_invalid_short_code(client: TestClient):
    response = client.get("/abcd1234", follow_redirects=False)
    assert response.status_code == 404

def test_successful_short_code(client: TestClient, db_session: Session):
    response = client.get("/a2df55sa", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://fastapi.tiangolo.com/tutorial/query-params"
