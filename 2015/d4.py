#! /usr/bin/env python3


'''
Mine for md5 hexdigest starting with 5 leading 0's
'''


# INFILE = 'd4t1.txt'
# INFILE = 'd4.txt'


import hashlib


def main():
    # key = 'abcdef'
    # key = 'pqrstuv'
    key = 'iwrupvqb'
    counter = 1
    found5 = False

    while True:
        testkey = f'{key}{counter}'.encode('utf8')
        res = hashlib.md5(testkey).hexdigest()

        if not found5 and res.startswith('00000'):
            print(f'Found valid value for "{key}" using "{counter}":  {res}')
            found5 = True

        if res.startswith('000000'):
            print(f'Found valid value for "{key}" using "{counter}":  {res}')
            break

        counter += 1


if __name__ == '__main__':
    main()
