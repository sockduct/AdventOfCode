#! /usr/bin/env python3.10

INFILE = 'd9p1t1.txt'
# INFILE = 'd9p1.txt'

'''
Read in a matrix:
2199943210
3987894921
9856789892
8767896789
9899965678

Find the low points - locations lower than any adjacent location.  Adjacencies
include items to the left, right, up, or down, but not diagonally.
'''

def is_lowpoint(ri, ci, rows, cols, item, row, matrix):
    '''
    A low point is an item that is less than items to the left, right, above
    and below.
    '''
    # Check for failure cases
    # Check left:
    if ci > 0 and row[ci - 1] <= item:
        return False
    # Check right:
    if ci + 1 < cols and row[ci + 1] <= item:
        return False
    # Check above:
    if ri > 0 and matrix[ri - 1][ci] <= item:
        return False
    # Check below:
    if ri + 1 < rows and matrix[ri + 1][ci] <= item:
        return False

    return True


def find_basin_points(ri, ci, rows, cols, row, matrix):
    '''
    Assumes point passed is a low point.

    All points surrounding a low point (including the low point).  The edge of
    a basin is an item with a height (value) of 9.

    Recursively check left, above, right, and below.
    '''
    HIGH_POINT = 9

    '''
    # Fail!
    * Can't go left and then right because infinite recursion results
    * Perhaps go only left and up, then...?

    Need to think through approach...
    '''
    # Check left:
    if ci > 0 and row[ci - 1] < HIGH_POINT:
        return 1 + find_basin_points(ri, ci - 1, rows, cols, row, matrix)
    # Check right:
    if ci + 1 < cols and row[ci + 1] < HIGH_POINT:
        return 1 + find_basin_points(ri, ci + 1, rows, cols, row, matrix)
    # Check above:
    if ri > 0 and matrix[ri - 1][ci] < HIGH_POINT:
        return 1 + find_basin_points(ri - 1, ci, rows, cols, matrix[ri - 1], matrix)
    # Check below:
    if ri + 1 < rows and matrix[ri + 1][ci] < HIGH_POINT:
        return 1 + find_basin_points(ri + 1, ci, rows, cols, matrix[ri + 1], matrix)
    # Surrounded by high points (base case)
    return 1


def main():
    matrix = []
    with open(INFILE) as infile:
        for line in infile:
            matrix.append([int(i) for i in line.strip()])

    rows = len(matrix)
    cols = len(matrix[0])
    for ri, row in enumerate(matrix):
        for ci, item in enumerate(row):
            if is_lowpoint(ri, ci, rows, cols, item, row, matrix):
                print(f'Found low point at ({ri}, {ci}):  {item}')
                basin_size = find_basin_points(ri, ci, rows, cols, row, matrix)
                print(f'Basin size:  {basin_size}')


if __name__ == '__main__':
    main()
