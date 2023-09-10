# -*- coding: utf-8
from typing import List, Tuple

import pygame

from .cell import Cell
from .constants import DEFAULT_BORDER_WIDTH, WHITE


class Board:
    cells = []

    def __init__(self, rect: pygame.Rect, puzzle: List[List[int]]) -> None:
        self.game_screen = pygame.display.get_surface()
        self.square_size = rect.width // 9
        self.surf = pygame.Surface(
            (self.square_size * 9 + 2, self.square_size * 9 + 2)).convert()
        self.rect = rect
        self.puzzle = puzzle
        self.cells = [
            Cell(
                self._make_rect(index),
                cid=index,
                value=value,
                is_definite=bool(value),
                border=self._make_border(index, DEFAULT_BORDER_WIDTH),
                parent_surf=self.surf
            )
            for index, value in enumerate(puzzle.flatten())
        ]

    def __repr__(self):
        return f'{self.cells}'  # pragma no cover

    def handle_number_entered(self, index, value, is_correct) -> None:
        """Set new value to selected_id cell"""
        if index is not None:
            self.cells[index].value = value
            self.cells[index].guessed = is_correct

    def handle_deleted(self, index: int) -> None:
        if index is not None:
            self.cells[index].value = 0
            self.cells[index].guessed = False

    def handle_clicked(self, pos: Tuple[int]) -> None:
        [cell.handle_clicked(pos) for cell in self.cells]

    def set_hints(self, value: bool) -> None:
        for cell in self.cells:  # pragma no cover
            cell.hint = value

    def draw(self) -> None:
        self.surf.fill(WHITE)
        [cell.draw() for cell in self.cells]
        self.game_screen.blit(self.surf, self.rect)

    def get_value(self, index: int) -> int or None:
        if 0 <= index < len(self.cells):
            return self.cells[index].value
        return None

    def get_values(self) -> List[int]:
        return [cell.value for cell in self.cells]

    def _make_rect(self, offset: int) -> pygame.Rect:
        rect = pygame.Rect(
            (offset // 9 * self.square_size, offset % 9 * self.square_size),
            (self.square_size, self.square_size)
        )
        return rect

    def _make_border(self, index: int, border=1) -> List[int]:
        """Adjusts border thickness of a cell depending on cell's index
        Returns list of [left, top, right, bottom] thickness in pixels
        """
        t = border
        t2 = 2 * border
        t4 = 4 * border
        ia = index + 1
        i9a = index + 9

        # every 3 cells t2 border or t1
        tp = t2 if index % 3 == 0 else t
        bm = t2 if ia % 3 == 0 else t
        lt = t2 if (index // 9) % 3 == 0 else t
        rt = t2 if (i9a // 9) % 3 == 0 else t

        # outside border t4
        tp = t4 if index % 9 == 0 else tp
        bm = t4 if ia % 9 == 0 else bm
        lt = t4 if (index // 9) == 0 else lt
        rt = t4 if (i9a // 9) % 9 == 0 else rt

        return [lt, tp, rt, bm]
