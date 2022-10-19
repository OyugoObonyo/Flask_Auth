from app.models import User
import pytest


def test_user_model_setup():
    user = User(email="user@mail.com", password="user_password", username="username")
    assert str(user) == user.email
    assert user.email == "user@mail.com"
    with pytest.raises(AttributeError):
        assert user.password


def test_save_user_to_db(user):
    assert user.email == "user@mail.com"
    with pytest.raises(AttributeError):
        assert user.password


def test_user_password(user):
    assert user.check_password("user_passworrd") is False
    assert user.check_password("user_password") is True


@pytest.mark.parametrize(
    "password", "output",
    [
        ("notavalidpassword", """
        Password should be at least 6 characters long and must contain 1
        """),
        ("Astrong!Password001", "valid"),
        ("S8ort", False),
        ("NosPecialCharact8", True)
    ]
)
def test_password_validity(user, password, output): 
    assert user.validate_password(password) is output


@pytest.mark.parametrize(
    "username",  "output",
    [
        ("me", False),
        ("User_99", True),
        ("peter-98.py", True),
        ("Notauser!", False)
    ]
)
def test_username_validity(user, username, output):
    assert user.validate_username(username) is output
