BULLET_SPEED = 15


class Shot:
    def __init__(self, initial_position, velocity_direction):
        self.__position = list(initial_position)
        self.__velocity = BULLET_SPEED * velocity_direction
        self.__alive = True

    def update(self):
        assert(self.__alive)
        self.__position[1] = self.__position[1] + self.__velocity

    def get_position(self):
        return tuple(self.__position)

    def alive(self):
        return self.__alive

    def kill(self):
        self.__alive = False

    def destroy(self):
        self.kill()

    def hits(self, object):
        object_position = object.get_position()
        object_size = object.get_size()
        new_position = list(self.__position)
        new_position[0] -= object_position[0]
        new_position[1] -= object_position[1]
        pos_magnitude = ((new_position[0] * new_position[0]) +
                         (new_position[1] * new_position[1]))

        return object_size*object_size >= pos_magnitude
