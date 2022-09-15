from datetime import timedelta
import os


class Config():
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '486fb9dc-e0e2-43ad-8b98-068e99f3f64e'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=20)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)