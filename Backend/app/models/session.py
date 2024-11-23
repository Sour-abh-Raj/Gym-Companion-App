from flask_pymongo import PyMongo
from datetime import datetime

mongo = PyMongo()

def init_db(app):
    mongo.init_app(app)

def save_exercise_session(user_id, exercise_type, count, duration):
    mongo.db.sessions.insert_one({
        "user_id": user_id,
        "exercise_type": exercise_type,
        "count": count,
        "duration": duration,
        "timestamp": datetime.utcnow()
    })

def get_user_history(user_id):
    return list(mongo.db.sessions.find({"user_id": user_id}))
