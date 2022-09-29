def test_full_logout(client, user):
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "user@mail.com",
            "username": "username",
            "password": "user_password",
        },
    )
    token = login_response.json["Token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 200
    assert response.json["Status"] == "OK"
    assert response.json["Message"] == "User logged out successfully"


def test_logout_without_token(client):
    response = client.post("/api/auth/logout")
    assert response.status_code == 401
    assert response.json["Status"] == "error"
    assert response.json["Message"] == "Please provide a valid authentication token"


def test_logout_with_invalid_header(client, user):
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "user@mail.com",
            "uername": "username",
            "password": "user_password",
        },
    )
    token = login_response.json["Token"]
    headers = {"Authorization": token}
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 401
    assert response.json["Status"] == "error"
    assert (
        response.json["Message"]
        == "Use a valid naming convention for the Authorization header"
    )


def test_logout_with_invalid_token(client):
    headers = {"Authorization": "Bearer anInvalidToken"}
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 400
    assert response.json["Status"] == "error"
    assert response.json["Message"] == "Invalid token"


def test_logout_with_expired_token(client, user):
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "user@mail.com",
            "username": "username",
            "password": "user_password",
        },
    )
    token = login_response.json["Token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/auth/logout", headers=headers)
    repeat_logout = client.post("/api/auth/logout", headers=headers)
    assert repeat_logout.status_code == 400
    assert repeat_logout.json["Status"] == "error"
    assert repeat_logout.json["Message"] == "Token expired. Please log in again"
