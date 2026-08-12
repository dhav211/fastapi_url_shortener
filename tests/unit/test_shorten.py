from src.shorten import create_short_code, strip_url


def test_create_short_code(monkeypatch):
    monkeypatch.setattr("src.shorten.choices", lambda chars, k: list("abcd1234"))
    short_code = create_short_code()
    assert short_code == "abcd1234"

def test_strip_url_with_https():
    assert strip_url("https://docs.sqlalchemy.org/en/20/orm/quickstart.html") == "docs.sqlalchemy.org/en/20/orm/quickstart.html"

def test_strip_url_with_trailing_slash():
    assert strip_url("https://www.boredpanda.com/most-destructive-thing-cat-ever-done/") == "boredpanda.com/most-destructive-thing-cat-ever-done"