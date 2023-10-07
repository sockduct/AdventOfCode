#! /usr/bin/env python3


'''
Optimal Seating Arrangement:
* Read in list of people - for each person states happiness differential if
  next to another person (positive or negative)
* Each person next to two people (treat list as circular)
* Find arrangement of people that maximizes happiness
'''


INFILE = 'd13.txt'
# INFILE = 'd13t1.txt'


# Libraries:
from collections import defaultdict
from itertools import permutations
from pathlib import Path
from pprint import pprint


def parse(line, people):
    line = line.strip('\n.')
    person, _, direction, number, *_, peer = line.split()
    people[person][peer] = int(number) if direction == 'gain' else -int(number)


def add_self(people):
    people['Me']

    for person in people:
        if person != 'Me':
            people['Me'][person] = 0
            people[person]['Me'] = 0


def happiness(arrangement, people):
    score = 0

    for index, person in enumerate(arrangement):
        left = index - 1 if index != 0 else -1
        right = index + 1 if index < len(arrangement) - 1 else 0
        score += people[person][arrangement[left]] + people[person][arrangement[right]]

    return score


def max_permute(people, verbose=False):
    max_score = 0

    arrangements = permutations(people)
    for arrangement in arrangements:
        score = happiness(arrangement, people)
        if verbose:
            print(f'Arrangement:  {arrangement} => Happiness score of {score}')
        if score > max_score:
            max_score = score

    return max_score


def main():
    people = defaultdict(dict)
    with open(Path(__file__).parent/INFILE) as infile:
        for line in infile:
            parse(line, people)

    # Part 2 - add self:
    add_self(people)
    # pprint(people)

    res = max_permute(people)
    print(f'Happiness change for optimal seating:  {res:,}')


if __name__ == '__main__':
    main()
