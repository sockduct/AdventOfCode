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


# Libraries:
from pathlib import Path
from reprlib import repr as altrepr


# Module:
def parse(line: str, *, recursive: bool=False) -> tuple[str, int]:
    output = ''
    index = 0
    while index < len(line):
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
        else:
            output += line[index:]
            break

    return output, len(output)


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
            res = parse(line.strip(), recursive=True)
            print(f'Decompressed "{altrepr(line.strip())}" to "{altrepr(res[0])}", length is {res[1]:,}')


if __name__ == '__main__':
    main()
