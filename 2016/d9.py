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
INFILE = 'd9t1.txt'


# Libraries:
from pathlib import Path
from reprlib import repr as altrepr


# Module:
def parse(line: str) -> tuple[str, int]:
    output = ''
    index = 0
    while index < len(line):
        start = line.find('(', index)
        if start >= 0:
            end = line.find(')', start)
            output += line[index:start]
            count, repeat = [int(n) for n in line[start + 1:end].split('x')]
            output += line[end + 1:end + 1 + count] * repeat
            index += end + 1 + count
        else:
            output += line[index:]
            break

    return output, len(output)


def main() -> None:
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        for line in infile:
            res = parse(line.strip())
            print(f'Decompressed "{altrepr(line.strip())}" to "{altrepr(res[0])}", length is {res[1]:,}')


if __name__ == '__main__':
    main()
