#! /usr/bin/env python3


'''
'''


INFILE = 'd25.txt'


# Libraries
from pathlib import Path
import re

# Local
from gridint import Grid


def diagadd(grid: Grid, start: int=0, stop: int=0, seed: int=1) -> None:
    multiplier = 252533
    divisor = 33554393

    num = seed
    for y in range(start, stop):
        for x in range(start, y + 1):
            row = y - x
            grid.set(x, row, num)
            # num += 1
            num *= multiplier
            num %= divisor


def main() -> None:
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        data = infile.read().strip()

    # To continue, please consult the code grid in the manual.  Enter the code at row 3011, column 3019.
    row, col = map(int, re.search(r'row (\d+), column (\d+).', data).groups())
    print(f'Looking for value at row {row}, column {col}.')

    # first = 1
    first = 20151125
    # size = 16
    size = (row if row >= col else col) * 2
    grid = Grid(size, size)
    diagadd(grid, stop=size, seed=first)
    print(f'Grid:\n{grid}')
    print(f'Grid[{row}, {col}] = {grid.point(col - 1, row - 1)}')

    # Temp
    return grid


if __name__ == '__main__':
    main()
