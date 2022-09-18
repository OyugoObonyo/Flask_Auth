from app.models import User
import pytest


def test_user_model_setup():
    user = User(
        email='user@mail.com',
        password='user_password'
    )
    assert str(user) == user.email
    assert user.email == 'user@mail.com'
    with pytest.raises(AttributeError):
        assert user.password
