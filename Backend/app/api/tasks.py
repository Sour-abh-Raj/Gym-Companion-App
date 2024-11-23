from app import celery
from app.models.session import save_exercise_session
from app.services.exercise import process_video_stream

@celery.task
def start_exercise_task(user_id, exercise_type, video_source):
    count, duration = process_video_stream(exercise_type, video_source)
    save_exercise_session(user_id, exercise_type, count, duration)
