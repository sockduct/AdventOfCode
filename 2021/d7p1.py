#! /usr/bin/env python3.10

from statistics import median

# INFILE = 'd7p1t1.txt'
INFILE = 'd7p1.txt'

def fuel_cost(subs_pos, target):
    return sum(abs(pos - target) for pos in subs_pos)

def main():
    with open(INFILE) as infile:
        subs_pos = [int(pos) for pos in infile.read().strip().split(',')]

    mid = int(median(subs_pos))
    fc = {i: fuel_cost(subs_pos, i) for i in range(-1, mid + 2)}
    best = min(fc, key=fc.get)
    print(f'Position {best} results in least fuel cost:  {fc[best]}')

if __name__ == '__main__':
    main()
