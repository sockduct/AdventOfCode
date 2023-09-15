#! /usr/bin/env python3


'''
Bitwise logic for 16-bt signal
* Parse input and determine all wire (lower case letters) values
'''


INFILE = 'd7.txt'
# INFILE = 'd7t1.txt'

MAXVAL = 2**16


# Libraries
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from pprint import pprint


def isnum(wire):
    try:
        val = int(wire)
    except (TypeError, ValueError):
        val = None

    return val


def gettype(val, wires):
    # Can we get a number?
    # Edge case - 0 is a number but not "truthy", add check for is not None:
    if ((res := isnum(val)) or res is not None or
            (res := isnum(wires[val])) or res is not None):
        return res
    # Is there an expression present?
    elif wires[val]:
        return deepcopy(wires[val])
    # Wire assignment:
    else:
        return val


def binop(lval, rval, wires):
    val1 = gettype(lval, wires)
    val2 = gettype(rval, wires)
    status = isinstance(val1, int) and isinstance(val2, int)

    return status, val1, val2


def parse(line, wires):
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
            if wires.get(outline):
                raise ValueError(f'wire {outline} already has value {wires[outline]}')
            wires[outline] = gettype(inval, wires)
        case ['NOT', inval, '->', outline]:
            val = gettype(inval, wires)
            if wires.get(outline):
                raise ValueError(f'wire {outline} already has value {wires[outline]}')
            wires[outline] = (
                MAXVAL + ~val if isinstance(val, int) else ['NOT', val]
            )
        case [lval, 'AND', rval, '->', outline]:
            status, val1, val2 = binop(lval, rval, wires)
            if wires.get(outline):
                raise ValueError(f'wire {outline} already has value {wires[outline]}')
            wires[outline] = val1 & val2 if status else [val1, 'AND', val2]
        case [lval, 'OR', rval, '->', outline]:
            status, val1, val2 = binop(lval, rval, wires)
            if wires.get(outline):
                raise ValueError(f'wire {outline} already has value {wires[outline]}')
            wires[outline] = val1 | val2 if status else [val1, 'OR', val2]
        case [lval, 'LSHIFT', rval, '->', outline]:
            status, val1, val2 = binop(lval, rval, wires)
            if wires.get(outline):
                raise ValueError(f'wire {outline} already has value {wires[outline]}')
            wires[outline] = val1 << val2 if status else [val1, 'LSHIFT', val2]
        case [lval, 'RSHIFT', rval, '->', outline]:
            status, val1, val2 = binop(lval, rval, wires)
            if wires.get(outline):
                raise ValueError(f'wire {outline} already has value {wires[outline]}')
            wires[outline] = val1 >> val2 if status else [val1, 'RSHIFT', val2]
        case _:
            raise ValueError(f'Unexpected sequence:  {line}')


def getwireval(wires, wireval):
    '''
    Recursively parse wires dict to calculate end value for wire passed in
    wireval
    '''
    ...


def main():
    # Can't use None for defaultdict, must use a callable for it to work as
    # desired:
    wires = defaultdict(lambda: None)
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line.strip(), wires)

    wireval = 'a'
    res = getwireval(wires, wireval)
    print(f'Value for wire {wireval}:  {res}')
    # pprint(wires)


if __name__ == '__main__':
    main()
