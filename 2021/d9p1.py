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
def main():
    with open(INFILE) as infile:
        matrix = list(infile.readline())

if __name__ == '__main__':
    main()
