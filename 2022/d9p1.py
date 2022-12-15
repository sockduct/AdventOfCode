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
# INFILE = r'\working\github\sockduct\aoc\2022\d9p1t1.txt'
# INFILE = 'd9p1t2.txt'
# INFILE = 'd9p1t2.txt'
INFILE = r'\working\github\sockduct\aoc\2022\d9p1t2.txt'
# INFILE = 'd9p1.txt'
# INFILE = r'\working\github\sockduct\aoc\2022\d9p1.txt'


from dataclasses import dataclass
from itertools import pairwise
from math import sqrt


@dataclass(frozen=True)
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


def display_grid(rope):
    output = [
        ['5', '.', '.', '.', '.', '.', '.', '\n'],
        ['4', '.', '.', '.', '.', '.', '.', '\n'],
        ['3', '.', '.', '.', '.', '.', '.', '\n'],
        ['2', '.', '.', '.', '.', '.', '.', '\n'],
        ['1', '.', '.', '.', '.', '.', '.', '\n'],
        ['0', '.', '.', '.', '.', '.', '.', '\n'],
        [' 012345\n']
    ]
    offset = 5
    output2 = [
        ['15', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        ['14', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        ['13', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        ['12', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        ['11', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        ['10', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        [' 9', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        [' 8', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        [' 7', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        [' 6', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        [' 5', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        [' 4', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        [' 3', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        [' 2', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        [' 1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        [' 0', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        ['-1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        ['-2', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        ['-3', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        ['-4', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        ['-5', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '\n'],
        ['  10987654321012345678901234\n'],
        ['   1    -         +    1\n']
    ]
    voffset = 15
    hoffset = 12

    for key in reversed(rope.keys()):
        match key:
            case 'head':
                value = 'H'
            case 'tail':
                value = 'T'
            case _:
                value = str(key)
        # output[offset - rope[key].y][rope[key].x + 1] = value
        output2[voffset - rope[key].y][rope[key].x + hoffset] = value

    # print(f'{"".join(col for row in output for col in row)}')
    print(f'{"".join(col for row in output2 for col in row)}')


def move_pos(coord, inc, dist, rope, rope_tail_visited, verbose=False):
    for _ in range(dist):
        match coord:
            case 'x':
                rope['head'] = Position(rope['head'].x + inc, rope['head'].y)
            case 'y':
                rope['head'] = Position(rope['head'].x, rope['head'].y + inc)
            case _:
                raise ValueError(f'Expected "x" or "y", got "{coord}".')

        head_moved = True
        if verbose:
            print(f'Head moved to {rope["head"]}, ', end='')

        # For each pair, check if 2nd knot needs to move
        for lead, trail in pairwise(rope.keys()):
            tail_moved = False
            if rope[lead].distance(rope[trail]) > 1:
                tail_moved = True
                hdist = rope[lead].x - rope[trail].x
                vdist = rope[lead].y - rope[trail].y

                match hdist, vdist:
                    # Move diagonally (right, down)
                    case (2, -1) | (1, -2):
                        rope[trail] = Position(rope[trail].x + 1, rope[trail].y - 1)
                    # Move right
                    case 2, 0:
                        rope[trail] = Position(rope[trail].x + 1, rope[trail].y)
                    # Move diagonally (right, up)
                    case (2, 1) | (1, 2) | (2, 2):
                        rope[trail] = Position(rope[trail].x + 1, rope[trail].y + 1)
                    # Move diagonally (left, down)
                    case (-2, -1) | (-1, -2):
                        rope[trail] = Position(rope[trail].x - 1, rope[trail].y - 1)
                    # Move left
                    case -2, 0:
                        rope[trail] = Position(rope[trail].x - 1, rope[trail].y)
                    # Move diagonally (left, up)
                    case (-2, 1) | (-1, 2) | (-2, 2):
                        rope[trail] = Position(rope[trail].x - 1, rope[trail].y + 1)
                    # Move up
                    case 0, 2:
                        rope[trail] = Position(rope[trail].x, rope[trail].y + 1)
                    # Move down
                    case 0, -2:
                        rope[trail] = Position(rope[trail].x, rope[trail].y - 1)
                    case _:
                        raise ValueError(f"Unexpected distance:  {hdist=}, {vdist=}, "
                                         f"{rope[lead]=}, {rope[trail]=}.")

                if verbose:
                    print(f"Tail moved to {rope[trail]}.")

                if trail == 'tail':
                    rope_tail_visited.add(rope[trail])
            elif verbose:
                print(f"Tail didn't move. (Distance={rope[lead].distance(rope[trail])})")

            if verbose and (head_moved or tail_moved):
                display_grid(rope)
                head_moved = False


def run_cmd(cmd, dist, rope, rope_tail_visited, verbose=False):
    match cmd:
        case 'U' | 'u':
            move_pos('y', 1, dist, rope, rope_tail_visited, verbose)
        case 'D' | 'd':
            move_pos('y', -1, dist, rope, rope_tail_visited, verbose)
        case 'L' | 'l':
            move_pos('x', -1, dist, rope, rope_tail_visited, verbose)
        case 'R' | 'r':
            move_pos('x', 1, dist, rope, rope_tail_visited, verbose)
        case _:
            raise ValueError(f'Expected U|D|L|R, got:  {cmd}')


def main(verbose=False):
    with open(INFILE) as infile:
        rope = dict(head=Position(0, 0), tail=Position(0, 0))
        rope_tail_visited = {rope['tail']}

        rope2 = {key: Position(0, 0) for key in ('head', 1, 2, 3, 4, 5, 6, 7, 8, 'tail')}
        rope2_tail_visited = {rope['tail']}

        commands = 0

        print(f"Start:  Head at {rope['head']}, Tail at {rope['tail']}")
        print(f'Start for rope2:  {", ".join(f"{key}={value}" for key, value in rope2.items())}')
        if verbose:
            display_grid(rope)

        for line in infile:
            cmd, dist = line.split()

            # run_cmd(cmd, int(dist), rope, rope_tail_visited, verbose)
            run_cmd(cmd, int(dist), rope2, rope2_tail_visited, verbose)
            commands += 1

    print(f"End:  Head at {rope['head']}, tail at {rope['tail']}")
    print(f'End for rope2:  {", ".join(f"{key}={value}" for key, value in rope2.items())}')
    print(f"Processed {commands:,} commands.")

    print(f"\nThe tail of the rope visited {len(rope_tail_visited):,} positions.")
    print(f"The tail of the rope2 visited {len(rope2_tail_visited):,} positions.\n")


if __name__ == '__main__':
    main(verbose=True)
