#! /usr/bin/env python3.10

INFILE = 'd19p1t1.txt'
# INFILE = 'd19p1.txt'


# Libraries
from pprint import pprint
import re


def main():
    scanners = {}
    with open(INFILE) as infile:
        current_scanner = ''
        for line in infile:
            if (scanner := re.match(r'^--- scanner (\d+) ---', line)):
                current_scanner = scanner[1]
                scanners[current_scanner] = []
            elif (beacon := re.match(r'^(-?\d+),(-?\d+),(-?\d+)', line)):
                beacon_coords = tuple(int(i) for i in beacon.groups())
                scanners[current_scanner].append(beacon_coords)
            elif line.strip() == '':
                continue
            else:
                raise ValueError("Unexpected line value:  ``{line}''")

    print('Read in:')
    pprint(scanners)


if __name__ == '__main__':
    main()
