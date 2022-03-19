#! /usr/bin/env python3.10


INFILE = 'd18p1t1.txt'
# INFILE = 'd18p1.txt'


import json
from pprint import pprint


class SnailfishNumber():
    def __init__(self):
        ...


def main():
    numbers = []
    with open(INFILE) as infile:
        for line in infile:
            numbers.append(json.loads(line))
    pprint(numbers)


if __name__ == '__main__':
    main()
