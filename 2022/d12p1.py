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
from itertools import pairwise
from pprint import pprint
import sys


# Third party libraries:
import numpy as np

# Local libraries:
# Ugly hack:
sys.path.insert(0, '..')
from ds import graph2


INFILE = 'd12p1t1.txt'
# INFILE = 'd12p1.txt'


def vlink(matrix, row, col):
    '''Link left, right, up, down vertices'''
    ...


def main():
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
    pprint(matrix)

    for row in range(len(matrix)):
        for col in range(len(row)):
            vlink(matrix)


if __name__ == '__main__':
    main()
