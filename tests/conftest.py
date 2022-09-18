from app import create_app
from app import db as _db
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
def db():
    _db.create_all()
    yield _db
    _db.session.close()
    _db.drop_all()
