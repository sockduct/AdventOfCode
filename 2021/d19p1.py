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


# Globals:
MAX_DIST = sqrt( 1_000**2 + 1_000**2 + 1_000**2 )  # Approx: 1,732.0508


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
    '''
    Take two scanners (graph portion) and return matching edges <= max_dist

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Next step:  From matching edges, pull out all vertices and find unique set
    '''
    matching_edges = []
    s1_edges = []
    s2_edges = []
    # max_dist = 1_000
    max_dist = MAX_DIST

    edges1 = sorted(scanner1.graph.edges())
    edges2 = sorted(scanner2.graph.edges())
    edge1 = None
    edge2 = None
    while edges1 and edges2:
        if not edge1:
            edge1 = edges1.pop()
        if not edge2:
            edge2 = edges2.pop()

        if isclose(edge1.label, edge2.label):
            if edge1.label <= max_dist:
                s1_edges.append(edge1)
                s2_edges.append(edge2)
                matching_edges.append((edge1, edge2))
            edge1 = None
            edge2 = None
        elif edge1.label > edge2.label:
            edge1 = None
        else:
            edge2 = None

    s1_vertices = set()
    for edge in s1_edges:
        s1_vertices.update(edge.endpoints())
    s2_vertices = set()
    for edge in s2_edges:
        s2_vertices.update(edge.endpoints())

    return s1_vertices, s2_vertices, matching_edges


def get_vert_edges(scanner):
    return {vertex.label: sorted(scanner.graph.incident_edges(vertex))
            for vertex in scanner.graph.vertices()}


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
* Refinement - the above is close, but from examining problem again, only need
  to find 12 matching vertices or 11 edges with matching distances
  * Refactor cmp_vertices to find vertex pairs with >= 11 matching edges
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
        current_beacons = []
        for line in infile:
            if (scanner := re.match(r'^--- scanner (\d+) ---', line)):
                current_scanner = int(scanner[1])
                current_processed = False
            elif (beacon := re.match(r'^(-?\d+),(-?\d+),(-?\d+)', line)):
                beacon_coords = tuple(int(i) for i in beacon.groups())
                current_beacons.append(beacon_coords)
            elif line.strip() == '':
                # Save current scanner and its beacons
                scanners.append(Scanner(current_scanner, current_beacons))
                current_beacons.clear()
                current_processed = True
            else:
                raise ValueError("Unexpected line value:  ``{line}''")

        if not current_processed:
            # Save current scanner and its beacons
            scanners.append(Scanner(current_scanner, current_beacons))
            current_beacons.clear()

        if current_scanner + 1 != len(scanners):
            raise ValueError('Missed last value!!!')


    print('Read in:')
    for scanner in scanners:
        print(f'Scanner {scanner.id} graph:  {scanner.graph!r}')
        #pprint(get_vert_edges(scanner))
        #print()

    # Find matching vertices in pairs of scanners
    same_verts = {k: [] for k in combinations(scanners, 2)}
    for key in same_verts:
        s1, s2 = key
        s1_vertices, s2_vertices, res = cmp_vertices(s1, s2)
        if res:
            print(f'For scanner {s1.id} and scanner {s2.id} found {len(res)} matching edges.')
            print(f'Scanner {s1.id} overlapping vertices:\n{[str(i) for i in s1_vertices]}')
            print(f'Scanner {s2.id} overlapping vertices:\n{[str(i) for i in s2_vertices]}')
            pprint(res)
            print()
            same_verts[key].extend(res)

    ### print(f'Found {len(same_verts)} matching vertices:')
    ### pprint(same_verts)

    # Temporary:
    return scanners


if __name__ == '__main__':
    main()
