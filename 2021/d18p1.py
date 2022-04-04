#! /usr/bin/env python3.10


INFILE = 'd18p1t1.txt'
# INFILE = 'd18p1.txt'


# Standard Library
import json
from pprint import pprint
import re


# Local:
from positional_list import PositionalList


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

    def _explode(self, poslist):
        '''
        Explode SnailfishNumber:
        To explode a pair, the pair's left value is added to the first regular number to the
        left of the exploding pair (if any), and the pair's right value is added to the first
        regular number to the right of the exploding pair (if any). Exploding pairs will always
        consist of two regular numbers. Then, the entire exploding pair is replaced with the
        regular number 0.
        '''
        cur = poslist.first()
        prev = None
        depth = 0
        explode = False
        while cur:
            match cur.element():
                case '[':
                    depth += 1
                    if depth >= 5 and not explode:
                        explode = True
                case ']':
                    depth -= 1
                case num if isinstance(num, int):
                    if explode and prev and isinstance(prev.element(), int):
                        # Look for number to the left:
                        leftval, leftcur = prev.element(), prev
                        prevleft = leftcur
                        while (prevleft := poslist.before(prevleft)):
                            if isinstance((lnum := prevleft.element()), int):
                                leftval += lnum
                                poslist.replace(prevleft, leftval)
                                break
                        poslist.delete(poslist.before(leftcur))
                        poslist.delete(leftcur)

                        # Look for number to the right:
                        rightval, rightcur = num, cur
                        nextright = rightcur
                        while (nextright := poslist.after(nextright)):
                            if isinstance((rnum := nextright.element()), int):
                                rightval += rnum
                                poslist.replace(nextright, rightval)
                                break
                        poslist.delete(poslist.after(rightcur))
                        poslist.replace(rightcur, 0)

                        # Immediately return after each explode
                        # depth -= 1
                        # explode = False
                        break
            prev = cur
            cur = poslist.after(cur)

        return poslist, explode

    def _split(self, poslist):
        '''
        Split SnailfishNumber:
        To split a regular number, replace it with a pair; the left element of the pair should
        be the regular number divided by two and rounded down, while the right element of the
        pair should be the regular number divided by two and rounded up. For example, 10 becomes
        [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
        '''
        ### To implement...
        cur = poslist.first()
        prev = None
        split = False
        while cur:
            match cur.element():
                case '[':
                    ...
                case ']':
                    ...
                case num if isinstance(num, int):
                    if split and prev and isinstance(prev.element(), int):
                        # Look for number to the left:
                        leftval, leftcur = prev.element(), prev
                        prevleft = leftcur
                        while (prevleft := poslist.before(prevleft)):
                            if isinstance((lnum := prevleft.element()), int):
                                leftval += lnum
                                poslist.replace(prevleft, leftval)
                                break
                        poslist.delete(poslist.before(leftcur))
                        poslist.delete(leftcur)

                        # Look for number to the right:
                        rightval, rightcur = num, cur
                        nextright = rightcur
                        while (nextright := poslist.after(nextright)):
                            if isinstance((rnum := nextright.element()), int):
                                rightval += rnum
                                poslist.replace(nextright, rightval)
                                break
                        poslist.delete(poslist.after(rightcur))
                        poslist.replace(rightcur, 0)

                        # Immediately return after each split
                        # split = False
                        break
            prev = cur
            cur = poslist.after(cur)

        return poslist, split

    def _reduce(self):
        '''
        Repeatedly:
        1) If any pair is nested inside four pairs, the leftmost such pair explodes.
        2) If any regular number is 10 or greater, the leftmost such regular number splits.
        3) If neither of the above apply, the number is reduced.
        Note:  For (1) and (2) only one such action occurs before starting at 1 again.  e.g., if
               there are no explodes and two splits, only one split occurs before checking for an
               explode again.

        *** Next Steps
        Leverage positional list ADT from Python DSA book for the task below:
        '''
        explode = True
        split = True
        poslist = self._poslist()

        # while explode or split:
        poslist, explode = self._explode(poslist)
            # poslist, split = self._split(poslist)

        self.number = json.loads(poslist.to_json())
        return self.number

    def _poslist(self):
        poslist = PositionalList()
        numstr = str(self.number)
        while (res := re.match(r'(\[|\]|\d+|,) *', numstr)):
            match res.group(1):
                case '[':
                    poslist.add_last('[')
                case ']':
                    poslist.add_last(']')
                case num if num[0] in '0123456789':
                    poslist.add_last(int(num))
                case ',':
                    pass
                case _:
                    raise ValueError(f"Unexpected value:  ``{res}''")
            numstr = numstr[len(res.group()):]
            if not res:
                break
        print(f'Positional List:  {poslist}')

        return poslist


def main():
    pairs = [
        [[[[[[9,8],1],2],3],4], [[[[0,9],2],3],4]],
        [[7,[6,[5,[4,[3,2]]]]], [7,[6,[5,[7,0]]]]],
        [[[6,[5,[4,[3,2]]]],1], [[6,[5,[7,0]]],3]],
        [[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]],
        [[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[7,0]]]]],
    ]

    for number, answer in pairs:
        print(f'Input:  {number},  Expected output:  {answer}')
        assert (num_reduced := SnailfishNumber(number)._reduce()) == answer, (
               f'{num_reduced} != {answer}')
        print('Success - next number...\n')

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
