#! /usr/bin/env python3.10


INFILE = 'd18p1t1.txt'
# INFILE = 'd18p1.txt'


import json
from pprint import pprint


class SnailfishNumber():
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return f'<SnailfishNumber({self.number})>'

    def __str__(self):
        return f'{self.number}'

    def __add__(self, other):
        number = SnailfishNumber([self.number, other.number])
        number._reduce()
        return number

    def __iadd__(self, other):
        self.number = [self.number, other.number]
        self._reduce()
        return self

    def _reduce(self):
        '''
        Repeatedly:
        1) If any pair is nested inside four pairs, the leftmost such pair explodes.
        2) If any regular number is 10 or greater, the leftmost such regular number splits.
        3) If neither of the above apply, the number is reduced.
        Note:  For (1) and (2) only one such action occurs before starting at 1 again.  e.g., if
               there are no explodes and two splits, only one split occurs before checking for an
               explode again.

        To explode a pair, the pair's left value is added to the first regular number to the
        left of the exploding pair (if any), and the pair's right value is added to the first
        regular number to the right of the exploding pair (if any). Exploding pairs will always
        consist of two regular numbers. Then, the entire exploding pair is replaced with the
        regular number 0.

        To split a regular number, replace it with a pair; the left element of the pair should
        be the regular number divided by two and rounded down, while the right element of the
        pair should be the regular number divided by two and rounded up. For example, 10 becomes
        [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.

        '''
        # Build out explode procedure...
        ...


def main():
    pairs = [
        [[[[[[9,8],1],2],3],4], [[[[0,9],2],3],4]],
        [[7,[6,[5,[4,[3,2]]]]], [7,[6,[5,[7,0]]]]],
        [[[6,[5,[4,[3,2]]]],1], [[6,[5,[7,0]]],3]],
        [[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]],
        [[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[7,0]]]]],
    ]

    for number, answer in pairs:
        assert SnailfishNumber(number)._reduce().number == answer

    '''
    numbers = []
    with open(INFILE) as infile:
        numbers.extend(json.loads(line) for line in infile)

    pprint(numbers)
    res = None
    for number in numbers:
        if res:
            print(res)
            res += SnailfishNumber(number)
        else:
            res = SnailfishNumber(number)

    print(f'Result:  {res}')
    '''


if __name__ == '__main__':
    main()
