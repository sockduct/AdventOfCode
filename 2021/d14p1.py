#! /usr/bin/env python3.10


from itertools import islice, pairwise


INFILE = 'd14p1t1.txt'
# INFILE = 'd14p1.txt'


class Polymer():
    def __init__(self, ptmpl, insrules):
        self.ptmpl = ptmpl
        self.insrules = insrules

    def __repr__(self):
        ptmpl = self.ptmpl if len(self.ptmpl) < 10 else f'{self.ptmpl[:10]}...'
        insrules = ', '.join(f'{a}=>{b}' for a, b in islice(self.insrules.items(), 4))
        if len(self.insrules) > 4:
            insrules += '...'
        return f'<Polymer({ptmpl}, {insrules})>'

    def __str__(self):
        max_width = 80
        max_items = 12

        ptmpl = self.ptmpl if len(self.ptmpl) < max_width else f'{self.ptmpl[:max_width]}...'
        insrules = ', '.join(f'{a}=>{b}' for a, b in islice(self.insrules.items(), max_items))
        if len(self.insrules) > max_items:
            insrules += '...'
        return (f'    Polymer Template:  {ptmpl}\n'
                f'Pair Insertion Rules:  {insrules}')

    def step(self, n=1):
        ptmpl = ''
        for p1, p2 in pairwise(self.ptmpl):
            key = p1 + p2
            mid = self.insrules[key]
            ptmpl = p1 + mid + p2 if not ptmpl else ptmpl + mid + p2

        self.ptmpl = ptmpl


def main():
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
    polymer.step()
    print(f'\n{polymer}')


if __name__ == '__main__':
    main()
