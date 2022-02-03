#! /usr/bin/env python3.10


from collections import Counter
from itertools import islice, pairwise


INFILE = 'd14p1t1.txt'
# INFILE = 'd14p1.txt'


class Polymer():
    def __init__(self, ptmpl, insrules):
        self.ptmpl = ptmpl
        self.insrules = insrules

    def __repr__(self):
        ptmpl_len = len(self.ptmpl)
        ptmpl = self.ptmpl if ptmpl_len < 10 else f'{self.ptmpl[:10]}...'
        insrules_len = len(self.insrules)
        insrules = ', '.join(f'{a}=>{b}' for a, b in islice(self.insrules.items(), 4))
        if insrules_len > 4:
            insrules += '...'
        return f'<Polymer({ptmpl} ({ptmpl_len}), {insrules} ({insrules_len}))>'

    def __str__(self):
        max_width = 80
        max_items = 12

        ptmpl_len = len(self.ptmpl)
        ptmpl = self.ptmpl if ptmpl_len < max_width else f'{self.ptmpl[:max_width]}...'
        insrules_len = len(self.insrules)
        insrules = ', '.join(f'{a}=>{b}' for a, b in islice(self.insrules.items(), max_items))
        if insrules_len > max_items:
            insrules += '...'
        return (f'    Polymer Template:  {ptmpl} ({ptmpl_len})\n'
                f'Pair Insertion Rules:  {insrules} ({insrules_len})\n'
                f'               Count:  {Counter(self.ptmpl)}')

    def diff(self, verbose=False):
        count = Counter(self.ptmpl)
        if verbose:
            print(f'Count:  {count}')
        vals = count.values()
        return max(vals) - min(vals)

    def step(self):
        ptmpl = ''
        for p1, p2 in pairwise(self.ptmpl):
            key = p1 + p2
            mid = self.insrules[key]
            ptmpl = p1 + mid + p2 if not ptmpl else ptmpl + mid + p2

        self.ptmpl = ptmpl


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

    print(f'\nDifference:  {polymer.diff()}')


if __name__ == '__main__':
    main()
