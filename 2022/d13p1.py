#! /usr/bin/env python3


'''
Distress Signal:
* Receive list of out-of-order packets (part 1 input)
* Identify how many pairs of packets in right order
'''


# INFILE = 'd13p1t1.txt'
# INFILE = r'\working\github\sockduct\aoc\2022\d13p1t1.txt'
# INFILE = 'd13p1.txt'
INFILE = r'\working\github\sockduct\aoc\2022\d13p1.txt'


from collections import deque
from functools import cmp_to_key
from itertools import zip_longest
from pprint import pprint


def getnext(deck):
    digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

    if not deck:
        return

    val = deck.popleft()
    if val in digits:
        while True:
            if deck[0] in digits:
                val += deck.popleft()
            else:
                break

    return val


def compare(left, right):
    ldeck = deque(left)
    rdeck = deque(right)

    while True:
        lval = getnext(ldeck)
        rval = getnext(rdeck)

        if lval is None and rval:
            # Left list ran out first:
            return -1
        elif lval and rval is None:
            # Right list ran out first:
            return 1
        elif lval is None and rval is None:
            # Lists equal
            return 0

        match [lval, rval]:
            case ['[', '[']:
                continue
            case [']', ']']:
                continue
            case [',', ',']:
                continue
            case ['[', ']']:
                # Right list ran out first
                return 1
            case [']', '[']:
                # Left list ran out first
                return -1
            case ['[', rval]:
                rdeck.appendleft(']')
                rdeck.appendleft(rval)
                rval = '['
            case [lval, '[']:
                ldeck.appendleft(']')
                ldeck.appendleft(lval)
                lval = '['
            case [lval, ']']:
                # Right list ran out first:
                return 1
            case [']', rval]:
                # Left list ran out first:
                return -1
            case [lval, rval]:
                lval = int(lval)
                rval = int(rval)
                if lval < rval:
                    return -1
                elif lval > rval:
                    return 1


def main(verbose=False):
    with open(INFILE) as infile:
        lines = infile.readlines()

    num_lines = len(lines)
    count = 0
    inorder_pairs = set()
    divpkt1 = '[[2]]'
    divpkt2 = '[[6]]'
    final_pairs = [divpkt1, divpkt2]
    i = 0
    while i < num_lines:
        line1 = lines[i].strip()
        i += 1
        if line1 == '':
            continue
        if i >= num_lines:
            raise ValueError('Expecting another line.')
        line2 = lines[i].strip()
        i += 1
        if line2 == '':
            raise ValueError('Expecting another line.')
        count += 1

        # Process line1 and line 2
        if (res := compare(line1, line2)) == -1:
            inorder_pairs.add(count)
            final_pairs.extend([line1, line2])
        elif res == 1:
            final_pairs.extend([line2, line1])
        else:
            raise ValueError('Expected lines to be < or >, not equivalent.')

    final_pairs = sorted(final_pairs, key=cmp_to_key(compare))
    divpkt1_index = final_pairs.index(divpkt1) + 1
    divpkt2_index = final_pairs.index(divpkt2) + 1
    decoder_key = divpkt1_index * divpkt2_index

    if verbose:
        pprint(final_pairs)

    print(f'\nPart 1 - in order pairs: {inorder_pairs}, sum: {sum(inorder_pairs):,}.')
    print(f'Part 2 - the decoder key = divider packet 1 index ({divpkt1_index}) * '
          f'divider packet 2 index ({divpkt2_index}) => {decoder_key:,}\n')


if __name__ == '__main__':
    main()
