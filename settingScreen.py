import settings
from screen import Screen
from Button import Button
from states import ScreenState


class SettingScreen(Screen):
    """Settings screen; its buttons depend on where it was reached from.

    - reached from START: a single "Back to Start";
    - reached from GAME: "Back to Game" (keeps the game state) plus
      "Back to Start" (resets the game).
    """

    def __init__(self, navigate, source_state):
        super().__init__()
        self.game_button = Button(
            "Back to Game", lambda: navigate(ScreenState.GAME)
        )
        self.start_button = Button(
            "Back to Start", lambda: navigate(ScreenState.START)
        )
        if source_state == ScreenState.GAME:
            self.buttons = [self.game_button, self.start_button]
        else:
            self.buttons = [self.start_button]
        self.sprites.add(*self.buttons)

    def arrange(self, surface):
        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2
        step = settings.BUTTON_HEIGHT + settings.BUTTON_GAP
        total = len(self.buttons) * step - settings.BUTTON_GAP
        y = center_y - total // 2 + settings.BUTTON_HEIGHT // 2
        for button in self.buttons:
            button.rect.center = (center_x, y)
            y += step