#! /usr/bin/env python3.10


# INFILE = 'd18p1t1.txt'
INFILE = 'd18p1.txt'


# Standard Library
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
    '''
    # Test exploding:
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

    '''
    # Test exploding and splitting:
    sn1 = SnailfishNumber([[[[4,3],4],4],[7,[[8,4],9]]])
    sn2 = SnailfishNumber([1,1])
    sn3 = sn1 + sn2
    print(f'Result:  {sn3}')
    '''

    '''
    # Test adding up lists:
    l1 = [[1,1], [2,2], [3,3], [4,4]]
    l2 = [[1,1], [2,2], [3,3], [4,4], [5,5]]
    l3 = [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6]]
    l4 = [[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
          [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
          [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
          [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
          [7,[5,[[3,8],[1,4]]]],
          [[2,[2,2]],[8,[8,1]]],
          [2,9],
          [1,[[[9,3],9],[[9,0],[0,7]]]],
          [[[5,[7,4]],7],1],
          [[[[4,2],2],6],[8,7]]]
    sn = None
    for n in l4:
        if not sn:
            sn = SnailfishNumber(n)
        else:
            sn += SnailfishNumber(n)
    print(f'Result:  {sn}')
    '''

    '''
    # Test magnitude:
    l1 = [[9,1], [1,9], [[9,1], [1,9]], [[1,2],[[3,4],5]]]
    l2 = [[[[[0,7],4],[[7,8],[6,0]]],[8,1]],
          [[[[1,1],[2,2]],[3,3]],[4,4]],
          [[[[3,0],[5,3]],[4,4]],[5,5]],
          [[[[5,0],[7,4]],[5,5]],[6,6]],
          [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]]
    for n in l2:
        print(f'Magnitude of {n} is {SnailfishNumber(n).magnitude()}')
    '''

    '''
    # Everything:
    l1 = [[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
          [[[5,[2,8]],4],[5,[[9,9],0]]],
          [6,[[[6,2],[5,6]],[[7,6],[4,7]]]],
          [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]],
          [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]],
          [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]],
          [[[[5,4],[7,7]],8],[[8,3],8]],
          [[9,3],[[9,9],[6,[4,9]]]],
          [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
          [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]]
    sn = None
    for n in l1:
        if not sn:
            sn = SnailfishNumber(n)
        else:
            sn += SnailfishNumber(n)
    print(f'Magnitude of {sn} is {sn.magnitude()}')
    '''

    numbers = []
    with open(INFILE) as infile:
        numbers.extend(json.loads(line) for line in infile)

    # pprint(numbers)
    res = None
    for number in numbers:
        if not res:
            res = SnailfishNumber(number)
        else:
            res += SnailfishNumber(number)

    print(f'Magnitude of {res} is {res.magnitude()}')


if __name__ == '__main__':
    main()
