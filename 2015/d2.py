#! /usr/bin/env python3


'''
Day 2 Challenge, 2015

Part 1 - need more wrapping paper
* List of dimensions of each present:  l x w x h
* Only want to order what's needed
* Find surface area of box:  2lw + 2wh + 2hl
* Add the area of the smallest side as extra for each present
* Given list of presents, how much wrapping paper to order?

Example:
* Present:  2 x 3 x 4
    * SA = 2 * 2 * 3 + 2 * 3 * 4 + 2 * 2 * 4 = 52 sq ft
    * Extra = 6 sq ft from smallest side
    * Total = 58 sq ft
* Present:  1 x 1 x 10
    * SA = 2*1 + 2*10 + 2*10 = 42
    * Extra = 1
    * Total = 43

Part 2 - need more ribbon
* Shortest distance around the sides or smallest perimeter of any one face
* Also need bow - length = cubic feet of volume of present

Example:
* Present:  2 x 3 x 4
    * Smallest perimeter:  2 + 2 + 3 + 3 = 10
    * Bow:  2 * 3 * 4 = 24
    * Total:  34
* Present:  1 x 1 x 10
    * Smallest perimeter:  1 + 1 + 1 + 1 = 4
    * Bow = 1 * 1 * 10 = 10
    * Total = 14
'''


INFILE = 'd2.txt'
# INFILE = 'd2t1.txt'


def get_size(present):
    l, w, h = map(int, present.split('x'))
    psize = 2 * l * w + 2 * w * h + 2 * h * l
    min_side = min((l * w, w * h, h * l))
    min_perim = min((2 * l + 2 * w, 2 * w + 2 * h, 2 * h + 2 * l))
    area = l * w * h

    return (psize + min_side, min_perim + area)


def main():
    total_wrap = 0
    total_bow = 0

    with open(INFILE) as infile:
        for present in infile:
            present = present.strip()
            wrap_size, bow_size = get_size(present)

            print(f'Present dimensions:  {present},  Wrapping paper size:  {wrap_size}'
                  f',  Bow size:  {bow_size}')
            total_wrap += wrap_size
            total_bow += bow_size

    print(f'Part 1, Total wrapping paper size needed:  {total_wrap:,}')
    print(f'Part 2, Total ribbon size needed for bows:  {total_bow:,}')


if __name__ == '__main__':
    main()
