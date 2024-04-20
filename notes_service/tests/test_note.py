import pytest


pytestmark = [pytest.mark.anyio]


async def test_create_note(test_client):
    note = {"title": "This is a test title",
            "content": "This is a test content"}
    response = test_client.post("/note/create", json=note)
    assert response.status_code == 200
    assert response.json()["title"] == "This is a test title"

    note = {"title": "",
            "content": "Some content"}
    response = test_client.post("/note/create", json=note)
    assert response.status_code == 422

    note = {"title": "Some title",
            "content": ""}

    response = test_client.post("/note/create", json=note)
    assert response.status_code == 422

async def test_delete_note(test_client):
    note = {"title": "This is a test title",
            "content": "This is a test content"}


