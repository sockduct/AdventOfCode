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
# See Scanner notes below
MAX_DIST = sqrt( 1_000**2 + 1_000**2 + 1_000**2 )  # Approx: 1,732.0508
MIN_SHARED_VERTICES = 12


'''
Scanner can see beacons up to 1,000 units away on each axis:
* +/- 1,000 units in x, y, and z-axis directions
'''
class Scanner():
    def __init__(self, id, beacons=None):
        self.id = id
        self.beacons = set(beacons) if isinstance(beacons, (list, tuple)) else None
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
            if not self.graph.get_edge(vertex1, vertex2):
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


def cmp_vert_offsets(offset_res, transform, scanner_offset, verbose=False):
    match offset_res:
        case True, True, True:
            scanner_offset = list(transform)
        case False, False, False:
            transform = list(transform)
            transform = [-i for i in transform]
        case x, y, z:
            transform = list(transform)
            if x:
                index = transform.index(1) if transform.count(1) else transform.index(-1)
                scanner_offset[index] = transform[index]
                if verbose:
                    print(f'\nFound x, {scanner_offset=}')
            if y:
                index = transform.index(2) if transform.count(2) else transform.index(-2)
                scanner_offset[index] = transform[index]
                if verbose:
                    print(f'\nFound y, {scanner_offset=}')
            if z:
                index = transform.index(3) if transform.count(3) else transform.index(-3)
                scanner_offset[index] = transform[index]
                if verbose:
                    print(f'\nFound z, {scanner_offset=}')

            # Not sure I shouldn't use index like above...
            if not x:
                transform[0] = -transform[0]
            if not y:
                transform[1] = -transform[1]
            if not z:
                transform[2] = -transform[2]
    return scanner_offset, transform


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
            if nested_value > 2 and not matched_nested:
                matched_nested = True
                s1_verts_equiv[base_key] = nested_key
            elif nested_value > 2:
                raise ValueError('Matched > 2 more than once...')

    # Calculating s2_verts_equiv produces a mirror image of above - not necessary

    return s1_verts_equiv


def get_vert_edges(scanner):
    return {vertex.label: sorted(scanner.graph.incident_edges(vertex))
            for vertex in scanner.graph.vertices()}


def get_vert_offsets(s1_verts_equiv, transform, verbose=False):
    s1_verts_dists = []

    if verbose:
        print(f'\n\nCalculating vertices offsets with transform of {transform}...')
    for s0v, s1v in s1_verts_equiv.items():
        s0vx, s0vy, s0vz = s0v.label
        # This is tricky - just do in one place:
        s1vx, s1vy, s1vz = vert_transform(s1v.label, transform)

        # The diff2's are the same but with opposite sign:
        xdiff1 = s0vx - s1vx
        # xdiff2 = s1vx - s0vx
        ydiff1 = s0vy - s1vy
        # ydiff2 = s1vy - s0vy
        zdiff1 = s0vz - s1vz
        # zdiff2 = s1vz - s0vz

        s1_verts_dists.append((xdiff1, ydiff1, zdiff1))

    return s1_verts_dists


def vert_adj(vertex, offsets):
    return tuple(vert + off for vert, off in zip(vertex, offsets))


def vert_transform(vertex, offset):
    sign = lambda x: -1 if x < 0 else 1

    return [vertex[abs(offind) - 1] * sign(offind) for offind in offset]


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
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

* Figure out scanning rotation/facing direction by using 12 matching beacons:
  * Each scanner is rotated some integer number of 90-degree turns around all
    of the x, y, and z axes. That is, one scanner might call a direction
    positive x, while another scanner might call that direction negative y. Or,
    two scanners might agree on which direction is positive x, but one scanner
    might be upside-down from the perspective of the other scanner. In total,
    each scanner could be in any of 24 different orientations: facing positive
    or negative x, y, or z, and considering any of four directions "up" from
    that facing.

* Use transform to play with various permutations:
  (1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)
  -and-
  (1, 2, 3), (1, 2, -3), (1, -2, 3), (-1, 2, 3),
  (1, -2, -3), (-1, -2, 3), (-1, 2, -3), (-1, -2, -3)

* For scanners 1 and 4, offset is (-3, 1, -2)
  * Each time a column is discovered (+/- x|y|z) - need to save
  * Not quite straight forward:  (-1, -3, -2) => valid y, means we now
    have (*, *, -2)
  * Then:  (2, 1, 3) => valid x, means we now have (*, 1, -2)
  * Finally:  (-3, -2, -1) => valid z, means we now have (-3, 1, -2)
Need to put this in code below...

Next step is transform the offset from 1 to 4 to offset from 0 to 4

