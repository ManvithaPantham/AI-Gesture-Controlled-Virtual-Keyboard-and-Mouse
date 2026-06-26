import cv2

# =========================
# Keyboard UI Configuration
# =========================

NORMAL_KEY_WIDTH = 60
NORMAL_KEY_HEIGHT = 55
KEY_GAP = 8

START_X = 20
START_Y = 120

KEY_COLOR = (55, 55, 60)
BORDER_COLOR = (120, 120, 120)
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (30, 30, 30)

SPECIAL_WIDTH = {
    "ESC": 70,
    "TAB": 90,
    "CAPS": 110,
    "SHIFT": 120,
    "BACK": 120,
    "ENTER": 120,
    "CTRL": 80,
    "ALT": 80,
    "WIN": 80,
    "FN": 70,
    "MENU": 80,
    "SPACE": 320
}


def draw_key(frame, x, y, width, height, text):

    # ---------------- Shadow ----------------

    cv2.rectangle(
        frame,
        (x + 3, y + 3),
        (x + width + 3, y + height + 3),
        SHADOW_COLOR,
        -1
    )

    # ---------------- Key ----------------

    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + height),
        KEY_COLOR,
        -1
    )

    # ---------------- Border ----------------

    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + height),
        BORDER_COLOR,
        2
    )

    # ---------------- Top Highlight ----------------

    cv2.line(
        frame,
        (x + 2, y + 2),
        (x + width - 2, y + 2),
        (170,170,170),
        1
    )

    # ---------------- Text ----------------

    font = cv2.FONT_HERSHEY_SIMPLEX

    scale = 0.60

    thickness = 2

    text_size = cv2.getTextSize(
        text,
        font,
        scale,
        thickness
    )[0]

    text_x = x + (width - text_size[0]) // 2

    text_y = y + (height + text_size[1]) // 2

    cv2.putText(
        frame,
        text,
        (text_x, text_y),
        font,
        scale,
        TEXT_COLOR,
        thickness
    )


def draw_keyboard(frame, layout):

    key_boxes = []

    for row_index, row in enumerate(layout):

        x = START_X

        y = START_Y + row_index * (NORMAL_KEY_HEIGHT + 10)

        for key in row:

            width = SPECIAL_WIDTH.get(
                key,
                NORMAL_KEY_WIDTH
            )

            draw_key(
                frame,
                x,
                y,
                width,
                NORMAL_KEY_HEIGHT,
                key
            )

            key_boxes.append(
                (
                    key,
                    x,
                    y,
                    width,
                    NORMAL_KEY_HEIGHT
                )
            )

            x += width + KEY_GAP

    return key_boxes