from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
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

    if not data:
        return jsonify({
            "success": False,
            "error": "Invalid JSON"
        }), 400
    
    genres = data.get("genres")
    movies = data.get("movies")

    if not isinstance(genres, list):
        return jsonify({"success": False, "error": "Genres must be array"}), 400

    if not isinstance(movies, list):
        return jsonify({"success": False, "error": "Movies must be array"}), 400

    genres = list(set(genres))
    movies = list(set(movies))

    result, status_code = UserService.onboard_user(user.id, genres, movies)
    return jsonify(result), status_code


@user_bp.route("/favourites", methods=["GET"])
@sign_in_required
@onboard_required
def get_user_favourites(user):
    page = request.args.get("page", type=int)
    data = UserService.get_favourites(user.id, page)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@user_bp.route("/favourites", methods=["POST"])
@sign_in_required
@onboard_required
def add_movie_to_favourites(user):
    movie_id = request.get_json().get("movie_id")
    data = UserService.add_to_favourites(user.id, movie_id)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@user_bp.route("/favourites", methods=["DELETE"])
@sign_in_required
@onboard_required
def delete_movie_from_favourites(user):
    movie_id = request.get_json().get("movie_id")
    data = UserService.remove_from_favourites(user.id, movie_id)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@user_bp.route("/favourites/<int:movie_id>", methods=["GET"])
@sign_in_required
@onboard_required
def check_movie_in_favourites(user, movie_id):
    data = UserService.check_favourite(user.id, movie_id)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@user_bp.route("/me", methods=["GET"])
@sign_in_required
def get_user_data(user):
    data = UserService.get_user_data(user.id)

    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200