from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

load_dotenv()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate(render_as_batch=True)


def create_app(config_class):
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    import app.auth.views as auth_views

    api.add_resource(auth_views.RegistrationView, '/register')
    api.add_resource(auth_views.LoginView, '/login')
    api.add_resource(auth_views.LogoutView, '/logout')
    api.add_resource(auth_views.TokenRefreshView, '/refresh')
    api.add_resource(auth_views.UserDetailView, '/me')

    return app
