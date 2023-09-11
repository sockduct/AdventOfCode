#! /usr/bin/env python3


'''
1000 x 1000 light grid
* Numbered 0 - 999
* Grid from (0, 0) - (999, 999)
* All lights start turned off
* Instructions on turning on, turning off, or toggling grids
* Coordinate pairs are inclusive:
    * (0, 0) - (2, 2) is entire 3 x 3 square
* Follow instructions and determine how many lights are on
'''


# INFILE = 'd6t1.txt'
# INFILE = 'd6t2.txt'
# INFILE = 'd6t3.txt'
# INFILE = 'd6t4.txt'
INFILE = 'd6.txt'
SIZE = 1_000
# SIZE = 20


from collections import namedtuple
from pathlib import Path


class Grid:
    def __init__(self, x, y, val=bool):
        self.x = x
        self.y = y
        if val.__name__ == 'bool':
            self.simple = True
            default_init = (True, False, lambda x: not x)
        elif val.__name__ == 'int':
            self.simple = False
            default_init = (1, 0, 2)
        else:
            raise ValueError(f'Expected val of bool|int, got "{val.__name__}"')

        self.vals = namedtuple('Values', 'on off toggle', defaults=default_init)()
        self.grid = [[self.vals.off for _ in range(x)] for _ in range(y)]

    def __repr__(self):
        return f'Grid({self.x}, {self.y})'

    def __str__(self):
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

        out = ''
        for row in range(y):
            for col in range(x):
                out += f'{int(self.grid[row][col])}'
            if xover:
                out += '...'
            out += '\n'

        if yover:
            out += '...\n'

        return out

    def status(self):
        enabled = sum(sum(row) for row in self.grid)
        disabled = self.x * self.y - enabled

        return enabled, disabled

    def update(self, p1, p2, op):
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
                val = self.vals.toggle if self.simple else (lambda x: x + 2)
            case _:
                raise ValueError(f'Expected on|off|toggle, got "{op}"')

        for y in range(p1[1], p2[1] + 1):
            for x in range (p1[0], p2[0] + 1):
                self.grid[y][x] = val(self.grid[y][x]) if alt else val

    def on(self, p1, p2):
        self.update(p1, p2, 'on')

    def off(self, p1, p2):
        self.update(p1, p2, 'off')

    def toggle(self, p1, p2):
        self.update(p1, p2, 'toggle')


def get_coords(p1, p2):
    p1 = tuple(map(int, p1.split(',')))
    p2 = tuple(map(int, p2.split(',')))

    return p1, p2


def process(line, grid, verbose=False):
    match line.split():
        case ['turn', 'on', p1, 'through', p2]:
            if verbose:
                print(f'Turning on {p1} - {p2}')
            p1, p2 = get_coords(p1, p2)
            grid.on(p1, p2)
        case ['toggle', p1, 'through', p2]:
            if verbose:
                print(f'Toggling {p1} - {p2}')
            p1, p2 = get_coords(p1, p2)
            grid.toggle(p1, p2)
        case ['turn', 'off', p1, 'through', p2]:
            if verbose:
                print(f'Turning off {p1} - {p2}')
            p1, p2 = get_coords(p1, p2)
            grid.off(p1, p2)
        case _:
            raise ValueError(f'Expected turn on|toggle|turn off..., got "{line.split()}"')


def main(verbose=False):
    # Override default for part 2
    # grid = Grid(SIZE, SIZE)
    grid = Grid(SIZE, SIZE, int)
    if verbose:
        print(f'Initial grid:\n{grid}')
    dirloc = Path(__file__).parent
    with open(dirloc/INFILE) as infile:
        for line in infile:
            process(line.strip(), grid, verbose)
            if verbose:
                print(f'Grid now:\n{grid}')

    if verbose:
        print(f'Final light grid:\n{grid}')
    print(f'Light grid has {grid.status()[0]:,} lights lit.')


if __name__ == '__main__':
    main()
