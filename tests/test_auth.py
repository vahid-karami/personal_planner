from fastapi.testclient import TestClient


def test_login_returns_access_token(client: TestClient) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={"username": "alice", "password": "supersecure123"},
    )

    assert register_response.status_code == 201
    assert register_response.json()["username"] == "alice"

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "alice", "password": "supersecure123"},
    )

    assert login_response.status_code == 200
    payload = login_response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]


def test_protected_tasks_require_authentication(client: TestClient) -> None:
    response = client.get("/api/v1/tasks/")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
