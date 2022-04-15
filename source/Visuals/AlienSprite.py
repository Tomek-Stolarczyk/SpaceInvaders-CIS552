import pygame
from Visuals.Common import load_texture
from Visuals.Common import BLACK
from Visuals.Common import RENDER_FPS


class AlienSprite(pygame.sprite.Sprite):
    def __init__(self, base_alien):
        pygame.sprite.Sprite.__init__(self)
        self.__base_alien = base_alien
        self.__current_texture = 0

        self.__textures = []
        self.__textures.append(load_texture("Alien3.0.png"))
        self.__textures.append(load_texture("Alien3.1.png"))
        self.__previous_position = [0, 0]
        self.__death_persist_seconds = 0.5 * RENDER_FPS

    def update(self):
        if self.__base_alien.alive():
            new_position = self.__base_alien.get_position()
            if (self.__previous_position[0] != new_position[0] or
               self.__previous_position[1] != new_position[1]):
                self.__previous_position[0] = new_position[0]
                self.__previous_position[1] = new_position[1]
                self.__current_texture ^= 1
            self.image = self.__textures[self.__current_texture].convert()
            self.image.set_colorkey(BLACK, pygame.RLEACCEL)

            self.rect = self.image.get_rect()
            self.rect.center = new_position

        else:
            self.__death_persist_seconds -= 1
            new_position = self.__base_alien.get_position()
            self.image = load_texture("Alien_Hit.png").convert()
            self.image.set_colorkey(BLACK, pygame.RLEACCEL)
            self.rect = self.image.get_rect()
            self.rect.center = new_position

            if self.__death_persist_seconds <= 0:
                self.kill()
