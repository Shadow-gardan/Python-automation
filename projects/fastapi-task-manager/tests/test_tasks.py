def create_task(client, **overrides):
    payload = {"title": "Prepare proposal", "description": "Draft the client proposal"}
    payload.update(overrides)
    return client.post("/api/v1/tasks", json=payload)


def test_create_task(client):
    response = create_task(client, priority="high")

    assert response.status_code == 201
    assert response.json()["title"] == "Prepare proposal"
    assert response.json()["priority"] == "high"
    assert response.json()["status"] == "pending"


def test_invalid_status_rejected(client):
    response = create_task(client, status="blocked")

    assert response.status_code == 422


def test_invalid_priority_rejected(client):
    response = create_task(client, priority="urgent")

    assert response.status_code == 422


def test_list_tasks(client):
    create_task(client)
    create_task(client, title="Review contract")

    response = client.get("/api/v1/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task(client):
    task_id = create_task(client).json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_missing_task_returns_404(client):
    response = client.get("/api/v1/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task(client):
    task_id = create_task(client).json()["id"]

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"status": "completed", "title": "Completed proposal"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["title"] == "Completed proposal"


def test_delete_task(client):
    task_id = create_task(client).json()["id"]

    response = client.delete(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 204
    assert client.get(f"/api/v1/tasks/{task_id}").status_code == 404


def test_filter_by_status(client):
    create_task(client, status="completed")
    create_task(client, title="Pending task")

    response = client.get("/api/v1/tasks?status=pending")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "pending"


def test_filter_by_priority(client):
    create_task(client, priority="high")
    create_task(client, title="Low task", priority="low")

    response = client.get("/api/v1/tasks?priority=high")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["priority"] == "high"


def test_pagination(client):
    for index in range(3):
        create_task(client, title=f"Task {index}")

    response = client.get("/api/v1/tasks?skip=1&limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_validation_errors(client):
    response = client.post("/api/v1/tasks", json={"title": ""})

    assert response.status_code == 422


def test_invalid_pagination_rejected(client):
    response = client.get("/api/v1/tasks?limit=101")

    assert response.status_code == 422
