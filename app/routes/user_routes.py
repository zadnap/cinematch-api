from flask import Blueprint, jsonify, request
from app.services.user_service import UserService
from app.decorators.onboard_blocked import onboard_blocked
from app.decorators.onboard_required import onboard_required
from app.decorators.sign_in_required import sign_in_required

user_bp = Blueprint("user", __name__)

@user_bp.route("/onboarding", methods=["POST"])
@sign_in_required
@onboard_blocked
def onboard_user(user):
    data = request.get_json()
    result, status_code = UserService.onboard_user(user.id, data)
    return jsonify(result), status_code


@user_bp.route("/favourites", methods=["GET"])
@sign_in_required
@onboard_required
def get_user_favourites(user):
    page = request.args.get("page", type=int)
    result, status_code = UserService.get_favourites(user.id, page)
    return jsonify(result), status_code


@user_bp.route("/favourites", methods=["POST"])
@sign_in_required
@onboard_required
def add_movie_to_favourites(user):
    movie_id = request.get_json().get("movie_id")
    result, status_code = UserService.add_to_favourites(user.id, movie_id)
    return jsonify(result), status_code


@user_bp.route("/favourites/<int:movie_id>", methods=["DELETE"])
@sign_in_required
@onboard_required
def delete_movie_from_favourites(user, movie_id):
    result, status_code = UserService.remove_from_favourites(user.id, movie_id)
    return jsonify(result), status_code


@user_bp.route("/favourites/<int:movie_id>", methods=["GET"])
@sign_in_required
@onboard_required
def check_movie_in_favourites(user, movie_id):
    result, status_code = UserService.check_favourite(user.id, movie_id)
    return jsonify(result), status_code


@user_bp.route("/me", methods=["GET"])
@sign_in_required
def get_user_data(user):
    result, status_code = UserService.get_user_data(user.id)
    return jsonify(result), status_code