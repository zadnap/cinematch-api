import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    JWTManager(app)
    CORS(
        app,
        resources={r"/*": {"origins": os.getenv("CORS_ORIGINS")}},
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