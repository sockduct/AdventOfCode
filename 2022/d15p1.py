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


# INFILE = Path(__file__).parent/'d15p1t1.txt'
INFILE = Path(__file__).parent/'d15p1.txt'


def find_covered(xmin, xmax, y, sensors, verbose=False):
    covered = 0

    if verbose:
        print(f'Examining range {xmin:,} - {xmax:,}...', end='', flush=True)
        xrange = abs(xmax - xmin)
        xoff = abs(xmin) if xmin < 0 else 0
        xlen = 0
        back = ''

    for x in range(xmin, xmax + 1):
        if verbose and x % 10_000 == 0:
            if xlen > 0:
                back = '\b' * xlen
            xpct = round(((x + xoff)/xrange) * 100)
            xlen = len(str(xpct)) + 1
            print(f'{back}{xpct}%', end='', flush=True)
        p = Point(x, y)
        for sensor, beaconinfo in sensors.items():
            beacon, beacondist = beaconinfo
            if sensor == p or beacon == p:
                # Don't count points occupied by sensor or beacon:
                break
            if sensor.mandist(p) <= beacondist:
                covered += 1
                break

    if verbose:
        print()

    return covered


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
            # radius" around each sensor (but not beacon - radius around sensor
            # covers beacon):
            if sx < minx or bx < minx or (sx - mandist) < minx:
                minx = min((sx, bx, sx - mandist))
            if sx > maxx or bx > maxx or (sx + mandist) > maxx:
                maxx = max((sx, bx, sx + mandist))
            if sy < miny or by < miny or (sy - mandist) < miny:
                miny = min((sy, by, sy - mandist))
            if sy > maxy or by > maxy or (sy + mandist) > maxy:
                maxy = max((sy, by, sy + mandist))

    if verbose:
        print('Input List - Sensor: Closest Beacon:')
        pprint(sensors, sort_dicts=False)

    '''
    # Calculate manhattan distance between sensor at (8, 7) and its beacon at
    # (2, 10)
    sensor = Point(8, 7)
    beacon = sensors[sensor][0]
    print(f'Manhattan distance between sensor {sensor} and beacon {beacon}:  '
            f'{sensor.mandist(beacon)}')
    grid.circle(sensor, sensor.mandist(beacon), '#', overwrite=False)
    '''

    gridmin = Point(minx, miny)
    gridmax = Point(maxx, maxy)

    '''
    grid = Grid(Point(minx, miny), Point(maxx, maxy))

    for sensor, beaconinfo in sensors.items():
        beacon, mandist = beaconinfo
        grid.plot(sensor, 'S')
        grid.plot(beacon, 'B')
        grid.circle(sensor, mandist, '#', overwrite=False)

    print(f'\nPlot of sensors and beacons:\n{grid}')
    '''

    # Retrieve grid row target:
    # row_target = 10  # Example problem input
    row_target = 2_000_000
    '''
    row = grid.getrow(row_target)
    cantbe = row.count('#')
    print(f"\nRow {row_target}:\n{row}\nNumber of positions where beacon can't be:  {cantbe:,}\n")
    '''
    res = find_covered(gridmin.x, gridmax.x, row_target, sensors, verbose=True)
    print(f"\nRow {row_target:,} - number of positions where beacon can't be:  {res:,}\n")


if __name__ == '__main__':
    main()
