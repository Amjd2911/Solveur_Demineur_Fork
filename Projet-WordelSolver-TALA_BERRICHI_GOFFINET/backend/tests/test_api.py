# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_health():
    response = client.get("/")
    assert response.status_code in [200, 404]


def test_wordle_solver_endpoint():
    payload = {
        "words": ["apple", "angle", "amble"],
        "constraints": {
            "green": {0: "a"},
            "yellow": {},
            "grey": []
        }
    }

    response = client.post("/wordle/solve", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "solutions" in data
    assert isinstance(data["solutions"], list)
