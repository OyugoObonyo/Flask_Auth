def test_full_logout(client, user):
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "user@mail.com",
            "username": "username",
            "password": "user_password",
        },
    )
    token = login_response.json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 200
    assert response.json["status"] == "OK"
    assert response.json["message"] == "User logged out successfully"


def test_logout_without_token(client):
    response = client.post("/api/auth/logout")
    assert response.status_code == 401
    assert response.json["status"] == "error"
    assert response.json["message"] == "Please provide a valid authorization header"


def test_logout_with_invalid_header(client, user):
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "user@mail.com",
            "uername": "username",
            "password": "user_password",
        },
    )
    token = login_response.json["access_token"]
    headers = {"Authorization": token}
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 401
    assert response.json["status"] == "error"
    assert response.json["message"] == "Please provide a valid authorization header"


def test_logout_with_invalid_token(client):
    headers = {"Authorization": "Bearer anInvalidToken"}
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 401
    assert response.json["status"] == "error"
    assert response.json["message"] == "token is invalid"


def test_logout_with_revoked_token(client, user):
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "user@mail.com",
            "username": "username",
            "password": "user_password",
        },
    )
    token = login_response.json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/auth/logout", headers=headers)
    repeat_logout = client.post("/api/auth/logout", headers=headers)
    assert repeat_logout.status_code == 401
    assert repeat_logout.json["status"] == "error"
    assert repeat_logout.json["message"] == "token has already been revoked"
