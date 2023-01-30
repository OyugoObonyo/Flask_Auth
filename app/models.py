from app import db, jwt
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import uuid


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = email = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    public_id = db.Column(db.String(36))
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password=None):
        self.email = email
        self.username = username
        if password:
            self.password_hash = self.set_password(password)
        self.public_id = str(uuid.uuid4())

    @property
    def password(self):
        raise AttributeError("Password not accessible")

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            return str(e)
        return "success"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        password_hash = generate_password_hash(password)
        return password_hash

    def __repr__(self):
        return f"{self.email}"


class BlockedToken(db.Model):
    """
    Token Model for storing JWT tokens
    """

    __tablename__ = "blocked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), index=True, nullable=False)
    token_type = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti, token_type):
        self.jti = jti
        self.token_type = token_type
        self.created_at = datetime.now()
