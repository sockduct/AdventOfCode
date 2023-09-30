#! /usr/bin/env python3


'''
Increment passwords

Password rules - see compliant function

Incrementing passwords:
* xx => xy => xz => ya => yb => ...
'''


INFILE = 'd11.txt'


# Libraries
from collections import deque
from itertools import pairwise
from string import ascii_lowercase


def increment(password):
    pos = -1

    while True:
        cur_char = password[pos]
        next_char = chr(ord(password[pos]) + 1)
        if next_char in ascii_lowercase:
            password[pos] = next_char
            break
        else:
            password[pos] = 'a'
            pos -= 1

    return password


def compliant(password, verbose=False):
    '''
    0) must be exactly eight lowercase letters
    1) must include one increasing straight of at least three letters, like abc,
       bcd, cde, and so on, up to xyz; they cannot skip letters - abd doesn't count
    2) may not contain the letters i, o, or l
    3) must contain at least two different, non-overlapping pairs of letters, like
       aa, bb, or zz
    '''
    if len(password) != 8:
        if verbose:
            print(f'Length of password != 8 ({len(password)})')
        return False

    valid = any(
        (
            ord(password[i]) + 1 == ord(password[i + 1])
            and ord(password[i + 1]) + 1 == ord(password[i + 2])
        )
        for i in range(6)
    )

    if not valid:
        if verbose:
            print(f'Failed test 1 - no 3 letter straight ({password})')
        return False

    # Test 2:
    banned = {'i', 'o', 'l'}
    if banned & set(password):
        # valid = False
        if verbose:
            print(f'Failed test 2 - contains "i", "o", and/or "l" ({password})')
        return False
    else:
        valid = True

    # Test 3:
    matches = 0
    last_match = -2
    for i, (l1, l2) in enumerate(pairwise(password)):
        if l1 == l2 and i > last_match + 1:
            matches += 1
            last_match = i

    if matches >= 2:
        valid = True
    else:
        valid = False
        if verbose:
            print('Failed test 3 - doesn\'t contain at least two non-overlapping '
                  f'pairs ({password})')

    return valid


def main(verbose=False):
    '''
    Test values:
    'hijklmmn' - 1st OK, 2nd fails
    'abbceffg' - 1st fails, 3rd OK
    'abbcegjk' - 3rd fails
    'abcdefgh' - next is 'abcdffaa'
    'ghijklmn' - next is 'ghjaabcc'
    '''
    # line = 'aaaaaaaa'
    # line = 'abcdefgh'
    # line = 'ghijklmn'
    # line = 'hxbxwxba'
    line = 'hxbxxyzz'

    password = deque(line)
    if verbose:
        print(f'Starting password:  {"".join(password)}')
    valid = False
    while not valid:
        res = increment(password)
        if verbose:
            print(f' Current password:  {"".join(password)}')
        valid = compliant(password, verbose)

    print(f'Resulting password:  {"".join(res)}')


if __name__ == '__main__':
    main()
