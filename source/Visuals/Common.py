import pygame
import os

WIDTH = 480  # width of our game window
HEIGHT = 640  # height of our game window
RENDER_FPS = 30  # frames per second

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

g_screen = None  # Global instance of render screen


def load_texture(texture_name):
    texture_path = os.path.join("assets", texture_name)
    texture = pygame.image.load(texture_path)
    return pygame.transform.scale(texture, (40, 40))
