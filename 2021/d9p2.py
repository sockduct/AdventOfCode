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

def is_lowpoint(ri, ci, matrix):
    '''
    A low point is an item that is less than items to the left, right, above
    and below.
    '''
    rows = len(matrix)
    cols = len(matrix[0])
    item = matrix[ri][ci]
    row = matrix[ri]

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


def find_basin_points(ri, ci, matrix):
    '''
    Assumes point passed is a low point.

    All points surrounding a low point (including the low point).  The edge of
    a basin is an item with a height (value) of 9.

    Check left, above, right, and below.
    '''
    HIGH_POINT = 9
    rows = len(matrix)
    cols = len(matrix[0])
    item = matrix[ri][ci]
    row = matrix[ri]
    basin_matrix = [ [False] * cols for row in range(rows)]

    ledge = ci
    redge = ci
    # Track contiguous low points through shadow matrix:
    basin_matrix[ri][ci] = True

    # Check left:
    while ledge > 0 and row[ledge - 1] < HIGH_POINT:
        ledge -= 1
        basin_matrix[ri][ledge] = True
    # Check right:
    while redge + 1 < cols and row[redge + 1] < HIGH_POINT:
        redge += 1
        basin_matrix[ri][redge] = True

    def find_row_points_up(basin_matrix, cur_row):
        cur_left = len(row) + 1
        cur_right = -1

        for col, val in enumerate(basin_matrix[cur_row + 1]):
            basin_matrix[cur_row][col] = val and matrix[cur_row][col] < HIGH_POINT
            # Find outermost edges:
            if basin_matrix[cur_row][col] and col < cur_left:
                cur_left = col
            if basin_matrix[cur_row][col] and col > cur_right:
                cur_right = col

        pass ##### Here to facilitate breakpoint
        # Check for low points to left and right in current row:
        for col, val in enumerate(basin_matrix[cur_row]):
            if val and col > 0 and not basin_matrix[cur_row][col - 1]:
                cur_col = col - 1
                while cur_col >= 0 and matrix[cur_row][cur_col] < HIGH_POINT:
                    basin_matrix[cur_row][cur_col] = True
                    cur_left = cur_col
                    cur_col -= 1
            if val and col + 1 < cols and not basin_matrix[cur_row][col + 1]:
                cur_col = col + 1
                while cur_col < cols and matrix[cur_row][cur_col] < HIGH_POINT:
                    basin_matrix[cur_row][cur_col] = True
                    cur_right = cur_col
                    cur_col += 1

        # Check for low points below when cur_left or cur_right extends beyond
        # ledge/redge
        if cur_left < ledge:
            cur_col = cur_left
            while cur_col < ledge:
                temp_row = cur_row + 1
                while temp_row <= ri:
                    if matrix[temp_row][cur_col] >= HIGH_POINT:
                        break
                    basin_matrix[temp_row][cur_col] = True
                    # Look left or right here
                    temp_col = cur_col - 1
                    while temp_col >= 0 and matrix[temp_row][temp_col] < HIGH_POINT:
                        basin_matrix[temp_row][temp_col] = True
                        temp_col -= 1
                    temp_col = cur_col + 1
                    while temp_col < cols and matrix[temp_row][temp_col] < HIGH_POINT:
                        basin_matrix[temp_row][temp_col] = True
                        temp_col += 1
                    # Iterate row
                    temp_row += 1
                cur_col += 1
        if cur_right > redge:
            cur_col = cur_right
            while cur_col > redge:
                temp_row = cur_row + 1
                while temp_row <= ri:
                    if matrix[temp_row][cur_col] >= HIGH_POINT:
                        break
                    basin_matrix[temp_row][cur_col] = True
                    # Look left or right here
                    temp_col = cur_col - 1
                    while temp_col >= 0 and matrix[temp_row][temp_col] < HIGH_POINT:
                        basin_matrix[temp_row][temp_col] = True
                        temp_col -= 1
                    temp_col = cur_col + 1
                    while temp_col < cols and matrix[temp_row][temp_col] < HIGH_POINT:
                        basin_matrix[temp_row][temp_col] = True
                        temp_col += 1
                    # Iterate row
                    temp_row += 1
                cur_col -= 1

        if cur_row > 0 and any(basin_matrix[cur_row]):
            find_row_points_up(basin_matrix, cur_row - 1)

    # Recursively check above:
    # Make sure that row above connected to valid point in row below - might not
    # be contiguous:
    if ri > 0:
        find_row_points_up(basin_matrix, ri - 1)

    def find_row_points_down(basin_matrix, cur_row):
        cur_left = len(row) + 1
        cur_right = -1

        for col, val in enumerate(basin_matrix[cur_row - 1]):
            basin_matrix[cur_row][col] = val and matrix[cur_row][col] < HIGH_POINT
            # Find outermost edges:
            if basin_matrix[cur_row][col] and col < cur_left:
                cur_left = col
            if basin_matrix[cur_row][col] and col > cur_right:
                cur_right = col

        # Check for low points to left and right in current row:
        for col, val in enumerate(basin_matrix[cur_row]):
            if val and col > 0 and not basin_matrix[cur_row][col - 1]:
                cur_col = col - 1
                while cur_col >= 0 and matrix[cur_row][cur_col] < HIGH_POINT:
                    basin_matrix[cur_row][cur_col] = True
                    cur_left = cur_col
                    cur_col -= 1
            if val and col + 1 < cols and not basin_matrix[cur_row][col + 1]:
                cur_col = col + 1
                while cur_col < cols and matrix[cur_row][cur_col] < HIGH_POINT:
                    basin_matrix[cur_row][cur_col] = True
                    cur_right = cur_col
                    cur_col += 1

        # Check for low points below when cur_left or cur_right extends beyond
        # ledge/redge
        if cur_left < ledge:
            cur_col = cur_left
            while cur_col < ledge:
                temp_row = cur_row - 1
                while temp_row > ri:
                    if matrix[temp_row][cur_col] >= HIGH_POINT:
                        break
                    basin_matrix[temp_row][cur_col] = True
                    # Look left or right here
                    temp_col = cur_col - 1
                    while temp_col >= 0 and matrix[temp_row][temp_col] < HIGH_POINT:
                        basin_matrix[temp_row][temp_col] = True
                        temp_col -= 1
                    temp_col = cur_col + 1
                    while temp_col < cols and matrix[temp_row][temp_col] < HIGH_POINT:
                        basin_matrix[temp_row][temp_col] = True
                        temp_col += 1
                    # Iterate row
                    temp_row -= 1
                cur_col += 1
        if cur_right > redge:
            cur_col = cur_right
            while cur_col > redge:
                temp_row = cur_row - 1
                while temp_row > ri:
                    if matrix[temp_row][cur_col] >= HIGH_POINT:
                        break
                    basin_matrix[temp_row][cur_col] = True
                    # Look left or right here
                    temp_col = cur_col - 1
                    while temp_col >= 0 and matrix[temp_row][temp_col] < HIGH_POINT:
                        basin_matrix[temp_row][temp_col] = True
                        temp_col -= 1
                    temp_col = cur_col + 1
                    while temp_col < cols and matrix[temp_row][temp_col] < HIGH_POINT:
                        basin_matrix[temp_row][temp_col] = True
                        temp_col += 1
                    # Iterate row
                    temp_row -= 1
                cur_col -= 1

        if cur_row + 1 < rows and any(basin_matrix[cur_row]):
            find_row_points_down(basin_matrix, cur_row + 1)

    # Recurively check below:
    # Make sure that row below connected to valid point in row above - might not
    # be contiguous:
    if ri + 1 < rows:
        # Find low points in row above low points in row below:
        find_row_points_down(basin_matrix, ri + 1)

    return sum(sum(row) for row in basin_matrix)


