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


INFILE = 'd9p1t1.txt'
# INFILE = 'd9p1.txt'


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'<Position({self.x, self.y})>'

    def __str__(self):
        return f'{self.x, self.y}'


def move_pos(coord, inc, dist, head, tail, head_visited, tail_visited):
    for _ in range(dist):
        # Debug
        print(f'Head at {head}')

        value = getattr(head, coord) + inc
        setattr(head, coord, value)
        head_visited.add(head)

        # Check if tail needs to move
        ...


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
        for line in infile:
            cmd, dist = line.split()

            run_cmd(cmd, int(dist), head, tail, head_visited, tail_visited)
            commands += 1

    # Debug
    print(f'Head ended at {head}')
    print(f'\nHead visited {len(head_visited):,} positions.')
    print(f'Processed {commands:,} commands.')

    print(f'\nThe tail of the rope visited {len(tail_visited):,} positions.\n')


if __name__ == '__main__':
    main()
