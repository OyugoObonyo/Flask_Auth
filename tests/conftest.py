from app import create_app
from app.models import User
from config import TestingConfig
import pytest


@pytest.fixture(scope="session")
def app():
    app = create_app(config_class=TestingConfig)
    return app


@pytest.fixture()
def user():
    user = User(
        email= "testuser@email.com",
        password="testpassword"
    )
    return user

