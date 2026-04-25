from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/sign-in", methods=["POST"])
def sign_in():
    result, status_code = AuthService.sign_in_user(request.json)
    return jsonify(result), status_code


@auth_bp.route("/sign-up", methods=["POST"])
def sign_up():
    result, status_code = AuthService.sign_up_user(request.json)
    return jsonify(result), status_code