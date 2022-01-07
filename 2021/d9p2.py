#! /usr/bin/env python3.10

from functools import reduce

# INFILE = 'd9p1t1.txt'
INFILE = 'd9p1.txt'

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

    Check left, above, right, and below.
    '''
    HIGH_POINT = 9

    cur_left = ci
    cur_right = ci
    total_points = 1  # Start with including low point (ri, ci)
    # Check left:
    while cur_left > 0 and row[cur_left - 1] < HIGH_POINT:
        cur_left -= 1
    # Check right:
    while cur_right + 1 < cols and row[cur_right + 1] < HIGH_POINT:
        cur_right += 1

    total_points += cur_right - cur_left

    def find_row_points_up(row, ref_inbasin, cur_row):
        # Find low points in row above low points in row below:
        inbasin = [(val and row[i] < HIGH_POINT) for i, val in enumerate(ref_inbasin)]

        # Check for low points to left and right in current row:
        for i, val in enumerate(inbasin):
            if val and i > 0 and not inbasin[i - 1]:
                temp_i = i - 1
                while temp_i >= 0 and row[temp_i] < HIGH_POINT:
                    inbasin[temp_i] = True
                    temp_i -= 1
            if val and i + 1 < cols and not inbasin[i + 1]:
                temp_i = i + 1
                while temp_i < cols and row[temp_i] < HIGH_POINT:
                    inbasin[temp_i] = True
                    temp_i += 1

        if cur_row > 0 and any(inbasin):
            return sum(inbasin) + find_row_points_up(matrix[cur_row - 1], inbasin, cur_row - 1)

        return sum(inbasin)

    # Recursively check above:
    # Make sure that row above connected to valid point in row below - might not
    # be contiguous:
    if ri > 0:
        inbasin = [(cur_left <= i <= cur_right) for i in range(len(row))]
        total_points += find_row_points_up(matrix[ri - 1], inbasin, ri - 1)

    def find_row_points_down(row, ref_inbasin, cur_row, rows):
        inbasin = [(val and row[i] < HIGH_POINT) for i, val in enumerate(ref_inbasin)]

        # Check for low points to left and right in current row:
        for i, val in enumerate(inbasin):
            if val and i > 0 and not inbasin[i - 1]:
                temp_i = i - 1
                while temp_i >= 0 and row[temp_i] < HIGH_POINT:
                    inbasin[temp_i] = True
                    temp_i -= 1
            if val and i + 1 < cols and not inbasin[i + 1]:
                temp_i = i + 1
                while temp_i < cols and row[temp_i] < HIGH_POINT:
                    inbasin[temp_i] = True
                    temp_i += 1

        if cur_row + 1 < rows and any(inbasin):
            return sum(inbasin) + find_row_points_down(matrix[cur_row + 1], inbasin,
                                                       cur_row + 1, rows)

        return sum(inbasin)

    # Recurively check below:
    # Make sure that row below connected to valid point in row above - might not
    # be contiguous:
    if ri + 1 < rows:
        # Find low points in row above low points in row below:
        inbasin = [(cur_left <= i <= cur_right) for i in range(len(row))]
        total_points += find_row_points_down(matrix[ri + 1], inbasin, ri + 1, rows)

    return total_points


def main(verbose=False):
    matrix = []
    with open(INFILE) as infile:
        for line in infile:
            matrix.append([int(i) for i in line.strip()])

    rows = len(matrix)
    cols = len(matrix[0])
    lowpoints = []
    for ri, row in enumerate(matrix):
        for ci, item in enumerate(row):
            if is_lowpoint(ri, ci, rows, cols, item, row, matrix):
                if verbose:
                    print(f'Found low point at ({ri}, {ci}):  {item}')
                lowpoints.append((ri, ci))

    basinsizes = []
    for ri, ci in lowpoints:
        basin_size = find_basin_points(ri, ci, rows, cols, matrix[ri], matrix)
        if verbose:
            print(f'Basin size:  {basin_size}')
        basinsizes.append(basin_size)

    '''
    Getting close, but my answer is too small (840,840)

    Look at 3 largest basins to see if missing low points

    Flaw in 105 basin...
    When go up and down:
    * Keep track of previous row left and right edges
    * If current row is wider left or right edge, then check above/below wider
      points down to starting/home row
    '''
    # Multiply three largest basins:
    res = reduce(lambda x, y: x * y, sorted(basinsizes, reverse=True)[:3])
    print(f'Basin sizes:  {basinsizes}')
    print(f'Ten largest basins:  {sorted(basinsizes, reverse=True)[:10]}')
    print(f'Result:  {res}')


if __name__ == '__main__':
    main()
