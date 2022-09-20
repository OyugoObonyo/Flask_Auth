from app.models import User

def test_full_registration(client):
    response = client.post("/api/auth/register", json={
        "email" : "user2@mail.com",
        "password": "password"
    })
    assert response.status_code == 201
    assert response.json["Message"] == "User successfully registered"
    assert response.json["Status"] == "OK"

def test_register_without_email(client):
    response = client.post("/api/auth/register", json={
        "password": "password"
    })
    assert response.status_code == 400
    assert response.json["Message"] == "Email or password cannot be blank"
    assert response.json["Status"] == "error"

def test_register_without_password(client):
    response = client.post("/api/auth/register", json={
        "email" : "user2@mail.com",
    })
    assert response.status_code == 400
    assert response.json["Message"] == "Email or password cannot be blank"
    assert response.json["Status"] == "error"

def test_register_already_existing_user(client, db):
    user = User(
        email="user21@mail.com",
        password="password"
    )
    db.session.add(user)
    db.session.commit()
    response = client.post("/api/auth/register", json={
        "email" : "user21@mail.com",
        "password": "password"
    })
    assert response.status_code == 400
    assert response.json["Message"] == "User already exists"
    assert response.json["Status"] == "error"
