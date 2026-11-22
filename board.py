import pygame

import settings
import textures


class Board(pygame.sprite.Sprite):
    """Caro board: grid rendering, move placement and win detection."""

    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = 2

    def __init__(self):
        super().__init__()
        self.rows = settings.BOARD_ROWS
        self.cols = settings.BOARD_COLS
        self.cell_size = settings.BOARD_CELL_SIZE
        self.grid = [[self.EMPTY] * self.cols for _ in range(self.rows)]
        self.current_player = self.PLAYER_X
        self.winner = None
        self.image = self._create_background()
        self.rect = self.image.get_rect()

    def _create_background(self):
        size = (self.cols * self.cell_size + 1, self.rows * self.cell_size + 1)
        surface = textures.solid_texture(size, settings.BOARD_COLOR)
        for index in range(self.rows + 1):
            y = index * self.cell_size
            pygame.draw.line(
                surface, settings.BOARD_GRID_COLOR, (0, y), (size[0] - 1, y)
            )
        for index in range(self.cols + 1):
            x = index * self.cell_size
            pygame.draw.line(
                surface, settings.BOARD_GRID_COLOR, (x, 0), (x, size[1] - 1)
            )
        return surface

    def handle_event(self, event):
        if (
            self.winner is None
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            cell = self.cell_at(event.pos)
            if cell is not None:
                self.place(*cell)

    def place(self, row, col):
        if self.grid[row][col] != self.EMPTY:
            return
        self.grid[row][col] = self.current_player
        self._draw_stone(row, col)
        if self._has_line_of_length(row, col):
            self.winner = self.current_player
        else:
            self.current_player = self.other_player(self.current_player)

    def reset(self):
        """Return the board to its initial state (also clears the winner)."""
        self.grid = [[self.EMPTY] * self.cols for _ in range(self.rows)]
        self.current_player = self.PLAYER_X
        self.winner = None
        self.image = self._create_background()

    def cell_at(self, pos):
        x = pos[0] - self.rect.left
        y = pos[1] - self.rect.top
        if not (
            0 <= x < self.image.get_width() and 0 <= y < self.image.get_height()
        ):
            return None
        return y // self.cell_size, x // self.cell_size

    @staticmethod
    def other_player(player):
        return Board.PLAYER_O if player == Board.PLAYER_X else Board.PLAYER_X

    def _draw_stone(self, row, col):
        center = (
            col * self.cell_size + self.cell_size // 2,
            row * self.cell_size + self.cell_size // 2,
        )
        radius = self.cell_size // 2 - 3
        color = (
            settings.PLAYER_X_COLOR
            if self.grid[row][col] == self.PLAYER_X
            else settings.PLAYER_O_COLOR
        )
        pygame.draw.circle(self.image, color, center, radius)

    def _has_line_of_length(self, row, col):
        player = self.grid[row][col]
        for delta_row, delta_col in ((0, 1), (1, 0), (1, 1), (1, -1)):
            count = (
                1
                + self._run_length(row, col, delta_row, delta_col, player)
                + self._run_length(row, col, -delta_row, -delta_col, player)
            )
            if count >= settings.WIN_LENGTH:
                return True
        return False

    def _run_length(self, row, col, delta_row, delta_col, player):
        count = 0
        row += delta_row
        col += delta_col
        while (
            0 <= row < self.rows
            and 0 <= col < self.cols
            and self.grid[row][col] == player
        ):
            count += 1
            row += delta_row
            col += delta_col
        return count