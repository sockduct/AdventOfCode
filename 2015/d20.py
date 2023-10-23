#! /usr/bin/env python3
#
# Note:  Use pypy to speed up since all computation!
# e.g., PS> & "\program files\pypy3.10\python" <this-file>


'''
Infinite Elves and Infinite Houses
'''


INFILE = 'd20.txt'


# Libraries
from pathlib import Path


def calc(n: int) -> int:
    multiple = 10

    return sum(multiple * value for value in range(1, n + 1) if n % value == 0)


def calc2(n: int) -> int:
    '''
    The Elves decide they don't want to visit an infinite number of houses.
    Instead, each Elf will stop after delivering presents to 50 houses. To make
    up for it, they decide to deliver presents equal to eleven times their
    number at each house.

    sum(
        multiple X each value in the range 1 to n + 1
        if n divides into value (with no remainder) and if value * limiter < n
    )
    '''
    multiple = 11
    limiter = 50

    '''
    total = 0
    for value in range(1, n + 1):
        if n % value == 0 and value * limiter >= n:
            total += multiple * value

    return total
    '''

    return sum(multiple * value for value in range(1, n + 1)
               if n % value == 0 and value * limiter >= n)


def main(verbose: bool=False) -> None:
    cwd = Path(__file__).parent

    with open(cwd/INFILE) as infile:
        for line in infile:
            target = int(line.strip())

    print(f'Target:  {target:,}')

    # for i in range(1, 11):
    # for i in range(770_000, 2_000_000):  # For Part 1
    for i in range(785_000, 2_000_000):  # For Part 2
        # Between 776,160 - 803,880
        res = calc2(i)
        if verbose or i % 1_000 == 0:
            # print(f'House {i:,} got {res:,} presents.')
            print(f'House {i:,} got {res:,} presents.')
        if res >= target:
            # print(f'House {i:,} got {res:,} presents.')
            print(f'House {i:,} got {res:,} presents.')
            break


if __name__ == '__main__':
    main()
