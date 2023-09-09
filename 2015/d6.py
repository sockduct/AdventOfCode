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


INFILE = 'd6t1.txt'
# INFILE = 'd6.txt'
SIZE = 1_000


class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = [False for _ in range(x) for _ in range(y)]

    def __repr__(self):
        return f'Grid({self.x}, {self.y})'

    def status(self):
        enabled = sum(sum(row) for row in self.grid)
        disabled = self.x * self.y - enabled

        return enabled, disabled

    def on(self):
        ...

    def off(self):
        ...

    def toggle(self):
        ...


def process(line, grid):
    match line.split():
        case ...


def main():
    grid = Grid(SIZE, SIZE)
    with open(INFILE) as infile:
        for line in infile:
            process(line.strip(), grid)

    print('Light grid has {grid.status()[0]:,} lights lit.')


if __name__ == '__main__':
    main()
