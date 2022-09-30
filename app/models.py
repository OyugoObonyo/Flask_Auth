from app import db, jwt
from datetime import datetime
from flask_jwt_extended import get_current_user
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = email = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.email = email
        self.username = username
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


class BlockedToken(db.Model):
    """
    Token Model for storing JWT tokens
    """

    __tablename__ = "blocked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), index=True, nullable=False)
    token_type = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(
        db.ForeignKey('users.id'),
        default=lambda: get_current_user().id,
        nullable=False,
    )

    # user_id and token_type are optional and they've
    # been added to audit the FE logic

    def __init__(self, jti, token_type):
        self.jti = jti
        self.token_type = token_type
        self.created_at = datetime.now()

    def __repr__(self):
        return f"{self.token}"


@jwt.token_in_blocklist_loader
def check_if_token_is_blocked(header, payload):
    jti = payload["jti"]
    token = BlockedToken.query.filter_by(jti=jti).scalar()
    return token is not None
