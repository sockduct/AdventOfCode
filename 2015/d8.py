#! /usr/bin/env python3


'''
Calculate difference between:
* The in-code representation of the string literal (how many characters)
* The in-memory string instance (how many characters)
* e.g., "" - 2 character string literal with 0 characters in-memory

Input list is a file that contains many double-quoted string literals, one on
each line.

The only escape sequences used are:
* '\' + '\' - represents a single backslash
* '\' + '"' - represents a lone double-quote character
* '\' + 'x' - hex escape plus two hexadecimal characters (represents a single
              character with that ASCII code)
'''


INFILE = 'd8.txt'
# INFILE = 'd8t1.txt'
#
# "ASCII" values for characters:
LOWER_A = 97
LOWER_Z = 122
BACKSLASH = 92
QUOTE = 34
LOWER_X = 120
LOWERCASE = range(LOWER_A, LOWER_Z + 1)


# Libraries:
from dataclasses import dataclass
from pathlib import Path
import re
from string import ascii_lowercase


# Types:
@dataclass
class Charcnt:
    encode: int = 0
    code: int = 0
    mem: int = 0
    remem: int = 0
    bs: int = 0
    dq: int = 0
    he: int = 0


def recount(line, counter):
    re1 = br'\\\\'
    re2 = b'"'
    # Does't work in Python
    # * '\\' + 'x' doesn't match <backslash> + x
    # * <backslash> + xHH is always interpreted as single character, can't split
    #   it up
    # * e.g., doesn't work:  re3 = r'\\x[0-9a-f]{2}'
    # * e.g., doesn't work:  re3 = r'<backslash>x[0-9a-f]{2}'
    #
    # Note:  This only works when read file in as binary file
    re3 = b'\\' + b'x'
    res = line
    for pattern in (re1, re2, re3):
        res = re.sub(pattern, '', res)

    counter.remem += len(res)


def parse(line, counter):
    '''
    PowerShell
    * Count occurrences of '\\' (d8.txt = 111):
        (sls '\\\\' -allmatches d8.txt).matches.count
    * Count occurrences of '\"' (d8.txt = 275 w/o striping edges quotes,
      otherwise 270):
        (sls '\\"' -allmatches d8.txt).matches.count
    * Count occurrences of <backslash> + 'xHH' (d8.txt = 123):
        (sls '\\' + 'x[0-9a-f]{2}' -allmatches d8.txt).matches.count
        Note:  Have to separate backslashes and x or Python tries to interpret
               as hex-escape!
    '''
    counter.code += len(line)
    # Strip quotes:
    # string = line.strip('"')
    string = line[1:-1]
    entity = []
    for index, char in enumerate(string):
        # For debugging only:
        curchar = chr(char)
        curindex = index
        # if char in ascii_lowercase:
        if not entity and char in LOWERCASE:
            counter.mem += 1
        elif entity:
            entity.append(char)
            if entity == [BACKSLASH, BACKSLASH]:
                counter.mem += 1
                counter.bs += 1
                entity.clear()
            elif entity == [BACKSLASH, QUOTE]:
                counter.mem += 1
                counter.dq += 1
                entity.clear()
            elif entity[:2] == [BACKSLASH, LOWER_X] and len(entity) == 4:
                counter.mem += 1
                counter.he += 1
                entity.clear()
        else:
            entity.append(char)


def build(line, counter):
    entity = []
    binarray = bytearray()
    for index, char in enumerate(line):
        # For debugging only:
        curchar = chr(char)
        curindex = index
        if not entity and char in LOWERCASE:
            binarray.append(char)
        else:
            entity.append(char)
            if entity == [QUOTE]:
                binarray.extend((BACKSLASH, QUOTE))
                entity.clear()
            elif entity == [BACKSLASH, BACKSLASH]:
                binarray.extend(entity)
                binarray.extend(entity)
                entity.clear()
            elif entity == [BACKSLASH, QUOTE]:
                binarray.extend((BACKSLASH, BACKSLASH))
                binarray.extend(entity)
                entity.clear()
            elif entity[:2] == [BACKSLASH, LOWER_X] and len(entity) == 4:
                binarray.append(BACKSLASH)
                binarray.extend(entity)
                entity.clear()

    binarray.insert(0, QUOTE)
    binarray.append(QUOTE)
    counter.encode += len(binarray)


def main():
    parent_dir = Path(__file__).parent
    counter = Charcnt()
    with open(parent_dir/INFILE, mode='rb') as infile:
        for line in infile:
            line = line.strip()
            parse(line, counter)
            build(line, counter)

    print(f'In-code = {counter.code}\nBackslashes = {counter.bs}\n'
          f'Double-quotes = {counter.dq}\nHex-escapes = {counter.he}\n'
          f'In-memory =  {counter.mem}\nDifference-1 = {counter.code - counter.mem}\n'
          f'Encoded = {counter.encode}\nDifference-2 = {counter.encode - counter.code}')


if __name__ == '__main__':
    main()
