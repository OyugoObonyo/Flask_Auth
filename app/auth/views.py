from app import db
from app.auth import bp
from app.models import BlockedToken, User
from flask import request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
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
            "Status": "error",
            "Message": "Email, username or password cannot be blank",
        }, 400
    user = User.query.filter_by(email=data.get("email")).first()
    if user is not None:
        return {"Status": "error", "Message": "User already exists"}, 400
    user = User(email=email, password=password, username=username)
    db.session.add(user)
    db.session.commit()
    return {"Status": "OK", "Message": "User successfully registered"}, 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        email = data["email"]
        password = data["password"]
    except KeyError:
        return {"Status": "error", "Message": "Email or password cannot be blank"}, 400
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return {"Status": "error", "Message": "Invalid username or password"}, 400
    access_token = create_access_token(identity=user.id)
    return {"Status": "OK", "access_token": access_token}, 200


@bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    token = get_jwt()
    jti = token["jti"]
    token_type = token["type"]
    blocked_token = BlockedToken(jti=jti, token_type=token_type)
    db.session.add(blocked_token)
    db.session.commit()
    return {"Status": "OK", "Message": "User logged out successfully"}, 200


@bp.route("/me")
@jwt_required()
def user_details():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return {"id": user.id, "email": user.email, "username": user.username}, 200
