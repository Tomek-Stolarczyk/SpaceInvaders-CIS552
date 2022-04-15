import pygame
from Visuals.Common import load_texture
from Visuals.Common import GREEN, BLACK
from Visuals.Common import RENDER_FPS


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, base_player):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_texture("Player.png").convert()
        colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        colorImage.fill(GREEN)
        self.image.blit(colorImage, (0, 0),
                        special_flags=pygame.BLEND_RGBA_MULT)
        self.__base_player = base_player
        self.rect = self.image.get_rect()
        self.rect.center = self.__base_player.get_position()
        self.__death_persist_seconds = 0.5 * RENDER_FPS

    def update(self):
        if self.__base_player.alive():
            self.rect.center = self.__base_player.get_position()
        else:
            self.__death_persist_seconds -= 1
            new_position = self.__base_player.get_position()
            self.image = load_texture("Alien_Hit.png").convert()
            self.image.set_colorkey(BLACK, pygame.RLEACCEL)
            colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
            colorImage.fill(GREEN)
            self.image.blit(colorImage, (0, 0),
                            special_flags=pygame.BLEND_RGBA_MULT)
            self.rect = self.image.get_rect()
            self.rect.center = new_position
            if self.__death_persist_seconds <= 0:
                self.kill()
