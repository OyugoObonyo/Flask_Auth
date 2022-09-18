from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, password):
        self.email = email
        self.password_hash = self.set_password(password)

    @property
    def password(self):
        raise AttributeError('Password not accessible')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        password_hash = generate_password_hash(password)
        return password_hash

    def __repr__(self):
        return f"{self.email}"


class BlacklistedToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    @staticmethod
    def is_blacklisted(auth_token):
        blacklisted_token = BlacklistedToken.query.filter_by(token=str(auth_token)).first()
        return blacklisted_token is not None

    def __repr__(self):
        return f'{self.token}'
