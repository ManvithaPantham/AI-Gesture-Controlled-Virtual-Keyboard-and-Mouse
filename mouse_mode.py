import pyautogui

# Prevent mouse from stopping program if moved to corner
pyautogui.FAILSAFE = False


class MouseMode:

    def __init__(self):

        self.screen_width, self.screen_height = pyautogui.size()

        # Previous cursor position (for smoothing)
        self.prev_x = 0
        self.prev_y = 0

        # Smoothing factor (higher = smoother)
        self.smoothening = 6
        # Mouse states
        self.mouse_down = False
        self.last_click = 0
        self.double_click_delay = 0.4
    # -------------------------------------
    def press_left(self):
        if not self.mouse_down:
            print("Mouse Down")
            pyautogui.mouseDown()
            
            self.mouse_down = True


    def release_left(self):
        if self.mouse_down:
            print("Mouse Up")
            pyautogui.mouseUp()
            self.mouse_down = False


    def single_click(self):
        pyautogui.click()


    def double_click(self):
        pyautogui.doubleClick()
    def move(self, x, y, cam_width, cam_height):

        # Convert camera coordinates to screen coordinates

        screen_x = int(x * self.screen_width / cam_width)
        screen_y = int(y * self.screen_height / cam_height)

        # Cursor smoothing

        current_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        current_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening

        pyautogui.moveTo(current_x, current_y)

        self.prev_x = current_x
        self.prev_y = current_y

    # -------------------------------------

    def left_click(self):

        pyautogui.click()

    # -------------------------------------

    def right_click(self):

        pyautogui.rightClick()

    # -------------------------------------

    def double_click(self):

        pyautogui.doubleClick()

    # -------------------------------------

    def drag_start(self):

        pyautogui.mouseDown()

    # -------------------------------------

    def drag_end(self):

        pyautogui.mouseUp()

    # -------------------------------------

    def scroll_up(self):

        pyautogui.scroll(250)

    # -------------------------------------

    def scroll_down(self):

        pyautogui.scroll(-250)

    # -------------------------------------

    def move_left(self, pixels=25):

        pyautogui.moveRel(-pixels, 0)

    # -------------------------------------

    def move_right(self, pixels=25):

        pyautogui.moveRel(pixels, 0)

    # -------------------------------------

    def move_up(self, pixels=25):

        pyautogui.moveRel(0, -pixels)

    # -------------------------------------

    def move_down(self, pixels=25):

        pyautogui.moveRel(0, pixels)