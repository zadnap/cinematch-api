from app import db
from app.models import User
from flask import jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    set_access_cookies,
    set_refresh_cookies 
)
from werkzeug.security import check_password_hash, generate_password_hash

class AuthService:
    @staticmethod
    def sign_in_user(data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"success": False, "message": "Missing username or password"}), 400
        
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            response = jsonify({
                "success": True,
                "message": "Sign in successfully",
                "user": {
                    "id": user.id,
                    "username": user.username
                }
            })
            set_access_cookies(response, access_token) 
            set_refresh_cookies(response, refresh_token)

            return response, 200
        
        return jsonify({"success": False, "message": "Incorrect username or password"}), 401


    @staticmethod
    def sign_up_user(data):
        username = data.get("username")
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if not username or not password or not password_confirmation:
            return jsonify({"success": False, "message": "Missing username, password or password confirmation"}), 400
        
        if password != password_confirmation:
            return jsonify({"success": False, "message": "Password does not match its confirmation"}), 422

        if User.query.filter_by(username=username).first():
            return jsonify({"success": False, "message": "Username already exists"}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            password_hash=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"success": True, "message": "Account created successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500