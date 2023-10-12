#! /usr/bin/env python3


'''
Which Aunt Sue?
'''


INFILE = 'd16.txt'
INFILE2 = 'd16clues.txt'


# Libraries:
from dataclasses import dataclass
import re


# Types:
@dataclass
class Clues:
    children: int | None = None
    cats: int | None = None
    samoyeds: int | None = None
    pomeranians: int | None = None
    akitas: int | None = None
    vizslas: int | None = None
    goldfish: int | None = None
    trees: int | None = None
    cars: int | None = None
    perfumes: int | None = None


def main():
    clues = Clues()
    with open(INFILE2) as infile:
        for line in infile:
            key, value = line.split()
            key = key.strip(':')
            clues.key = int(value)

    sues = {}
    with open(INFILE) as infile:
        for line in infile:
            sue_number, items = re.match(r'Sue (\d+): (.*)', line).groups()
            items = items.split(',')
            items = [item.split() for item in items]
            sues[sue_number] = { }


if __name__ == '__main__':
    main()
