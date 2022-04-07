#! /usr/bin/env python3.10

INFILE = 'd19p1t1.txt'
# INFILE = 'd19p1.txt'


# Libraries
from itertools import combinations
from math import sqrt
from pprint import pprint
import re


class Scanner():
    def __init__(self, id, beacons=None):
        self.id = id
        self.beacons = tuple(beacons) if isinstance(beacons, (list, tuple)) else None

    def __getitem__(self, key):
        return self.beacons[key]

    def __repr__(self):
        return f'<Scanner(id={self.id}, {len(self.beacons)} beacons)>'

    def calc_dists(self):
        '''
        Calculate the distance between all combinations of beacons and store.
        '''
        self.edges = [(b1, b2, self.distance(b1, b2, byind=False))
                      for b1, b2 in combinations(self.beacons, 2)]

    def distance(self, b1, b2, byind=True):
        '''
        Calculate distance between two beacons seen by scanner, b1 and b2, using
        the distance formula.
        '''
        if byind:
            b1x, b1y, b1z = self[b1]
            b2x, b2y, b2z = self[b2]
        else:
            b1x, b1y, b1z = b1
            b2x, b2y, b2z = b2

        return sqrt( (b2x - b1x)**2 + (b2y - b1y)**2 + (b2z - b1z)**2 )


'''
Start here:
* Believe looking for matching (isomorphic?) subgraphs between two scanners:
  * Beacon positions are vertices
  * Distances between all beacons are edge weights
  * Looking for 12 beacons where all edge weights between them match (or are
    really close since we're dealing with floats)
  * Find ADT and algorithm for this
* Calculate distance between all beacons scanner can see
  * Believe Graph ADT - points are vertices, distances between are weights
* When comparing beacons under a scanner - looking for 12 beacons where
  distances are same
  * Finding matching sub-graph between scanners (weights between 12 vertices
    match)
'''
def main():
    scanners = []
    with open(INFILE) as infile:
        current_scanner = -1
        current_beacons = []
        for line in infile:
            if (scanner := re.match(r'^--- scanner (\d+) ---', line)):
                # Save last scanner and its beacons
                if current_scanner >= 0:
                    scanners.append(Scanner(current_scanner, current_beacons))
                    current_beacons.clear()
                current_scanner = int(scanner[1])
            elif (beacon := re.match(r'^(-?\d+),(-?\d+),(-?\d+)', line)):
                beacon_coords = tuple(int(i) for i in beacon.groups())
                current_beacons.append(beacon_coords)
            elif line.strip() == '':
                continue
            else:
                raise ValueError("Unexpected line value:  ``{line}''")

    print('Read in:')
    pprint(scanners)

    scanners[0].calc_dists()
    scanners[1].calc_dists()
    pprint(scanners[0].edges)
    pprint(scanners[1].edges)

    # Temporary:
    return scanners


if __name__ == '__main__':
    main()
