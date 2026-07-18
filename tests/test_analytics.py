def test_leaderboard_shape(client):
    response = client.get("/api/leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert "page" in data
    assert "limit" in data
    assert "total_contributors" in data
    assert "leaderboard" in data
    assert isinstance(data["leaderboard"], list)


def test_leaderboard_pagination(client):
    response = client.get("/api/leaderboard?page=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["leaderboard"]) <= 2


def test_heatmap_unknown_user(client):
    response = client.get("/api/heatmap/completelyunknownuser12345")
    assert response.status_code == 404
    assert "No commits found" in response.json()["detail"]