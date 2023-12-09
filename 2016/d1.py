#! /usr/bin/env python3


'''
Follow the directions (grid traversal)
* e.g., L2, R3
* Calculate distance from start
'''


INFILE = 'd1.txt'
# INFILE = 'd1t1.txt'


# Libraries
from pathlib import Path


# Types
class Location:
    def __init__(self, heading: str='N', offset_ns: int=0, offset_we: int=0) -> None:
        self.header = heading
        self.offset_ns = offset_ns
        self.offset_we = offset_we

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.header}, {self.offset_ns}, {self.offset_we})'

    def __str__(self) -> str:
        ns = 'North' if self.offset_ns >= 0 else 'South'
        we = 'East' if self.offset_we >= 0 else 'West'

        ns_str = '' if self.offset_ns == 0 else f'{abs(self.offset_ns)} blocks {ns}'
        we_str = '' if self.offset_we == 0 else f'{abs(self.offset_we)} blocks {we}'

        if ns_str and we_str:
            offset_str = f'{ns_str}, {we_str} from'
        elif ns_str:
            offset_str = ns_str
        elif we_str:
            offset_str = we_str
        else:
            offset_str = 'at'

        return (f'Facing {self.header}, {offset_str} starting position.')

    def move(self, steps: int) -> None:
        match self.header:
            case 'N':
                self.offset_ns += steps
            case 'E':
                self.offset_we += steps
            case 'S':
                self.offset_ns -= steps
            case 'W':
                self.offset_we -= steps

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
    location = Location()

    for step in directions:
        location.step(step)

    if verbose:
        print(location)

    return location.offset()


def main():
    with open(INFILE) as infile:
        for line in infile:
            directions = parse(line)
            offset = travel(directions)

            print(f'Following these directions:\n{line.strip()}\nOffset from start:  {offset}\n')


if __name__ == '__main__':
    main()
