import pygame

import settings
import textures


class Button(pygame.sprite.Sprite):
    """Clickable button whose appearance is built from hand-made textures."""

    def __init__(self, text, on_click, font=None):
        super().__init__()
        self.on_click = on_click
        self.text = text
        self.font = font or pygame.font.SysFont(
            settings.FONT_NAME, settings.FONT_SIZE
        )
        self.normal_image = self._create_image(settings.BUTTON_COLOR, text)
        self.hover_image = self._create_image(settings.BUTTON_HOVER_COLOR, text)
        self.image = self.normal_image
        self.rect = self.image.get_rect()

    def _create_image(self, color, text):
        surface = textures.solid_texture(
            (settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT), color
        )
        pygame.draw.rect(
            surface, settings.BUTTON_BORDER_COLOR, surface.get_rect(), 2
        )
        label = self.font.render(text, True, settings.BUTTON_TEXT_COLOR)
        surface.blit(label, label.get_rect(center=surface.get_rect().center))
        return surface

    def handle_event(self, event):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            self.on_click()

    def update(self):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        self.image = self.hover_image if hovered else self.normal_image