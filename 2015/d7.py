#! /usr/bin/env python3


'''
Bitwise logic for 16-bt signal
* Parse input and determine all wire (lower case letters) values
'''


# INFILE = 'd7.txt'
# Change value of wire b to result from part 1:
INFILE = 'd72.txt'
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


def evalexpr(wires, wirevals, expr):
    # Check for NOT expression (only unary operator):
    if len(expr) == 2:
        op, uexpr = expr
        if op != 'NOT':
            raise ValueError(f'Expected "NOT", got:  {op}')

        if isinstance(uexpr, int):
            return MAXVAL + ~val
        elif isinstance(uexpr, str):
            return MAXVAL + ~getwireval(wires, wirevals, uexpr)
        else:
            return MAXVAL + ~evalexpr(wires, wirevals, uexpr)
    # Check for binary expression:
    else:
        lexpr, op, rexpr = expr
        if isinstance(lexpr, list):
            lexpr = evalexpr(wires, wirevals, lexpr)
        elif isinstance(lexpr, str):
            lexpr = getwireval(wires, wirevals, lexpr)
        if isinstance(rexpr, list):
            rexpr = evalexpr(wires, wirevals, rexpr)
        elif isinstance(rexpr, str):
            rexpr = getwireval(wires, wirevals, rexpr)

        match op:
            case 'AND':
                return lexpr & rexpr
            case 'OR':
                return lexpr | rexpr
            case 'LSHIFT':
                return lexpr << rexpr
            case 'RSHIFT':
                return lexpr >> rexpr
            case _:
                raise ValueError(f'Expected operator of AND|OR|LSHIFT|RSHIFT, got "{op}"')


def getwireval(wires, wirevals, wire, verbose=False):
    '''
    Recursively parse wires dict to calculate end value for wire passed in
    wireval

    Cases:
    1) wire = integer
    2) wire = [<expr>]
        2a) <expr> = NOT, wire
        2b) <expr> = lvalue, BINOP, rvalue
            2bi) xvalue = integer|wire

    Bitwise Operators:
    * NOT
    * AND
    * OR
    * LSHIFT
    * RSHIFT
    '''
    # Do we have wireval?
    if wire in wirevals:
        return wirevals[wire]

    wirevals[wire] = evalexpr(wires, wirevals, wires[wire])

    return wirevals[wire]


def main(verbose=False):
    # Can't use None for defaultdict, must use a callable for it to work as
    # desired:
    wires = defaultdict(lambda: None)
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line.strip(), wires)

    # Store resulting wire values:
    wirevals = {k: v for k, v in wires.items() if isinstance(v, int)}

    wire = 'a'
    res = getwireval(wires, wirevals, wire)
    print(f'Value for wire {wire}:  {res}')

    '''
    # Part 2 - Reset wire 'b' to result from part 1 and recalculate wire 'a':
    wires['b'] = res
    # Reset wirevals:
    wirevals = {k: v for k, v in wires.items() if isinstance(v, int)}
    res = getwireval(wires, wirevals, wire)
    print(f'Part 2, Value for wire {wire}:  {res}')
    '''

    # Debugging:
    # pprint(wires)


if __name__ == '__main__':
    main()
