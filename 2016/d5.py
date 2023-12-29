#! /usr/bin/env python3


'''
Find password
* Calculate one character at a time by taking MD5 hash of input and an integer
  index starting from 0 and incrementing
* Take output of above in hex form
* Looking for output with 5 leading zeroes - take 6th character as password
  digit
'''


INFILE = 'd5.txt'
# INFILE = 'd5t1.txt'


# Libraries
from hashlib import md5
from itertools import count
from pathlib import Path


# Module
def get_pass(data: str, use_pos: bool=False, verbose: bool=True) -> str:
    valid_pos = set(range(8))
    password = []
    if use_pos:
        pos_pass = ['' for _ in range(8)]
        pos_found = [False for _ in range(8)]

    for i in count():
        candidate = bytes(data + str(i), encoding='utf8')
        res = md5(candidate).hexdigest()
        if res.startswith('00000'):
            if use_pos:
                pos = int(res[5], 16)
                if pos in valid_pos and not pos_found[pos]:
                    pos_pass[pos] = res[6]
                    pos_found[pos] = True
                if verbose:
                    print(f'Found position {pos:>2}:  {res[6]} - {sum(pos_found)} of 8')
            else:
                if verbose:
                    print(f'Found next character:  {res[5]}')
                password.append(res[5])
            if (not use_pos and len(password) >= 8) or (use_pos and all(pos_pass)):
                break
        '''
        if verbose and i % 1_000_000 == 0:
            print('.', end='', flush=True)
        '''

    if verbose:
        print()

    return ''.join(pos_pass) if use_pos else ''.join(password)


def main() -> None:
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        data = infile.read().strip()

    # Part 1:
    # password = get_pass(data)
    #
    # Part 2:
    password = get_pass(data, use_pos=True)
    print(f'Password:  {password}')


if __name__ == '__main__':
    main()
