from fastapi.testclient import TestClient


def test_task_creation_and_user_scoping(
    client: TestClient,
    create_user_and_token,
) -> None:
    alice_headers = create_user_and_token("alice")
    bob_headers = create_user_and_token("bob")

    create_response = client.post(
        "/api/v1/tasks/",
        headers=alice_headers,
        json={
            "title": "Alice private task",
            "description": "Only Alice should see this",
            "is_completed": False,
        },
    )

    assert create_response.status_code == 201, create_response.text
    created_task = create_response.json()
    task_id = created_task["id"]

    alice_list_response = client.get("/api/v1/tasks/", headers=alice_headers)
    assert alice_list_response.status_code == 200
    assert len(alice_list_response.json()) == 1
    assert alice_list_response.json()[0]["title"] == "Alice private task"

    bob_list_response = client.get("/api/v1/tasks/", headers=bob_headers)
    assert bob_list_response.status_code == 200
    assert bob_list_response.json() == []

    bob_detail_response = client.get(f"/api/v1/tasks/{task_id}", headers=bob_headers)
    assert bob_detail_response.status_code == 404


def test_task_filtering_and_search(
    client: TestClient,
    create_user_and_token,
) -> None:
    headers = create_user_and_token("carol")

    task_payloads = [
        {
            "title": "Write report",
            "description": "Quarterly finance summary",
            "is_completed": False,
            "due_date": "2026-08-01T09:00:00",
        },
        {
            "title": "Team meeting",
            "description": "Discuss report outcomes",
            "is_completed": True,
            "due_date": "2026-08-03T14:00:00",
        },
        {
            "title": "Buy groceries",
            "description": "Milk and bread",
            "is_completed": False,
            "due_date": "2026-08-10T18:00:00",
        },
    ]

    for payload in task_payloads:
        response = client.post("/api/v1/tasks/", headers=headers, json=payload)
        assert response.status_code == 201, response.text

    search_response = client.get("/api/v1/tasks/?q=report", headers=headers)
    assert search_response.status_code == 200
    search_titles = {task["title"] for task in search_response.json()}
    assert search_titles == {"Write report", "Team meeting"}

    completed_response = client.get("/api/v1/tasks/?is_completed=true", headers=headers)
    assert completed_response.status_code == 200
    completed_tasks = completed_response.json()
    assert len(completed_tasks) == 1
    assert completed_tasks[0]["title"] == "Team meeting"

    due_date_response = client.get(
        "/api/v1/tasks/?due_date_from=2026-08-02T00:00:00&due_date_to=2026-08-31T23:59:59",
        headers=headers,
    )
    assert due_date_response.status_code == 200
    due_date_titles = {task["title"] for task in due_date_response.json()}
    assert due_date_titles == {"Team meeting", "Buy groceries"}


def test_task_pagination_limit_and_offset(
    client: TestClient,
    create_user_and_token,
) -> None:
    headers = create_user_and_token("dave")

    for index in range(15):
        response = client.post(
            "/api/v1/tasks/",
            headers=headers,
            json={
                "title": f"Task {index}",
                "description": f"Task number {index}",
                "is_completed": False,
            },
        )
        assert response.status_code == 201, response.text

    first_page_response = client.get("/api/v1/tasks/?skip=0&limit=10", headers=headers)
    assert first_page_response.status_code == 200
    first_page = first_page_response.json()
    assert len(first_page) == 10
    assert first_page[0]["title"] == "Task 0"
    assert first_page[-1]["title"] == "Task 9"

    second_page_response = client.get("/api/v1/tasks/?skip=10&limit=10", headers=headers)
    assert second_page_response.status_code == 200
    second_page = second_page_response.json()
    assert len(second_page) == 5
    assert second_page[0]["title"] == "Task 10"


def test_task_pagination_validation_bounds(
    client: TestClient,
    create_user_and_token,
) -> None:
    headers = create_user_and_token("erin")

    invalid_limit_response = client.get("/api/v1/tasks/?limit=101", headers=headers)
    assert invalid_limit_response.status_code == 422

    invalid_skip_response = client.get("/api/v1/tasks/?skip=-1", headers=headers)
    assert invalid_skip_response.status_code == 422
