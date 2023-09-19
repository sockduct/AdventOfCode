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
    code: int = 0
    mem: int = 0
    remem: int = 0


def recount(line, counter):
    re1 = r'\\'
    re2 = '"'
    # Does't work - don't know how to make hex escape codes wildcards:
    re3 = r'\\x[0-9a-f]{2}'
    res = line
    for pattern in (re1, re2, re3):
        res = re.sub(pattern, '', res)

    counter.remem += len(res)


def process(line, counter):
    counter.code += len(line)
    # Strip quotes:
    # string = line.strip('"')
    string = line[1:-1]
    entity = []
    char_count = 0
    for char in string:
        # if char in ascii_lowercase:
        if not entity and char in LOWERCASE or char == QUOTE:
            char_count += 1
        elif entity:
            entity.append(char)
            if entity == [BACKSLASH, BACKSLASH]:
                char_count += 1
                entity.clear()
            elif entity[:2] == [BACKSLASH, LOWER_X] and len(entity) == 4:
                char_count += 1
                entity.clear()
        else:
            entity.append(char)

    counter.mem += char_count


def main():
    parent_dir = Path(__file__).parent
    counter = Charcnt()
    with open(parent_dir/INFILE, mode='rb') as infile:
        for line in infile:
            process(line.strip(), counter)

    print(f'In-code = {counter.code}\nIn-memory =  {counter.mem}\n'
          f'Difference = {counter.code - counter.mem}')


if __name__ == '__main__':
    main()
