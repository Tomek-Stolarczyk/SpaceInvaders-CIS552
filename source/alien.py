ALIEN_SPEED = 10

DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
DIRECTION_DOWN_LEFT = 3
DIRECTION_DOWN_RIGHT = 4
DIRECTION_NONE = 5


class Alien:
    def __init__(self, location):
        self.__alive = True
        self.__location = list(location)
        self.__alien_size = 20
        self.__points = self.__location[1]/(self.__alien_size)

    def get_position(self):
        return tuple(self.__location)

    def move(self, direction):
        global ALIEN_SPEED
        if (direction in [DIRECTION_DOWN_LEFT, DIRECTION_DOWN_RIGHT]):
            self.__location[1] += self.__alien_size
        elif direction == DIRECTION_LEFT:
            self.__location[0] -= ALIEN_SPEED
        elif direction == DIRECTION_RIGHT:
            self.__location[0] += ALIEN_SPEED

    def kill(self):
        self.__alive = False

    def alive(self):
        return self.__alive

    def get_size(self):
        return self.__alien_size

    def points(self):
        return self.__points

    def update(self):
        pass

    def destroy(self):
        pass


class DeadAlien:
    def __init__(self, location):
        self.__alive = False
        self.__location = list(location)
        self.__alien_size = 20

    def get_position(self):
        return tuple(self.__location)

    def move(self, direction):
        global ALIEN_SPEED
        if (direction in [DIRECTION_DOWN_LEFT, DIRECTION_DOWN_RIGHT]):
            self.__location[1] += self.__alien_size
        elif direction == DIRECTION_LEFT:
            self.__location[0] -= ALIEN_SPEED
        elif direction == DIRECTION_RIGHT:
            self.__location[0] += ALIEN_SPEED

    def kill(self):
        self.__alive = False

    def alive(self):
        return self.__alive

    def get_size(self):
        return self.__alien_size

    def update(self):
        pass

    def destroy(self):
        pass
