import pytest


def test_full_login(client, user):
    response = client.post(
        "/api/auth/login", json={"email": "user@mail.com", "password": "user_password"}
    )
    assert response.status_code == 200
    assert response.json["status"] == "OK"
    assert response.json["access_token"] is not None
    assert response.json["refresh_token"] is not None


def test__login_without_username_and_password(client):
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 401
    assert response.json["status"] == "error"
    assert response.json["message"] == "Email or password cannot be blank"


def test_login_with_inexistent_email(client):
    response = client.post(
        "/api/auth/login", json={"email": "user1@mail.com", "password": "user_password"}
    )
    assert response.status_code == 401
    assert response.json["status"] == "error"
    assert response.json["message"] == "Invalid email or password"
    with pytest.raises(KeyError):
        assert response.json["access_token"]
        assert response.json["refresh_token"]


def test_login_with_wrong_password(client, user):
    response = client.post(
        "/api/auth/login", json={"email": "user@mail.com", "password": "wrong_pasword"}
    )
    assert response.status_code == 401
    assert response.json["status"] == "error"
    assert response.json["message"] == "Invalid email or password"
    with pytest.raises(KeyError):
        assert response.json["access_token"]
        assert response.json["refresh_token"]


def test_login_without_password(client):
    response = client.post("/api/auth/login", json={"email": "user@mail.com"})
    assert response.status_code == 401
    assert response.json["status"] == "error"
    assert response.json["message"] == "Email or password cannot be blank"
    with pytest.raises(KeyError):
        assert response.json["access_token"]
        assert response.json["refresh_token"]


def test_login_without_email(client):
    response = client.post("/api/auth/login", json={"password": "user_password"})
    assert response.status_code == 401
    assert response.json["status"] == "error"
    assert response.json["message"] == "Email or password cannot be blank"
    with pytest.raises(KeyError):
        assert response.json["access_token"]
        assert response.json["refresh_token"]
