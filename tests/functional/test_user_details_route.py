def test_full_user_details(client, user):
    login_response = client.post(
        "/api/auth/login", json={"email": "user@mail.com", "password": "user_password"}
    )
    token = login_response.json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_details_response = client.get("/api/auth/me", headers=headers)
    assert user_details_response.status_code == 200
    assert user_details_response.json["email"] == "user@mail.com"
    assert user_details_response.json["id"] is not None


def test_user_details_without_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    assert response.json["status"] == "error"
    assert response.json["message"] == "Please provide a valid authorization header"


def test_user_details_with_invalid_header(client, user):
    login_response = client.post(
        "/api/auth/login", json={"email": "user@mail.com", "password": "user_password"}
    )
    token = login_response.json["access_token"]
    headers = {"Authorization": token}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 401
    assert response.json["status"] == "error"
    assert response.json["message"] == "Please provide a valid authorization header"


def test_user_details_with_invalid_token(client):
    headers = {"Authorization": "Bearer anInvalidToken"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 401
    assert response.json["status"] == "error"
    assert response.json["message"] == "token is invalid"
