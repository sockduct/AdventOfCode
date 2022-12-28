#! /usr/bin/env python3


'''
Regolith Reservoir
* Part 1 Input - 2D vertical slice of cave above you
  * Scan data shows path of rock structures (x, y)
    * x represents distance to the right
    * y represents distance down
'''


# INFILE = 'd14p1t1.txt'
INFILE = r'\working\github\sockduct\aoc\2022\d14p1t1.txt'
# INFILE = 'd14p1.txt'
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


def build_graph(point_lines, bounds):
    width = bounds['right'].x - bounds['left'].x
    woff1 = bounds['sand_orig'].x - bounds['left'].x
    woff2 = bounds['right'].x - bounds['sand_orig'].x
    hoff = 3
    voff = 4

    outlines = [
        (f"{' ' * voff}{str(bounds['left'].x)[i]}{' ' * (woff1 - 1)}"
         f"{str(bounds['sand_orig'].x)[i]}{' ' * (woff2 - 1)}"
         f"{str(bounds['right'].x)[i]}")
            for i in range(hoff)
    ]
    outlines.extend(
        f"{i:3} {'.' * (width + 1)}" for i in range(bounds['lower'].y + 1)
    )

    newline = outlines[hoff][:voff + woff1] + SANDSRC + outlines[hoff][voff + woff1:-1]
    outlines[hoff] = newline

    for line in point_lines:
        for c1, c2 in pairwise(line):
            c12 = c1.offset(c2)
            if c12.x:
                # X-offset
                left = c1.x if c1 < c2 else c2.x
                right = c2.x if c2 > c1 else c1.x
                xoff1 = left - bounds['left'].x
                xoff2 = right - bounds['left'].x
                outlines[hoff + c1.y] = (
                    outlines[hoff + c1.y][:voff + xoff1] + ROCK * c12.x +
                    outlines[hoff + c1.y][voff + xoff2:]
                )
            else:
                # Y-offset
                xoff = c1.x - bounds['left'].x
                for yoff in range(c1.y, c2.y + 1):
                    outlines[hoff + yoff] = (
                        outlines[hoff + yoff][:voff + xoff] + ROCK +
                        outlines[hoff + yoff][voff + xoff:-1]
                    )

    return outlines


def main(verbose=True):
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

    graph = build_graph(point_lines, bounds)

    if verbose:
        print()
        for line in graph:
            print(line)
        print()

    # Next step - iterate through drawing sand, see AoC 2022, Day 14 overview
    ...


if __name__ == '__main__':
    main()
