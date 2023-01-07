#! /usr/bin/env python3


'''
Beacon Exclusion Zone:
* Sensors at integer coordinates
  * Knows its own position
  * Can determine position of beacon closest to it as measured by the
    manhattan distance
  * There is never a tie where two beacons are the same distance from a sensor
* Beacons at integer coordinates
'''


# Standard library:
from pathlib import Path
from pprint import pprint
import re
import sys


# Local libraries - find relative to script:
LOCAL_LIB = str(Path(__file__).parent.parent)
sys.path.append(LOCAL_LIB)
from ds.grid import Grid, Point


# INFILE = 'd15p1t1.txt'
INFILE = Path(__file__).parent / 'd15p1t1.txt'
# INFILE = 'd15p1.txt'


def main(verbose=True):
    # Key is sensor, value is closest beacon
    sensors = {}
    pattern = r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
    minx = 0
    maxx = 5
    miny = 0
    maxy = 5
    with open(INFILE) as infile:
        for line in infile:
            # Parse
            if not (res := re.fullmatch(pattern, line.strip())):
                raise ValueError(f'Error parsing:  {line.strip()}')
            sx, sy, bx, by = map(int, res.groups())
            sensors[Point(sx, sy)] = Point(bx, by)

            # Find corners of grid:
            if sx < minx or bx < minx:
                minx = min((sx, bx))
            if sx > maxx or bx > maxx:
                maxx = max((sx, bx))
            if sy < miny or by < miny:
                miny = min((sy, by))
            if sy > maxy or by > maxy:
                maxy = max((sy, by))

    grid = Grid(Point(minx, miny), Point(maxx, maxy))
    for sensor, beacon in sensors.items():
        grid.plot(sensor, 'S')
        grid.plot(beacon, 'B')

    if verbose:
        print('\nInput List - Sensor: Closest Beacon:')
        pprint(sensors, sort_dicts=False)

    print(f'\nPlot of sensors and beacons:\n{grid}')


if __name__ == '__main__':
    main()
