#! /usr/bin/env python3


'''
Remove decoy data:
* list of room names
* name format:
    * lowercase letters separated by dashes followed by a dash and a sector ID
      (number), and a checksum in square brackets
    * e.g., aaaaa-bbb-z-y-x-123[abxyz]
    * valid name has checksum with 5 most common letters from name, in order,
      with ties broken by alphabetization
'''


INFILE = 'd4.txt'
# INFILE = 'd4t1.txt'


# Libraries
from collections import Counter
from pathlib import Path


# Module
def valid_name(line: str) -> int:
    line = line.strip()

    base, checksum = line.split('[')
    checksum = checksum.strip(']')
    checksum = ''.join(sorted(checksum))

    *name, sid = base.split('-')
    sid = int(sid)
    name = ''.join(name)

    name_let = Counter(sorted(name))
    # Fails: When extract from Counter this way, not ordered by most common
    # occurrence but by insertion order!
    # calc_checksum = ''.join(list(name_let.keys())[:5])
    calc_checksum = ''.join(sorted(k for k, _ in name_let.most_common(5)))

    return sid if calc_checksum == checksum else 0


def main() -> None:
    valid_count = 0
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        for line in infile:
            valid_count += valid_name(line)

    print(f'Sum of valid room\'s sector IDs:  {valid_count:,}')


if __name__ == '__main__':
    main()
