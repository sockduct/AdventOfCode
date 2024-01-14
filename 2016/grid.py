#! /usr/bin/env python3

#
# To do:
# * Fix mypy errors - not sure how to fix some of them, so just ignored
#   See # type: ...
#

'''
Simple grid class
'''


# Libraries
from typing import Any, Callable, NamedTuple, Sequence, cast


class Values(NamedTuple):
    on: bool|int
    off: bool|int
    toggle: bool|int|Callable[[bool], bool]


class Grid:
    def __init__(self, x: int, y: int, val: type[bool|int]=bool, x_str_max: int=10,
                 y_str_max: int=10, alt_str_on: str='*', alt_str_off: str='.',
                 alt_str: bool=False) -> None:
        self.x = x
        self.y = y
        self.x_str_max = x_str_max
        self.y_str_max = y_str_max
        self.alt_str_on = alt_str_on
        self.alt_str_off = alt_str_off
        self.alt_str = alt_str
        if val.__name__ == 'bool':
            self.simple = True
            self.vals = Values(True, False, lambda x: not x)
        elif val.__name__ == 'int':
            self.simple = False
            self.vals = Values(1, 0, 2)
        else:
            raise ValueError(f'Expected val of bool|int, got "{val.__name__}"')

        self.grid = [[self.vals.off for _ in range(x)] for _ in range(y)]

    def __repr__(self) -> str:
        return f'Grid({self.x}, {self.y})'

    def __str__(self) -> str:
        # Limit to first 10x10
        xover = False
        yover = False

        if self.x > self.x_str_max:
            x = self.x_str_max
            xover = True
        else:
            x = self.x

        if self.y > self.y_str_max:
            y = self.y_str_max
            yover = True
        else:
            y = self.y

        out = ''
        for row in range(y):
            for col in range(x):
                if self.alt_str:
                    out += self.alt_str_on if self.grid[row][col] else self.alt_str_off
                else:
                    out += f'{int(self.grid[row][col])}'
            if xover:
                out += '...'
            out += '\n'

        if yover:
            out += '...\n'

        return out

    def altstr(self, state: bool) -> None:
        self.alt_str = state

    def point(self, x: int, y: int) -> bool|int:
        return self.grid[y][x]

    def status(self) -> tuple[int, int]:
        enabled = sum(sum(row) for row in self.grid)
        disabled = self.x * self.y - enabled

        return enabled, disabled

    def update(self, p1: int|Sequence[int], p2: int|Sequence[int], op: str) -> None:
        # val: bool|int|Callable[[bool|int], bool|int] # type: couldn't get right, using Any...
        val: Any
        match op:
            case 'on':
                if self.simple:
                    alt = False
                    val = self.vals.on
                else:
                    alt = True
                    val = lambda x: x + self.vals.on
            case 'off':
                if self.simple:
                    alt = False
                    val = self.vals.off
                else:
                    alt = True
                    val = lambda x: x - 1 if x > 1 else 0
            case 'toggle':
                alt = True
                val = (self.vals.toggle if self.simple
                       else (lambda x: x + 2)) # type: ignore[return-value]
            case _:
                raise ValueError(f'Expected on|off|toggle, got "{op}"')

        # Could just look for a generic sequence or iterable:
        if isinstance(p1, (list, tuple)):
            for y in range(p1[1], p2[1] + 1): # type: ignore[index]
                for x in range (p1[0], p2[0] + 1): # type: ignore[index]
                    self.grid[y][x] = val(self.grid[y][x]) if alt else val
        else:
            self.grid[p2][p1] = val(self.grid[p2][p1]) if alt else val # type: ignore [index]

    def on(self, p1: int|Sequence[int], p2: int|Sequence[int]) -> None:
        self.update(p1, p2, 'on')

    def off(self, p1: int|Sequence[int], p2: int|Sequence[int]) -> None:
        self.update(p1, p2, 'off')

    def toggle(self, p1: int|Sequence[int], p2: int|Sequence[int]) -> None:
        self.update(p1, p2, 'toggle')

    def rotate_row(self, row: int, amount: int) -> None:
        if amount > self.x:
            amount %= self.x

        on = self.vals[0]
        off = self.vals[1]

        # Build new row:
        new_row = [off for _ in range(self.x)]
        for col in range(self.x):
            if self.grid[row][col] == on:
                new_col = (col + amount) % self.x
                new_row[new_col] = on

        # Replace row in grid:
        self.grid[row] = new_row

    def rotate_col(self, col: int, amount: int) -> None:
        if amount > self.y:
            amount %= self.y

        on = self.vals[0]
        off = self.vals[1]

        # Build new column:
        new_col = [off for _ in range(self.y)]
        for row in range(self.y):
            if self.grid[row][col] == on:
                new_row = (row + amount) % self.y
                new_col[new_row] = on

        # Update grid column:
        for row in range(self.y):
            self.grid[row][col] = new_col[row]
