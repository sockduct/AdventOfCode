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


INFILE = 'd18.txt'
# INFILE = 'd18t1.txt'


# Libraries:
from pathlib import Path
from grid import Grid


def neighbors_on(grid, x, y):
    count = 0

    for yn in range(y - 1, y + 2):
        if 0 <= yn < grid.y:
            for xn in range(x - 1, x + 2):
                if 0 <= xn < grid.x and not (xn == x and yn == y):
                    if grid.point(xn, yn):
                        count += 1

    return count


def cycle(grid):
    new_grid = Grid(grid.x, grid.y)

    for y in range(grid.y):
        for x in range(grid.x):
            amount = neighbors_on(grid, x, y)
            if grid.point(x, y) and 2 <= amount <= 3:
                new_grid.on(x, y)
            elif not grid.point(x, y) and amount == 3:
                new_grid.on(x, y)

    return new_grid


def cycle2(grid):
    'Corners always on - cannot be turned off'
    corners = tuple([(0, 0), (0, grid.y - 1), (grid.x - 1, 0), (grid.x - 1, grid.y - 1)])
    new_grid = Grid(grid.x, grid.y)
    corners_on(new_grid)

    for y in range(grid.y):
        for x in range(grid.x):
            # Skip corners:
            if (x, y) in corners:
                continue

            amount = neighbors_on(grid, x, y)
            if grid.point(x, y) and 2 <= amount <= 3:
                new_grid.on(x, y)
            elif not grid.point(x, y) and amount == 3:
                new_grid.on(x, y)

    return new_grid


def corners_on(grid):
    'Turn corners on'
    for x, y in [(0, 0), (0, grid.y - 1), (grid.x - 1, 0), (grid.x - 1, grid.y - 1)]:
        grid.on(x, y)


def main(verbose=False):
    # cycles = 5
    # size = 6
    cycles = 100
    size = 100
    grid = Grid(size, size)

    mydir = Path(__file__).parent
    with open(mydir/INFILE) as infile:
        for y, line in enumerate(infile):
            for x, char in enumerate(line.strip()):
                if char == '#':
                    grid.on(x, y)

    corners_on(grid)

    print(f'Initial grid has {grid.status()[0]} lights on:\n{grid}')

    for n in range(cycles):
        # grid = cycle(grid)
        grid = cycle2(grid)
        if verbose:
            print(f'Grid after {n + 1} cycle(s) has {grid.status()[0]} lights on:\n{grid}')

    print(f'\nFinal grid has {grid.status()[0]} lights on:\n{grid}')


if __name__ == '__main__':
    main()
