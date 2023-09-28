#! /usr/bin/env python3


'''
Increment passwords

Password rules:
* must be exactly eight lowercase letters
* must include one increasing straight of at least three letters, like abc, bcd,
  cde, and so on, up to xyz; they cannot skip letters - abd doesn't count
* may not contain the letters i, o, or l
* must contain at least two different, non-overlapping pairs of letters, like
  aa, bb, or zz

Incrementing passwords:
* xx => xy => xz => ya => yb => ...
'''


INFILE = 'd11.txt'


# Libraries
from collections import deque
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


def main(verbose=True):
    '''
    Test values:
    'hijklmmn' - 1st OK, 2nd fails
    'abbceffg' - 1st fails, 3rd OK
    'abbcegjk' - 3rd fails
    'abcdefgh' - next is 'abcdffaa'
    'ghijklmn' - next is 'ghjaabcc'
    '''
    # line = 'hxbxwxba'
    # line = 'aaaaaaaa'
    line = 'abcdefgh'

    password = deque(line)
    if verbose:
        print(f'Starting password:  {"".join(password)}')
    for _ in range(50):
        res = increment(password)
        if verbose:
            print(f' Current password:  {"".join(password)}')


if __name__ == '__main__':
    main()
