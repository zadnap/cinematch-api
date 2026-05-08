from flask import Blueprint, jsonify, request
from app.services.movie_service import MovieService
from flask_jwt_extended import get_jwt_identity, jwt_required

movies_bp = Blueprint("movies", __name__)

@movies_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    page = request.args.get("page", 1, type=int)
    result, status_code = MovieService.search_movies(query, page)
    return jsonify(result), status_code


@movies_bp.route("/detail/<int:movie_id>", methods=["GET"])
def get_movie_by_id(movie_id):
    result, status_code = MovieService.get_details(movie_id)
    return jsonify(result), status_code


@movies_bp.route("/all-genres", methods=["GET"])
def get_all_genres():
    result, status_code = MovieService.get_genres()
    return jsonify(result), status_code


@movies_bp.route("/by-genres", methods=["GET"])
def get_movies_by_genres():
    page = request.args.get("page", 1, type=int)
    ids = request.args.get("ids")
    result, status_code = MovieService.get_by_genres(ids, page)
    return jsonify(result), status_code


@movies_bp.route("/upcoming", methods=["GET"])
@jwt_required(optional=True)
def get_upcoming_movies():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    result, status_code = MovieService.get_upcoming(page, user_id)
    return jsonify(result), status_code


@movies_bp.route("/trending", methods=["GET"])
@jwt_required(optional=True)
def get_trending_movies():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    result, status_code = MovieService.get_trending(page, user_id)
    return jsonify(result), status_code


@movies_bp.route("/trailers", methods=["GET"])
def get_preview_trailers():
    limit = request.args.get("limit", 5, type=int)
    result, status_code = MovieService.get_trailers(limit)
    return jsonify(result), status_code


@movies_bp.route("/featured", methods=["GET"])
def get_featured_movie():
    result, status_code = MovieService.get_featured_movie()
    return jsonify(result), status_code