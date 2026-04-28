from flask import Blueprint, jsonify, request
from app.services.movie_service import MovieService

movies_bp = Blueprint("movies", __name__)

@movies_bp.route("/search", methods=["GET"])
def search():
    return jsonify({"message": "Searching success"})


@movies_bp.route("/detail/<string:id>", methods=["GET"])
def get_movie_by_id(id):
    data = MovieService.get_details(id)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@movies_bp.route("/genres", methods=["GET"])
def get_all_genres():
    data = MovieService.get_genres()
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200

@movies_bp.route("/genres/<string:id>", methods=["GET"])
def get_movies_by_genre(id):
    page = request.args.get("page", 1, type=int)
    data = MovieService.get_by_genre(id, page)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@movies_bp.route("/upcoming", methods=["GET"])
def get_upcoming_movies():
    page = request.args.get("page", 1, type=int)
    data = MovieService.get_upcoming(page)
    
    if not data.get("success"):
        return jsonify(data), 500

    return jsonify(data), 200


@movies_bp.route("/trending", methods=["GET"])
def get_trending_movies():
    page = request.args.get("page", 1, type=int)
    data = MovieService.get_trending(page)
    
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