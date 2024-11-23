import sys
import os
from app import create_app, socketio

# Add the parent directory (Backend) to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)