Need to figure out how Scanner's 0 & 1 beacons related to Scanner
1 & 4...
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

    '''
    ### Next Step...

    Can't figure out how to get Offset from Scanner 0 for Scanner 2...
    '''
    # Find matching vertices in pairs of scanners
    #!# same_verts = {k: [] for k in combinations(scanners, 2)}
    #!# same_verts = {(scanners[4], scanners[2]): []}
    path_to_s0 = {}
    #!# same_verts = {(scanners[1], scanners[4]): []}
    same_verts = {(scanners[0], scanners[1]): [],
                  (scanners[1], scanners[3]): [],
                  (scanners[1], scanners[4]): [],
                  (scanners[4], scanners[2]): []}
    for key, value in same_verts.items():
        s1, s2 = key
        s1_vertices, s2_vertices, edges = cmp_vertices(s1, s2)
        if edges:
            ### print(f'\n\nFor scanner {s1.id} and scanner {s2.id} found {len(edges)} matching edges.')
            ### print(f'\nScanner {s1.id} overlapping vertices - {len(s1_vertices)}:\n{[str(i) for i in s1_vertices]}')
            ### print(f'\nScanner {s2.id} overlapping vertices - {len(s2_vertices)}:\n{[str(i) for i in s2_vertices]}\n')
            # pprint(edges)
            print(f'\n\nScanner {s1.id} and scanner {s2.id} have {len(s2_vertices)} '
                   'overlapping vertices.')
            value.extend(edges)

        if min(len(s1_vertices), len(s2_vertices)) >= MIN_SHARED_VERTICES:
            s1_verts_equiv = get_equiv_vertices(s1_vertices, s2_vertices, edges)
            print('Left scanner vertices and corresponding right scanner vertices:')
            pprint(s1_verts_equiv)


            scanner_offset = [None, None, None]
            for transform in permutations((1, 2, 3)):
                s1_vert_offsets = get_vert_offsets(s1_verts_equiv, transform)
                ### print(f'\nScanner 0 vertices offsets versus Scanner 1 with transform {transform}:')
                ### pprint(s1_vert_offsets)

                offset_res = check_vert_offsets(s1_vert_offsets)
                scanner_offset, transform = cmp_vert_offsets(offset_res, transform, scanner_offset)

                if not all(scanner_offset):
                    # Re-run:
                    s1_vert_offsets = get_vert_offsets(s1_verts_equiv, transform)
                    ### print('\n\nScanner 0 vertices offsets versus Scanner 1 after negation '
                    ###       f'({transform}):')
                    ### pprint(s1_vert_offsets)

                    offset_res = check_vert_offsets(s1_vert_offsets)
                    scanner_offset, transform = cmp_vert_offsets(offset_res, transform, scanner_offset)

                if all(scanner_offset):
                    break

            # Don't assume current result is OK - could have found offsets piecemeal:
            s1_vert_offsets = get_vert_offsets(s1_verts_equiv, scanner_offset)
            print(f'Found scanner offset ({scanner_offset}):  {s1_vert_offsets[0]}')

            # Now rotate each vertex and add to scanner 0:
            # If s1 not scanner 0, need to find additional transformation to get
            # to scanner 0
            if s1.id == 0:
                ### Added, 0 to tuple - may require refactoring:
                path_to_s0[s2.id] = (scanner_offset, s1_vert_offsets[0], 0)
                additional_offset = None
            elif s1.id in path_to_s0:
                ### Added, s1.id to tuple - may require refactoring and not
                ### positive this is correct:
                path_to_s0[s2.id] = (scanner_offset, s1_vert_offsets[0], s1.id)
                # Adjust scanner_offset to factor in additional transformations:
                while True:
                    additional_offset = [path_to_s0[s1.id]]
            else:
                raise LookupError('Unable to find path to Scanner 0 for sequence '
                                  f'Scanner {s1.id} => Scanner {s2.id}')
            for vertex in s2.graph.vertices():
                vlabel = vertex.label
                # Transform vertex using scanner_offset
                vlabel = vert_transform(vlabel, scanner_offset)
                # Adjust vertex using s1_vert_offsets[0]
                vlabel = vert_adj(vlabel, s1_vert_offsets[0])
                # Check for additional transformations:
                ### Current Next Step:
                # Need to do this recursively...
                if additional_offset:
                    vlabel = vert_transform(vlabel, additional_offset[0])
                    vlabel = vert_adj(vlabel, additional_offset[1])
                # Add vertex to Scanner 0:
                scanners[0].beacons.add(vlabel)
            # Process new vertices:
            scanners[0]._build_graph()
            # Show:
            print(f'Scanner 0 now has {scanners[0].graph.vertex_count()} vertices')
            ### pprint(tuple(scanners[0].graph.vertices()))

        else:
            print(f'Scanner {s1.id} and/or Scanner {s2.id} have less then {MIN_SHARED_VERTICES} '
                   'vertices in common - skipping...')


if __name__ == '__main__':
    main()
