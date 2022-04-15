import keyboard
from threading import Thread


class VirtualKeyboard:
    def __init__(self):
        self.__left_pressed = False
        self.__right_pressed = False
        self.__space_pressed = False

    def get_key_pressed(self, key):
        if key == "left":
            return self.__left_pressed
        if key == "right":
            return self.__right_pressed
        if key == "space":
            return self.__space_pressed
        return False

    def key_down(self, key):
        if key == "left":
            self.__left_pressed = True
        if key == "right":
            self.__right_pressed = True
        if key == "space":
            self.__space_pressed = True

    def key_up(self, key):
        if key == "left":
            self.__left_pressed = False
        if key == "right":
            self.__right_pressed = False
        if key == "space":
            self.__space_pressed = False

    def destroy(self):
        pass


class PhysicalKeyboard:
    def __init__(self):
        self.__left_pressed = False
        self.__right_pressed = False
        self.__running = True
        self.__thread = Thread(target=lambda: self.keyboard_parsing())
        self.__thread.start()

    def keyboard_parsing(self):
        while self.__running:
            event = keyboard.read_event()
            if event.name == "right":
                self.__right_pressed = event.event_type == keyboard.KEY_DOWN
            if event.name == "left":
                self.__left_pressed = event.event_type == keyboard.KEY_DOWN
            if event.name == "esc":
                print("quit requested")

    def get_key_pressed(self):
        if self.__left_pressed:
            return "left"
        if self.__right_pressed:
            return "right"
        return None

    def press_key(self, key):
        raise Exception("Shouldn't be called")

    def destroy(self):
        self.__running = False
        keyboard.write("q")
        self.__thread.join()
