import pytest
from app.main import app, todos


@pytest.fixture
def client():
    app.config["TESTING"] = True
    todos.clear()

    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_get_todos(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_todo(client):
    response = client.post("/todos", json={"title": "Study Python"})
    assert response.status_code == 201
    assert response.get_json()["title"] == "Study Python"


def test_add_todo_without_title(client):
    response = client.post("/todos", json={})
    assert response.status_code == 400


def test_second_todo_id(client):
    client.post("/todos", json={"title": "First"})
    response = client.post("/todos", json={"title": "Second"})
    assert response.get_json()["id"] == 2
