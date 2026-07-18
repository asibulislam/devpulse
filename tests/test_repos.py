from tests.conftest import unique_username, register_user, get_token, auth_headers


def test_sync_without_token(client):
    response = client.post("/api/repos/fastapi/fastapi/sync")
    assert response.status_code == 401


def test_stored_commits_unsynced_repo(client):
    response = client.get("/api/repos/nonexistent/repo/commits/stored")
    assert response.status_code == 404
    assert "not synced yet" in response.json()["detail"]


def test_activity_unsynced_repo(client):
    response = client.get("/api/repos/nonexistent/repo/activity")
    assert response.status_code == 404
    assert "not synced yet" in response.json()["detail"]


def test_stored_commits_pagination_shape(client):
    response = client.get("/api/repos/fastapi/fastapi/commits/stored?page=1&limit=5")
    if response.status_code == 200:
        data = response.json()
        assert "page" in data
        assert "limit" in data
        assert "total" in data
        assert "pages" in data
        assert "commits" in data
    else:
        assert response.status_code == 404