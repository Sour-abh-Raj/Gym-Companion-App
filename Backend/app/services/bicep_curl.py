# bicep_curl.py
import cv2
import numpy as np
from utils.pose import PoseDetector  # Updated import path

class BicepCurlCounter:
    def __init__(self):
        self.pose_detector = PoseDetector.PoseDetectorModified()
        self.counter = 0
        self.movement_dir = 0
        self.correct_form = 0
        self.exercise_feedback = "Fix Form"

    def process_frame(self, frame):
        frame = self.pose_detector.findPose(frame, False)
        landmarks_list = self.pose_detector.findPosition(frame, False)

        if len(landmarks_list) != 0:
            elbow_angle = self.pose_detector.findAngle(frame, 11, 13, 15, landmarks_list)
            shoulder_angle = self.pose_detector.findAngle(frame, 23, 11, 13, landmarks_list)
            progress_percentage = np.interp(elbow_angle, (50, 160), (0, 100))
            progress_bar = np.interp(elbow_angle, (50, 160), (380, 50))

            if elbow_angle < 150 and shoulder_angle > 150:
                self.correct_form = 1

            if self.correct_form == 1:
                if progress_percentage == 100 and elbow_angle >= 160:
                    self.exercise_feedback = "Up"
                    if self.movement_dir == 0:
                        self.counter += 0.5
                        self.movement_dir = 1
                elif progress_percentage == 0 and elbow_angle < 50 and shoulder_angle > 150:
                    self.exercise_feedback = "Down"
                    if self.movement_dir == 1:
                        self.counter += 0.5
                        self.movement_dir = 0
                else:
                    self.exercise_feedback = "Fix Form"

        return {
            "frame": frame,
            "counter": int(self.counter),
            "feedback": self.exercise_feedback,
            "progress": int(progress_percentage)
        }
