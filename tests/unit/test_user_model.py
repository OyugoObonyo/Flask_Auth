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


def test_save_user_to_db(db):
    user = User(
        email='user@mail.com',
        password='user_password'
    )
    db.session.add(user)
    db.session.commit()
    retrieved_user = User.query.filter_by(email=user.email).first()
    assert retrieved_user.email == user.email
    with pytest.raises(AttributeError):
        assert retrieved_user.password
