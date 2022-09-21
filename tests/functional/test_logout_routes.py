def test_full_logout(client, user):
    login_response = client.post("/api/auth/login", json = {
        "email" : "user@mail.com",
        "password": "user_password"
    })
    token = login_response.json["Token"]
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 200
    assert response.json["Status"] == "OK"
    assert response.json["Message"] == "User logged out successfully"

def test_logout_without_token(client):
    response = client.post("/api/auth/logout")
    assert response.status_code == 400
    assert response.json["Status"] == "error"
    assert response.json["Message"] == "Please provide a valid authentication token"

def test_logout_with_invalid_header(client, user):
    login_response = client.post("/api/auth/login", json = {
        "email" : "user@mail.com",
        "password": "user_password"
    })
    token = login_response.json["Token"]
    headers = {
        'Authorization': token
    }
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 200
    assert response.json["Status"] == "OK"
    assert response.json["Message"] == "User logged out successfully"
