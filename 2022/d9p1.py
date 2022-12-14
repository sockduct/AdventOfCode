#! /usr/bin/env python3


'''
Rope Bridge
* Model rope with knots at each end on 2D grid

Input - Part 1:
* Follow series of motions for head, can determine how tail will move
* Head and Tail must be touching (L-R, T-B, Diagonally, Overlapping)
* If head is two steps away (L-R, U-D), tail must move in that direction so its
  only one step away
* If head and tail aren't touching and aren't in same row or column, tail moves
  one step diagonally to catch up
* Work out where tail goes as head moves around
* Assume head and tail start overlapping

Input - Part 1, Details:
* R = right, L = left, U = up, D = down, # = how many steps
* After each step, update position of tail if head is no longer adjacent
* Count all positions tail visited at least once
'''


# INFILE = 'd9p1t1.txt'
INFILE = r'\working\github\sockduct\aoc\2022\d9p1t1.txt'
# INFILE = 'd9p1t2.txt'
# INFILE = 'd9p1.txt'
# INFILE = r'\working\github\sockduct\aoc\2022\d9p1.txt'


from dataclasses import dataclass
from math import sqrt


# Treat Position as immutable to allow use in sets
@dataclass(unsafe_hash=True)
class Position:
    x: int
    y: int

    def __str__(self):
        return f'({self.x}, {self.y})'

    def distance(self, other):
        '''
        Use Chebyshev Distance instead of Euclidean Distance
        See:
        * https://chris3606.github.io/GoRogue/articles/grid_components/measuring-distance.html
        * https://www.omnicalculator.com/math/manhattan-distance

        Euclidean Distance:
        sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
        '''
        return (
            max(abs(other.x - self.x), abs(other.y - self.y)) if isinstance(other, Position)
                else NotImplemented
        )


def display_grid(head, tail):
    output = [
        ['4', ' ', ' ', ' ', ' ', ' ', ' \n'],
        ['3', ' ', ' ', ' ', ' ', ' ', ' \n'],
        ['2', ' ', ' ', ' ', ' ', ' ', ' \n'],
        ['1', ' ', ' ', ' ', ' ', ' ', ' \n'],
        ['0', ' ', ' ', ' ', ' ', ' ', ' \n'],
        [' 012345\n']
    ]

    # Tail:
    output[4 - tail.y][tail.x + 1] = 'T'

    # Head:
    output[4 - head.y][head.x + 1] = 'H'

    print(f'{"".join(col for row in output for col in row)}')


def move_pos(coord, inc, dist, head, tail, head_visited, tail_visited):
    for _ in range(dist):
        value = getattr(head, coord) + inc
        setattr(head, coord, value)
        head_visited.add(head)
        # Debug
        print(f'Head moved to {head}, ', end='')

        # Check if tail needs to move
        if head.distance(tail) > 1:
            hdist = head.x - tail.x
            vdist = head.y - tail.y

            match hdist, vdist:
                # Could combine diagonals
                # e.g., could add:  | 1, -2:
                case 2, -1:
                    tail.x += 1
                    tail.y -= 1
                case 2, 0:
                    tail.x += 1
                case 2, 1:
                    tail.x += 1
                    tail.y += 1
                case -2, -1:
                    tail.x -= 1
                    tail.y -= 1
                case -2, 0:
                    tail.x -= 1
                case -2, 1:
                    tail.x -= 1
                    tail.y += 1
                case -1, 2:
                    tail.y += 1
                    tail.x -= 1
                case 0, 2:
                    tail.y += 1
                case 1, 2:
                    tail.y += 1
                    tail.x += 1
                case -1, -2:
                    tail.y -= 1
                    tail.x -= 1
                case 0, -2:
                    tail.y -= 1
                case 1, -2:
                    tail.y -= 1
                    tail.x += 1
                case _:
                    raise ValueError(f'Unexpected distance:  {hdist=}, {vdist=}, {head=}, {tail=}.')

            # Debug
            print(f'Tail moved to {tail}.')

            tail_visited.add(tail)
        else:
            # Debug
            print(f'Tail didn\'t move. (Distance={head.distance(tail)})')

        display_grid(head, tail)


def run_cmd(cmd, dist, head, tail, head_visited, tail_visited):
    match cmd:
        case 'U' | 'u':
            move_pos('y', 1, dist, head, tail, head_visited, tail_visited)
        case 'D' | 'd':
            move_pos('y', -1, dist, head, tail, head_visited, tail_visited)
        case 'L' | 'l':
            move_pos('x', -1, dist, head, tail, head_visited, tail_visited)
        case 'R' | 'r':
            move_pos('x', 1, dist, head, tail, head_visited, tail_visited)
        case _:
            raise ValueError(f'Expected U|D|L|R, got:  {cmd}')


def main():
    with open(INFILE) as infile:
        head = Position(0, 0)
        tail = Position(0, 0)
        tail_visited = {tail}
        head_visited = {head}
        commands = 0

        # Debug
        print(f'Start:  Head at {head}, Tail at {tail}')
        display_grid(head, tail)

        for line in infile:
            cmd, dist = line.split()

            run_cmd(cmd, int(dist), head, tail, head_visited, tail_visited)
            commands += 1

    # Debug
    print(f'End:  Head at {head}, tail at {tail}')
    print(f'\nHead visited {len(head_visited):,} positions.')
    print(f'Processed {commands:,} commands.')

    print(f'\nThe tail of the rope visited {len(tail_visited):,} positions.\n')


if __name__ == '__main__':
    main()
