from app import db, jwt
from app.auth import bp
from app.models import BlockedToken, User
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required
)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    try:
        email = data["email"]
        password = data["password"]
        username = data["username"]
    except KeyError:
        return {
            "status": "error",
            "msg": "Email, username or password cannot be blank",
        }, 400
    user = User.query.filter_by(email=data.get("email")).first()
    if user is not None:
        return {"status": "error", "msg": "User already exists"}, 400
    user = User(email=email, password=password, username=username)
    db.session.add(user)
    db.session.commit()
    return {"status": "OK", "msg": "User successfully registered"}, 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        email = data["email"]
        password = data["password"]
    except KeyError:
        return {"status": "error", "msg": "Email or password cannot be blank"}, 400
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return {"status": "error", "msg": "Invalid username or password"}, 400
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return {"status": "OK", "access_token": access_token, "refresh_token": refresh_token}, 200


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"access_token": access_token}, 200


@bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    token = get_jwt()
    jti = token["jti"]
    token_type = token["type"]
    blocked_token = BlockedToken(jti=jti, token_type=token_type)
    db.session.add(blocked_token)
    db.session.commit()
    return {"status": "OK", "msg": "User logged out successfully"}, 200


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(header, payload):
    identity = payload["sub"]
    return User.query.filter_by(id=identity).first()


@jwt.token_in_blocklist_loader
def check_if_token_is_blocked(header, payload):
    jti = payload["jti"]
    token = BlockedToken.query.filter_by(jti=jti).scalar()
    return token is not None


@bp.route("/me")
@jwt_required()
def user_details():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return {"id": user.id, "email": user.email, "username": user.username}, 200
