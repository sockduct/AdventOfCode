#! /usr/bin/env python3


'''
Simple grid class composed of integers
'''


# Libraries:
from itertools import chain


class Grid:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.unset = -1

        self.grid = [[self.unset for _ in range(x)] for _ in range(y)]

    def __repr__(self) -> str:
        return f'Grid({self.x}, {self.y})'

    def __str__(self) -> str:
        # Limit to first 10x10
        xover = False
        yover = False

        if self.x > 10:
            x = 10
            xover = True
        else:
            x = self.x

        if self.y > 10:
            y = 10
            yover = True
        else:
            y = self.y

        # Maximum digit width:
        width = len(str(max(chain.from_iterable(self.grid))))
        # Account for commas and add an extra space:
        width += width//3 + 1

        out = f'{"":{width}} |'
        # Grid column headers:
        for col in range(1, x + 1):
            out += f'{col:^{width}} '
        # (continued...)
        out += f'\n{"":->{width}}-+'
        for col in range(x):
            out += f'{"":->{width}}+'
        out += '\n'

        # Actual Grid:
        for row in range(y):
            out += f'{row + 1:^{width}} |'
            for col in range(x):
                out += f'{self.grid[row][col]:{width},} '
            if xover:
                out += '...'
            out += '\n'

        if yover:
            out += '...\n'

        return out

    def point(self, x: int, y: int) -> int:
        return self.grid[y][x]

    def set(self, x: int, y: int, val: int) -> None:
        self.grid[y][x] = val
