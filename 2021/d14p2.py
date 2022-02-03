#! /usr/bin/env python3.10


from collections import Counter
from itertools import islice, pairwise


INFILE = 'd14p1t1.txt'
# INFILE = 'd14p1.txt'


'''
Now have fast encoding -> quickly step through pair insertion rules

Problem:  How to go from polymer (pair count) to actual polymer string
* Tricky because of sequencing:
  Go from CH=1, HB=1, NC=1, NB=1, BC=1, CN=1 to NCNBCHB
* Start with keeping track of first and last sequences
* Look for pattern - step through
'''
class Polymer():
    def __init__(self, ptmpl, insrules):
        self.ptmpl = ptmpl
        self.insrules = insrules
        # First and last pairs:
        self.first = ptmpl[:2]
        self.last = ptmpl[-2:]

        # Fast map from old pair to new pairs:
        self.xformrules = {key: (key[0] + val, val + key[1]) for key, val in insrules.items()}

        # Convert polymer template into pairs (keys) where value is counter
        self.polymer = {key: 0 for key in insrules}

        for p1, p2 in pairwise(self.ptmpl):
            self.polymer[p1 + p2] += 1

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

    def build_polymer(self):
        '''
        Works, but doesn't scale.

        Largest sequence is over 3 trillion characters - even with 64bit Python
        this results in a memory error.  Need to count digits without building
        string.
        '''
        polymer_str = self.first
        polymer = self.polymer.copy()
        polymer[self.first] -= 1
        while True:
            for key, val in polymer.items():
                if val and key[0] == polymer_str[-1]:
                    polymer_str += key[1]
                    polymer[key] -= 1
            if sum(polymer.values()) == 0:
                break

        return polymer_str

    def diff(self, verbose=True):
        polymer_str = self.build_polymer()
        count = Counter(polymer_str)
        if verbose:
            print(f'\nCount:  {count}')
        vals = count.values()
        return max(vals) - min(vals)

    def step(self):
        polymer = {key: 0 for key in self.insrules}
        last = ''
        for key, val in self.polymer.items():
            if val:
                key1, key2 = self.xformrules[key]
                if key == self.first:
                    self.first = key1
                polymer[key1] += val
                polymer[key2] += val
                last = key2

        self.last = last
        self.polymer = polymer

        # Too slow...
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

    for n in range(1, 11):
        polymer.step()
        if verbose:
            print(f'\n                Step:  {n}')
            print(f'Polymer:  {polymer.polymer}')

    print(f'Polymer values:  {sum(polymer.polymer.values()):,}')
    print(f'\nDifference:  {polymer.diff()}')


if __name__ == '__main__':
    main()
