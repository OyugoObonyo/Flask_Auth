import os
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, password):
        self.email = email
        self.password_hash = self.set_password(password)

    @property
    def password(self):
        raise AttributeError('Attribute not accessible')

    def set_password(self, password):
        password_hash = generate_password_hash(password)
        return password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

