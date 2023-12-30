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


# Libraries:
from collections import deque
from pathlib import Path
from string import ascii_lowercase as lowercase


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


def main() -> None:
    addrs = []
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        addrs.extend(line.strip() for line in infile)

    count = get_tlscount(addrs)
    print(f'Found {count:,} IPs supporting TLS')


if __name__ == '__main__':
    main()
