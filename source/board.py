import pygame
import threading
import random
from player import Player
from alien import Alien
from alien import DIRECTION_LEFT
from alien import DIRECTION_RIGHT
from alien import DIRECTION_DOWN_LEFT
from alien import DIRECTION_DOWN_RIGHT
from shot import Shot

GAME_FPS = 10  # for playing
# GAME_FPS = 1000 # for simulations
ALIEN_ATTACK_RATE = 10  # 1 shot every ALIEN_ATTACK_RATE*GAME_FPS seconds
ALIEN_MOVEMENT_RATE = 5  # 1 movement every 5 ticks


class Board:
    def __init__(self, board_size_x, board_size_y, keyboard):
        self.__score = 0
        self.__size_x = board_size_x
        self.__size_y = board_size_y
        self.__player = Player(keyboard, (20, board_size_y - 20), board_size_x)
        self.__shots = []
        self.__running = True
        self.__clock = pygame.time.Clock()
        self.__game_thread = threading.Thread(target=lambda: self.game_loop())
        self.__traveling_direction = DIRECTION_RIGHT
        self.__game_over = False
        self.initialize_aliens()

    def initialize_aliens(self):
        global ALIEN_ATTACK_RATE, GAME_FPS
        self.__alien_shoot_counter = ALIEN_ATTACK_RATE
        self.__alien_movement_counter = ALIEN_MOVEMENT_RATE
        self.__aliens = []
        for j in range(0, 5):
            for i in range(0, 10):
                self.__aliens.append(Alien((20 + 40 * i, 40 * (j + 1))))

    def get_next_travel_direction(self):
        if self.__traveling_direction == DIRECTION_DOWN_LEFT:
            self.__traveling_direction = DIRECTION_LEFT
        elif self.__traveling_direction == DIRECTION_DOWN_RIGHT:
            self.__traveling_direction = DIRECTION_RIGHT

        lowest_alien = 0

        for alien in self.__aliens:
            if alien.alive():
                alien_position = alien.get_position()
                if alien_position[1] > lowest_alien:
                    lowest_alien = alien_position[1]

                # Check bounce off right wall
                if ((self.__traveling_direction == DIRECTION_LEFT) and 
                    (alien_position[0] - alien.get_size() < 0)):
                    self.__traveling_direction = DIRECTION_DOWN_RIGHT
                # Check bounce off left wall
                elif ((self.__traveling_direction == DIRECTION_RIGHT) and 
                    (alien_position[0] + alien.get_size() > self.__size_x)):
                    self.__traveling_direction = DIRECTION_DOWN_LEFT
        
        # Check bottoming out
        if ((self.__traveling_direction == DIRECTION_DOWN_LEFT) and 
            (lowest_alien > (self.__size_y * 3 / 4))):
            self.__traveling_direction = DIRECTION_LEFT
        elif ((self.__traveling_direction == DIRECTION_DOWN_RIGHT) and 
            (lowest_alien > (self.__size_y * 3 / 4))):
            self.__traveling_direction = DIRECTION_RIGHT

        return self.__traveling_direction

    def get_most_forward_alien_in_column(self, col):
        alien = None
        # TODO not getting most forward alien
        for i in range(col, len(self.__aliens), 10):
            if self.__aliens[i].alive():
                alien = self.__aliens[i]

        return alien

    def print_aliens(self):
        printable = ""
        for i in range(5):
            for j in range(10):
                alien_index = j+i*10
                alien = self.__aliens[alien_index]
                printable += str(alien.get_position()) + ""
                if alien.alive():
                    printable += "A "
                else:
                    printable += "D "
            printable += "\n"
        print(printable)

    def get_shooting_alien(self):
        most_forward_aliens = [self.get_most_forward_alien_in_column(i) for i in range(10)]     
        most_forward_alive_aliens = [i for i in most_forward_aliens if i is not None and i.alive()]
        
        shooting_alien = random.choice(most_forward_alive_aliens)
        return shooting_alien 

    def update_aliens(self):
        if self.__alien_shoot_counter == 0:
            self.__alien_shoot_counter = ALIEN_ATTACK_RATE
            shooting_alien = self.get_shooting_alien()
            bullet_position = list(shooting_alien.get_position())
            bullet_position[1] += shooting_alien.get_size() + 10
            self.__shots.append(Shot(bullet_position, 1))
        else:
            self.__alien_shoot_counter -= 1

        if self.__alien_movement_counter == 0:
            self.__alien_movement_counter = ALIEN_MOVEMENT_RATE
        
            direction = self.get_next_travel_direction()
            for alien in self.__aliens:
                alien.move(direction)
        else:
            self.__alien_movement_counter -= 1

    def start(self):
        self.__game_thread.start()

    def get_shots(self):
        return self.__shots
    
    def get_aliens(self):
        return self.__aliens
    
    def get_player(self):
        return self.__player

    def destroy(self):
        self.__running = False
        self.__game_thread.join()
        self.__player.destroy()
        [shot.destroy() for shot in self.__shots]
        [alien.destroy() for alien in self.__aliens]

    def get_score(self):
        return self.__score

    def get_game_over(self):
        return self.__game_over

    def game_loop(self):
        while not self.__game_over and self.__running:
            self.__player.update()
            if self.__player.get_shoot():
                bullet_position = list(self.__player.get_position())
                bullet_position[1] -= self.__player.get_size() + 5
                self.__shots.append(Shot(bullet_position, -1))
            [shot.update() for shot in self.__shots]

            self.update_aliens()

            # Check for collision
            for shot in self.__shots:
                if ((shot.get_position()[1] < 0) or
                    (shot.get_position()[1] > self.__size_y)):
                    shot.kill()
                for alien in self.__aliens:
                    if alien.alive() and shot.hits(alien):
                        alien.kill()
                        shot.kill()
                        self.__score += alien.points()
                        alive_aliens = len([alien for alien in self.__aliens if alien.alive()])
                        if alive_aliens == 0:
                            self.__game_over = True
                if shot.hits(self.__player):
                    shot.kill()
                    self.__player.kill()
                    self.__game_over = True

            self.__shots = [shot for shot in self.__shots if shot.alive()]

            self.__clock.tick(GAME_FPS)