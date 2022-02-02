#! /usr/bin/env python3.10


from collections import Counter
from itertools import islice, pairwise


INFILE = 'd14p1t1.txt'
# INFILE = 'd14p1.txt'


'''
Need more efficient approach:
* There are 4 - 10 elements (can encode as 0 - 9)
* Rather than encoding as UTF-8 or worse, encode as int or something more efficient
  * Map each element to a digit

* Encode in a way that makes easy to update - perhaps favor encoding over printing or
  displaying efficiently
* When step through to apply insertion rules, need more efficient updating approach
  * Group insertion rules - set that results in element 1, set that results in element
    2, ...
'''
class Polymer():
    def __init__(self, ptmpl, insrules):
        self.ptmpl = ptmpl
        self.insrules = insrules

        # Fast map from old pair to new pairs:
        self.xformrules = {key: (key[0] + val, val + key[1]) for key, val in insrules.items()}

        # Convert polymer template into pairs (keys) where value is counter
        self.polymer = {key: 0 for key in insrules}

        for p1, p2 in pairwise(self.ptmpl):
            self.polymer[p1 + p2] += 1

        # Convert to more efficient representations:
        '''
        elements = set(self.ptmpl) | set(self.insrules.values())
        self.ptmpl_map = dict(enumerate(elements))
        self.insrules_map = {
            frozenset({key for key, val in self.insrules.items() if val == e}): e
            for e in elements
        }
        '''

    def __repr__(self):
        ptmpl_len = len(self.ptmpl)
        ptmpl = self.ptmpl if ptmpl_len < 10 else f'{self.ptmpl[:10]}...'
        insrules_len = len(self.insrules)
        insrules = ', '.join(f'{a}=>{b}' for a, b in islice(self.insrules.items(), 4))
        if insrules_len > 4:
            insrules += '...'
        return f'<Polymer({ptmpl} ({ptmpl_len:,}), {insrules} ({insrules_len}))>'

    def __str__(self):
        max_width = 80
        max_items = 12

        ptmpl_len = len(self.ptmpl)
        ptmpl = self.ptmpl if ptmpl_len < max_width else f'{self.ptmpl[:max_width]}...'
        insrules_len = len(self.insrules)
        insrules = ', '.join(f'{a}=>{b}' for a, b in islice(self.insrules.items(), max_items))
        if insrules_len > max_items:
            insrules += '...'
        return (f'    Polymer Template:  {ptmpl} ({ptmpl_len:,})\n'
                f'Pair Insertion Rules:  {insrules} ({insrules_len})')

    def diff(self, verbose=True):
        count = Counter(self.ptmpl)
        if verbose:
            print(f'\nCount:  {count}')
        vals = count.values()
        return max(vals) - min(vals)

    def step(self):
        # ptmpl = self.ptmpl[:1]
        # for p1, p2 in pairwise(self.ptmpl):
        # for start, stop in enumerate(range(2, len(self.ptmpl) + 1)):
        '''
        for top in range(2, len(self.ptmpl) + 1):
            val = self.ptmpl[top - 2:top]
            ptmpl += self.insrules[val] + val[1]

        self.ptmpl = ptmpl
        '''
        polymer = {key: 0 for key in self.insrules}
        for key, val in self.polymer.items():
            if val:
                key1, key2 = self.xformrules[key]
                polymer[key1] += val
                polymer[key2] += val

        self.polymer = polymer

        # self.ptmpl = ''.join(key * val for key, val in polymer.items())


def main(verbose=True):
    with open(INFILE) as infile:
        ptmpl = ''
        insrules = {}
        for line in infile:
            line = line.strip()
            if '>' in line:
                key, val = line.split(' -> ')
                insrules[key] = val
            elif line:
                ptmpl = line
            else:
                continue

    polymer = Polymer(ptmpl, insrules)
    print(polymer)

    # Works for 10 steps - fails for 40, believe n^2 growth, need better
    # approach:
    for n in range(1, 11):
        polymer.step()
        if verbose:
            print(f'\n                Step:  {n}\n{polymer}')
            # print(f'\nDifference:  {polymer.diff()}')
            print(f'Polymer:  {polymer.polymer}')

    print(f'\nDifference:  {polymer.diff()}')


if __name__ == '__main__':
    main()
