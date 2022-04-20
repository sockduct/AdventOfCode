#! /usr/bin/env python3.10

INFILE = 'd19p1t1.txt'
# INFILE = 'd19p1.txt'


# Libraries
# Standard Library:
from collections import defaultdict
from itertools import combinations, permutations
from math import isclose, sqrt
from pprint import pprint
import re

# Local
from graph import Graph


# Globals:
MAX_DIST = sqrt( 1_000**2 + 1_000**2 + 1_000**2 )  # Approx: 1,732.0508


'''
Scanner can see beacons up to 1,000 units away on each axis:
* +/- 1,000 units in x, y, and z-axis directions
'''
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


def check_vert_offsets(vert_offsets):
    offsets = len(vert_offsets)
    found_x = (vert_offsets[0][0] * offsets == sum(offset[0] for offset in vert_offsets))
    found_y = (vert_offsets[0][1] * offsets == sum(offset[1] for offset in vert_offsets))
    found_z = (vert_offsets[0][2] * offsets == sum(offset[2] for offset in vert_offsets))

    return found_x, found_y, found_z


def cmp_vertices(scanner1, scanner2):
    '''
    Take two scanners (graph portion) and return matching edges <= max_dist
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


def get_equiv_vertices(s1_vertices, s2_vertices, edges):
    s1_verts = {vert: defaultdict(int) for vert in s1_vertices}
    s2_verts = {vert: defaultdict(int) for vert in s2_vertices}
    for e1, e2 in edges:
        s1_v1, s1_v2 = e1.endpoints()
        s2_v1, s2_v2 = e2.endpoints()
        s1_verts[s1_v1][s2_v1] += 1
        s1_verts[s1_v1][s2_v2] += 1
        s1_verts[s1_v2][s2_v1] += 1
        s1_verts[s1_v2][s2_v2] += 1
        s2_verts[s2_v1][s1_v1] += 1
        s2_verts[s2_v1][s1_v2] += 1
        s2_verts[s2_v2][s1_v1] += 1
        s2_verts[s2_v2][s1_v2] += 1

    #pprint(s1_verts)
    #pprint(s2_verts)

    # With this having matching vertices
    s1_verts_equiv = {}
    for base_key, base_values in s1_verts.items():
        matched_nested = False
        for nested_key, nested_value in base_values.items():
            if nested_value == 11 and not matched_nested:
                matched_nested = True
                s1_verts_equiv[base_key] = nested_key
            elif nested_value == 11:
                raise ValueError('Matched 11 more than once...')

    '''
    # These are mirror image of above and not necessary:
    s2_verts_equiv = {}
    for base_key, base_values in s2_verts.items():
        matched_nested = False
        for nested_key, nested_value in base_values.items():
            if nested_value == 11 and not matched_nested:
                matched_nested = True
                s2_verts_equiv[base_key] = nested_key
            elif nested_value ==11 and matched_nested:
                raise ValueError('Matched 11 more than once...')
    '''

    return s1_verts_equiv


def get_vert_edges(scanner):
    return {vertex.label: sorted(scanner.graph.incident_edges(vertex))
            for vertex in scanner.graph.vertices()}


def get_vert_offsets(s1_verts_equiv, transform):
    s1_verts_dists = []

    print(f'\n\nCalculating vertices offsets with transform of {transform}...')
    for s0v, s1v in s1_verts_equiv.items():
        abs_transform = list(map(abs, transform))
        match abs_transform:
            case 1, 2, 3:
                s0vx, s0vy, s0vz = s0v.label
                s1vx, s1vy, s1vz = s1v.label
            case 1, 3, 2:
                s0vx, s0vz, s0vy = s0v.label
                s1vx, s1vz, s1vy = s1v.label
            case 2, 1, 3:
                s0vy, s0vx, s0vz = s0v.label
                s1vy, s1vx, s1vz = s1v.label
            case 2, 3, 1:
                s0vy, s0vz, s0vx = s0v.label
                s1vy, s1vz, s1vx = s1v.label
            case 3, 1, 2:
                s0vz, s0vx, s0vy = s0v.label
                s1vz, s1vx, s1vy = s1v.label
            case 3, 2, 1:
                s0vz, s0vy, s0vx = s0v.label
                s1vz, s1vy, s1vx = s1v.label

        if -1 in transform:
            s1vx = -s1vx
        if -2 in transform:
            s1vy = -s1vy
        if -3 in transform:
            s1vz = -s1vz

        # The diff2's are the same but with opposite sign:
        xdiff1 = s0vx - s1vx
        # xdiff2 = s1vx - s0vx
        ydiff1 = s0vy - s1vy
        # ydiff2 = s1vy - s0vy
        zdiff1 = s0vz - s1vz
        # zdiff2 = s1vz - s0vz

        s1_verts_dists.append((xdiff1, ydiff1, zdiff1))

    return s1_verts_dists


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
    for key, value in same_verts.items():
        s1, s2 = key
        s1_vertices, s2_vertices, edges = cmp_vertices(s1, s2)
        if edges:
            print(f'\n\nFor scanner {s1.id} and scanner {s2.id} found {len(edges)} matching edges.')
            print(f'\nScanner {s1.id} overlapping vertices - {len(s1_vertices)}:\n{[str(i) for i in s1_vertices]}')
            print(f'\nScanner {s2.id} overlapping vertices - {len(s2_vertices)}:\n{[str(i) for i in s2_vertices]}\n')
            # pprint(edges)
            print()
            value.extend(edges)

        s1_verts_equiv = get_equiv_vertices(s1_vertices, s2_vertices, edges)
        print('Scanner 0 vertices (left) and corresponding scanner 1 vertices (right):')
        pprint(s1_verts_equiv)

        '''
        ### Next Step:
        * Figure out scanning rotation/facing direction by using 12 matching
          beacons

          Each scanner is rotated some integer number of 90-degree turns around all
          of the x, y, and z axes. That is, one scanner might call a direction positive
          x, while another scanner might call that direction negative y. Or, two scanners
          might agree on which direction is positive x, but one scanner might be upside-down
          from the perspective of the other scanner. In total, each scanner could be in
          any of 24 different orientations: facing positive or negative x, y, or z, and
          considering any of four directions "up" from that facing.

        * Use transform to play with various permutations:
          (1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)
          -and-
          (1, 2, 3), (1, 2, -3), (1, -2, 3), (-1, 2, 3),
          (1, -2, -3), (-1, -2, 3), (-1, 2, -3), (-1, -2, -3)
        '''

        for transform in permutations((1, 2, 3)):
            s1_vert_offsets = get_vert_offsets(s1_verts_equiv, transform)
            print('\nScanner 0 vertices offsets versus Scanner 1:')
            pprint(s1_vert_offsets)

            if all(found_res := check_vert_offsets(s1_vert_offsets)):
                print(f'Found scanner offset:  {s1_vert_offsets[0]}')
            else:
                found_x, found_y, found_z = found_res
                transform = list(transform)
                if not found_x:
                    transform[0] = -transform[0]
                if not found_y:
                    transform[1] = -transform[1]
                if not found_z:
                    transform[2] = -transform[2]

                # Re-run:
                s1_vert_offsets = get_vert_offsets(s1_verts_equiv, transform)
                print('\n\nScanner 0 vertices offsets versus Scanner 1 after negation:')
                pprint(s1_vert_offsets)

                if all(check_vert_offsets(s1_vert_offsets)):
                    print(f'Found scanner offset:  {s1_vert_offsets[0]}')
                    break

        # Start with just 0 and 1:
        # break

    ### print(f'Found {len(same_verts)} matching vertices:')
    ### pprint(same_verts)

    # Temporary:
    return scanners


if __name__ == '__main__':
    main()
