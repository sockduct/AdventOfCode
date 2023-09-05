#! /usr/bin/env python3


'''
String examination:
* Nice strings:
    1) Contain at least 3 vowels (aeiou)
    2) Contains at least 1 letter that appears twice in a row (e.g., xx)
    3) Does NOT contain strings:  ab, cd, pq, or xy
* Other strings are "naughty"
'''


# INFILE = 'd5t1.txt'
INFILE = 'd5.txt'


from collections import Counter
from itertools import pairwise


def nice_string(string, verbose=False):
    vowels = {'a', 'e', 'i', 'o', 'u'}
    letter_count = Counter(string)
    vowel_count = sum(count for vowel, count in letter_count.items() if vowel in vowels)
    # Check 1:
    # if len(vowels & letter_count.keys()) < 3:
    if vowel_count < 3:
        if verbose:
            print(f'String "{string}" failed test 1 - naughty.')
        return False

    # Check 2 - doesn't work, must be consecutive:
    '''
    if sum(letter_count.values()) <= len(letter_count.values()):
        if verbose:
            print(f'String "{string}" failed test 2 - naughty.')
        return False
    '''

    # Checks 2 and 3:
    stop_strings = {('a', 'b'), ('c', 'd'), ('p', 'q'), ('x', 'y')}
    pair_present = False
    for pair in pairwise(string):
        if pair in stop_strings:
            if verbose:
                print(f'String "{string}" failed test 3 - naughty.')
            return False
        if not pair_present and pair[0] == pair[1]:
            pair_present = True

    if not pair_present:
        if verbose:
            print(f'String "{string}" failed test 2 - naughty.')
        return False

    return True


def main():
    string_count = dict(total=0, nice=0, naughty=0)
    with open(INFILE) as infile:
        for line in infile:
            string_count['total'] += 1
            if nice_string(line.strip()):
                string_count['nice'] += 1
            else:
                string_count['naughty'] += 1

    print(f'String tally:\n* Nice:  {string_count["nice"]}'
          f'\n* Naughty:  {string_count["naughty"]}\n* Total:  {string_count["total"]}')


if __name__ == '__main__':
    main()
