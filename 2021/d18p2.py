#! /usr/bin/env python3.10


# INFILE = 'd18p1t1.txt'
INFILE = 'd18p1.txt'


# Standard Library
from itertools import permutations
import json
from math import ceil, floor
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
        Explode SnailfishNumber - If any pair is nested inside four pairs, the leftmost such
        pair explodes:

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
        Split SnailfishNumber - If any regular number is 10 or greater, the leftmost such regular
        number splits:

        To split a regular number, replace it with a pair; the left element of the pair should
        be the regular number divided by two and rounded down, while the right element of the
        pair should be the regular number divided by two and rounded up. For example, 10 becomes
        [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
        '''
        cur = poslist.first()
        split = False
        while cur:
            match cur.element():
                case '[' | ']':
                    pass
                case num if isinstance(num, int):
                    if num >= 10:
                        split = True
                        lnum = floor(num/2)
                        rnum = ceil(num/2)
                        poslist.add_before(cur, '[')
                        poslist.replace(cur, lnum)
                        newpos = poslist.add_after(cur, rnum)
                        poslist.add_after(newpos, ']')

                        # Immediately return after each split
                        # split = False
                        break
            cur = poslist.after(cur)

        return poslist, split

    def _reduce(self, verbose=False):
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

        while explode or split:
            poslist, explode = self._explode(poslist)
            if explode:
                if verbose:
                    print(f'After explode, poslist now:  {json.loads(poslist.to_json())}')
                continue
            poslist, split = self._split(poslist)
            if split and verbose:
                print(f'After split, poslist now:  {json.loads(poslist.to_json())}')

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

        return poslist

    def _magnitude(self, poslist):
        '''
        The magnitude of a pair (SnailfishNumber) is 3 times the magnitude of its left
        element plus 2 times the magnitude of its right element. The magnitude of a
        regular number is just that number.

        For example, the magnitude of [9,1] is 3*9 + 2*1 = 29; the magnitude of [1,9]
        is 3*1 + 2*9 = 21. Magnitude calculations are recursive: the magnitude of
        [[9,1],[1,9]] is 3*29 + 2*21 = 129.
        '''
        calc = False
        cur = poslist.first()
        prev = None
        while cur:
            match cur.element():
                case '[' | ']':
                    pass
                case num if isinstance(num, int):
                    if prev and isinstance(prev.element(), int):
                        calc = True
                        lnum = prev.element() * 3
                        rnum = num * 2
                        mnum = lnum + rnum

                        poslist.delete(poslist.before(prev))
                        poslist.delete(poslist.after(cur))
                        poslist.delete(prev)
                        poslist.replace(cur, mnum)

                        # Immediately return after each calculation
                        break
            prev = cur
            cur = poslist.after(cur)

        return poslist, calc

    def magnitude(self, verbose=False):
        '''
        The magnitude of a pair (SnailfishNumber) is 3 times the magnitude of its left
        element plus 2 times the magnitude of its right element. The magnitude of a
        regular number is just that number.

        For example, the magnitude of [9,1] is 3*9 + 2*1 = 29; the magnitude of [1,9]
        is 3*1 + 2*9 = 21. Magnitude calculations are recursive: the magnitude of
        [[9,1],[1,9]] is 3*29 + 2*21 = 129.
        '''
        calc = True
        poslist = self._poslist()

        while calc:
            poslist, calc = self._magnitude(poslist)
            if calc and verbose:
                print(f'After calculation, poslist now:  {json.loads(poslist.to_json())}')

        return poslist.first().element()


def main():
    numbers = []
    with open(INFILE) as infile:
        numbers.extend(SnailfishNumber(json.loads(line)) for line in infile)

    number_permutations = list(permutations(numbers, 2))
    np_addition = []
    np_magnitude = []
    for num_perm in number_permutations:
        np_addition.append((res := num_perm[0] + num_perm[1]))
        np_magnitude.append(res.magnitude())

    max_magnitude = max(np_magnitude)
    max_index = np_magnitude.index(max_magnitude)
    print(f'Largest magnitude is {max_magnitude} from {number_permutations[max_index]} which'
          f' adds to {np_addition[max_index]}.')


if __name__ == '__main__':
    main()
