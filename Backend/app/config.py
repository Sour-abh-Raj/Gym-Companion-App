import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/exercise_data")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    SOCKETIO_MESSAGE_QUEUE = os.getenv("SOCKETIO_MESSAGE_QUEUE", "redis://localhost:6379/1")
