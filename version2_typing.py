import cv2
import mediapipe as mp
import time

# ---------------- SETTINGS ----------------

PINCH_THRESHOLD = 0.04
TYPE_COOLDOWN = 0.6

typed_text = ""
last_press = 0
caps_lock = False

# ---------------- CAMERA ----------------

cap = cv2.VideoCapture(0)

# ---------------- MEDIAPIPE ----------------

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# ---------------- KEYBOARD ----------------

keys = [
    ["1","2","3","4","5","6","7","8","9","0"],
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L"],
    ["Z","X","C","V","B","N","M"]
]

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    camera_frame = frame.copy()

    # Glass panel
    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (10, 100),
        (630, 470),
        (30, 30, 30),
        -1
    )

    frame = cv2.addWeighted(
        overlay,
        0.75,
        frame,
        0.25,
        0
    )

    # Title
    cv2.putText(
        frame,
        "AI Gesture Keyboard V2",
        (150, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,255),
        2
    )

    # Typing Box
    cv2.rectangle(
        frame,
        (20, 50),
        (620, 90),
        (255,255,255),
        -1
    )

    cv2.putText(
        frame,
        typed_text[-25:],
        (30, 78),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,0,0),
        2
    )

    key_boxes = []

    # Draw Keyboard
    for row_index, row in enumerate(keys):

        for col_index, key in enumerate(row):

            x = 20 + col_index * 60

            if row_index == 1:
                x += 10

            if row_index == 2:
                x += 35

            if row_index == 3:
                x += 80

            y = 120 + row_index * 60

            cv2.rectangle(
                frame,
                (x, y),
                (x + 50, y + 50),
                (60,60,60),
                -1
            )

            cv2.rectangle(
                frame,
                (x, y),
                (x + 50, y + 50),
                (200,200,200),
                2
            )

            cv2.putText(
                frame,
                key,
                (x + 13, y + 33),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )

            key_boxes.append((key, x, y, 50, 50))

    # SPACE BAR

    cv2.rectangle(
        frame,
        (140, 370),
        (500, 430),
        (60,60,60),
        -1
    )

    cv2.rectangle(
        frame,
        (140, 370),
        (500, 430),
        (200,200,200),
        2
    )

    cv2.putText(
        frame,
        "SPACE",
        (240, 408),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        2
    )

    key_boxes.append(
        ("SPACE", 140, 370, 360, 60)
    )
    cv2.rectangle(
    frame,
    (520, 370),
    (640, 430),
    (60,60,60),
    -1
)

    cv2.rectangle(
    frame,
    (520, 370),
    (640, 430),
    (200,200,200),
    2
)

    cv2.putText(
    frame,
    "BACK",
    (535, 408),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255,255,255),
    2
)

    key_boxes.append(("BACK",520,370,120,60))
    cv2.rectangle(
    frame,
    (20, 370),
    (130, 430),
    (60,60,60),
    -1
)

    cv2.rectangle(
    frame,
    (20, 370),
    (130, 430),
    (200,200,200),
    2
)

    cv2.putText(
    frame,
    "ENTER",
    (28, 408),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (255,255,255),
    2
)

    key_boxes.append(("ENTER",20,370,110,60))
    cv2.rectangle(
    frame,
    (650, 400),
    (780, 460),
    (60,60,60),
    -1
)

    cv2.rectangle(
    frame,
    (650, 400),
    (780, 460),
    (200,200,200),
    2
)

    cv2.putText(
    frame,
    "CAPS",
    (670,438),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255,255,255),
    2
)

    key_boxes.append(("CAPS",650,400,130,60))
    # ---------------- HAND TRACKING ----------------

    rgb = cv2.cvtColor(
        camera_frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        index_tip = hand.landmark[8]
        thumb_tip = hand.landmark[4]

        distance = (
            (index_tip.x - thumb_tip.x) ** 2 +
            (index_tip.y - thumb_tip.y) ** 2
        ) ** 0.5

        h, w, _ = frame.shape

        ix = int(index_tip.x * w)
        iy = int(index_tip.y * h)

        # Red Cursor

        cv2.circle(
            frame,
            (ix, iy),
            12,
            (0,0,255),
            -1
        )

        cv2.putText(
            frame,
            f"Distance: {distance:.3f}",
            (20, 460),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

        # Hover Detection

        for key, x, y, width, height in key_boxes:

            if (
                x < ix < x + width and
                y < iy < y + height
            ):

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (255,120,0),
                    -1
                )

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (255,255,255),
                    2
                )

                cv2.putText(
                    frame,
                    key,
                    (x + 10, y + 33),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255,255,255),
                    2
                )

                cv2.putText(
                    frame,
                    f"Hover: {key}",
                    (220,105),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,255),
                    2
                )

                current_time = time.time()

                if (
                    distance < PINCH_THRESHOLD and
                    current_time - last_press > TYPE_COOLDOWN
                ):

                    if key == "SPACE":
                        typed_text += " "
                    elif key == "BACK":
                        typed_text = typed_text[:-1]

                    elif key == "ENTER":
                        typed_text += "|"

                    elif key == "CAPS":
                        caps_lock = not caps_lock

                    else:
                        if caps_lock:
                            typed_text += key.upper()
                        else:
                            typed_text += key.lower()

                last_press = current_time

    cv2.imshow(
        "AI Gesture Keyboard V2",
        frame
    )

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()