from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/sign-in", methods=["POST"])
def sign_in():
    result = AuthService.sign_in_user(request.json)
    return jsonify(result)


@auth_bp.route("/sign-up", methods=["POST"])
def sign_up():
    result = AuthService.sign_up_user(request.json)
    return jsonify(result)