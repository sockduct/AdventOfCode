#! /usr/bin/env python3


'''
Given sets of 3 sides
* How many are valid triangles?
    * e.g., A + B > C
'''


INFILE = 'd3.txt'
# INFILE = 'd3t1.txt'


# Libraries
from pathlib import Path


# Module
def valid_triangle(line: str) -> bool:
    a, b, c = sorted(map(int, line.split()))
    return a + b > c


def main() -> None:
    triangle_count = 0
    cwd = Path(__file__).parent
    c1, c2, c3 = '', '', ''
    with open(cwd/INFILE) as infile:
        for line_no, line in enumerate(infile):
            '''
            # Part 1:
            if valid_triangle(line):
                triangle_count += 1
            '''
            if line_no % 3 == 0:
                c1, c2, c3 = line.split()
            else:
                tmp1, tmp2, tmp3 = line.split()
                c1 += f' {tmp1}'
                c2 += f' {tmp2}'
                c3 += f' {tmp3}'

            if (line_no + 1) % 3 == 0:
                for col in c1, c2, c3:
                    if valid_triangle(col):
                        triangle_count += 1

    print(f'Valid triangles:  {triangle_count:,}')


if __name__ == '__main__':
    main()
