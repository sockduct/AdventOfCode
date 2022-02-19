#! /usr/bin/env python3.10


# Standard library
from pprint import pprint

# 3rd party:
from graph import Graph
from shortest_paths import shortest_path_lengths


# INFILE = 'd15p1t1a.txt'
# INFILE = 'd15p1t1.txt'
INFILE = 'd15p1.txt'


'''
Map:
  0 1 2
0 1 1 6
1 1 3 8
2 2 1 3

Directions:
* Start in top left
* Destination is bottom right
* No diagonal movement, only left/right or up/down
* Number in each position is risk level
* Don't count risk level from starting position unless you "enter" it
* Add risk of each position you enter
* Find path with lowest total risk

Thoughts on Approach:
* Actual data is 100x100 matrix - probably too big for backtracking
* Thinking this is a weighted graph problem
* Convert number matrix into weighted graph and then use Dijkstra's shortest
  path first algorithm to find least cost path
'''


def magnify(matrix, factor):
    rows = len(matrix)
    cols = rows
    row_width = rows * factor
    mult = factor - 1  # Matrix expansion multiplier
    new_cols = 2 * mult  # How many incremented column groups to add

    # Add enough empty rows to expand out matrix:
    for _ in range(rows * mult):
        matrix.append([])

    for row in range(rows):
        inc_row = matrix[row].copy()
        new_col_group = []
        # Build out enough new row groups for across and down:
        for _ in range(new_cols):
            inc_row = [(col + 1 if col < 9 else 1) for col in inc_row]
            new_col_group.extend(inc_row)

        # Expand out current row:
        matrix[row].extend(new_col_group[:cols * mult])

        # Build out new rows:
        for new_row_mult in range(mult):
            start_col = cols * new_row_mult
            end_col = start_col + row_width
            cur_row = (rows * (new_row_mult + 1)) + row
            matrix[cur_row].extend(new_col_group[start_col:end_col])

    return matrix


def main():
    matrix = []
    with open(INFILE) as infile:
        matrix.extend([int(e) for e in line.strip()] for line in infile)

    matrix = magnify(matrix, 5)
    '''
    pprint(matrix)
    return 0
    '''

    cavern = Graph(directed=True)
    for row, line in enumerate(matrix):
        cur_vertex = None
        cur_val = 0
        for col, val in enumerate(line):
            left_vertex = cur_vertex
            left_val = cur_val
            cur_vertex = cavern.insert_vertex((row, col))
            cur_val = val
            if left_vertex:
                cavern.insert_uni_edge(left_vertex, cur_vertex, cur_val)
                cavern.insert_uni_edge(cur_vertex, left_vertex, left_val)
            if row > 0:
                up_vertex = cavern.get_vertex((row - 1, col))
                cavern.insert_uni_edge(up_vertex, cur_vertex, cur_val)
                cavern.insert_uni_edge(cur_vertex, up_vertex, matrix[row - 1][col])

    spf_lens = shortest_path_lengths(cavern, cavern.get_vertex((0, 0)))

    matrix_width = len(matrix) - 1
    furthest_point = (matrix_width, matrix_width)
    print(f'Shortest path from (0, 0) to {furthest_point}:  '
          f'{spf_lens[cavern.get_vertex(furthest_point)]}')

    '''
    pprint(spf_lens)

    pprint(matrix)
    print(f'\n{cavern}')
    '''


if __name__ == '__main__':
    main()
