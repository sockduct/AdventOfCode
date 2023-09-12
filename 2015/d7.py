#! /usr/bin/env python3


'''
Bitwise logic for 16-bt signal
* Parse input and determine all wire (lower case letters) values
'''


# INFILE = 'd7.txt'
INFILE = 'd7t1.txt'

MAXVAL = 2**16


# Libraries
from collections import defaultdict
from copy import deepcopy
from pprint import pprint


def isnum(wire):
    try:
        val = int(wire)
    except ValueError:
        val = None

    return val


def parse(line, wires, values):
    '''
    Bitwise Operators:
    * NOT
    * AND
    * OR
    * LSHIFT
    * RSHIFT
    '''
    match line.split():
        case [inval, '->', outline]:
            # Can we get a number?
            if (val := isnum(inval)) or (val := values[inval]) or (val := isnum(wires[inval])):
                wires[outline] = val
            # Is there an expression present?
            elif wires[inval]:
                wires[outline] = deepcopy(wires[inval])
            # Wire assignment:
            else:
                wires[outline] = inval
        case ['NOT', inval, '->', outline]:
            wires[outline] = MAXVAL + ~wires[inval]
        case [inval1, 'AND', inval2, '->', outline]:
            wires[outline] = wires[inval1] & wires[inval2]
        case [inval1, 'OR', inval2, '->', outline]:
            wires[outline] = wires[inval1] | wires[inval2]
        case [inval, 'LSHIFT', val, '->', outline]:
            wires[outline] = wires[inval] << int(val)
        case [inval, 'RSHIFT', val, '->', outline]:
            wires[outline] = wires[inval] >> int(val)
        case _:
            raise ValueError(f'Unexpected sequence:  {line}')


def main():
    # Can't use None for defaultdict, must use a callable for it to work as
    # desired:
    values = defaultdict(lambda: None)
    wires = defaultdict(lambda: None)
    with open(INFILE) as infile:
        for line in infile:
            parse(line.strip(), wires, values)

    pprint(wires)


if __name__ == '__main__':
    main()
