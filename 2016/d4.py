#! /usr/bin/env python3


'''
Remove decoy data:
* list of room names
* name format:
    * lowercase letters separated by dashes followed by a dash and a sector ID
      (number), and a checksum in square brackets
    * e.g., aaaaa-bbb-z-y-x-123[abxyz]
    * valid name has checksum with 5 most common letters from name, in order,
      with ties broken by alphabetization
'''


INFILE = 'd4.txt'
# INFILE = 'd4t1.txt'


# Libraries
from collections import Counter
from pathlib import Path
from string import ascii_lowercase


# Module
def rotate(encname: str, sid: int) -> str:
    let_rot = sid % 26
    dash_rot = sid % 2
    enclist = list(encname)

    unenclist = []
    for char in enclist:
        if char in ascii_lowercase:
            new_pos = ord(char) + let_rot
            if new_pos > ord('z'):
                new_pos -= ord('z') - ord('a') + 1
            unenclist.append(chr(new_pos))
        elif char == '-':
            new_char = ' ' if dash_rot == 1 else char
            unenclist.append(new_char)
        else:
            raise ValueError(f'Unexpected character:  {char}')

    return ''.join(unenclist)


def valid_name(line: str) -> tuple[bool, str, int]:
    line = line.strip()

    base, checksum = line.split('[')
    checksum = checksum.strip(']')
    checksum = ''.join(sorted(checksum))

    *namelist, sidstr = base.split('-')
    sid = int(sidstr)
    encname = '-'.join(namelist)
    name = ''.join(namelist)

    name_let = Counter(sorted(name))
    # Fails: When extract from Counter this way, not ordered by most common
    # occurrence but by insertion order!
    # calc_checksum = ''.join(list(name_let.keys())[:5])
    calc_checksum = ''.join(sorted(k for k, _ in name_let.most_common(5)))

    return (True, encname, sid) if calc_checksum == checksum else (False, encname, sid)


def main(verbose: bool=False) -> None:
    valid_count = 0
    unenc_words = {}
    target_word = 'northpole object storage'
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        for line in infile:
            status, encname, sid = valid_name(line)
            if status:
                valid_count += sid
                unenc_words[(rotate(encname, sid))] = sid

    print(f'Sum of valid room\'s sector IDs:  {valid_count:,}')
    if verbose:
        print('Valid, decrypted words:')
        for word in sorted(unenc_words):
            print(word)
    print(f'Sector ID where North Pole Objects stored:  {unenc_words[target_word]}')


if __name__ == '__main__':
    main()
