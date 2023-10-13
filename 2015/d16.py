#! /usr/bin/env python3


'''
Which Aunt Sue?
'''


INFILE = 'd16.txt'
INFILE2 = 'd16clues.txt'


# Libraries:
from pathlib import Path
from pprint import pprint
import re


def sue_match(sue_vals, clues):
    for attr, count in clues.items():
        if attr in sue_vals and sue_vals[attr] != count:
            return False

    return True


def main(verbose=False):
    directory = Path(__file__).parent
    clues = {}
    with open(directory/INFILE2) as infile:
        for line in infile:
            key, value = line.split()
            clues[key.strip(':')] = int(value)

    if verbose:
        pprint(clues)

    sues = {}
    with open(directory/INFILE) as infile:
        for linenum, line in enumerate(infile):
            sue_number, items = re.match(r'Sue (\d+): (.*)', line).groups()
            sue_number = int(sue_number)
            sues[sue_number] = {key.strip(':'): int(value) for key, value in
                [item.split() for item in items.split(',')]
            }
            if verbose and linenum > 30:
                pprint(sues)
                break

    print('Looking for match with:')
    pprint(clues)
    for sue_num, sue_vals in sues.items():
        if sue_match(sue_vals, clues):
            print(f'Possible match with Sue {sue_num}:  {sue_vals}')


if __name__ == '__main__':
    main()
