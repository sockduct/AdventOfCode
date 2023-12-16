#! /usr/bin/env python3


'''
Bathroom Security
* For a key pad:
    123
    456
    789
* Use the instructions:
    ULL
    RRDDD
    ...
* Start from 5 and follow where possible to determine key pad combination
'''


INFILE = 'd2.txt'
# INFILE = 'd2t1.txt'


# Libraries
from pathlib import Path


# Module
class Keypad:
    def __init__(self, alt: bool=False) -> None:
        if not alt:
            self.keys: tuple[tuple[str, ...], ...] = (
                ('1', '2', '3'),
                ('4', '5', '6'),
                ('7', '8', '9')
            )
        else:
            self.keys = (
                ('',  '',  '1', '',  ''),
                ('',  '2', '3', '4', ''),
                ('5', '6', '7', '8', '9'),
                ('',  'A', 'B', 'C', ''),
                ('',  '',  'D', '',  '')
            )
        self.row = 1
        self.col = 1

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.loc})'

    def up(self) -> None:
        if self.row > 0 and self.keys[self.row - 1][self.col] != '':
            self.row -= 1

    def down(self) -> None:
        if self.row + 1 < len(self.keys) and self.keys[self.row + 1][self.col] != '':
            self.row += 1

    def left(self) -> None:
        if self.col > 0 and self.keys[self.row][self.col - 1] != '':
            self.col -= 1

    def right(self) -> None:
        if self.col + 1 < len(self.keys[0]) and self.keys[self.row][self.col + 1] != '':
            self.col += 1

    @property
    def loc(self) -> str:
        return self.keys[self.row][self.col]


def parse(line: str, keypad: Keypad) -> None:
    for char in line.strip():
        match char:
            case 'U':
                keypad.up()
            case 'D':
                keypad.down()
            case 'L':
                keypad.left()
            case 'R':
                keypad.right()
            case _:
                raise ValueError(f'Unexpected value:  {char}')


def main() -> None:
    code = []
    keypad = Keypad(alt=True)
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line, keypad)
            code.append(keypad.loc)

    print(f'Keypad code is:  {"".join(code)}')


if __name__ == '__main__':
    main()
