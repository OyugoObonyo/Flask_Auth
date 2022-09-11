from base64 import decode
from app import db
from app.auth import bp
from app.models import User
from flask import request


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
    token = user.encode_auth_token(user.id)
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
