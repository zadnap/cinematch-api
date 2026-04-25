from flask import Blueprint, jsonify

user_bp = Blueprint("user", __name__)

@user_bp.route("/onboarding", methods=["POST"])
def onboard_user():
    return jsonify({"message": "Onboarding success"})


@user_bp.route("/favourites", methods=["GET"])
def get_user_favourites():
    return jsonify({"message": "Getting favourite movies success"})


@user_bp.route("/favourites", methods=["POST"])
def add_movie_to_favourites():
    return jsonify({"message": "Adding movie to favourite success"})