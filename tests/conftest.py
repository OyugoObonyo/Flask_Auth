from app import create_app
from app import db as _db
from config import TestingConfig
import os
import pytest


@pytest.fixture(scope="session")
def app():
    app = create_app(config_class=TestingConfig)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("TEST_DATABASE_URL")
    return app

@pytest.fixture(scope="session")
def app_client(app):
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()

@pytest.fixture(scope="session")
def db(app):
    _db.app = app 
    _db.create_all()
    yield _db
    _db.session.close()
    _db.drop_all()
