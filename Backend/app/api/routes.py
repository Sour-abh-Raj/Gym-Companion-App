from flask import Blueprint, request, jsonify
from app.models.session import save_exercise_session, get_user_history
from app.sockets.socket import socketio

exercise_blueprint = Blueprint("exercise", __name__)

@exercise_blueprint.route("/start-exercise", methods=["POST"])
def start_exercise():
    data = request.json
    socketio.emit("start_exercise", data, broadcast=True)
    return jsonify({"status": "Exercise started"}), 200

@exercise_blueprint.route("/stop-exercise", methods=["POST"])
def stop_exercise():
    data = request.json
    save_exercise_session(data["user_id"], data["exercise_type"], data["count"], data["duration"])
    return jsonify({"status": "Exercise stopped"}), 200

@exercise_blueprint.route("/history/<user_id>", methods=["GET"])
def history(user_id):
    history_data = get_user_history(user_id)
    return jsonify(history_data), 200
