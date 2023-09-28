#! /usr/bin/env python3


'''
Look-and-say sequences are generated iteratively, using the previous value as
input for the next step.
 * For each step, take the previous value, and replace each run of digits
   (like 111) with the number of digits (3) followed by the digit itself (1).
 * Starting with the digits in your puzzle input, apply this process 40 times.
   What is the length of the result?
'''


INFILE = 'd10.txt'


# Libraries
from collections import deque
from pathlib import Path
import re


def parse(line):
    new_digit = ''
    while len(line) > 0:
        digit = line[0]
        number = len(re.match(f'{line[0]}+', line).group())
        new_digit += f'{number}{digit}'
        line = line[number:]

    return new_digit


def parse2(line):
    '''
    For each step, take the previous value, and replace each run of digits
    (like 111) with the number of digits (3) followed by the digit itself (1).

    Cases:
    * last and current match:
        * increment count, continue
    * last and current don't match
        * build out new_number, update last_digit and digit_count
    * On each pass, check if line empty
        * Yes then build out new_number from final data
    '''
    new_number = deque()
    last_digit = line.popleft()
    digit_count = 1
    while line:
        digit = line.popleft()
        # Continuous run?
        if last_digit == digit:
            digit_count += 1
        # No - new run:
        else:
            new_number.extend((str(digit_count), last_digit))
            last_digit = digit
            digit_count = 1

        # Empty?
        if not line:
            new_number.extend((str(digit_count), last_digit))

    # Edge case where line consists of single number
    if not new_number:
        new_number.extend((str(digit_count), last_digit))

    return new_number


def main(verbose=False):
    with open(Path(__file__).parent/INFILE) as infile:
        line = infile.read().strip()

    # Test cases:
    # line = '1321131112'
    # line = '1'
    # line = '11'

    line2 = deque(line)
    count = 50

    if verbose:
        # print(f'Starting with:  {line}')
        print(f'Starting with:  {line2}')
    for i in range(1, count + 1):
        # res = parse(line)
        res2 = parse2(line2)
        if verbose:
            # print(f'{i:>2}) Transformed to:  {res}')
            print(f'{i:>2}) Transformed to:  {res2}')
        if i >= 35:
            # print(f'Count:  {i},  Current length:  {len(res):,},  {len(res2):,}')
            print(f'Count:  {i},  Current length:  {len(res2):,}')

        # line = res
        line2 = res2

    # print(f'Length after {count} transforms:  {len(res):,}')
    print(f'Length after {count} transforms:  {len(res2):,}')


if __name__ == '__main__':
    main()
