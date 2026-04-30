from flask import Blueprint, jsonify, request
from app.services.movie_service import MovieService
from flask_jwt_extended import get_jwt_identity, jwt_required

movies_bp = Blueprint("movies", __name__)

@movies_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    page = request.args.get("page", 1, type=int)
    data = MovieService.search_movies(query, page)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@movies_bp.route("/detail/<string:id>", methods=["GET"])
def get_movie_by_id(id):
    data = MovieService.get_details(id)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@movies_bp.route("/all-genres", methods=["GET"])
def get_all_genres():
    data = MovieService.get_genres()
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@movies_bp.route("/by-genres", methods=["GET"])
@jwt_required(optional=True)
def get_movies_by_genres():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    ids = request.args.get("ids")

    if not ids:
        return jsonify({"success": False, "message": "ids is required"}), 400

    genre_ids = [g.strip() for g in ids.split(",")]

    if not all(g.isdigit() for g in genre_ids):
        return jsonify({"success": False, "message": "Invalid genre ids"}), 400

    data = MovieService.get_by_genres(genre_ids, page, user_id)

    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@movies_bp.route("/upcoming", methods=["GET"])
@jwt_required(optional=True)
def get_upcoming_movies():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    data = MovieService.get_upcoming(page, user_id)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@movies_bp.route("/trending", methods=["GET"])
@jwt_required(optional=True)
def get_trending_movies():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    data = MovieService.get_trending(page, user_id)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@movies_bp.route("/trailers", methods=["GET"])
def get_preview_trailers():
    limit = request.args.get("limit", 5, type=int)
    data = MovieService.get_trailers(limit)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@movies_bp.route("/featured", methods=["GET"])
def get_featured_movie():
    data = MovieService.get_featured_movie()
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200