from enum import Enum, auto


class ScreenState(Enum):
    """Game scenes. Used instead of boolean flags to switch screens."""

    START = auto()
    SETTINGS = auto()
    GAME = auto()