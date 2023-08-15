#! /usr/bin/env python3


'''
Day 2 Challenge, 2015

Need more wrapping paper
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
'''


INFILE = 'd2.txt'
# INFILE = 'd2t1.txt'


def get_size(present):
    l, w, h = map(int, present.split('x'))
    psize = 2 * l * w + 2 * w * h + 2 * h * l
    min_side = min((l * w, w * h, h * l))

    return psize + min_side


def main():
    total = 0

    with open(INFILE) as infile:
        for present in infile:
            present = present.strip()
            psize = get_size(present)
            print(f'Present dimensions:  {present},  Wrapping paper size:  {psize}')
            total += psize

    print(f'Total wrapping paper size needed:  {total:,}')


if __name__ == '__main__':
    main()
