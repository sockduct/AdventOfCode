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
SAND_ORIG = '500,0'
ROCK = '#'
AIR = '.'
SAND = 'o'
SANDSRC = '+'


from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __str__(self):
        return f'{self.x, self.y}'

    @classmethod
    def pair(cls, coords):
        x, y = coords
        return cls(x, y)


def main(verbose=True):
    coord_lines = []
    with open(INFILE) as infile:
        coord_lines.extend(line.strip().split(' -> ') for line in infile)

    # When parsing coordinates find left most and right most points to bound graph
    left_bound = None
    right_bound = None
    point_lines = []
    for coords in coord_lines:
        line = []
        for x, y in [(map(int, coord.split(','))) for coord in coords]:
            line.append(p := Point(x, y))
            if left_bound and p < left_bound or not left_bound:
                left_bound = p
            if right_bound and p > right_bound or not right_bound:
                right_bound = p
        point_lines.append(line)

    if verbose:
        for lnum, line in enumerate(point_lines):
            print(f'{lnum + 1}:  ', end='')
            for cnum, coord in enumerate(line):
                if cnum > 0:
                    print(', ', end='')
                print(f'{coord}', end='')
            print()
        print(f'\nLeft bound:  {left_bound}\nRight bound:  {right_bound}\n')

    # Next step - draw graph, see AoC 2022, Day 14 overview


if __name__ == '__main__':
    main()
