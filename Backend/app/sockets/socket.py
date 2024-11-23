from flask_socketio import SocketIO, emit

socketio = SocketIO()

@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

def send_feedback(data):
    emit("feedback", data, broadcast=True)
