"""
Just another implementation of Conway's Game Of Life
inspired by 'Gravitar' (https://youtu.be/_HoW9riels0)
and a talk given by Jack Diederich (https://youtu.be/o9pEzgHorH0, PyCon US, Sta. Clara 2012).
"""
import sys
from random import randrange
from typing import Set, Tuple

import pygame as game

Point = Tuple[int, int]

BLACK = (0, 0, 0)
AMBER = (255, 192, 64)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 564
X_BIAS = SCREEN_WIDTH >> 1
Y_BIAS = SCREEN_HEIGHT >> 1
PIXEL_SIZE = 3

EF = {(0, -1), (0, 0), (0, 1), (0, 2), (1, -2), (2, -2), (-1, 0), (1, 0)}
THE_T = {(1, 0), (0, 1), (1, 1), (1, 2), (2, 2)}
INVERSE_T = {(1, 0), (1, 1), (1, 2), (0, 2), (2, 1)}
R_PENTOMINO = {(1, 0), (1, 1), (1, 2), (2, 0), (0, 1)}
GLIDER = {(0, 0), (1, 0), (2, 0), (2, 1), (1, 2)}
LINE_OF_SEVEN = {(-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0)}
LINE_OF_EIGHT = {(-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)}
LINE_OF_EIGHT_WITH_A_HOOK = {(-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
                            (3, -1)}
LINE_OF_TEN = {(x, 0) for x in range(-5, 5)}
CROSS = {(x, 0) for x in range(-5, 5)} | {(0, y) for y in range(-5, 5)}
ARROW = {(x, 0) for x in range(-5, 5)} | {(3, -1), (3, 1), (2, -2), (2, 2)}
RANDOM = set((randrange(-80, 80), randrange(-50, 50)) for _ in range(6502))


def neighbours(cell: Point) -> Point:
    x, y = cell
    yield x - 1, y - 1
    yield x, y - 1
    yield x + 1, y - 1
    yield x - 1, y
    yield x + 1, y
    yield x - 1, y + 1
    yield x, y + 1
    yield x + 1, y + 1


def advance(cells: Set[Point]) -> Set[Point]:
    new_cells = set()
    updated = cells | set(new_cell for cell in cells for new_cell in neighbours(cell))
    for new_cell in updated:
        count = sum((neighbour in cells) for neighbour in neighbours(new_cell))
        if count == 3 or (count == 2 and new_cell in cells):
            new_cells.add(new_cell)
    return new_cells


def run_application(baseline: Set[Tuple[int, int]]) -> None:
    cells = baseline.copy()
    game.init()
    screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        for event in game.event.get():
            if event.type == game.QUIT:
                sys.exit(0)
        screen.fill(BLACK)
        for x, y in cells:
            game.draw.rect(screen, AMBER, (
                PIXEL_SIZE * x + X_BIAS,
                PIXEL_SIZE * y + Y_BIAS,
                PIXEL_SIZE,
                PIXEL_SIZE
            ))
        game.display.flip()
        cells = advance(cells)
        game.time.delay(34)


if __name__ == '__main__':
    run_application(RANDOM)

# last line of code
