#! /usr/bin/env python 3


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
import re


def parse(line):
    new_digit = ''
    while len(line) > 0:
        digit = line[0]
        number = len(re.match(f'{line[0]}+', line).group())
        new_digit += f'{number}{digit}'
        line = line[number:]

    return new_digit


def main(verbose=False):
    with open(INFILE) as infile:
        line = infile.read().strip()

    # line = '1321131112'
    # line = '1'
    count = 40

    if verbose:
        print(f'Starting with:  {line}')
    for i in range(1, count + 1):
        res = parse(line)
        if verbose:
            print(f'{i:>2}) Transformed to:  {res}')

        line = res

    print(f'Length after {count} transforms:  {len(res)}')


if __name__ == '__main__':
    main()
