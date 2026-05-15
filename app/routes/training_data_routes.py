from flask import Blueprint, jsonify
from app.services.training_data_service import TrainingDataService

training_data_bp = Blueprint("training-data", __name__)

@training_data_bp.route("/user-features/all", methods=["GET"])
def get_all_user_features():
    result, status_code = TrainingDataService.get_all_user_features()
    return jsonify(result), status_code


@training_data_bp.route("/ratings", methods=["GET"])
def get_ratings():
    result, status_code = TrainingDataService.get_ratings()
    return jsonify(result), status_code


@training_data_bp.route("/favourites", methods=["GET"])
def get_favourite_movies():
    result, status_code = TrainingDataService.get_favourite_movies()
    return jsonify(result), status_code