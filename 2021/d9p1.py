#! /usr/bin/env python3.10

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


def main():
    matrix = []
    with open(INFILE) as infile:
        for line in infile:
            matrix.append([int(i) for i in line.strip()])

    lowpoints = []
    rows = len(matrix)
    cols = len(matrix[0])
    for ri, row in enumerate(matrix):
        for ci, item in enumerate(row):
            if is_lowpoint(ri, ci, rows, cols, item, row, matrix):
                lowpoints.append(item)

    risk_level = sum(lowpoints) + len(lowpoints)
    print(f'Found {len(lowpoints)} low points:  {lowpoints}')
    print(f'Risk level:  {risk_level}')


if __name__ == '__main__':
    main()
