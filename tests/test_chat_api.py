from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_chat_rejects_empty_message():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "",
            "thread_id": "test-thread",
        },
    )

    assert response.status_code == 422


def test_chat_rejects_empty_thread_id():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Hello",
            "thread_id": "",
        },
    )

    assert response.status_code == 422