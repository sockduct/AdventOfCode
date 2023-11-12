#! /usr/bin/env python3


'''
'''


INFILE = 'd25.txt'


# Libraries
from pathlib import Path
import re

# Local
from gridint import Grid


def diagadd(grid: Grid, start: int=0, stop: int=0) -> None:
    num = 1
    for y in range(start, stop):
        for x in range(start, y + 1):
            row = y - x
            grid.set(x, row, num)
            num += 1


def main() -> None:
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        data = infile.read().strip()

    # To continue, please consult the code grid in the manual.  Enter the code at row 3011, column 3019.
    row, col = map(int, re.search(r'row (\d+), column (\d+).', data).groups())
    print(f'Looking for value at row {row}, column {col}.')

    grid = Grid(19, 19)
    diagadd(grid, stop=19)
    print(f'Grid:\n{grid}')


if __name__ == '__main__':
    main()
