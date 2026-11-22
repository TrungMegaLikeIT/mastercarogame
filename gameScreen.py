import settings
from screen import Screen
from board import Board
from Button import Button
from states import ScreenState


class GameScreen(Screen):
    """Game screen: the Caro board plus 'Start' and 'Settings' buttons."""

    def __init__(self, navigate):
        super().__init__()
        self.board = Board()
        self.start_button = Button("Home", lambda: navigate(ScreenState.START))
        self.settings_button = Button(
            "Settings", lambda: navigate(ScreenState.SETTINGS)
        )
        self.sprites.add(self.board, self.start_button, self.settings_button)

    def reset(self):
        self.board.reset()

    def arrange(self, surface):
        center_x = surface.get_width() // 2
        self.board.rect.midtop = (center_x, settings.BOARD_MARGIN)
        button_center_y = (
            surface.get_height()
            - settings.BUTTON_MARGIN
            - settings.BUTTON_HEIGHT // 2
        )
        offset = (settings.BUTTON_WIDTH + settings.BUTTON_GAP) // 2
        self.start_button.rect.center = (center_x - offset, button_center_y)
        self.settings_button.rect.center = (center_x + offset, button_center_y)