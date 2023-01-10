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
INFILE = Path(__file__).parent/'d15p1t1.txt'
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
            sensor = Point(sx, sy)
            beacon = Point(bx, by)
            mandist = sensor.mandist(beacon)
            sensors[sensor] = (beacon, mandist)

            # Find corners of grid including accounting for "manhattan distance
            # radius" around each point:
            if sx < minx or bx < minx or (sx - mandist) < minx or (bx - mandist) < minx:
                minx = min((sx, bx, sx - mandist, bx - mandist))
            if sx > maxx or bx > maxx or (sx + mandist) > maxx or (bx + mandist) > maxx:
                maxx = max((sx, bx, sx + mandist, bx + mandist))
            if sy < miny or by < miny or (sy - mandist) < miny or (by - mandist) < miny:
                miny = min((sy, by, sy - mandist, by - mandist))
            if sy > maxy or by > maxy or (sy + mandist) > maxy or (by + mandist) > maxy:
                maxy = max((sy, by, sy + mandist, by + mandist))

    grid = Grid(Point(minx, miny), Point(maxx, maxy))
    for sensor, beaconinfo in sensors.items():
        beacon, _ = beaconinfo
        grid.plot(sensor, 'S')
        grid.plot(beacon, 'B')

    # Calculate manhattan distance between sensor at (8, 7) and its beacon at
    # (2, 10)
    sensor = Point(8, 7)
    beacon = sensors[sensor][0]
    print(f'Manhattan distance between sensor {sensor} and beacon {beacon}:  '
          f'{sensor.mandist(beacon)}')

    # Next steps:
    # * Plot all points <= calculated distance around sensor at (8, 7) - only
    #   plot if point empty (== '.').
    ...

    if verbose:
        print('\nInput List - Sensor: Closest Beacon:')
        pprint(sensors, sort_dicts=False)

    print(f'\nPlot of sensors and beacons:\n{grid}')


if __name__ == '__main__':
    main()
