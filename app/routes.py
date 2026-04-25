from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)

@bp.route("/auth/sign-in", methods=["POST"])
def sign_in():
    return jsonify({"message": "Sign in success"})


@bp.route("/auth/sign-up", methods=["POST"])
def sign_up():
    return jsonify({"message": "Sign up success"})


@bp.route("/onboard", methods=["POST"])
def onboard():
    return jsonify({"message": "Onboarding success"})


@bp.route("/favourites", methods=["GET"])
def get_user_favourites():
    return jsonify({"message": "Getting favourite movies success"})


@bp.route("/favourites", methods=["POST"])
def add_movie_to_favourites():
    return jsonify({"message": "Adding movie to favourite success"})


@bp.route("/search", methods=["GET"])
def search():
    return jsonify({"message": "Searching success"})


@bp.route("/movies/detail/<id>", methods=["GET"])
def get_movie_by_id(id):
    return jsonify({"movie_id": id})


@bp.route("/movies/<genre>", methods=["GET"])
def get_movies_by_genre(genre):
    return jsonify({"genre": genre})


@bp.route("/upcoming", methods=["GET"])
def get_upcoming_movies():
    return jsonify({"message": "Getting upcoming success"})


@bp.route("/trending", methods=["GET"])
def get_trending_movies():        
    return jsonify({"message": "Getting trending success"})


@bp.route("/trailers", methods=["GET"])
def get_trailers():
    return jsonify({"message": "Getting trailers success"})