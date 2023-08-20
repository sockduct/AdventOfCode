#! /usr/bin/env python3


'''
Day 3 Challenge, 2015

Part 1 - perfectly spherical houses in a vacuum
* Santa delivering presents to homes using infinite 2D grid
* He begins by delivering present to starting location
* Moves are N(^)/S(v)/E(>)/W(<) only, no diagonals
* Present delivered after each move
* Some homes visited more than once
* How many homes receive at least 1 present?

Example:
> - delivers presents to 2 homes - 1 at start, 1 to east
^>v< - delivers presents to 4 homes in a square - including twice to the home at his start/end location
^v^v^v^v^v - delivers bunch of presents to only 2 homes
'''


# INFILE = 'd3t3.txt'
INFILE = 'd3.txt'


class Grid:
    def __init__(self, width=10, height=10):
        '''
        array access is y, x but presenting to user as x, y
        '''
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def __repr__(self):
        return f'Grid({self.width}, {self.height})'

    def deliver(self):
        '''Deliver present to current grid location'''
        self.grid[self.y][self.x] += 1

    def north(self):
        self.y += 1
        self.deliver()

    def south(self):
        self.y -= 1
        self.deliver()

    def west(self):
        self.x -= 1
        self.deliver()

    def east(self):
        self.x += 1
        self.deliver()

    def visited(self):
        return sum(sum(bool(element) for element in row) for row in self.grid)


def process(line, grid):
    grid.deliver()
    for element in line:
        match element:
            case '^':
                grid.north()
            case 'v':
                grid.south()
            case '>':
                grid.east()
            case '<':
                grid.west()
            case _:
                raise ValueError(f'Unexpected value:  {element}')


def main():
    grid = Grid()
    with open(INFILE) as infile:
        for line in infile:
            process(line, grid)

    print(f'Homes receiving at least one present:  {grid.visited()}')


if __name__ == '__main__':
    main()
