#! /usr/bin/env python3.10

INFILE = 'd19p1t1.txt'
# INFILE = 'd19p1.txt'


# Libraries
# Standard Library:
from itertools import combinations
from math import isclose, sqrt
from pprint import pprint
import re

# Local
from graph import Graph


class Scanner():
    def __init__(self, id, beacons=None):
        self.id = id
        self.beacons = tuple(beacons) if isinstance(beacons, (list, tuple)) else None
        if self.beacons is None:
            raise ValueError('Current design assumes Scanner only created with sequence of beacons')

        self.graph = Graph()
        self._build_graph()

    def __getitem__(self, key):
        return self.beacons[key]

    def __repr__(self):
        return f'<Scanner(id={self.id}, {len(self.beacons)} beacons)>'

    def _build_graph(self):
        '''
        Calculate the distance between all combinations of beacons (vertices)
        and store in graph.
        '''
        self.edges = [(b1, b2, self.distance(b1, b2, byind=False))
                      for b1, b2 in combinations(self.beacons, 2)]

        for coords1, coords2, dist in self.edges:
            if (vertex1 := self.graph.get_vertex(coords1)) is None:
                vertex1 = self.graph.insert_vertex(coords1)
            if (vertex2 := self.graph.get_vertex(coords2)) is None:
                vertex2 = self.graph.insert_vertex(coords2)
            self.graph.insert_edge(vertex1, vertex2, dist)

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


def cmp_vertices(scanner1, scanner2):
    matching_vertices = []

    for vertex1 in scanner1.vertices():
        for vertex2 in scanner2.vertices():
            # 1) Same number of edges?
            if scanner1.degree(vertex1) == scanner2.degree(vertex2):
                # 2) Weights for each edge "match" or very close (because floats)
                v1_edges = sorted(scanner1.incident_edges(vertex1))
                v2_edges = sorted(scanner2.incident_edges(vertex2))

                for e1, e2 in zip(v1_edges, v2_edges):
                    if not isclose(e1, e2):
                        continue

                matching_vertices.append(vertex1.label, vertex2.label)

    return matching_vertices


'''
Start here:
* Simpler solution:
  * Create weighted (labeled) graphs
  ### \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/ ###
  * For each vertex in graph1 (scanner 0) look for vertex in graph2 (scanner 1)
    with:
    * Same number of edges
    * Matching (or very close) weights for each edge
  * Looking for 12 matching vertices between graphs (scanners)
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
X Complex and believe unnecessary:
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
* Believe looking for matching (isomorphic?) subgraphs between two scanners:
  * Beacon positions are vertices
  * Distances between all beacons are edge weights
  * Looking for 12 beacons where all edge weights between them match (or are
    really close since we're dealing with floats)
  * Find ADT and algorithm for this
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
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
    for scanner in scanners:
        print(f'Scanner {scanner.id} graph:  {scanner.graph!r}')

    # Find matching vertices in pairs of scanners
    same_verts = {k: [] for k in combinations(scanners, 2)}
    for key in same_verts:
        s1, s2 = key
        if res := cmp_vertices(s1, s2):
            same_verts[key].extend(res)

    # Temporary:
    return scanners


if __name__ == '__main__':
    main()
