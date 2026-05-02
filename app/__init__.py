import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import timedelta
from app.utils.str_to_bool import str_to_bool

db = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = str_to_bool(os.getenv("JWT_COOKIE_SECURE", "False"))
    app.config["JWT_COOKIE_SAMESITE"] = os.getenv("JWT_COOKIE_SAMESITE")
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/auth/refresh"

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    JWTManager(app)

    cors_origins = os.getenv("CORS_ORIGINS", "")
    origins_list = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

    CORS(
        app,
        origins=origins_list,
        supports_credentials=True
    )

    with app.app_context():
        from . import models 

        from app.routes.auth_routes import auth_bp
        from app.routes.movie_routes import movies_bp
        from app.routes.user_routes import user_bp

        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(movies_bp, url_prefix="/movies")
        app.register_blueprint(user_bp, url_prefix="/user")

    return app