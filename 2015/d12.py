#! /usr/bin/env python3


'''
'''


INFILE = 'd12.txt'
# INFILE = 'd12t1.txt'
# INFILE = 'd12t2.txt'


# Libraries:
import json
from pathlib import Path


def parse(data, red_check=False):
    '''
    Top level:
    * if list parse elements
    * elif dict parse values
    * else error

    For each element/value:
    * if list/dict, recursively parse
    * elif int accrue
    * elif non-int ignore
    '''
    res = 0

    if isinstance(data, list):
        for element in data:
            if isinstance(element, (list, dict)):
                res += parse(element, red_check)
            elif isinstance(element, int):
                res += element
            # else ignore non-ints...
    elif isinstance(data, dict):
        if red_check and 'red' in data.values():
            return res
        for element in data.values():
            if isinstance(element, (list, dict)):
                res += parse(element, red_check)
            elif isinstance(element, int):
                res += element
            # else ignore non-ints...
    else:
        raise ValueError(f'Expected list|dict, got:  {type(data)}')

    return res


def main():
    with open(Path(__file__).parent/INFILE) as infile:
        data = json.load(infile)

    # res = parse(data)
    res = parse(data, red_check=True)
    print(f'Result:  {res:,}')


if __name__ == '__main__':
    main()
