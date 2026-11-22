import pygame

import settings
from states import ScreenState
from startScreen import StartScreen
from settingScreen import SettingScreen
from gameScreen import GameScreen


class App:
    """Owns the pygame window, the main loop and screen transitions."""

    def __init__(self):
        self.screen = self.create_screen()
        self.clock = pygame.time.Clock()
        self.screens = {
            ScreenState.START: StartScreen(self.navigate),
            ScreenState.SETTINGS: SettingScreen(
                self.navigate, ScreenState.START
            ),
            ScreenState.GAME: GameScreen(self.navigate),
        }
        self.state = ScreenState.START
        self.running = True

    def create_screen(self):
        if settings.FULLSCREEN:
            surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            surface = pygame.display.set_mode(
                (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT),
                pygame.RESIZABLE,
            )
        pygame.display.set_caption(settings.WINDOW_TITLE)
        return surface

    def navigate(self, target):
        if target == ScreenState.START:
            # Leaving the game for good (Home or Back to Start): fresh board.
            self.screens[ScreenState.GAME].reset()
        elif target == ScreenState.SETTINGS:
            # self.state is the screen we are coming from.
            self.screens[ScreenState.SETTINGS] = SettingScreen(
                self.navigate, self.state
            )
        self.state = target

    def handle_event(self, event, current):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            settings.FULLSCREEN = not settings.FULLSCREEN
            self.screen = self.create_screen()
        current.handle_event(event)

    def step(self):
        current = self.screens[self.state]
        current.layout(self.screen)
        for event in pygame.event.get():
            self.handle_event(event, current)
        current.update()
        current.render(self.screen)
        pygame.display.flip()
        self.clock.tick(settings.FPS)

    def run(self):
        while self.running:
            self.step()