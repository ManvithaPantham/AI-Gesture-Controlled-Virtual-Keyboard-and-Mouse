import time


class GestureEngine:

    def __init__(self):

        self.last_toggle = 0
        self.toggle_delay = 1.0

    def detect_gesture(self, finger_count, pinch):

        # ---------- Left Click / Drag ----------
        if pinch < 0.05:
            return "PINCH"

        # ---------- Cursor Movement ----------
        elif finger_count == 1:
            return "MOVE"

        # ---------- Right Click ----------
        elif finger_count == 2:
            return "RIGHT_CLICK"

        # ---------- Toggle Mode ----------
        elif finger_count == 3:

            current = time.time()

            if current - self.last_toggle > self.toggle_delay:

                self.last_toggle = current
                return "TOGGLE_MODE"

        # ---------- Scroll ----------
        elif finger_count == 4:
            return "SCROLL"

        # ---------- Pause ----------
        elif finger_count == 5:
            return "PAUSE"

        return "NONE"