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


def main(verbose: bool=False) -> None:
    cwd = Path(__file__).parent

    with open(cwd/INFILE) as infile:
        for line in infile:
            target = int(line.strip())

    print(f'Target:  {target:,}')

    for i in range(770_000, 2_000_000):
        if verbose or i % 1_000 == 0:
            print(f'House {i:,} got {calc(i):,} presents.')
        if res := calc(i) >= target:
            print(f'House {i:,} got {calc(i):,} presents.')
            break


if __name__ == '__main__':
    main()
