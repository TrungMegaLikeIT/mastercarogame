import pygame

import settings


class Screen:
    """Base class for every screen: owns sprites, event, update and drawing."""

    def __init__(self):
        self.sprites = pygame.sprite.LayeredUpdates()
        self._laid_out_size = None

    def layout(self, surface):
        """(Re)position sprites whenever the surface size changes."""
        size = surface.get_size()
        if size != self._laid_out_size:
            self._laid_out_size = size
            self.arrange(surface)

    def arrange(self, surface):
        """Position this screen's sprites for the given surface."""

    def reset(self):
        """Restore this screen to its initial state (no-op by default)."""

    def handle_event(self, event):
        for sprite in self.sprites:
            handler = getattr(sprite, "handle_event", None)
            if handler is not None:
                handler(event)

    def update(self):
        self.sprites.update()

    def render(self, surface):
        surface.fill(settings.BACKGROUND_COLOR)
        self.sprites.draw(surface)