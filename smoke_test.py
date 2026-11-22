"""Headless end-to-end check — run `python smoke_test.py` from the repo root.

Uses the SDL dummy driver, so it needs no display. Verifies screen transitions,
settings button sets, board rules, win detection and game reset.
"""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

pygame.init()
pygame.font.init()

import settings
from app import App
from states import ScreenState
from board import Board


def click(app, pos):
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos))
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=pos))
    app.step()


def cell_pos(board, row, col):
    half = board.cell_size // 2
    return (
        board.rect.left + col * board.cell_size + half,
        board.rect.top + row * board.cell_size + half,
    )


def empty_grid(board):
    return all(cell == Board.EMPTY for row in board.grid for cell in row)


def main():
    app = App()
    app.step()  # lay out the start screen
    assert app.state == ScreenState.START

    # --- Settings from the start menu has a single button. ---
    start_screen = app.screens[ScreenState.START]
    click(app, start_screen.settings_button.rect.center)
    assert app.state == ScreenState.SETTINGS
    settings_screen = app.screens[ScreenState.SETTINGS]
    assert settings_screen.buttons == [settings_screen.start_button]
    assert settings_screen.start_button.text == "Back to Start"
    app.step()  # lay out the freshly created settings screen
    click(app, settings_screen.start_button.rect.center)
    assert app.state == ScreenState.START

    # --- Start a game. ---
    click(app, app.screens[ScreenState.START].start_button.rect.center)
    assert app.state == ScreenState.GAME
    game_screen = app.screens[ScreenState.GAME]
    board_obj = game_screen.board
    app.step()  # one frame to lay out the game screen
    assert board_obj.rect.midtop == (
        settings.WINDOW_WIDTH // 2,
        settings.BOARD_MARGIN,
    )

    # --- Stone placement and X/O alternation. ---
    click(app, cell_pos(board_obj, 3, 3))
    assert board_obj.grid[3][3] == Board.PLAYER_X
    click(app, cell_pos(board_obj, 3, 4))
    assert board_obj.grid[3][4] == Board.PLAYER_O

    # --- Occupied cells are refused. ---
    click(app, cell_pos(board_obj, 3, 3))
    assert board_obj.grid[3][3] == Board.PLAYER_X

    # --- Settings from the game has two buttons. ---
    click(app, game_screen.settings_button.rect.center)
    assert app.state == ScreenState.SETTINGS
    settings_screen = app.screens[ScreenState.SETTINGS]
    assert settings_screen.buttons == [
        settings_screen.game_button,
        settings_screen.start_button,
    ]
    assert settings_screen.game_button.text == "Back to Game"
    app.step()  # lay out the freshly created settings screen

    # "Back to Game" keeps the same game instance and its moves.
    click(app, settings_screen.game_button.rect.center)
    assert app.state == ScreenState.GAME
    assert app.screens[ScreenState.GAME] is game_screen
    assert board_obj.grid[3][3] == Board.PLAYER_X
    assert board_obj.grid[3][4] == Board.PLAYER_O

    # --- Win detection: X fills row 0 while O answers in row 1. ---
    for col in range(settings.WIN_LENGTH):
        click(app, cell_pos(board_obj, 0, col))  # X
        if col < settings.WIN_LENGTH - 1:
            click(app, cell_pos(board_obj, 1, col))  # O
    assert board_obj.winner == Board.PLAYER_X, board_obj.winner

    # The board locks after a win.
    click(app, cell_pos(board_obj, 2, 2))
    assert board_obj.grid[2][2] == Board.EMPTY

    # --- "Back to Start" resets the game for the next run. ---
    click(app, game_screen.settings_button.rect.center)
    assert app.state == ScreenState.SETTINGS
    settings_screen = app.screens[ScreenState.SETTINGS]
    app.step()  # lay out the freshly created settings screen
    click(app, settings_screen.start_button.rect.center)
    assert app.state == ScreenState.START
    click(app, app.screens[ScreenState.START].start_button.rect.center)
    assert app.state == ScreenState.GAME
    assert app.screens[ScreenState.GAME] is game_screen  # same instance, reset
    assert empty_grid(board_obj)
    assert board_obj.winner is None
    assert board_obj.current_player == Board.PLAYER_X

    # The reset board accepts moves again.
    click(app, cell_pos(board_obj, 5, 5))
    assert board_obj.grid[5][5] == Board.PLAYER_X

    # --- F11 toggles fullscreen. ---
    assert settings.FULLSCREEN is False
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F11))
    app.step()
    assert settings.FULLSCREEN is True
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F11))
    app.step()
    assert settings.FULLSCREEN is False

    pygame.quit()
    print("smoke_test: all checks passed")


if __name__ == "__main__":
    main()