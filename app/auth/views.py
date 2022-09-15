from app import db
from app.auth import bp
from app.models import User
from flask import request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
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
    print(user.password)
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
    token = create_access_token(identity=user.id, additional_claims=claim)
    return {
        "Status": "OK",
        "Token": token
    }, 200



@bp.route("/me")
@jwt_required()
def get_current_user():
    current_user = get_jwt()
    return {
        "id": current_user.get("id"),
        "email": current_user.get("email")
    }, 200