#! /usr/bin/env python3


'''
Day 1
* Ground floor = 0
* ( = up one floor
* ) = down one floor

Part 1:
* Calculate resulting level from input line

Part 2:
* Find position of first character which causes going to basement (-1)
Note:  First character on line is position 1, 2nd is 2, ...
'''


# INFILE = 'd1t1.txt'
INFILE = 'd1.txt'


def get_level(iterable):
    level = 0

    for direction in iterable:
        match direction:
            case '(':
                level += 1
            case ')':
                level -= 1
            case _:
                raise ValueError(f'Unexpected value:  {direction=}')

    return level


def get_1pos_4level(iterable, target_level):
    level = 0

    for pos, direction in enumerate(iterable, start=1):
        match direction:
            case '(':
                level += 1
            case ')':
                level -= 1
            case _:
                raise ValueError(f'Unexpected value:  {direction=}')

        if level == target_level:
            return pos

    raise ValueError(f'Never reached {target_level=}')


def main():
    directions = []
    with open(INFILE) as infile:
        directions.extend(line.strip() for line in infile)

    for line in directions:
        level = get_level(line)
        try:
            basement = get_1pos_4level(line, -1)
        except ValueError as err:
            basement = None
        if len(line) < 10:
            print(f'{line} => {level}', end='')
        else:
            print(f'{line[:9]}... => {level}', end='')
        if basement:
            print(f',  Reached basement at position={basement}')
        else:
            print()


if __name__ == '__main__':
    main()
