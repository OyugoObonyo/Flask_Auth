def test_full_registration(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "user2@mail.com",
            "username": "test_username",
            "password": "password",
        },
    )
    assert response.status_code == 201
    assert response.json["Message"] == "User successfully registered"
    assert response.json["Status"] == "OK"


def test_register_without_email(client):
    response = client.post(
        "/api/auth/register", json={"username": "username", "password": "password"}
    )
    assert response.status_code == 400
    assert response.json["Message"] == "Email, username or password cannot be blank"
    assert response.json["Status"] == "error"


def test_register_without_username(client):
    response = client.post(
        "/api/auth/register", json={"email": "user@mai.com", "password": "password"}
    )
    assert response.status_code == 400
    assert response.json["Message"] == "Email, username or password cannot be blank"
    assert response.json["Status"] == "error"


def test_register_without_password(client):
    response = client.post(
        "/api/auth/register", json={"email": "user2@mail.com", "username": "username"}
    )
    assert response.status_code == 400
    assert response.json["Message"] == "Email, username or password cannot be blank"
    assert response.json["Status"] == "error"


def test_register_already_existing_user(client, user):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "user@mail.com",
            "username": "username",
            "password": "user_password",
        },
    )
    assert response.status_code == 400
    assert response.json["Message"] == "User already exists"
    assert response.json["Status"] == "error"
