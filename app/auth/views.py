from app import db
from app.auth import bp
from app.models import BlacklistedToken, User
from flask import request
from app.utils.tokens import encode_auth_token, decode_auth_token


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
    }, 201


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
    token = encode_auth_token(user.id)
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


@bp.route("/logout", methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return {
            "Status": "error",
            "Message": "Please provide a valid authentication token"
        }
    auth_token = auth_header.split(" ")[1]
    resp = decode_auth_token(auth_token)
    if not isinstance(resp, str):
        blacklisted_token = BlacklistedToken(auth_token)
        db.session.add(blacklisted_token)
        db.session.commit()
        return {
            "Status": "OK",
            "Message": "User logged out successfully"
        }, 200
    return {
        "Status": "OK",
        "Message": resp
    }


@bp.route('/me')
def user_details():
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return {
            "Status": "error",
            "Message": "Please provide a valid authentication token"
        }
    auth_token = auth_header.split(" ")[1]
    resp = decode_auth_token(auth_token)
    if isinstance(resp, int):
        user = User.query.get(resp)
        return {
            "username": user.id,
            "email": user.email
        }, 200
    return {
        "Status": "error",
        "Message": resp
    }, 400