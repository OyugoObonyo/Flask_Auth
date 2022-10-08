from app import db
from app.models import BlockedToken, User
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_current_user,
    jwt_required
)
from flask_restful import Resource


class RegistrationView(Resource):
    def post(self):
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
        user = User.query.filter_by(email=data.get("email")).first()
        if user is not None:
            return {"status": "error", "message": "User already exists"}, 400
        user = User(email=email, password=password, username=username)
        db.session.add(user)
        db.session.commit()
        return {
            "status": "OK",
            "message": "User successfully registered",
            "username": user.username,
            "email": user.email}, 201


class LoginView(Resource):
    def post(self):
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


class LogoutView(Resource):
    @jwt_required()
    def post(self):
        token = get_jwt()
        jti = token["jti"]
        token_type = token["type"]
        blocked_token = BlockedToken(jti=jti, token_type=token_type)
        db.session.add(blocked_token)
        db.session.commit()
        return {
            "status": "OK",
            "message": "User logged out successfully"}, 200


class UserDetailView(Resource):
    @jwt_required()
    def get(self):
        user = get_current_user()
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username}, 200


class TokenRefreshView(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_current_user().id
        access_token = create_access_token(identity=identity)
        return {"access_token": access_token}, 200
