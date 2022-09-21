import pytest

def test_full_login(client, user):
    response = client.post("/api/auth/login", json = {
        "email" : "user@mail.com",
        "password": "user_password"
    })
    assert response.status_code == 200
    assert response.json["Status"] == "OK"
    assert response.json["Token"] is not None

def test_login_with_inexistent_email(client):
    response = client.post("/api/auth/login", json = {
        "email" : "user1@mail.com",
        "password": "user_password"
    })
    assert response.status_code == 400
    assert response.json["Status"] == "error"
    assert response.json["Message"] == "Invalid username or password"
    with pytest.raises(KeyError):
        assert response.json["Token"]

def test_login_with_wrong_password(client, user):
    response = client.post("/api/auth/login", json = {
        "email" : "user@mail.com",
        "password": "wrong_pasword"
    })
    assert response.status_code == 400
    assert response.json["Status"] == "error"
    assert response.json["Message"] == "Invalid username or password"
    with pytest.raises(KeyError):
        assert response.json["Token"]

def test_login_without_password(client):
    response = client.post("/api/auth/login", json = {
        "email" : "user@mail.com"
    })
    assert response.status_code == 400
    assert response.json["Status"] == "error"
    assert response.json["Message"] == "Invalid username or password"
    with pytest.raises(KeyError):
        assert response.json["Token"]

def test_login_without_email(client):
    response = client.post("/api/auth/login", json = {
        "password" : "user_password"
    })
    assert response.status_code == 400
    assert response.json["Status"] == "error"
    assert response.json["Message"] == "Invalid username or password"
    with pytest.raises(KeyError):
        assert response.json["Token"]