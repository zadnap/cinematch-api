from app import db
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils.validators import validate_password, validate_username

class AuthService:
    @staticmethod
    def refresh_token(user_id): 
        user = User.query.get(user_id)
        if not user:
            return {"success": False, "message": "User not found"}, 404

        new_access_token = create_access_token(identity=user_id)
        response = {
            "success": True, 
            "access_token": new_access_token,
            "message": "Token refresh successful"
        }

        return response, 200

    @staticmethod
    def sign_in_user(data):
        username = data.get("username").strip()
        password = data.get("password")

        if not username or not password:
            return {"success": False, "message": "Missing username or password"}, 400
        
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            response = {
                "success": True,
                "message": "Sign in successfully",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "username": user.username
                }
            }

            return response, 200
        
        return {"success": False, "message": "Incorrect username or password"}, 401


    @staticmethod
    def sign_up_user(data):
        username = data.get("username")
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if not username or not password or not password_confirmation:
            return {"success": False, "message": "Missing username, password or password confirmation"}, 400
        
        error = validate_username(username)
        if error:
            return {"success": False, "message": error}, 422

        error = validate_password(password)
        if error:
            return {"success": False, "message": error}, 422    
        
        if password != password_confirmation:
            return {"success": False, "message": "Password does not match its confirmation"}, 422

        if User.query.filter_by(username=username).first():
            return {"success": False, "message": "Username already exists"}, 400

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            password_hash=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return {"success": True, "message": "Account created successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": "Server error", "error": str(e)}, 500