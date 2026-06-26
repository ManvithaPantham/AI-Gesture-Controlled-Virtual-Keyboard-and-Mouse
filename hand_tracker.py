import cv2
import mediapipe as mp
import math


class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.drawer = mp.solutions.drawing_utils

        # Finger tip landmarks
        self.tip_ids = [4, 8, 12, 16, 20]

    # ------------------------------------

    def find_hand(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return self.hands.process(rgb)

    # ------------------------------------

    def draw_hand(self, frame, hand):

        self.drawer.draw_landmarks(
            frame,
            hand,
            self.mp_hands.HAND_CONNECTIONS
        )

    # ------------------------------------

    def get_index(self, hand, width, height):

        point = hand.landmark[8]

        return (
            int(point.x * width),
            int(point.y * height)
        )

    # ------------------------------------

    def get_thumb(self, hand, width, height):

        point = hand.landmark[4]

        return (
            int(point.x * width),
            int(point.y * height)
        )

    # ------------------------------------

    def get_middle(self, hand, width, height):

        point = hand.landmark[12]

        return (
            int(point.x * width),
            int(point.y * height)
        )

    # ------------------------------------

    def get_ring(self, hand, width, height):

        point = hand.landmark[16]

        return (
            int(point.x * width),
            int(point.y * height)
        )

    # ------------------------------------

    def get_pinky(self, hand, width, height):

        point = hand.landmark[20]

        return (
            int(point.x * width),
            int(point.y * height)
        )

    # ------------------------------------

    def pinch_distance(self, hand):

        thumb = hand.landmark[4]
        index = hand.landmark[8]

        return math.hypot(
            thumb.x - index.x,
            thumb.y - index.y
        )

    # ------------------------------------

    def finger_count(self, hand):

        count = 0

        # Thumb
        if hand.landmark[4].x < hand.landmark[3].x:
            count += 1

        # Other four fingers
        tips = [8, 12, 16, 20]
        joints = [6, 10, 14, 18]

        for tip, joint in zip(tips, joints):

            if hand.landmark[tip].y < hand.landmark[joint].y:
                count += 1

        return count

    # ------------------------------------

    def get_all_points(self, hand, width, height):

        points = []

        for landmark in hand.landmark:

            points.append(
                (
                    int(landmark.x * width),
                    int(landmark.y * height)
                )
            )

        return points