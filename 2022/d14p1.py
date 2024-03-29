#! /usr/bin/env python3


'''
Regolith Reservoir
* Part 1 Input - 2D vertical slice of cave above you
  * Scan data shows path of rock structures (x, y)
    * x represents distance to the right
    * y represents distance down
  * Sand movement - see drop_sand
'''


# INFILE = 'd14p1t1.txt'
# INFILE = r'\working\github\sockduct\aoc\2022\d14p1t1.txt'
# INFILE = r'\working\github\sockduct\aoc\2022\d14p1t2.txt'
INFILE = 'd14p1.txt'
# INFILE = r'\working\github\sockduct\aoc\2022\d14p1.txt'
#
ROCK = '#'
AIR = '.'
SAND = 'o'
SANDSRC = '+'


from dataclasses import dataclass
from itertools import pairwise


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __str__(self):
        return f'{self.x, self.y}'

    def __add__(self, other):
        return (
            Point(self.x + other.x, self.y + other.y)
                if isinstance(other, self.__class__)
                else NotImplemented
        )

    def __sub__(self, other):
        return (
            Point(self.x - other.x, self.y - other.y)
                if isinstance(other, self.__class__)
                else NotImplemented
        )

    @classmethod
    def pair(cls, coords):
        x, y = coords
        return cls(x, y)

    def offset(self, other):
        return (
            Point(abs(self.x - other.x), abs(self.y - other.y))
                if isinstance(other, self.__class__)
                else NotImplemented
        )


def calc_offsets(bounds, floor=False, floor_offset=10, point_lines=None):
    if floor:
        bounds['left'] = Point(bounds['left'].x - floor_offset, bounds['left'].y)
        bounds['right'] = Point(bounds['right'].x + floor_offset, bounds['right'].y)
        bounds['lower'] = Point(bounds['lower'].x, bounds['lower'].y + 2)

        point_lines.append([Point(bounds['left'].x, bounds['lower'].y),
                            Point(bounds['right'].x, bounds['lower'].y)])

    bounds['width'] = bounds['right'].x - bounds['left'].x
    bounds['woff1'] = bounds['sand_orig'].x - bounds['left'].x
    bounds['woff2'] = bounds['right'].x - bounds['sand_orig'].x
    bounds['voff'] = 3
    bounds['hoff'] = 4


def build_graph(point_lines, bounds):
    # Create numbers at top of graph for x-axis:
    outlines = [
        list(f"{' ' * bounds['hoff']}{str(bounds['left'].x)[i]}{' ' * (bounds['woff1'] - 1)}"
             f"{str(bounds['sand_orig'].x)[i]}{' ' * (bounds['woff2'] - 1)}"
             f"{str(bounds['right'].x)[i]}")
                for i in range(bounds['voff'])
    ]
    # Create numbers at the side of graph for y-axis and "air":
    outlines.extend(
        list(f"{i:3} {AIR * (bounds['width'] + 1)}") for i in range(bounds['lower'].y + 1)
    )
    # Draw sand source:
    outlines[bounds['voff']][bounds['hoff'] + bounds['woff1']] = SANDSRC

    # Draw in lines of rock using coordinates:
    for line in point_lines:
        for c1, c2 in pairwise(line):
            c12 = c1.offset(c2)
            if c12.x:
                # X-offset
                left = c1.x if c1 < c2 else c2.x
                right = c2.x if c2 > c1 else c1.x
                xoff1 = left - bounds['left'].x
                xoff2 = right - bounds['left'].x
                for xoff in range(xoff1, xoff2 + 1):
                    outlines[bounds['voff'] + c1.y][bounds['hoff'] + xoff] = ROCK
            else:
                # Y-offset
                xoff = c1.x - bounds['left'].x
                top = c1.y if c1 < c2 else c2.y
                bottom = c2.y if c2 > c1 else c1.y
                for yoff in range(top, bottom + 1):
                    outlines[bounds['voff'] + yoff][bounds['hoff'] + xoff] = ROCK

    return outlines


def display(graph):
    print()
    for line in graph:
        print(''.join(line))
    print()


def drop_sand(graph, bounds) -> bool:
    '''
    Sand movement:
    0) Originates from 500, 0
    1) Goes down one step if possible (nothing in the way)
    2) If can't go down, tries to go diagonally left
    3) If can't go diagonally left, tries to go diagonally right
    *) If can't do any of of 1-3, then stops, and next unit starts (step 0)
    '''
    rowmax = len(graph)
    colmax = len(graph[0])
    rowstart = bounds['voff'] + 1
    colstart = bounds['hoff'] + bounds['woff1']

    # Check if sand backed up:
    if graph[rowstart - 1][colstart] == 'o':
        return False

    # Start 1 below Sand Origin:
    row = rowstart
    col = colstart

    while True:
        match graph[row][col]:
            # AIR:
            case '.':
                row += 1
                # Off the graph?
                if row >= rowmax:
                    return False
            # ROCK:
            case '#' | 'o':
                # Off the graph?
                if (col - 1) < bounds['hoff'] or (col + 1) >= colmax:
                    return False
                # Check diagonally left:
                if graph[row][col - 1] == '.':
                    col -= 1
                # Check diagonally right:
                elif graph[row][col + 1] == '.':
                    col += 1
                # Nowhere to go - stop here:
                # Note:  Will overwrite sand source - OK
                else:
                    graph[row - 1][col] = 'o'
                    return True


def main(verbose=False):
    coord_lines = []
    with open(INFILE) as infile:
        coord_lines.extend(line.strip().split(' -> ') for line in infile)

    # When parsing coordinates find left most and right most points to bound graph
    bounds = dict(left=None, right=None, lower=None, sand_orig=Point(500, 0))
    point_lines = []
    for coords in coord_lines:
        line = []
        for x, y in [(map(int, coord.split(','))) for coord in coords]:
            line.append(p := Point(x, y))
            if bounds['left'] and p < bounds['left'] or not bounds['left']:
                bounds['left'] = p
            if bounds['right'] and p > bounds['right'] or not bounds['right']:
                bounds['right'] = p
            if bounds['lower'] and p.y > bounds['lower'].y or not bounds['lower']:
                bounds['lower'] = p
        point_lines.append(line)

    if verbose:
        for lnum, line in enumerate(point_lines):
            print(f'{lnum + 1}:  ', end='')
            for cnum, coord in enumerate(line):
                if cnum > 0:
                    print(', ', end='')
                print(f'{coord}', end='')
            print()
        print(f"\nLeft bound:  {bounds['left']}\nRight bound:  {bounds['right']}\n"
              f"Lower bound:  {bounds['lower']}")

    calc_offsets(bounds, floor=True, floor_offset=200, point_lines=point_lines)
    graph = build_graph(point_lines, bounds)

    if verbose:
        display(graph)

    counter = 0
    while drop_sand(graph, bounds):
        if verbose:
            display(graph)
        counter += 1

    display(graph)

    print(f'\nDropped units of sand before overflow:  {counter:,}\n')


if __name__ == '__main__':
    main()
