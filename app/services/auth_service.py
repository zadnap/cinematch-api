from app import db
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils.validators import validate_password, validate_username
from app.utils.response import success, error

class AuthService:
    @staticmethod
    def refresh_token(user_id): 
        new_access_token = create_access_token(identity=user_id)
        return success({ "access_token": new_access_token }, "Token refreshed")


    @staticmethod
    def sign_in_user(data):
        username = (data.get("username") or "").strip()
        password = data.get("password")
        if not username or not password:
            return error("MISSING_CREDENTIALS", "Username and password are required")
        
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return error("INVALID_CREDENTIALS", "Incorrect username or password", 401)
        
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return success({ "access_token": access_token, "refresh_token": refresh_token }, "Sign in successfully")


    @staticmethod
    def sign_up_user(data):
        username = (data.get("username") or "").strip()
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if not username or not password or not password_confirmation:
            return error("MISSING_FIELDS", "Missing username, password or password confirmation")
        
        errorMsg = validate_username(username)
        if errorMsg:
            return error("INVALID_USERNAME", errorMsg, 422)

        errorMsg = validate_password(password)
        if errorMsg:
            return error("INVALID_PASSWORD", errorMsg, 422)
        
        if password != password_confirmation:
            return error("PASSWORD_MISMATCH", "Password does not match its confirmation", 422)

        if User.query.filter_by(username=username).first():
            return error("USERNAME_EXISTS", "Username already exists", 409)

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            password_hash=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return success({}, "Account created successfully", 201)
        except Exception as e:
            print(f"[SIGN UP ERROR] {e}")
            db.session.rollback()
            return error("SERVER_ERROR", "Server error", 500)