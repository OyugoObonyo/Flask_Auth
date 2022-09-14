from app import db
from app.auth import bp
from app.models import User
from flask import request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required
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
        }, 400
    token = create_access_token(identity=user.id)
    if token:
        return {
            "Status": "OK",
            "Token": token
        }, 200
    else:
        return {
            "Status": "error",
            "Message": "Log in Attempt failed, please try again"
        }, 400


@bp.route("/me")
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return {
        "id": user.id,
        "email": user.email
    }, 200