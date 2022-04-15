PLAYER_SIZE = 25


class Player:
    def __init__(self, keyboard, location, board_limit):
        self.__location = list(location)
        self.__keyboard = keyboard
        self.__shoot = False
        self.__board_limit = board_limit
        self.__space_pressed = False
        self.__alive = True

    def update(self):
        if self.__keyboard.get_key_pressed("left"):
            self.__location[0] -= 10
        elif self.__keyboard.get_key_pressed("right"):
            self.__location[0] += 10

        if self.__location[0] < 0:
            self.__location[0] = 0
        if self.__location[0] > self.__board_limit:
            self.__location[0] = self.__board_limit

        if self.__keyboard.get_key_pressed("space"):
            self.__space_pressed = True
        else:
            if self.__space_pressed:
                self.__shoot = True
                self.__space_pressed = False

    def alive(self):
        return self.__alive

    def get_position(self):
        return self.__location

    def get_shoot(self):
        if self.__shoot:
            self.__shoot = False
            return True
        else:
            return False

    def destroy(self):
        pass

    def kill(self):
        self.__alive = False

    def get_size(self):
        return PLAYER_SIZE
