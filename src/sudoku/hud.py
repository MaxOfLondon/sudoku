
from os.path import abspath, dirname, join
from typing import Any, Tuple

import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from .constants import CUSTOM_EVENT, WHITE

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + "/../img"

class RoundButton(pygame.sprite.Sprite):
    def __init__(
        self,
        parent_surf: pygame.Surface,
        pos: pygame.Vector2,
        filepath: str,
        id: str,
        *groups: pygame.sprite.Group
    ):
        super().__init__(*groups)
        self.id = id
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image_orig = self.image.copy()
        self.image_hover = self.image.copy()
        self.image_hover.fill(
            ((0, 20, 20, 255)),
            special_flags=pygame.BLEND_ADD)
        # TODO create image_selected by yellow circle and impose image
        self.image_selected = self.image.copy()
        self.image_selected.fill(
            ((70, 90, 0, 255)),
            special_flags=pygame.BLEND_ADD)
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.Vector2(pos)
        self.selected = False

    def handle_clicked(self, pos: Tuple[int]):
        x, y = pos
        if self.rect.collidepoint(x, y):
            event = pygame.event.Event(
                CUSTOM_EVENT,
                key='hud_button_clicked',
                id=self.id)
            pygame.event.post(event)

    def handle_mouseover(self, pos: Tuple[int]):
        x, y = pos
        if self.rect.collidepoint(x, y):
            self.image = self.image_hover
        elif self.selected:
            self.image = self.image_selected
        else:
            self.image = self.image_orig

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

class Hud:
    def __init__(self, parent_surf, **kwargs: Any):
        self.parent_surf = parent_surf
        self.top_rect = kwargs['top_rect']
        self.bottom_rect = kwargs['bottom_rect']
        self.bottom_surf = pygame.Surface(
            (self.bottom_rect.width, self.bottom_rect.height)
        ).convert()
        self.top_surf = pygame.Surface(
            (self.top_rect.width, self.top_rect.height)
        ).convert()
        self.surf_top_bg = self.top_surf.copy()
        self.surf_top_bg.blit(kwargs['start_surf'], kwargs['top_rect'])

        self.ui_manager = kwargs['ui_manager']
        self.clock_font = pygame.font.SysFont("freesans", 40)

        self.controls_btm = []
        self.controls_top = []

        labels = [str(i) for i in range(1, 10)]
        for i, label in enumerate(labels):
            button = RoundButton(
                parent_surf=self.bottom_surf,
                pos=(2 + i*41, 5),
                filepath=join(IMAGE_PATH, f'{label}.png'),
                id=label
            )
            self.controls_btm.append(button)

        self.controls_btm.append(
            RoundButton(
                parent_surf=self.bottom_surf,
                pos=(2 + 9*41, 5),
                filepath=join(IMAGE_PATH, 'delete.png'),
                id='delete'
            )
        )

        self.controls_btm.append(
            RoundButton(
                parent_surf=self.bottom_surf,
                pos=(34 + 10*41, 5),
                filepath=join(IMAGE_PATH, 'hint.png'),
                id='hint'
            )
        )

        self.controls_top.append(
            RoundButton(
                parent_surf=self.top_surf,
                pos=(self.top_rect.width - 42, 0),
                filepath=join(IMAGE_PATH, 'reset.png'),
                id='reset'
            )
        )

        self.controls_top.append(
            RoundButton(
                parent_surf=self.top_surf,
                pos=(4, 2),
                filepath=join(IMAGE_PATH, 'pause.png'),
                id='pause'
            )
        )

        self.slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                (self.top_rect.width//2, 10),
                (self.top_rect.width//2 - 45, 20)),
            start_value=50,
            value_range=(0, 100),
            click_increment=0.5,
            manager=self.ui_manager,
            container=None,
            object_id=ObjectID(
                object_id='difficulty', class_id='#slider_difficulty'
            ),
        )

    def handle_ckicked(self, pos: Tuple[int]) -> None:
        x_top_panel, y_top_panel = x_btm_panel, y_btm_panel = pos
        x_top_panel -= self.top_rect.left
        y_top_panel -= self.top_rect.top
        x_btm_panel -= self.bottom_rect.left
        y_btm_panel -= self.bottom_rect.top

        [button.handle_clicked((x_btm_panel, y_btm_panel))
            for button in self.controls_btm]
        [button.handle_clicked((x_top_panel, y_top_panel))
            for button in self.controls_top]

    def handle_mousemotion(self, event: pygame.event.Event) -> None:
        x_top_panel, y_top_panel = x_btm_panel, y_btm_panel = event.pos
        x_top_panel -= self.top_rect.left
        y_top_panel -= self.top_rect.top
        x_btm_panel -= self.bottom_rect.left
        y_btm_panel -= self.bottom_rect.top

        [button.handle_mouseover((x_btm_panel, y_btm_panel))
            for button in self.controls_btm]
        [button.handle_mouseover((x_top_panel, y_top_panel))
            for button in self.controls_top]

    def draw(self, elapsed_seconds, hint_on):
        if hint_on:
            self.controls_btm[10].select()
        else:
            self.controls_btm[10].unselect()
        self.bottom_surf.fill(WHITE)
        [self.bottom_surf.blit(button.image, button.pos)
            for button in self.controls_btm]
        self.top_surf.blit(self.surf_top_bg, self.surf_top_bg.get_rect())
        [self.top_surf.blit(button.image, button.pos)
            for button in self.controls_top]
        self.parent_surf.blit(self.bottom_surf, self.bottom_rect)
        self.parent_surf.blit(self.top_surf, self.top_rect)
        self.draw_clock(elapsed_seconds)

    def draw_clock(self, elapsed_seconds):
        clock_str = self.get_clock_str(elapsed_seconds)
        clock_surf = self.clock_font.render(clock_str, True, WHITE)
        clock_rect = clock_surf.get_rect(
            left=38, centery=(self.top_rect.h//2)*1.2
        )
        self.top_surf.blit(clock_surf, clock_rect)
        self.parent_surf.blit(self.top_surf, self.top_surf.get_rect())

    def get_clock_str(self, seconds_in: int) -> str:
        (days, hours, minutes, secods) = Hud.normalize_seconds(seconds_in)
        return f"{days if days else ''} {hours:0>2}:{minutes:0>2}:{secods:0>2}"

    @staticmethod
    def normalize_seconds(seconds: int) -> tuple:
        (days, remainder) = divmod(seconds, 86400)
        (hours, remainder) = divmod(remainder, 3600)
        (minutes, seconds) = divmod(remainder, 60)

        return (int(days), int(hours), int(minutes), int(seconds))
