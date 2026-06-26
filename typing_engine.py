import time


class TypingEngine:

    def __init__(self):

        self.text = ""

        self.caps = False
        self.shift = False

        self.last_press = 0

        self.cooldown = 0.25
        self.pinch_threshold = 0.04

        # Shift + Number symbols
        self.shift_numbers = {
            "1": "!",
            "2": "@",
            "3": "#",
            "4": "$",
            "5": "%",
            "6": "^",
            "7": "&",
            "8": "*",
            "9": "(",
            "0": ")"
        }

    # ------------------------------------
    # Replace last typed word with prediction
    # ------------------------------------

    def replace_last_word(self, word):

        words = self.text.split()

        if len(words) == 0:
            self.text = word + " "
        else:
            words[-1] = word
            self.text = " ".join(words) + " "

    # ------------------------------------

    def can_type(self, distance):

        current = time.time()

        if (
            distance < self.pinch_threshold
            and current - self.last_press > self.cooldown
        ):

            self.last_press = current
            return True

        return False

    # ------------------------------------

    def press(self, key):

        # ---------- SPACE ----------

        if key == "SPACE":
            self.text += " "
            return True

        # ---------- BACKSPACE ----------

        if key == "BACK":
            self.text = self.text[:-1]
            return True

        # ---------- ENTER ----------

        if key == "ENTER":
            self.text += " | "
            return True

        # ---------- CAPS ----------

        if key == "CAPS":
            self.caps = not self.caps
            return True

        # ---------- SHIFT ----------

        if key == "SHIFT":
            self.shift = True
            return True

        # ---------- TAB ----------

        if key == "TAB":
            self.text += "    "
            return True

        # ---------- IGNORE KEYS ----------

        if key in [
            "CTRL",
            "ALT",
            "WIN",
            "MENU",
            "FN",
            "ESC",
            "F1", "F2", "F3", "F4",
            "F5", "F6", "F7", "F8",
            "F9", "F10", "F11", "F12"
        ]:
            return False

        # ---------- CHARACTERS ----------

        if len(key) == 1:

            # Shift + Number

            if self.shift and key in self.shift_numbers:

                self.text += self.shift_numbers[key]
                self.shift = False
                return True

            # Letters

            if key.isalpha():

                if self.caps ^ self.shift:
                    self.text += key.upper()
                else:
                    self.text += key.lower()

                self.shift = False
                return True

            # Numbers

            self.text += key
            self.shift = False
            return True

        return False

    # ------------------------------------

    def get_text(self):
        return self.text

    # ------------------------------------

    def clear(self):
        self.text = ""

    # ------------------------------------

    def backspace(self):
        self.text = self.text[:-1]

    # ------------------------------------

    def get_last_word(self):

        words = self.text.split()

        if not words:
            return ""

        return words[-1]