#! /usr/bin/env python3


'''
Treetop Tree House
* Count number of trees visible from outside the tree grid when looking directly
  along a row or column

Part 1 Input:
* Map with height of each tree (#)
  * Each tree has a height from 0 - 9
  * Can see trees on edge
  * Can see interior trees from top/bottom/left/right if they are higher than
    trees in the path to get to them
    * e.g., 686 - can see the tree with height of 8
* Find how many trees visible from outside the grid

Part 2:
* Measure viewing distance from a tree:
  * Look in each direction and stop if you reach edge or tree same height or taller
  * If tree on edge, one of its viewing distances will be 0
  * Count number of trees it can see
* Find tree's scenic score:
  * Left view * right view * up view * down view
* Find highest scenic score
'''


# INFILE = 'd8p1t1.txt'
# INFILE = r'\working\github\sockduct\aoc\2022\d8p1t1.txt'
INFILE = 'd8p1.txt'


import itertools
from pprint import pprint

import numpy as np


def visible(line, pos):
    return max(line[:pos]) < line[pos] or max(line[pos + 1:]) < line[pos]


def scenic_score(line, pos):
    left = (line[:pos] < line[pos]).astype(int)
    edge = np.where(left == 0)
    left_view = sum(left[edge[0][-1] + 1:]) + 1 if len(edge[0]) > 0 else sum(left)

    right = (line[pos + 1:] < line[pos]).astype(int)
    edge = np.where(right == 0)
    right_view = sum(right[:edge[0][0]]) + 1 if len(edge[0]) > 0 else sum(right)

    return left_view * right_view


def main():
    with open(INFILE) as infile:
        lines = infile.readlines()

    matrix = np.array([[int(n) for n in line.strip()] for line in lines])

    visible_nodes = 0
    max_sscore = 0
    rows = len(matrix)
    cols = len(matrix[0])
    visible_nodes += (2 * cols)  # Add top and bottom edge
    visible_nodes += (2 * (rows - 2))  # Add left and right edges
    for row, col in itertools.product(range(1, rows - 1), range(1, cols - 1)):
        if visible(matrix[row], col) or visible(matrix[:, col], row):
            visible_nodes += 1
        max_sscore = max(
            max_sscore, scenic_score(matrix[row], col) * scenic_score(matrix[:, col], row)
        )

    print(f'\nNumber of trees visible from outside the tree grid:  {visible_nodes:,}')
    print(f'Maximum scenic score from trees within the tree grid:  {max_sscore:,}\n')

    # Debugging
    pprint(matrix)


if __name__ == '__main__':
    main()
