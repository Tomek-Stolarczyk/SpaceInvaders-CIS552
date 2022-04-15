import pygame
from board import Board
from keyboards import VirtualKeyboard
from threading import Thread
from Visuals.Common import WIDTH, HEIGHT
from Visuals.Common import GREEN, WHITE, BLACK
from Visuals.Common import RENDER_FPS
from Visuals.Common import g_screen
from Visuals.PlayerSprite import PlayerSprite
from Visuals.AlienSprite import AlienSprite


def map_to_key(pygame_key):
    if pygame.K_LEFT == pygame_key:
        return "left"
    if pygame.K_RIGHT == pygame_key:
        return "right"
    if pygame.K_SPACE == pygame_key:
        return "space"
    return None


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
