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


# INFILE = 'd3t1.txt'
# INFILE = 'd3t2.txt'
INFILE = 'd3.txt'


from collections import defaultdict


def deliver(grid, x, y):
    grid[(x, y)] += 1


def process(line, robo=False):
    if robo:
        dgrid2 = defaultdict(int)
        x2 = 0
        y2 = 0
        deliver(dgrid2, x2, y2)
    dgrid = defaultdict(int)
    x = 0
    y = 0
    deliver(dgrid, x, y)

    for counter, element in enumerate(line.strip(), 1):
        match element:
            case '^':
                if robo and counter % 2 == 0:
                    y2 += 1
                else:
                    y += 1
            case 'v':
                if robo and counter % 2 == 0:
                    y2 -= 1
                else:
                    y -= 1
            case '>':
                if robo and counter % 2 == 0:
                    x2 += 1
                else:
                    x += 1
            case '<':
                if robo and counter % 2 == 0:
                    x2 -= 1
                else:
                    x -= 1
            case _:
                raise ValueError(f'Unexpected value:  {element}')

        if robo and counter % 2 == 0:
            deliver(dgrid2, x2, y2)
        else:
            deliver(dgrid, x, y)

    if robo:
        print(f'Homes receiving at least one present:  {len(dgrid.keys() | dgrid2.keys())}')
    else:
        print(f'Homes receiving at least one present:  {len(dgrid.keys())}')


def main():
    with open(INFILE) as infile:
        for line in infile:
            process(line, robo=True)


if __name__ == '__main__':
    main()
