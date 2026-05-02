from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity,
    set_access_cookies, 
    create_access_token, 
    unset_jwt_cookies
)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    response = jsonify({"success": True, "message": "Token refresh successful"})
    set_access_cookies(response, create_access_token(identity=user_id))
    return response


@auth_bp.route("/sign-in", methods=["POST"])
def sign_in():
    result, status_code = AuthService.sign_in_user(request.json)
    return result, status_code


@auth_bp.route("/sign-up", methods=["POST"])
def sign_up():
    result, status_code = AuthService.sign_up_user(request.json)
    return result, status_code


@auth_bp.route("/sign-out", methods=["POST"])
def logout():
    response = jsonify({"success": True, "message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200