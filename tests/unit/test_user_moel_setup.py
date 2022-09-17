def test_user_model_setup(user):
    assert user.email == "testuser@email.com"
    assert user.password == "testpassword"