import pygame
from board import Board
from keyboards import VirtualKeyboard
from threading import Thread
import os

WIDTH = 480  # width of our game window
HEIGHT = 640  # height of our game window
RENDER_FPS = 30  # frames per second

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DRAW_HITBOX = False
g_screen = None


def map_to_key(pygame_key):
    if pygame.K_LEFT == pygame_key:
        return "left"
    if pygame.K_RIGHT == pygame_key:
        return "right"
    if pygame.K_SPACE == pygame_key:
        return "space"
    return None


def load_texture(texture_name):
    texture_path = os.path.join("assets", texture_name)
    texture = pygame.image.load(texture_path)
    return pygame.transform.scale(texture, (40, 40))


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
        global DRAW_HITBOX, g_screen
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

            if DRAW_HITBOX:
                alien_size = self.__base_alien.get_size()
                pygame.draw.circle(g_screen, BLUE, new_position, alien_size)

        else:
            self.__death_persist_seconds -= 1
            new_position = self.__base_alien.get_position()
            self.image = load_texture("Alien_Hit.png").convert()
            self.image.set_colorkey(BLACK, pygame.RLEACCEL)
            self.rect = self.image.get_rect()
            self.rect.center = new_position

            if DRAW_HITBOX:
                alien_size = self.__base_alien.get_size()
                pygame.draw.circle(g_screen, BLUE, new_position, alien_size)
            if self.__death_persist_seconds <= 0:
                self.kill()


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

        global DRAW_HITBOX, g_screen
        if DRAW_HITBOX:
            player_size = self.__base_player.get_size()
            pygame.draw.circle(g_screen, BLUE, self.rect.center, player_size)


class PyGameRenderer:
    def __init__(self):
        self.__keyboard = VirtualKeyboard()

        self.__board = Board(WIDTH, HEIGHT-40, self.__keyboard)
        self.__player = self.__board.get_player()
        pygame.init()
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        global g_screen
        g_screen = self.__screen
        pygame.display.set_caption("Space Invaders")
        self.__clock = pygame.time.Clock()
        self.__running = True
        self.__render_thread = Thread(target=lambda: self.render_thread())
        self.__all_sprites = pygame.sprite.Group()
        self.__all_sprites.add(PlayerSprite(self.__player))

        for alien in self.__board.get_aliens():
            self.__all_sprites.add(AlienSprite(alien))

    def render_bullets(self):
        bullets = self.__board.get_shots()
        for bullet in bullets:
            rect = pygame.Rect(0, 0, 3, 3)
            rect.center = bullet.get_position()
            pygame.draw.rect(self.__screen, GREEN, rect)

    def render_game_over(self):
        score = self.__board.get_score()
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"Game Over - Score: {score}", True, WHITE, BLACK)
        textRect = text.get_rect()
        score_position = [WIDTH//2, HEIGHT//2]
        textRect.center = score_position
        self.__screen.blit(text, textRect)

    def render_score(self):
        score = self.__board.get_score()
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"Score: {score}", True, WHITE, BLACK)
        textRect = text.get_rect()
        player_y = self.__player.get_position()[1]
        player_height_offset = self.__player.get_size()*(3/2)
        score_position = [WIDTH//4, player_y + player_height_offset]
        textRect.center = score_position
        self.__screen.blit(text, textRect)

    def render_thread(self):
        while self.__running:
            if self.__board.get_game_over():
                self.__clock.tick(RENDER_FPS)

                self.__screen.fill(BLACK)
                self.__all_sprites.update()
                self.__all_sprites.draw(self.__screen)
                self.render_game_over()
                pygame.display.flip()
            else:
                self.__clock.tick(RENDER_FPS)
                self.__screen.fill(BLACK)
                self.__all_sprites.update()

                self.__all_sprites.draw(self.__screen)
                self.render_bullets()
                self.render_score()
                pygame.display.flip()
        print("Quit render thread")

    def window_event_loop(self):
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                if event.type == pygame.KEYDOWN:
                    self.__keyboard.key_down(map_to_key(event.key))
                if event.type == pygame.KEYUP:
                    self.__keyboard.key_up(map_to_key(event.key))
        print("quit window event loop")

    def start(self):
        self.__board.start()
        self.__render_thread.start()
        self.window_event_loop()

    def destroy(self):
        self.__board.destroy()
        self.__render_thread.join()
        pygame.quit()
