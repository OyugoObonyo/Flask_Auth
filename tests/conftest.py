from app import create_app, db
from app.models import User
from config import TestingConfig
import pytest


@pytest.fixture(scope="session")
def app():
    app = create_app(config_class=TestingConfig)
    return app


@pytest.fixture(scope="session")
def app_client():
    app = create_app(config_class=TestingConfig)
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()

@pytest.fixture(scope="session")
def app_db():
    db.create_all()
    user = User(
        email='user@mail.com',
        password='user_password'
    )
    db.session.add(user)
    db.session.commit()
    yield db
    db.drop_all()
