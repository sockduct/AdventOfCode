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


# INFILE = 'd9.txt'
# INFILE = 'd9t1.txt'
INFILE = 'd9t2.txt'
# INFILE = 'd9t3.txt'


# Libraries:
from pathlib import Path
from reprlib import repr as altrepr


# Module:
def parse(line: str, *, recursive: bool=False, verbose: bool=False) -> tuple[str, int]:
    output = ''
    index = 0
    loops = 0
    while index < (cur_len := len(line)):
        loops += 1
        start = line.find('(', index)
        if start >= 0:
            end = line.find(')', start)
            if not recursive:
                output += line[index:start]
            else:
                output = line[:start]

            count, repeat = [int(n) for n in line[start + 1:end].split('x')]
            output += line[end + 1:end + 1 + count] * repeat
            index = start
            if not recursive:
                index = end + 1 + count
            else:
                line = output + line[end + 1 + count:]
                index = line.find('(')
                if index == -1:
                    index = len(output)

            if verbose and loops % 1_000 == 0:
                print(f'{loops:,} iterations, at position {index:,} of {cur_len:,} {(index/cur_len) * 100:.2f}')
        else:
            output += line[index:]
            break

    return output, len(output)


def section_len(line: str, start: int, secend: int|None=None) -> tuple[int, int]:
    '''
    Examples:
    * (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated 241,920 times.
    * (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.
    '''

    ### Not counting characters between parentheses on bottom case...
    end = line.find(')', start)
    count, repeat = [int(n) for n in line[start + 1:end].split('x')]

    if not secend:
        secend = end + 1 + count
    seclen = 0
    interimlen = 0
    end_adj = False
    while True:
        next_start = line.find('(', end + 1, secend)
        if next_start >= 0:
            seclen += next_start - end - 1 # len(line[start:next_start])
            next_seclen, index = section_len(line, next_start, secend)
            interimlen += next_seclen
            end = index - 1
            end_adj = True
        else:
            # seclen += (count * repeat)
            if interimlen:
                seclen += interimlen * repeat
            else:
                seclen += count * repeat
            # seclen += ((interimlen + count) * repeat)
            break

    # seclen += (next_seclen * repeat)

    if end_adj:
        index = end + 1
    else:
        index = end + 1 + count
    # index = end + 1

    return seclen, index


def parse2(line: str, *, verbose: bool=False) -> int:
    '''
    Optimized for fast, recursive calculations

    Examples:
    (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated 241,920 times.
    (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.

    ### Need to think through algorithmically:
    * For each step, what are the possibilities?
    * How do you deal with each one?
    '''
    outlen = 0
    index = 0
    while index < len(line):
        start = line.find('(', index)
        if start >= 0:
            outlen += len(line[index:start])
            seclen, index = section_len(line, start)
            outlen += seclen
        else:
            outlen += len(line[index:])
            break

    return outlen


def section_len2(line: str) -> int:
    '''
    Examples:
    (20x12)(13x14)(7x10)(1x12)A
    (3x3)ABC(2x3)XY(5x2)PQRST
    '''
    seclen = 0
    index = len(line) - 1
    while index >= 0:
        end = line.rfind(')', None, index + 1)
        if end >= 0:
            start = line.rfind('(', None, end)
            count, repeat = [int(n) for n in line[start + 1:end].split('x')]

            remaining = len(line[end + 1:index + 1])
            if count > remaining and count > seclen:
                raise ValueError(f'For section "{line}", count of {count} goes past '
                                 'end of section.')
            elif count < remaining:
                raise ValueError(f'For section "{line}", count of {count} is less '
                                 'than remaining part of section.')

            seclen += count * repeat
            index = start - 1
        else:
            seclen += len(line[:index + 1])
            break

    return seclen


def parse3(line: str) -> int:
    '''
    Optimized for fast, recursive calculations

    Examples:
    (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated 241,920 times.
    (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.
    '''
    # When backtracking - have to figure out if previous parenthetical pair includes pair to
    # right (*) or not (+) and calculate accordingly.
    outlen = 0
    index = 0
    while index < len(line):
        start = line.find('(', index)
        if start >= 0:
            end = line.find(')', start)
            count, repeat = [int(n) for n in line[start + 1:end].split('x')]

            outlen += len(line[index:start])
            seclen = section_len2(line[end + 1:end + 1 + count])
            outlen += seclen * repeat
            index = end + 1 + count
        else:
            outlen += len(line[index:])
            break

    return outlen


def main() -> None:
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        for line in infile:
            # Part 1:
            # res = parse(line.strip())
            #
            # Part 2:
            ### Too slow - need alternate approach.  Maybe just find markers and
            ### calculate number of characters?
            # res = parse(line.strip(), recursive=True, verbose=True)
            # print(f'Decompressed "{altrepr(line.strip())}" to "{altrepr(res[0])}", length is {res[1]:,}')
            # res = parse2(line.strip(), verbose=True)
            # print(f'Decompressed "{altrepr(line.strip())}", length is {res:,}')
            res = parse3(line.strip())
            print(f'Decompressed "{altrepr(line.strip())}", length is {res:,}')


if __name__ == '__main__':
    main()
