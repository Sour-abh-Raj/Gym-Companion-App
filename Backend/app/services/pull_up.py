# pull_up.py
import cv2
import numpy as np
from utils.pose import PoseDetector # Updated import path

class PullUpCounter:
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
            shoulder_angle = self.pose_detector.findAngle(frame, 12, 14, 16, landmarks_list)
            hip_angle = self.pose_detector.findAngle(frame, 24, 12, 26, landmarks_list)
            progress_percentage = np.interp(hip_angle, (90, 160), (0, 100))
            progress_bar = np.interp(hip_angle, (90, 160), (380, 50))

            if hip_angle > 160 and shoulder_angle > 40:
                self.correct_form = 1

            if self.correct_form == 1:
                if progress_percentage == 0 and hip_angle <= 90:
                    self.exercise_feedback = "Up"
                    if self.movement_dir == 0:
                        self.counter += 0.5
                        self.movement_dir = 1
                elif progress_percentage == 100 and hip_angle > 160 and shoulder_angle > 40:
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
