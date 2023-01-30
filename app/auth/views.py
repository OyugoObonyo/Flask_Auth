from app import db
from app.auth import bp
from app.auth.utils.oauth import oauth
from app.models import BlockedToken, User
from flask import redirect, request, url_for
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_current_user,
    jwt_required
)

@bp.route('/')
def home():
    return "Hello index page!"

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
            "message": "Email, username or password cannot be blank",
        }, 400
    user = User(email=email, password=password, username=username)
    status = user.save()
    if status != "success":
        return {"status": "error", "message": status}, 400
    return {
        "status": "OK",
        "message": "User successfully registered",
        "username": user.username,
        "email": user.email}, 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        email = data["email"]
        password = data["password"]
    except KeyError:
        return {"status": "error", "message": "Email or password cannot be blank"}, 401
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return {"status": "error", "message": "Invalid email or password"}, 401
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return {
        "status": "OK",
        "access_token": access_token,
        "refresh_token": refresh_token}, 200


@bp.route('/login/google')
def google_login():
    redirect_uri = url_for('auth.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@bp.route('/login/google/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    print(token)
    user_info = oauth.google.userinfo()
    print("USER INFO: ", user_info)
    user = User( 
        username=user_info["name"],
        email=user_info["email"]
    )
    user.save()
    return redirect(url_for('auth.home'))


@bp.route("/logout")
@jwt_required()
def logout():
    token = get_jwt()
    jti = token["jti"]
    token_type = token["type"]
    blocked_token = BlockedToken(jti=jti, token_type=token_type)
    db.session.add(blocked_token)
    db.session.commit()
    return {
        "status": "OK",
        "message": "User logged out successfully"}, 200


@bp.route("/me")
@jwt_required()
def user_details():
    user = get_current_user()
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username}, 200


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_current_user().id
    access_token = create_access_token(identity=identity)
    return {"access_token": access_token}, 200
