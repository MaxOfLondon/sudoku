# -*- coding: utf-8
from os.path import abspath, dirname, join, normpath
from types import SimpleNamespace
from typing import List, Optional, Tuple, TypedDict, Union

import pygame

from .constants import (BLACK, BUBBLEGUM, CREAM, CUSTOM_EVENT_TYPE, FONT_SCALE,
                        WHITE)
from .util import attributes

BASE_PATH = abspath(dirname(__file__))

class CellArgs(TypedDict):
    border_top: Optional[int]
    border_right: Optional[int]
    border_bottom: Optional[int]
    border_left: Optional[int]
    border: Optional[List[int]]
    is_definite: Optional[bool]
    is_show_value: Optional[bool]
    font: Optional[pygame.Font]
    font_size: Optional[Union[int, float]]
    parent_surf: Optional[pygame.Surface]
    background_color: Optional[Tuple[int]]
    selected_color: Optional[Tuple[int]]
    definite_color: Optional[Tuple[int]]
    border_color: Optional[Tuple[int]]
    selected_line_width: Optional[int]


class Cell():
    cid = -1
    value = 0
    color = '#ffffff'
    border_color = '#000000'
    selected_color = '#0000ff'
    background_color = WHITE
    definite_color = CREAM
    border_top = 1
    border_bottom = 1
    border_left = 1
    border_right = 1
    selected_line_width = 3

    font = None
    font_size = None

    _definite = False
    _hint_on = False
    _guessed = False
    _show_value = True
    _selected = False

    def __init__(self, rect: pygame.Rect, **kwargs: CellArgs) -> None:
        """A square cell with a digit displayed.
        Offers theming of borders, selection and background colors.

        ### Params:
            rect: pygame.Rect: The bounding rectangle for the cell
                relative to parent_surf.

        ### Optional Params: CellArgs dictionary
            value: int = 0
                A value between 0 and 9.
                The value is displayed if:
                    - is_definite is True
                    - is_definite is False and is_show_value is True

            is_definite: bool = False
                If True the cell canot be highlited or edited and will
                be painted with definite_color background.

            is_show_value: bool = True
                Enables value to be drawn in the cell. See: value

            parent_surf: pygame.Surface = pygame.display.get_surface()
                A parent surface the cell will be painted on. Defaults
                to pygame diplay surface.

            background_color: Tuple = WHITE (255, 255, 255)
                RGB tuple value of normal cell background.

            border_color: Tuple = BLACK (0, 0, 0)
                RGB tuple value of inset border drawn around the cell

            definite_color: Tuple = CREAM (255, 255, 204)
                RGB tuple value of 'constant' value

            selected_color: Tuple = (0, 0, 255)
                RGB tuple value of selection border.

            border_left,
            border_top,
            border_right,
            border_bottom: int = 1
                Thickness of the border in pixels.

        Returns: None
        """
        self.rect = pygame.Rect(
            (rect.left, rect.top),
            (max(rect.width, rect.height), max(rect.width, rect.height))
        )
        self._dimension = rect.width
        self.surf = pygame.Surface((self._dimension, self._dimension))\
            .convert_alpha()

        kwargs_list = [
            'cid',
            'value',
            'is_definite',
            'is_show_value',
            'parent_surf',
            'border_top',
            'border_right',
            'border_bottom',
            'border_left',
            'font',
            'font_size',
            'background_color',
            'definite_color',
            'selected_color',
            'border_color',
            'selected_line_width'
        ]
        for key in kwargs:
            if key in kwargs_list:
                value = kwargs.get(key, None)
                if key.startswith('is_'):
                    key = key[2:]
                setattr(self, key, value)

        # TODO if specified cap the value

        if 'parent_surf' in kwargs:
            self.parent_surf = kwargs.get('parent_surf')
        else:
            self.parent_surf = pygame.display.get_surface()  # pragma no cover

        if self.font_size is None:
            self.font_size = int(self._dimension * FONT_SCALE)
        if self.font is None:
            if not pygame.font.get_init():
                pygame.font.init()  # pragma no cover
            self.font = pygame.font.Font(
                normpath(join(BASE_PATH, '../fonts/FreeSans.otf')),
                self.font_size)
        if 'border' in kwargs:
            self.border_left = kwargs['border'][0]
            self.border_top = kwargs['border'][1]
            self.border_right = kwargs['border'][2]
            self.border_bottom = kwargs['border'][3]

        self._set_border_offset()
        self._set_selected_offset()

    def __repr__(self):
        return attributes(self)  # pragma no cover

    def __str__(self):
        return str(attributes(self))

    def draw(self):
        self._draw_background()
        self._draw_number()
        self._draw_border()
        self._draw_selected()
        self.parent_surf.blit(self.surf, self.rect)

    def toggle_hint(self):
        self._hint_on = not self._hint_on

    def handle_clicked(self, pos: Tuple[int]) -> None:
        if self.rect.collidepoint(pos) and not self._definite:
            self._toggle_selected()
            event = pygame.event.Event(
                CUSTOM_EVENT_TYPE,
                key='selection_change',
                cid=self.cid,
                selected=self._selected)
            pygame.event.post(event)

    @property
    def hint(self) -> bool:
        return self._hint_on

    @hint.setter
    def hint(self, value: bool) -> None:
        self._hint_on = value

    @property
    def guessed(self) -> bool:
        return self._guessed

    @guessed.setter
    def guessed(self, value: bool) -> None:
        self._guessed = value

    @property
    def display(self) -> bool:
        return self._show_value

    @display.setter
    def display(self, value: bool) -> None:
        self._show_value = value

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        self._selected = value

    def _set_border_offset(self):
        offset_l_t = [
            v//2 if v % 2 else v//2 - 1
            for v in [self.border_left, self.border_top]
        ]
        offset_r_b = [
            v - v//2 if v % 2 else v//2 + 1
            for v in [self.border_right, self.border_bottom]
        ]

        offset = offset_l_t + offset_r_b
        border_names = ['left', 'top', 'right', 'bottom']
        self.border_offset = SimpleNamespace(
            **dict(zip(border_names, offset)))

    def _set_selected_offset(self):
        offset_l_t = [
            v//2 if v % 2 else v//2 - 1
            for v in [self.selected_line_width, self.selected_line_width]
        ]

        offset_r_b = [
            v - v//2 if v % 2 else v//2 + 1
            for v in [self.selected_line_width, self.selected_line_width]
        ]

        offset = offset_l_t + offset_r_b
        selected_names = ['left', 'top', 'right', 'bottom']
        self.selected_offset = SimpleNamespace(
            **dict(zip(selected_names, offset)))

    def _set_bg_color(self):
        color = WHITE
        if self._definite:
            color = self.definite_color
        elif self._hint_on:
            if not self._guessed and self.value > 0:
                color = BUBBLEGUM
        self.color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'

    def _toggle_selected(self):
        if not self._definite:
            self._selected = not self._selected

    def _draw_background(self):
        self._set_bg_color()
        self.surf.fill(self.color)

    def _draw_number(self):
        if (self._show_value and self.value):
            surf = self.font.render(str(self.value), True, BLACK, self.color)
            rect = surf.get_rect(center=(
                self._dimension//2, (self._dimension//2)*1.1)
            )
            self.surf.blit(surf, rect)

    def _draw_border(self):
        # left
        pygame.draw.line(
            self.surf,
            self.border_color,
            (self.border_offset.left, 0),
            (self.border_offset.left, self._dimension),
            self.border_left
        )
        # top
        pygame.draw.line(
            self.surf,
            self.border_color,
            (0, self.border_offset.top),
            (self._dimension, self.border_offset.top),
            self.border_top
        )
        # right
        pygame.draw.line(
            self.surf,
            self.border_color,
            (self._dimension - self.border_offset.right, 0),
            (self._dimension - self.border_offset.right, self._dimension),
            self.border_right
        )
        # bottom
        pygame.draw.line(
            self.surf,
            self.border_color,
            (0, self._dimension - self.border_offset.bottom),
            (self._dimension, self._dimension - self.border_offset.bottom),
            self.border_bottom
        )

    def _draw_selected(self):
        if not self._selected:
            return
        x1 = self.selected_offset.left + self.border_left
        y1 = self.selected_offset.top + self.border_top
        x2 = self._dimension - self.selected_offset.right - self.border_right
        y2 = self._dimension - self.selected_offset.bottom - self.border_bottom
        # letf
        pygame.draw.line(
            self.surf,
            self.selected_color,
            (x1, y1),
            (x1, y2),
            self.selected_line_width
        )
        # top
        pygame.draw.line(
            self.surf,
            self.selected_color,
            (x1, y1),
            (x2, y1),
            self.selected_line_width
        )
        # right
        pygame.draw.line(
            self.surf,
            self.selected_color,
            (x2, y1),
            (x2, y2),
            self.selected_line_width
        )
        # bottom
        pygame.draw.line(
            self.surf,
            self.selected_color,
            (x1, y2),
            (x2, y2),
            self.selected_line_width
        )
