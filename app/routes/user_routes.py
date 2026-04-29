from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.user_service import UserService

user_bp = Blueprint("user", __name__)

@user_bp.route("/onboarding", methods=["POST"])
def onboard_user():
    return jsonify({"message": "Onboarding success"})


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