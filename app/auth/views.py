from app import db
from app.auth import bp
from app.models import BlacklistedToken, User
from flask import request
from app.utils.tokens import encode_auth_token, decode_auth_token


@bp.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    try:
        email = data["email"]
        password = data["password"]
    except KeyError:
        return {
            "Status": "error",
            "Message": "Email or password cannot be blank"
        }, 400
    user = User.query.filter_by(email=data.get('email')).first()
    if user is not None:
        return {
            "Status": "error",
            "Message": "User already exists"
        }, 400
    user = User(
        email = email,
        password= password
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
    try:
        email = data["email"]
        password = data["password"]
    except KeyError:
        return {
            "Status": "error",
            "Message": "Email or password cannot be blank"
        }, 400
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return {
            "Status": "error",
            "Message": "Invalid username or password"
        }, 400
    token = encode_auth_token(user.id)
    return {
        "Status": "OK",
        "Token": token
    }, 200


@bp.route("/logout", methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return {
            "Status": "error",
            "Message": "Please provide a valid authentication token"
        }, 401
    try:
        auth_token = auth_header.split(" ")[1]
    except IndexError:
        return {
            "Status": "error",
            "Message": "Use a valid naming convention for the Authorization header"
        }, 401
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
        "Status": "error",
        "Message": resp
    }, 400


@bp.route('/me')
def user_details():
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return {
            "Status": "error",
            "Message": "Please provide a valid authentication token"
        }, 401
    try:
        auth_token = auth_header.split(" ")[1]
    except IndexError:
        return {
            "Status": "error",
            "Message": "Use a valid naming convention for the Authorization header"
        }, 401
    resp = decode_auth_token(auth_token)
    if isinstance(resp, int):
        user = User.query.get(resp)
        return {
            "id": user.id,
            "email": user.email
        }, 200
    return {
        "Status": "error",
        "Message": resp
    }, 400