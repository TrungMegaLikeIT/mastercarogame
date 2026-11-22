import pygame


def solid_texture(size, color):
    """Create a texture manually in code: a single-color RGBA surface.

    The project has no image assets, so every texture is generated this way.
    """
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(color)
    return surface