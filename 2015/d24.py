#! /usr/bin/env python3


'''
Balancing Loads
* List of packages by weight
* Must split into 3 groups of exactly the same weight
* In addition, the first group needs as few packages as possible
* If there are multiple ways to arrange packages in the first group, must choose
  option with smallest "quantum entanglement" - or the product of the weights of
  the group
* Calculate "quantum entanglement" of group 1
'''


INFILE = 'd24.txt'
# INFILE = 'd24t1.txt'


# Libraries
from itertools import combinations
from math import prod
from pathlib import Path


def get_target(weights: list[int]) -> int:
    total = sum(weights)
    target = total//3
    if target * 3 != total:
        raise ValueError('Total weight must be divisible by 3!')

    return target


def get_group1(weights: list[int], target) -> list[int]:
    # Simple case:
    if candidate := [e for e in weights if e == target]:
        return [min(candidate)]

    # Otherwise look:
    for num in range(2, len(weights) - 2):
        # This is legitimate - not sure how to make mypy happy:
        if candidate := [e for e in combinations(weights, num)  # type: ignore[misc]
                         if sum(e) == target]:
            return list(min(candidate))

    return []


def get_groups(weights: list[int], target: int) -> tuple[list[int], list[int]]:
    for num in range(2, len(weights) - 1):
        if candidate := [e for e in combinations(weights, num) if sum(e) == target]:
            break

    group2 = list(min(candidate))
    group3 = list(set(weights) - set(group2))

    return group2, group3


def main() -> None:
    cwd = Path(__file__).parent
    # Note:  Assuming weights are sorted and unique
    weights: list[int] = []
    with open(cwd/INFILE) as infile:
        weights.extend(int(line.strip()) for line in infile)

    target = get_target(weights)
    group1 = get_group1(weights, target)

    remaining = list(set(weights) - set(group1))
    group2, group3 = get_groups(remaining, target)

    qe = prod(group1)

    print(f'Group 1:  {group1}\nGroup 2:  {group2}\nGroup 3:  {group3}')
    print(f'Quantum Entanglement of Group 1:  {qe}')


if __name__ == '__main__':
    main()
