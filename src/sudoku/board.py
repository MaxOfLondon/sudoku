# -*- coding: utf-8
from typing import List, Tuple

import pygame

from .cell import Cell
from .constants import WHITE


class Board:
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
                id=index,
                value=value,
                is_definite=bool(value),
                border=self._make_border(index),
                parent_surf=self.surf
            )
            for index, value in enumerate(puzzle.flatten())
        ]

    def handle_number_entered(self, id, value, is_correct) -> None:
        """Set new value to selected_id cell"""
        if id is not None:
            self.cells[id].value = value
            self.cells[id].guessed = is_correct
            self.cells[id].draw()

    def handle_deleted(self, id: int) -> None:
        if id is not None:
            self.cells[id].value = 0
            self.cells[id].draw()

    def handle_clicked(self, pos: Tuple) -> None:
        [cell.handle_clicked(pos) for cell in self.cells]

    def set_hints(self, hint_on):
        for cell in self.cells:
            cell.hint = hint_on
        self.draw()

    def draw(self) -> None:
        self.surf.fill(WHITE)
        [cell.draw() for cell in self.cells]
        self.game_screen.blit(self.surf, self.rect)

    def get_value(self, id) -> int or None:
        return self.cells[id].value

    def get_values(self) -> List[int]:
        return [cell.value for cell in self.cells]

    def _make_rect(self, index: int) -> pygame.Rect:
        rect = pygame.Rect(
            index // 9 * self.square_size,
            index % 9 * self.square_size,
            self.square_size,
            self.square_size
        )
        return rect

    def _make_border(self, index: int) -> List[int]:
        t = 1
        t2 = 2 * t
        t4 = 4 * t
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