def main(verbose=False):
    matrix = []
    with open(INFILE) as infile:
        for line in infile:
            matrix.append([int(i) for i in line.strip()])

    lowpoints = []
    for ri, row in enumerate(matrix):
        for ci, item in enumerate(row):
            if is_lowpoint(ri, ci, matrix):
                if verbose:
                    print(f'Found low point at ({ri}, {ci}):  {item}')
                lowpoints.append((ri, ci))

    basinsizes = []
    for ri, ci in lowpoints:
        basin_size = find_basin_points(ri, ci, matrix)
        if verbose:
            print(f'Basin size:  {basin_size}')
        basinsizes.append(basin_size)

    '''
    Getting close, but my answer is too small (840,840)
    Getting closer, my answer is too large (3,344,952)
    Current answer:  848,848
    Work through current break point - another off by one error!
    '''
    # Multiply three largest basins:
    res = reduce(lambda x, y: x * y, sorted(basinsizes, reverse=True)[:3])
    print(f'Number of low points:  {len(lowpoints)}')
    print('Low points:')
    cur = 0
    while cur < len(lowpoints):
        print(lowpoints[cur:cur + 10])
        cur += 10
    print(f'Number of basins:  {len(basinsizes)}')
    print('Basin sizes:')
    cur = 0
    while cur < len(basinsizes):
        print(basinsizes[cur:cur + 10])
        cur += 10
    print(f'Ten largest basins:  {sorted(basinsizes, reverse=True)[:10]}')
    print(f'Result:  {res}')


if __name__ == '__main__':
    main()
