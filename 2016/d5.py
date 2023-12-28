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
def get_pass(data: str, verbose: bool=True) -> str:
    password = []
    for i in count():
        candidate = bytes(data + str(i), encoding='utf8')
        res = md5(candidate).hexdigest()
        if res.startswith('00000'):
            password.append(res[5])
            if len(password) >= 8:
                break
        if verbose and i % 1_000_000 == 0:
            print('.', end='', flush=True)

    if verbose:
        print()

    return ''.join(password)


def main() -> None:
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        data = infile.read().strip()

    password = get_pass(data)
    print(f'Password:  {password}')


if __name__ == '__main__':
    main()
