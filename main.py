
import pygame
import settings

pygame.init()

def create_screen():
    if settings.FULLSCREEN:
        screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )
    else:
        screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT),
            pygame.RESIZABLE
        )

    pygame.display.set_caption(settings.WINDOW_TITLE)
    return screen


screen = create_screen()
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Toggle Fullscreen with F11
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                settings.FULLSCREEN = not settings.FULLSCREEN
                screen = create_screen()

    screen.fill(settings.BACKGROUND_COLOR)

    pygame.display.flip()
    clock.tick(settings.FPS)

pygame.quit()