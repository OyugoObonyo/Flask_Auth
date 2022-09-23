def test_full_user_details(client, user):
    login_response = client.post("/api/auth/login", json = {
        "email" : "user@mail.com",
        "password": "user_password"
    })
    token = login_response.json["Token"]
    headers = {
        'Authorization': f'Bearer {token}'
    }
    user_details_response = client.get("/api/auth/me", headers=headers)
    assert user_details_response.status_code == 200
    assert user_details_response.json["email"] == "user@mail.com"
    assert user_details_response.json["id"] is not None

def test_user_details_without_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    assert response.json["Status"] == "error"
    assert response.json["Message"] == "Please provide a valid authentication token"

def test_user_details_with_invalid_header(client, user):
    login_response = client.post("/api/auth/login", json = {
        "email" : "user@mail.com",
        "password": "user_password"
    })
    token = login_response.json["Token"]
    headers = {
        'Authorization': token
    }
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 401
    assert response.json["Status"] == "error"
    assert response.json["Message"] == "Use a valid naming convention for the Authorization header"

def test_user_details_with_invalid_token(client):
    headers = {
        'Authorization': 'Bearer anInvalidToken'
    }
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 400
    assert response.json["Status"] == "error"
    assert response.json["Message"] == "Invalid token"