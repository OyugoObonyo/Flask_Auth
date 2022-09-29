from app import create_app
from app import db as _db
from config import TestingConfig
from app.models import User
import os
import pytest


@pytest.fixture(scope="session")
def app():
    app = create_app(config_class=TestingConfig)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("TEST_DATABASE_URL")
    return app


@pytest.fixture(scope="session")
def db(app):
    _db.app = app
    _db.create_all()
    yield _db
    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    _db.create_all()
    yield client
    ctx.pop()
    _db.session.close()
    _db.drop_all()


@pytest.fixture()
def user(db):
    _user = User(email="user@mail.com", username="username", password="user_password")
    db.session.add(_user)
    db.session.commit()
    retrieved_user = User.query.filter_by(email=_user.email).first()
    yield retrieved_user
    db.session.delete(retrieved_user)
    db.session.commit()
