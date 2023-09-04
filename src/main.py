# -*- coding: utf-8
import asyncio
import os
import sys

import i18n  # noqa # fix pygbag failing to source module
import pygame
import pygame_gui  # noqa # fix pygbag failing to source module

from sudoku.constants import HEIGHT, WIDTH
from sudoku.game import Game

os.environ['PYGAME_FORCE_SCALE'] \
    = os.environ.get('PYGAME_FORCE_SCALE', 'photo')
os.environ['PYGAME_BLEND_ALPHA_SDL2'] \
    = os.environ.get('PYGAME_BLEND_ALPHA_SDL2', '1')
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] \
    = os.environ.get('PYGAME_HIDE_SUPPORT_PROMPT', '1')

pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT))

if sys.platform in ('emscripten', 'wasi'):
    """browser's game window customisation"""
    import platform
    platform.window.onbeforeload = None
    platform.window.onbeforeunload = None
    platform.document.body.style.background = '#e6f2ff'

async def main():
    game = Game()
    await (game.run())

if __name__ == '__main__':
    asyncio.run(main())
