from src.shorten import create_short_code


def test_create_short_code(monkeypatch):
    monkeypatch.setattr("src.shorten.choices", lambda chars, k: list("abcd1234"))
    short_code = create_short_code()
    assert short_code == "abcd1234"