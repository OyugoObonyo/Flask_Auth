from app import db
from app.auth import bp
from app.models import User
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)

@bp.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user is not None:
        return {
            "Status": "error",
            "Message": "User already exists"
        }, 400
    user = User(
        email =data.get('email'),
        password=data.get('password')
    )
    db.session.add(user)
    db.session.commit()
    return {
        "Status": "OK",
        "Message": "User successfully registered"
    }, 200

@bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    if data is None:
        return {
            "Status": "error",
            "Message": "username or password cannot be blank"
        }, 400
    user = User.query.filter_by(email=data.get('email')).first()
    if user is None or not user.check_password(data.get('password')):
        return {
            "Status": "error",
            "Message": "Invalid username or password"
        }, 401
    claim = {"email": user.email, "id": user.id}
    access_token = create_access_token(identity=user.id, additional_claims=claim)
    refresh_token = create_refresh_token(identity=user.id, additional_claims=claim)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@bp.route("/me")
@jwt_required()
def get_current_user():
    current_user = get_jwt()
    print(current_user)
    return {
        "id": current_user.get("id"),
        "email": current_user.get("email")
    }, 200