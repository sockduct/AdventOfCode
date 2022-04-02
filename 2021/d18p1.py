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

        *** Next Steps
        Leverage positional list ADT from Python DSA book for the task below:
        '''
        # Build out explode procedure...
        poslist = self._poslist()
        cur = poslist.first()
        left_stack = []
        left = True
        depth = 0
        explode = False
        split = False
        while cur:
            match cur.element():
                case '[':
                    depth += 1
                    left = True
                    if depth >= 4 and not explode:
                        explode = True
                        print('Explode next pair!')
                case ']':
                    depth -= 1
                case num if isinstance(num, int):
                    if left:
                        left_stack.append((num, cur))
                        left = False
                    else:
                        if explode:
                            print('Exploding...')
                            leftval, leftcur = left_stack[-1]
                            poslist.delete(poslist.before(leftcur))
                            poslist.delete(leftcur)
                            if len(left_stack) > 1:
                                leftval += left_stack[-2][0]
                                poslist.replace(left_stack[-2][1], leftval)
                            rightval, rightcur = num, cur
                            nextright = rightcur
                            while (nextright := poslist.after(nextright)):
                                if isinstance((rnum := nextright.element()), int):
                                    rightval += rnum
                                    poslist.replace(nextright, rightval)
                                    break
                            poslist.delete(poslist.after(rightcur))
                            poslist.replace(rightcur, 0)

                            explode = False
                case ',':
                    left = False if left else True
            cur = poslist.after(cur)

        print(f'Exploded positional List:  {poslist}')
        self.number = json.loads(poslist.to_json())
        return self.number

    def _poslist(self):
        poslist = PositionalList()
        numstr = str(self.number)
        while (res := re.match(r'(\[|\]|\d+|,) *', numstr)):
            match res.group(1):
                case '[':
                    poslist.add_last('[')
                    '''
                    depth += 1
                    if depth >= 4 and not explode:
                        explode = True
                        print('Explode next pair!')
                    '''
                case ']':
                    poslist.add_last(']')
                    ### depth -= 1
                case num if num[0] in '123456789':
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
