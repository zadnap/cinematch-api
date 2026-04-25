import os
from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv()

def create_app():
    from .routes import bp

    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    return app