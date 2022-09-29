from app.models import User
import pytest


def test_user_model_setup():
    user = User(
        email='user@mail.com',
        password='user_password',
        username="username"
    )
    assert str(user) == user.email
    assert user.email == 'user@mail.com'
    with pytest.raises(AttributeError):
        assert user.password


def test_save_user_to_db(user):
    assert user.email == 'user@mail.com'
    with pytest.raises(AttributeError):
        assert user.password

def test_user_password(user):
    assert user.check_password('user_passworrd') is False
    assert user.check_password('user_password') is True

