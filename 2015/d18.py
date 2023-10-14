#! /usr/bin/env python3


'''
Like a GIF for your yard
* Initialize 100x100 light grid from file:
    * '#' = on
    * '.' = off
* Each round, build new grid from current grid:
    * Count number of neighbors - for example, A has 8, B has 5:
        1B5...
        234...
        ......
        ..123.
        ..8A4.
        ..765.
    * A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    * A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
'''


# INFILE = 'd18.txt'
INFILE = 'd18t1.txt'


# Libraries:
from pathlib import Path
from grid import Grid


def main(verbose=True):
    size = 6
    grid = Grid(size, size)

    mydir = Path(__file__).parent
    with open(mydir/INFILE) as infile:
        for y, line in enumerate(infile):
            for x, char in enumerate(line.strip()):
                if char == '#':
                    grid.on(x, y)

    if verbose:
        print(f'Initial grid:\n{grid}')


if __name__ == '__main__':
    main()
