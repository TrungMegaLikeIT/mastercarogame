import settings
from screen import Screen
from Button import Button
from states import ScreenState


class StartScreen(Screen):
    """Start screen with 'Start' and 'Settings' buttons."""

    def __init__(self, navigate):
        super().__init__()
        self.start_button = Button("Start", lambda: navigate(ScreenState.GAME))
        self.settings_button = Button(
            "Settings", lambda: navigate(ScreenState.SETTINGS)
        )
        self.sprites.add(self.start_button, self.settings_button)

    def arrange(self, surface):
        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2
        offset = (settings.BUTTON_HEIGHT + settings.BUTTON_GAP) // 2
        self.start_button.rect.center = (center_x, center_y - offset)
        self.settings_button.rect.center = (center_x, center_y + offset)