from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "email": "test_user@example.com",
            "password": "123456"
        }
    )

    assert response.status_code in [200, 400]


def test_login_user():
    client.post(
        "/auth/register",
        json={
            "email": "login_user@example.com",
            "password": "123456"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "login_user@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_todo_with_auth():
    client.post(
        "/auth/register",
        json={
            "email": "todo_user@example.com",
            "password": "123456"
        }
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "todo_user@example.com",
            "password": "123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/todos/",
        json={
            "title": "Test todo",
            "description": "Test description"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test todo"


def test_get_my_todos_with_auth():
    client.post(
        "/auth/register",
        json={
            "email": "list_user@example.com",
            "password": "123456"
        }
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "list_user@example.com",
            "password": "123456"
        }
    )

    token = login_response.json()["access_token"]

    client.post(
        "/todos/",
        json={
            "title": "User todo",
            "description": "Only my todo"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    response = client.get(
        "/todos/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_todos_without_token_are_blocked():
    response = client.get("/todos/")

    assert response.status_code == 401