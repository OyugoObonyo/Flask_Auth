from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = email = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    public_id = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.email = email
        self.username = username
        self.public_id = uuid.uuid4().hex
        self.password_hash = self.set_password(password)

    @property
    def password(self):
        raise AttributeError("Password not accessible")

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

    __tablename__ = "blacklist_tokens"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    @staticmethod
    def is_blacklisted(auth_token):
        blacklisted_token = BlacklistedToken.query.filter_by(
            token=str(auth_token)
        ).first()
        return blacklisted_token is not None

    def __repr__(self):
        return f"{self.token}"
