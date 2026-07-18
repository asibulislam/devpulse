from tests.conftest import unique_username, register_user, get_token, auth_headers


def test_register_success(client):
    username = unique_username()
    response = register_user(client, username)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert "hashed_password" not in data


def test_register_duplicate_username(client):
    username = unique_username()
    register_user(client, username)
    response = register_user(client, username)
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]


def test_login_success(client):
    username = unique_username()
    register_user(client, username)
    response = client.post("/api/auth/login", data={
        "username": username,
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    username = unique_username()
    register_user(client, username)
    response = client.post("/api/auth/login", data={
        "username": username,
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_get_me_with_token(client):
    username = unique_username()
    register_user(client, username)
    token = get_token(client, username)
    response = client.get("/api/auth/me", headers=auth_headers(token))
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert "hashed_password" not in data


def test_get_me_without_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_update_profile(client):
    username = unique_username()
    register_user(client, username)
    token = get_token(client, username)
    response = client.patch(
        "/api/auth/me",
        json={"github_username": f"gh_{username}", "email": f"{username}@test.com"},
        headers=auth_headers(token)
    )
    assert response.status_code == 200
    data = response.json()
    assert data["github_username"] == f"gh_{username}"
    assert data["email"] == f"{username}@test.com"


def test_stats_without_github_username(client):
    username = unique_username()
    register_user(client, username)
    token = get_token(client, username)
    response = client.get("/api/auth/me/stats", headers=auth_headers(token))
    assert response.status_code == 400
    assert "github_username" in response.json()["detail"]