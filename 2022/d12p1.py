#! /usr/bin/env python3


'''
Hill Climbing Algorithm

Part 1 Input:
* Heightmap of surrounding area
  * top view grid of a-z, with a=lowest elevation, z=highest
  * Current position=S (elevation=a), Best signal position=E (elevation=z)
  * Get from S to E in as few steps as possible
  * Can move up/down/left/right
  * Elevation of destination square can be at most one higher (but can be much lower)
* What is the fewest steps required to move from S to E, following above rules?
'''


# Standard library:
from itertools import product
from pprint import pprint
import sys


# Local libraries:
# Ugly hack:
# sys.path.insert(0, '..')
sys.path.insert(0, r'\working\github\sockduct\aoc')
from ds import graph2
from ds.shortest_paths import shortest_path_lengths


# INFILE = 'd12p1t1.txt'
# INFILE = r'\working\github\sockduct\aoc\2022\d12p1t1.txt'
INFILE = 'd12p1.txt'


def getval(char):
    if char == 'S':
        return ord('a')
    elif char == 'E':
        return ord('z')
    elif 'a' <= char <= 'z':
        return ord(char)
    else:
        raise ValueError(f'Exepcted a-z|S|E, got {char}.')


def vlink(topology, matrix, row, rows, col, cols):
    '''Link left, right, up, down vertices'''
    current = getval(matrix[row][col].label[-1])
    # Up:
    if (up := row - 1) >= 0:
        above = getval(matrix[up][col].label[-1])
        if above - current <= 1:
            topology.insert_uni_edge(matrix[row][col], matrix[up][col], 1)
    # Down:
    if (down := row + 1) < rows:
        below = getval(matrix[down][col].label[-1])
        if below - current <= 1:
            topology.insert_uni_edge(matrix[row][col], matrix[down][col], 1)
    # Left:
    if (left := col - 1) >= 0:
        toleft = getval(matrix[row][left].label[-1])
        if toleft - current <= 1:
            topology.insert_uni_edge(matrix[row][col], matrix[row][left], 1)
    # Right:
    if (right := col + 1) < cols:
        toright = getval(matrix[row][right].label[-1])
        if toright - current <= 1:
            topology.insert_uni_edge(matrix[row][col], matrix[row][right], 1)


def display(topology, rows, cols):
    vertices = {vertex.label[:2]: vertex.label for vertex in topology.vertices()}

    for row in range(rows):
        for col in range(cols):
            vertex = topology.get_vertex(vertices[(row, col)])
            print(f'{vertex}', end='')
            if col + 1 < cols:
                vertex_right = topology.get_vertex(vertices[(row, col + 1)])
                if (topology.get_edge(vertex, vertex_right) and
                        topology.get_edge(vertex_right, vertex)):
                    print(' <=> ', end='')
                elif topology.get_edge(vertex, vertex_right):
                    print(' ==> ', end='')
                elif topology.get_edge(vertex_right, vertex):
                    print(' <== ', end='')
                else:
                    print('  x  ', end='')
        print()
        if row + 1 < rows:
            for col in range(cols):
                vertex = topology.get_vertex(vertices[(row, col)])
                vertex_below = topology.get_vertex(vertices[(row + 1, col)])
                if (topology.get_edge(vertex, vertex_below) and
                        topology.get_edge(vertex_below, vertex)):
                    print('  \/   /\       ', end='')
                elif topology.get_edge(vertex, vertex_below):
                    print('  \/            ', end='')
                elif topology.get_edge(vertex_below, vertex):
                    print('       /\       ', end='')
                else:
                    print('    x           ', end='')
            print()


def main(verbose=False):
    topology = graph2.Graph(directed=True)
    matrix = []
    with open(INFILE) as infile:
        for row_count, line in enumerate(infile):
            row = []
            row.extend(
                topology.insert_vertex((row_count, col_count, char))
                    for col_count, char in enumerate(line.strip())
            )
            matrix.append(row)

    # Debugging:
    if verbose:
        pprint(matrix)

    rows = len(matrix)
    cols = len(matrix[0])
    for row, col in product(range(rows), range(cols)):
        if matrix[row][col].label[-1] == 'S':
            start = matrix[row][col]
        elif matrix[row][col].label[-1] == 'E':
            end = matrix[row][col]
        vlink(topology, matrix, row, rows, col, cols)

    # Debugging:
    if verbose:
        # print(topology)
        # pprint(list(topology.vertices()))
        # pprint(topology.edges())
        display(topology, rows, cols)

    spflens = shortest_path_lengths(topology, start)
    if verbose:
        pprint(spflens)

    distance = spflens[end]
    print(f'\nPart 1 - shortest distance from start {start} to end {end}:  {distance}.')

    lowpoints = {label: vertex for label, vertex in topology._vlabels.items()
                  if label[-1] in {'S', 'a'}}
    distmap = {
        coord: shortest_path_lengths(topology, vertex)[end]
            for coord, vertex in lowpoints.items()
    }
    lowpoint_dist = min(distmap.items(), key=lambda k: k[1])
    print(f'Part 2 - shortest distance from lowest point {lowpoint_dist[0]} to end {end}:  '
          f'{lowpoint_dist[1]}.\n')


if __name__ == '__main__':
    main()
