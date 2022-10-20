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


@pytest.mark.parametrize(
    "email, username, password, output",
    [
        ("user@email.com", "User_99", "Astrong!Password001", "valid"),
        ("user.com", "User_99", "Astrong!Password001",
            "The email address is not valid. It must have exactly\
 one @-sign."),
        ("user@testuser.com", "User_99", "Astrong!Password001",
            "The domain name testuser.com does not send email."),
        ("user@email.com", "me", "Astrong!Password001",
            "Username should be at least 3 characters long and\
 may only contain letters, numbers, '-', '.' and '_'"),
        ("user@email.com", "User_99", "S8ort",
            "Password should be at least 6 characters long\
 and must contain at least 1 uppercase letter, 1 lowercase\
 letter and 1 number")
    ]
)
def test_user_validate_details(user, email, username, password, output):
    assert user.validate_user_details(email, username, password) == output
