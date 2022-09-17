import os


def test_app_configurations(app):
    assert app.config("TESTING") == True
    assert app.config("SQLALCHEMY_DATABASE_URI") == os.environ.get("TEST_SQLALCHEMY_DATABASE_URI")