#! /usr/bin/env python3


'''
String examination:

Part 1:
* Nice strings:
    1) Contain at least 3 vowels (aeiou)
    2) Contains at least 1 letter that appears twice in a row (e.g., xx)
    3) Does NOT contain strings:  ab, cd, pq, or xy
* Other strings are "naughty"

Part 2:
* Nice strings:
    1) It contains a pair of any two letters that appears at least twice in the
       string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not
       like aaa (aa, but it overlaps).
    2) It contains at least one letter which repeats with exactly one letter
       between them, like xyx, abcdefeghi (efe), or even aaa.
'''



# INFILE = 'd5t1.txt'
# INFILE = 'd5t2.txt'
INFILE = 'd5.txt'


from collections import Counter, defaultdict
import contextlib
from itertools import islice, pairwise, zip_longest
from pathlib import Path


class EarlyExit(Exception):
    pass


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


def nice_string2(string, line_count=0, verbose=True):
    '''
    1) It contains a pair of any two letters that appears at least twice in the
       string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not
       like aaa (aa, but it overlaps).
    2) It contains at least one letter which repeats with exactly one letter
       between them, like xyx, abcdefeghi (efe), or even aaa.
    '''

    count = defaultdict(list)
    for pos, pair in enumerate(pairwise(string)):
        count[pair].append(pos)

    # Check for item 1:
    candidates = {k: v for k, v in count.items() if len(v) > 1}
    if not any(candidate for candidate, pos in candidates.items()
               if len(pos) > 2 or abs(pos[0] - pos[1]) > 1):
        if verbose:
            print(f'{line_count:>4}:  {string} naughty - failed test 1')
        return False

    '''
    if verbose:
        print(f'{line_count:>4}:  {string} passed test 1 => {count}')
    '''

    # Check for item 2:
    for pair1, pair2 in zip(pairwise(string), pairwise(islice(string, 1, None))):
        if pair1[0] == pair2[1]:
            return True

    if verbose:
        print(f'{line_count:>4}:  {string} naughty - failed test 2')
    return False


def main(verbose=True):
    string_count = dict(total=0, nice=0, naughty=0)
    line_count = 0
    with contextlib.suppress(EarlyExit):
        with open(Path(__file__).parent/INFILE) as infile:
            for line in infile:
                line_count += 1
                string_count['total'] += 1
                # Part 1:
                # if nice_string(line.strip()):
                # Part 2:
                if nice_string2(line.strip(), line_count):
                    string_count['nice'] += 1
                    if verbose:
                        print(f'{line_count:>4}:  {line.strip()} nice')
                else:
                    string_count['naughty'] += 1

                '''
                if line_count > 20:
                    raise EarlyExit
                '''

    print(f'String tally:\n* Nice:  {string_count["nice"]}'
          f'\n* Naughty:  {string_count["naughty"]}\n* Total:  {string_count["total"]}')


if __name__ == '__main__':
    main()
