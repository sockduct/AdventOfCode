#! /usr/bin/env python3


'''
Decompress string
* Ignore whitespace
* Look for markers:  (axb), e.g., (10x2)
    * Take subsequent a characters after marker and repeat that sequence b times
    * Continue reading file after repeated data
    * Marker itself not included in output
    * If marker within group of "a" characters, ignore it and treat it like
      normal characters
'''


INFILE = 'd9.txt'
# INFILE = 'd9t1.txt'
# INFILE = 'd9t2.txt'
# INFILE = 'd9t3.txt'
# INFILE = 'd9t4.txt'


# Libraries:
from math import prod
from pathlib import Path
from reprlib import repr as altrepr
from string import ascii_uppercase as uppers


# Module:
def get_secval(line: str, stack: list[tuple[int, int, int]], offset: int) -> int:
    'Calculate section value'
    val = 0
    for char in line:
        if char not in uppers:
            raise ValueError(f'Expected value in A-Z, got:  {char}')

        val += prod(s[2] for s in stack if s[0] <= offset <= s[1])
        offset += 1

    return val


def parse4(line: str, *, recursive: bool=False) -> int:
    '''
    Stack-based calculator

    Examples:
    (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated 241,920 times.
    (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.
    ORNXNQJQ(151x7)(5x9)OFIXU(27x3)(21x9)VDCYQELDJQUAFZUHFZVSU(34x15)(12x10)SEDIUUVFPEKY(3x9)
        NHR(1x11)I(15x6)(9x13)CMNDUYGYR(40x6)(4x7)RMNG(25x8)XPDSEYNCWFQFAKUMITWMBLMIK
    '''
    stack = []
    index = 0
    outlen = 0
    while index < len(line):
        start = line.find('(', index)
        if start >= 0:
            end = line.find(')', start)
            count, repeat = [int(n) for n in line[start + 1:end].split('x')]
            if recursive:
                stack.append((end + 1, end + count, repeat))

            # For non-recursive passes, this will always be true:
            if not stack:
                outlen += len(line[index:start])
            else:
                outlen += get_secval(line[index:start], stack, index)

            if not recursive:
                outlen += len(line[end + 1:end + 1 + count]) * repeat
                index = end + 1 + count
            else:
                index = end + 1
        else:
            if not stack:
                outlen += len(line[index:])
            else:
                outlen += get_secval(line[index:], stack, index)
            break

    return outlen


def main() -> None:
    cwd = Path(__file__).parent
    '''
    for file in ('d9t1.txt', 'd9t2.txt', 'd9t4.txt', 'd9.txt'):
        INFILE = file
        print(f'Processing {INFILE}...')
    '''

    with open(cwd/INFILE) as infile:
        for line in infile:
            # Part 1:
            # res = parse4(line.strip())
            #
            # Part 2:
            res = parse4(line.strip(), recursive=True)
            print(f'Decompressed "{altrepr(line.strip())}", length is {res:,}')


if __name__ == '__main__':
    main()
