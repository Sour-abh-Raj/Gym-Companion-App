from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from app.api.routes import exercise_blueprint
from app.config import Config
from celery import Celery
from app.models.session import init_db

socketio = SocketIO()

def create_celery_app(app=None):
    app = app or create_app()
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"]
    )
    celery.conf.update(app.config)
    return celery

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(exercise_blueprint, url_prefix='/exercise')
    init_db(app)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    # CORS(app, resources={r"/exercise/*": {"origins": "http://localhost:3000"}})
    socketio.init_app(app, cors_allowed_origins="*")
    # SocketIO.init_app(app, cors_allowed_origins="*", manage_session=False)
    # SocketIO.init_app(app, cors_allowed_origins="http://localhost:3000")
    # CORS(app)
    # CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})   
    return app

celery = create_celery_app()
