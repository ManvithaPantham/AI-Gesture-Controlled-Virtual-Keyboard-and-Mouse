import cv2
import time

from keyboard_layout import KEYBOARD_LAYOUT
from keyboard_ui import draw_keyboard
from hand_tracker import HandTracker
from typing_engine import TypingEngine
from mouse_mode import MouseMode
from prediction import PredictionEngine
from gesture_engine import GestureEngine
from sound_engine import SoundEngine

# ==========================================
# Camera
# ==========================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ==========================================
# Modules
# ==========================================

tracker = HandTracker()
engine = TypingEngine()
mouse = MouseMode()
predictor = PredictionEngine()
gesture = GestureEngine()
sound = SoundEngine()

mode = "KEYBOARD"

fps_time = time.time()

# ==========================================
# Main Loop
# ==========================================

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    camera = frame.copy()

    h, w, _ = frame.shape

    # ==========================================
    # Glass Background
    # ==========================================

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (0, 80),
        (1280, 720),
        (40, 40, 45),
        -1
    )

    frame = cv2.addWeighted(
        overlay,
        0.60,
        frame,
        0.40,
        0
    )

    # ==========================================
    # Header
    # ==========================================

    cv2.putText(
        frame,
        "AI Gesture Keyboard Pro",
        (360,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        2
    )

    cv2.putText(
        frame,
        f"MODE : {mode}",
        (1030,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )

    cv2.putText(
        frame,
        f"CAPS : {'ON' if engine.caps else 'OFF'}",
        (40,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )

    # ==========================================
    # Keyboard Screen
    # ==========================================

    prediction_boxes = []
    key_boxes = []

    if mode == "KEYBOARD":

        # Typing Box

        cv2.rectangle(
            frame,
            (40,60),
            (1240,105),
            (255,255,255),
            -1
        )

        cv2.putText(
            frame,
            engine.get_text()[-70:],
            (50,90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,0),
            2
        )

        # Keyboard

        key_boxes = draw_keyboard(
            frame,
            KEYBOARD_LAYOUT
        )

        # Prediction Bar

        predictions = predictor.predict(
            engine.get_text()
        )

        x = 50

        for word in predictions:

            prediction_boxes.append(
                (word, x, 600, 130, 35)
            )

            cv2.rectangle(
                frame,
                (x,600),
                (x+130,635),
                (65,65,65),
                -1
            )

            cv2.rectangle(
                frame,
                (x,600),
                (x+130,635),
                (180,180,180),
                2
            )

            cv2.putText(
                frame,
                word,
                (x+8,623),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255,255,255),
                2
            )

            x += 145

    # ==========================================
    # Mouse Screen
    # ==========================================

    else:

        cv2.putText(
            frame,
            "MOUSE MODE",
            (440,130),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0,255,0),
            3
        )

        cv2.putText(
            frame,
            "Move Index Finger",
            (430,190),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            "Pinch = Left Click / Drag",
            (340,235),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            "2 Fingers = Right Click",
            (355,280),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            "4 Fingers = Scroll",
            (390,325),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

    # ==========================================
    # Hand Detection
    # ==========================================

    results = tracker.find_hand(camera)

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        tracker.draw_hand(frame, hand)

        ix, iy = tracker.get_index(hand, w, h)

        distance = tracker.pinch_distance(hand)

        finger_count = tracker.finger_count(hand)

        gesture_name = gesture.detect_gesture(
            finger_count,
            distance
        )
                # ==========================================
        # Cursor
        # ==========================================

        cv2.circle(
            frame,
            (ix, iy),
            18,
            (255,255,255),
            2
        )

        cv2.circle(
            frame,
            (ix, iy),
            8,
            (0,140,255),
            -1
        )

        cv2.putText(
            frame,
            f"Pinch : {distance:.3f}",
            (980,70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Gesture : {gesture_name}",
            (980,95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,0),
            2
        )

        # ==========================================
        # Prediction Selection
        # ==========================================

        prediction_selected = False

        if mode == "KEYBOARD":

            for word, px, py, pw, ph in prediction_boxes:

                if px < ix < px + pw and py < iy < py + ph:

                    cv2.rectangle(
                        frame,
                        (px, py),
                        (px + pw, py + ph),
                        (0,255,0),
                        3
                    )

                    if distance < 0.05:

                        if engine.can_type(distance):

                            engine.replace_last_word(word)

                            sound.play()

                            prediction_selected = True

                            break

        # ==========================================
        # Keyboard Hover
        # ==========================================

        if mode == "KEYBOARD" and not prediction_selected:

            for key, x, y, width, height in key_boxes:

                if x < ix < x + width and y < iy < y + height:

                    cv2.rectangle(
                        frame,
                        (x,y),
                        (x+width,y+height),
                        (0,140,255),
                        3
                    )

                    cv2.putText(
                        frame,
                        f"Hover : {key}",
                        (40,690),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0,255,255),
                        2
                    )

                    if distance < 0.05:

                        if engine.can_type(distance):

                            if engine.press(key):

                                sound.play()

                            if key == "ESC":

                                cap.release()

                                cv2.destroyAllWindows()

                                exit()

        # ==========================================
        # Mouse Mode
        # ==========================================

        if mode == "MOUSE":

            mouse.move(ix, iy, w, h)

            # Left Click / Drag

            if distance < 0.05:

                mouse.press_left()

            else:

                mouse.release_left()

            # Right Click

            if gesture_name == "RIGHT_CLICK":

                mouse.right_click()

            # Scroll

            elif gesture_name == "SCROLL":

                mouse.scroll_up()
                    # ==========================================
        # FPS
        # ==========================================

        current = time.time()

        fps = int(
            1 / max(current - fps_time, 0.0001)
        )

        fps_time = current

        cv2.putText(
            frame,
            f"FPS : {fps}",
            (1120,700),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

    # ==========================================
    # Display Window
    # ==========================================

    cv2.imshow(
        "AI Gesture Keyboard Pro",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    # ==========================================
    # Toggle Keyboard / Mouse
    # ==========================================

    if key == ord("m"):

        if mode == "KEYBOARD":
            mode = "MOUSE"
        else:
            mode = "KEYBOARD"

    # ==========================================
    # Clear Typed Text
    # ==========================================

    elif key == ord("c"):

        engine.clear()

    # ==========================================
    # Exit Application
    # ==========================================

    elif key == 27:

        break

# ==========================================
# Cleanup
# ==========================================

cap.release()

cv2.destroyAllWindows()