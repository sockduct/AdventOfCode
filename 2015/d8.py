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


# Libraries:
from dataclasses import dataclass
from pathlib import Path
from string import ascii_lowercase


# Types:
@dataclass
class Charcnt:
    code: int = 0
    mem: int = 0


def process(line, counter):
    counter.code += len(line)
    string = line.strip('"')
    entity = None
    char_count = 0
    hex_esc = False
    for char in string:
        if char in ascii_lowercase:
            char_count += 1
        elif char == '"':
            char_count += 1
        elif hex_esc:
            if len(entity) == 4:
                char_count += 1
                entity = None
                hex_esc = False
        elif entity:
            entity += char
            if entity == '\\\\':
                char_count += 1
                entity = None
            elif entity == '\\x':
                hex_esc = True
        else:
            entity = char

    counter.mem += char_count


def main():
    parent_dir = Path(__file__).parent
    counter = Charcnt()
    with open(parent_dir/INFILE) as infile:
        for line in infile:
            process(line.strip(), counter)

    print(f'In-code = {counter.code}\nIn-memory =  {counter.mem}\n'
          f'Difference = {counter.code - counter.mem}')


if __name__ == '__main__':
    main()
