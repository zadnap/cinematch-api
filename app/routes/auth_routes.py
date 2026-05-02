from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    result, status_code = AuthService.refresh_token(user_id)
    return jsonify(result), status_code


@auth_bp.route("/sign-in", methods=["POST"])
def sign_in():
    result, status_code = AuthService.sign_in_user(request.json)
    return jsonify(result), status_code


@auth_bp.route("/sign-up", methods=["POST"])
def sign_up():
    result, status_code = AuthService.sign_up_user(request.json)
    return jsonify(result), status_code
