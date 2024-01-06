#! /usr/bin/env python3


'''
IPv7
* Count IPs supporting "TLS"
* Yes if 4-character sequence which is a pair of two different characters
  followed by the reverse of that pair - e.g., abba
* Mirrored-pair must be outside of brackets - e.g., [abba] doesn't count
* If there's a mirrored-pair inside of brackets it doesn't count
'''


INFILE = 'd7.txt'
# INFILE = 'd7t1.txt'
# INFILE = 'd7t2.txt'


# Libraries:
from collections import deque
from pathlib import Path
import re
from string import ascii_lowercase as lowercase

# 3rd party:
from more_itertools import flatten, sliding_window


# Module:
def get_tlscount(addrs: list[str]) -> int:
    '''
    Examples:
    abba[mnop]qrst - Yes
    abcd[bddb]xyyx - No
    aaaa[qwer]tyui - No
    ioxxoj[asdfgh]zxcvbn - Yes
    '''
    count = 0
    in_brackets = False
    for addr in addrs:
        addrq = deque(addr)
        candidate = False
        # Prime it:
        second, third, forth = addrq.popleft(), addrq.popleft(), addrq.popleft()
        while addrq:
            try:
                match (first := second, second := third, third := forth, forth := addrq.popleft()):
                    case (a, b, c, d) if a == b:
                        continue
                    case (abcd) if '[' in abcd:
                        in_brackets = True
                        # Keep rolling until '[' not present:
                        continue
                    case (abcd) if ']' in abcd:
                        in_brackets = False
                        # Keep rolling until ']' not present:
                        continue
                    case (a, b, c, d) if (
                        a in lowercase and b in lowercase and c in lowercase and d in lowercase
                    ):
                        pass
                    case _:
                        raise ValueError(f'Unexpected value set:  {first}, {second}, {third},'
                                         f' {forth}')
            except IndexError:
                break

            val_tls = (first, second) == (forth, third)

            if val_tls and not in_brackets:
                candidate = True
            elif val_tls:
                candidate = False
                break

        if candidate:
            count += 1

    return count


def get_sslcandidates(group: str, inside: bool=False) -> set[tuple[str, str, str]]:
    candidates = sliding_window(group, 3)
    if not inside:
        return {
            (first, second, third)
            for first, second, third in candidates
            if first == third and first != second
        }
    else:
        return {
            (second, first, second)
            for first, second, third in candidates
            if first == third and first != second
        }


def get_sslcount(addrs: list[str]) -> int:
    '''
    Examples:
    aba[bab]xyz - yes
    xyx[xyx]xyx - no
    aaa[kek]eke - yes
    zazbz[bzb]cdb - yes

    ### Refactor to deal with this:
    'rnqfzoisbqxbdlkgfh[lwlybvcsiupwnsyiljz]kmbgyaptjcsvwcltrdx[ntrpwgkrfeljpye]jxjdlgtntpljxaojufe'
    Two groups - outside, inside
    * even groups are outside (0, 2, ...)
    * odd groups are inside (1, 3, ...)
    ** gotcha - sequences can't span groups (e.g., can't have sequence from group1 and group3)
    '''
    count = 0
    for addr in addrs:
        outside = []
        inside = []
        for i, block in enumerate(re.split(r'\[|\]', addr)):
            outside.append(block) if i % 2 == 0 else inside.append(block)

        outside_candidates = list(flatten(get_sslcandidates(candidate) for candidate in outside))
        inside_candidates = set(flatten(get_sslcandidates(candidate, inside=True)
                                        for candidate in inside))
        candidate = any(group in inside_candidates for group in outside_candidates)

        if candidate:
            count += 1

    return count


def main() -> None:
    addrs: list[str] = []
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        addrs.extend(line.strip() for line in infile)

    # Part 1:
    # count = get_tlscount(addrs)
    # print(f'Found {count:,} IPs supporting TLS')
    #
    # Part 2:
    count = get_sslcount(addrs)
    print(f'Found {count:,} IPs supporting SSL')


if __name__ == '__main__':
    main()
