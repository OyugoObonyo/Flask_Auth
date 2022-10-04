from flask import Blueprint
from app import jwt
from app.models import User, BlockedToken

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

from app.auth import views


# Serves the get_current_user() function
@jwt.user_lookup_loader
def retrieve_current_user(header, payload):
    identity = payload["sub"]
    return User.query.filter_by(id=identity).first()


@jwt.token_in_blocklist_loader
def check_token_is_blocked(header, payload):
    jti = payload["jti"]
    token = BlockedToken.query.filter_by(jti=jti).scalar()
    return token is not None


@jwt.revoked_token_loader
def handle_revoked_token_response(header, payload):
    return {
        "message": "token has already been revoked",
        "status": "error"
    }, 401


@jwt.invalid_token_loader
def handle_invalid_token_response(error):
    return {
        "message": "token is invalid",
        "status": "error",
        "description": error
    }, 401


@jwt.expired_token_loader
def handle_expired_token_response(header, payload):
    return {
        "message": "token is expired",
        "status": "error"
    }
