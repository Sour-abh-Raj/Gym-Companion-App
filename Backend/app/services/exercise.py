import base64
import cv2
import numpy as np
from flask import jsonify
from importlib import import_module

EXERCISE_CLASSES = {
    "bicep_curl": "app.services.bicep_curl.BicepCurlCounter",
    "pull_up": "app.services.pull_up.PullUpCounter",
}

def base64_to_image(base64_str):
    image_data = base64.b64decode(base64_str)
    np_array = np.frombuffer(image_data, np.uint8)
    return cv2.imdecode(np_array, cv2.IMREAD_COLOR)

def get_exercise_class(exercise_type):
    class_path = EXERCISE_CLASSES.get(exercise_type)
    if not class_path:
        return None
    module_name, class_name = class_path.rsplit(".", 1)
    module = import_module(module_name)
    return getattr(module, class_name)
