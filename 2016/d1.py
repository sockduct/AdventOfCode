#! /usr/bin/env python3


'''
Follow the directions (grid traversal)
* e.g., L2, R3
* Calculate distance from start
'''


INFILE = 'd1.txt'
# INFILE = 'd1t1.txt'
# INFILE = 'd1t2.txt'


# Libraries
from collections import defaultdict
from pathlib import Path


# Types
class Location:
    def __init__(self, heading: str='N', offset_ns: int=0, offset_we: int=0,
                 check_repeats: bool=False, first_only: bool=True) -> None:
        self.header = heading
        self.offset_ns = offset_ns
        self.offset_we = offset_we
        self.check_repeats = check_repeats
        self.first_only = first_only
        self.repeat_shown = False
        self.visited = defaultdict(int, {(offset_ns, offset_we): 1})

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.header}, {self.offset_ns}, {self.offset_we})'

    def __str__(self) -> str:
        return (f'Facing {self.header}, {self.pos_str()}.')

    def pos_str(self) -> str:
        ns = 'North' if self.offset_ns >= 0 else 'South'
        we = 'East' if self.offset_we >= 0 else 'West'

        ns_str = '' if self.offset_ns == 0 else f'{abs(self.offset_ns)} blocks {ns}'
        we_str = '' if self.offset_we == 0 else f'{abs(self.offset_we)} blocks {we}'

        if ns_str and we_str:
            offset_str = f'{ns_str}, {we_str} from'
        elif ns_str:
            offset_str = f'{ns_str} from'
        elif we_str:
            offset_str = f'{we_str} from'
        else:
            offset_str = 'at'

        return (f'{offset_str} starting position')

    def move(self, steps: int) -> None:
        match self.header:
            case 'N':
                for _ in range(steps):
                    self.offset_ns += 1
                    self.visited[(self.offset_ns, self.offset_we)] += 1
            case 'E':
                for _ in range(steps):
                    self.offset_we += 1
                    self.visited[(self.offset_ns, self.offset_we)] += 1
            case 'S':
                for _ in range(steps):
                    self.offset_ns -= 1
                    self.visited[(self.offset_ns, self.offset_we)] += 1
            case 'W':
                for _ in range(steps):
                    self.offset_we -= 1
                    self.visited[(self.offset_ns, self.offset_we)] += 1

        if self.check_repeats and 2 in self.visited.values():
            if self.first_only:
                if self.repeat_shown:
                    return
                else:
                    self.repeat_shown = True

            for key, val in self.visited.items():
                if val >= 2:
                    print(f'Visited {Location(self.header, key[0], key[1]).pos_str()} '
                          f'{val} times.')

    def new_heading(self, turn: str) -> None:
        match self.header, turn:
            case ['N', 'L']:
                self.header = 'W'
            case ['N', 'R']:
                self.header = 'E'
            case ['E', 'L']:
                self.header = 'N'
            case ['E', 'R']:
                self.header = 'S'
            case ['S', 'L']:
                self.header = 'E'
            case ['S', 'R']:
                self.header = 'W'
            case ['W', 'L']:
                self.header = 'S'
            case ['W', 'R']:
                self.header = 'N'
            case _:
                raise ValueError(f'Unexpected combination:  {self.header}, {turn}')

    def left(self, steps: int) -> None:
        self.new_heading('L')
        self.move(steps)

    def right(self, steps: int) -> None:
        self.new_heading('R')
        self.move(steps)

    def step(self, direction: str) -> None:
        left_right = direction[0]
        distance = int(direction[1:])

        if left_right == 'L':
            self.left(distance)
        elif left_right == 'R':
            self.right(distance)
        else:
            raise ValueError(f'Expected L|R, got:  {left_right}')

    def offset(self) -> int:
        return abs(self.offset_ns) + abs(self.offset_we)


def parse(line: str) -> list[str]:
    return [e.strip() for e in line.split(',')]


def travel(directions: tuple[str]|list[str], verbose: bool=True) -> int:
    location = Location(check_repeats=True)

    for step in directions:
        location.step(step)

    if verbose:
        print(f'\n{location}')

    return location.offset()


def main() -> None:
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        for line in infile:
            directions = parse(line)
            offset = travel(directions)

            print(f'Following these directions:\n{line.strip()}\nOffset from start:  {offset}\n')


if __name__ == '__main__':
    main()
