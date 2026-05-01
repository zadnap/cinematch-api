from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.user_service import UserService

user_bp = Blueprint("user", __name__)

@user_bp.route("/onboarding", methods=["POST"])
@jwt_required()
def onboard_user():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": {"message": "Invalid JSON"}
        }), 400
    
    if not isinstance(genres, list):
        return jsonify({
            "success": False,
            "error": {"message": "Genres must be an array"}
        }), 400

    if not isinstance(movies, list):
        return jsonify({
            "success": False,
            "error": {"message": "Movies must be an array"}
        }), 400

    if len(genres) < 3:
        return jsonify({
            "success": False,
            "error": {"message": "Please select at least 3 genres"}
        }), 400

    if not all(isinstance(g, int) for g in genres):
        return jsonify({
            "success": False,
            "error": {"message": "Invalid genre IDs"}
        }), 400

    if not all(isinstance(m, int) for m in movies):
        return jsonify({
            "success": False,
            "error": {"message": "Invalid movie IDs"}
        }), 400

    genres = list(set(genres))
    movies = list(set(movies))

    result, status_code = UserService.onboard_user(user_id, genres, movies)
    return jsonify(result), status_code


@user_bp.route("/favourites", methods=["GET"])
@jwt_required()
def get_user_favourites():
    page = request.args.get("page", type=int)
    user_id = get_jwt_identity()
    data = UserService.get_favourites(user_id, page)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@user_bp.route("/favourites", methods=["POST"])
@jwt_required()
def add_movie_to_favourites():
    user_id = get_jwt_identity()
    movie_id = request.get_json().get("movie_id")
    data = UserService.add_to_favourites(user_id, movie_id)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@user_bp.route("/favourites", methods=["DELETE"])
@jwt_required()
def delete_movie_from_favourites():
    user_id = get_jwt_identity()
    movie_id = request.get_json().get("movie_id")
    data = UserService.remove_from_favourites(user_id, movie_id)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@user_bp.route("/favourites/<int:movie_id>", methods=["GET"])
@jwt_required()
def check_movie_in_favourites(movie_id):
    user_id = get_jwt_identity()
    data = UserService.check_favourite(user_id, movie_id)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200