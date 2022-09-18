from app import db
from app.models import User


def test_set_password_hash(user_data):
    user = User(
        email=user_data["email"],
        password=user_data["password"]
    )
    assert user.password_hash == user.set_password(user_data["password"])

def test_check_password_hash(user_data):
    user = User(
        email=user_data["email"],
        password=user_data["password"]
    )
    db.session.add(user)
    db.session.commit()
    assert user.check_password(user_data["password"]) is True
    assert user.check_password("pasword") is False
