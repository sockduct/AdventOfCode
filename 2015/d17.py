#! /usr/bin/env python3


'''
No such thing as too much
* Read in container sizes from file
* Filling all containers entirely, how many different combinations of containers
  can exactly fit all 150 liters of eggnog?
'''


INFILE = 'd17.txt'
# INFILE = 'd17t1.txt'


# Libraries:
from itertools import combinations
from pathlib import Path


def get_combos(data, target):
    options = []
    for r in range(2, len(data)):
        options.extend(list(combinations(data, r)))

    return [item for item in options if sum(item) == target]


def get_min_combos(data, target):
    for r in range(2, len(data)):
        if options := [item for item in combinations(data, r) if sum(item) == target]:
            return options


def main(verbose=False):
    mydir = Path(__file__).parent
    # target = 25
    target = 150
    data = []
    with open(mydir/INFILE) as infile:
        for line in infile:
            data.append(int(line.strip()))

    # combos = get_combos(data, target)
    combos = get_min_combos(data, target)

    if verbose:
        print(f'Possible combinations:  {combos}')
    print(f'Number of combinations:  {len(combos):,}')


if __name__ == '__main__':
    main()
