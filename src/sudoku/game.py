import asyncio
import os
from os.path import abspath, dirname
from typing import List

import pygame
import pygame_gui

from .board import Board
from .constants import CHECK_GAME_OVER, CUSTOM_EVENT, HEIGHT, WIDTH
from .data import Data
from .hud import Hud
from .logic import Logic

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + "/../img/"
IMG_NAMES = [str(i) for i in range(1, 10)] \
    + ['delete', 'hint', 'start', 'gameover', 'reset', 'pause']
IMAGES = {
    name: pygame.image.load(f'{IMAGE_PATH}{name}.png') for name in IMG_NAMES
}

difficulty = 50

class Game:
    """Game manager"""

    def __init__(self) -> None:
        global IMAGES
        global difficulty
        self.start_img = IMAGES.get('start').convert()
        self.gameover_img = IMAGES.get('gameover').convert_alpha()

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Sudoku')
        # pygame.event.set_blocked(pygame.MOUSEMOTION)

        self.game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game_pause_screen = pygame.surface.Surface((WIDTH, HEIGHT))
        self.gameover_screen = pygame.surface.Surface((WIDTH, HEIGHT))
        self.game_screen_rect = self.game_screen.get_rect()

        self.ui_manager = pygame_gui.UIManager(
            self.game_screen_rect.size,
            os.path.join(os.path.abspath("."), 'sudoku/theme.json')
        )

        self.clock = pygame.time.Clock()
        self.difficulty = difficulty
        self.board = None
        self.hud = None
        self.logic = None
        self.elapsed_seconds = 0
        self.state = 'start'
        # self.reset_game()

    def reset_game(self) -> None:
        self.selected_id = None
        self.hint_on = False

        # logic
        self.logic = Logic()
        solution, puzzle = self.logic.create_game(self.difficulty)
        self.puzzle = Data(data=puzzle)
        self.solution = Data(data=solution)

        # board
        self.board_rect = pygame.Rect(
            6, 40, self.game_screen_rect.width - 8,
            self.game_screen_rect.width - 8)
        self.board = Board(self.board_rect, self.puzzle)

        # hud
        self.top_rect = pygame.Rect(0, 0, 500, self.board_rect.top)
        self.bottom_rect = pygame.Rect(
            4, self.board_rect.y + self.board_rect.h,
            self.game_screen.get_width() - 8, 600 - 50 - self.board_rect.h)
        # only one instance of hud to be kept between resets
        if self.hud is None:
            self.hud = Hud(
                self.game_screen,
                bottom_rect=self.bottom_rect,
                top_rect=self.top_rect,
                ui_manager=self.ui_manager,
                start_surf=self.start_img)

        self.draw()
        self.elapsed_seconds = 0

    def draw(self) -> None:
        if self.state == 'start':
            self.game_screen.blit(self.start_img, self.game_screen_rect)
        self.draw_board_and_hud()

    def get_expected_value(self, id) -> int:
        col = id % 9
        row = (id // 9) % 9
        return self.solution[row, col]

    def handle_input_key_down(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.state == 'playing':
                    # take grayscale screenshot
                    pygame.transform.grayscale(
                        self.game_screen, self.game_pause_screen)
                    self.state = 'pause'
                    pygame.time.set_timer(CHECK_GAME_OVER, 0)
                elif self.state == 'pause':
                    self.game_screen.blit(
                        self.start_img, self.game_screen_rect)
                    self.state = 'playing'
                    pygame.time.set_timer(CHECK_GAME_OVER, 1000)
            else:
                if event.key >= pygame.K_0 and event.key <= pygame.K_9:
                    value = event.key - 48
                    expeceted_value = self.get_expected_value(self.selected_id)
                    self.board.handle_number_entered(
                        self.selected_id, value, value == expeceted_value)
                elif event.key == pygame.K_h:
                    self.hint_on = not self.hint_on
                    self.board.set_hints(self.hint_on)
                    self.hud.draw(self.elapsed_seconds, self.hint_on)
                elif event.key == pygame.K_DELETE \
                        or event.key == pygame.K_BACKSPACE \
                        or event.key == pygame.K_x:
                    self.board.handle_deleted(self.selected_id)
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_f:
                    pygame.time.set_timer(CHECK_GAME_OVER, 0)
                    self.state = 'start'

    def handle_hud_button_clicked(self, event: pygame.event.Event) -> None:
        if event.id.isnumeric():
            event = pygame.event.Event(
                CUSTOM_EVENT,
                key='number_entered',
                value=int(event.id))
            pygame.event.post(event)
        elif event.id == 'delete':
            event = pygame.event.Event(
                pygame.KEYDOWN,
                key=pygame.K_DELETE)
            pygame.event.post(event)
        elif event.id == 'hint':
            event = pygame.event.Event(
                pygame.KEYDOWN,
                key=pygame.K_h)
            pygame.event.post(event)
        elif event.id == 'pause':
            event = pygame.event.Event(
                pygame.KEYDOWN,
                key=pygame.K_SPACE)
            pygame.event.post(event)
        elif event.id == 'reset':
            event = pygame.event.Event(
                pygame.KEYDOWN,
                key=pygame.K_r)
            pygame.event.post(event)

    def handle_custom_events(self, event: pygame.event.Event) -> None:
        if event.type == CUSTOM_EVENT and hasattr(event, 'key'):
            if event.key == 'hint_toggle':
                event = pygame.event.Event(
                    pygame.KEYDOWN,
                    key=pygame.K_h
                )
                pygame.event.post(event)
            if event.key == 'selection_change':
                id = event.id
                selected = event.selected
                if not selected:
                    self.selected_id = None
                if self.selected_id is not None and self.selected_id != id:
                    self.board.cells[self.selected_id].selected = False
                self.selected_id = id
            if event.key == 'number_entered':
                if self.selected_id:
                    value = event.value
                    expeceted_value = self.get_expected_value(
                        self.selected_id)
                    self.board.handle_number_entered(
                        self.selected_id, value, value == expeceted_value)
            if event.key == 'hud_button_clicked':
                self.handle_hud_button_clicked(event)

        if event.type == CHECK_GAME_OVER:
            if self.logic.is_game_over(
                self.board.get_values(),
                self.solution.flatten()
            ):
                # take grayscale screenshot
                pygame.transform.grayscale(
                    self.game_screen, self.gameover_screen)
                self.gameover_screen.blit(
                    self.gameover_img, (0, 0)
                )
                self.state = 'gameover'

    def handle_input_quit(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False

    def handle_input_mousedown(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == 'playing':
                x, y = x_board, y_board = pygame.mouse.get_pos()
                x_board, y_board = pygame.mouse.get_pos()

                # TODO adjast for padding is hardcoded
                x_board -= self.board.rect.left - 1
                y_board -= self.board.rect.top - 1
                [self.board.handle_clicked((x_board, y_board))]

                self.hud.handle_ckicked((x, y))

            elif self.state == 'pause':
                event = pygame.event.Event(
                    pygame.KEYDOWN,
                    key=pygame.K_SPACE)
                pygame.event.post(event)

    def handle_input_mosusemove(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            if self.state == 'playing':
                self.hud.handle_mousemotion(event)

    def handle_difficulty_change(self, event: pygame.event.Event) -> None:
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            self.difficulty = int(event.value)

    def handle_start(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_game()
            pygame.time.set_timer(CHECK_GAME_OVER, 1000)
            self.state = 'playing'
            self.elapsed_seconds = 0

    def handle_gameover(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_game()
            self.state = 'start'
            pygame.time.set_timer(CHECK_GAME_OVER, 1000)

    def handle_reset(self) -> None:
        self.reset_game()
        self.state = 'playing'

    def process_pause_state_events(self, events: List[pygame.event.Event]) \
            -> None:
        for event in events:
            self.handle_input_key_down(event)
            self.handle_input_quit(event)
            self.handle_input_mousedown(event)

    def process_playing_state_events(self, events: List[pygame.event.Event]) \
            -> None:
        for event in events:
            self.handle_custom_events(event)
            self.handle_input_key_down(event)
            self.handle_input_quit(event)
            self.handle_input_mosusemove(event)
            self.handle_input_mousedown(event)
            self.handle_difficulty_change(event)
            self.ui_manager.process_events(event)

    def handle_start_state_events(self, events: List[pygame.event.Event]) \
            -> None:
        for event in events:
            self.handle_start(event)
            self.handle_input_quit(event)

    def draw_board_and_hud(self) -> None:
        self.board.draw()
        self.hud.draw(self.elapsed_seconds, self.hint_on)
        self.ui_manager.draw_ui(self.game_screen)

    async def run(self) -> None:
        """Game loop"""
        self.running = True
        while self.running:
            time_delta = self.clock.tick(60)/1000.0
            events = pygame.event.get()
            if self.state == 'playing':
                self.elapsed_seconds += time_delta
                self.ui_manager.update(time_delta)
                self.draw_board_and_hud()
                self.process_playing_state_events(events)
                self.board.draw()
            elif self.state == 'start':
                self.game_screen.blit(self.start_img, self.game_screen_rect)
                self.handle_start_state_events(events)
            elif self.state == 'gameover':
                self.game_screen.blit(
                    self.gameover_screen, self.game_screen_rect)
                for event in events:
                    self.handle_gameover(event)
                    self.handle_input_quit(event)
            elif self.state == 'pause':
                self.game_screen.blit(
                    self.game_pause_screen, self.game_screen_rect)
                self.process_pause_state_events(events)

            pygame.display.update()
            await asyncio.sleep(0)
        pygame.quit()
        quit()
