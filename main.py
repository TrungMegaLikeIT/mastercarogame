import pygame

from app import App


def main():
    pygame.init()
    pygame.font.init()
    app = App()
    app.run()
    pygame.quit()


if __name__ == "__main__":
    main()