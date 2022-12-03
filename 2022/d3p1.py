#! /usr/bin/env python3


'''
Backpacks (rucksacks):
* Each has two compartments
* List of items, each belongs in one of the compartments
* One item per backpack in the wrong compartment

Input:
* List of all items in the backpack
* Each item is one letter (lower and upper represent different items)
* All items concatenated together on one line
* Items split equally between two compartments
* Find items that are in both compartments

Prioritizing:
* Every item can be converted to a priority
* Items a - z have priority 1 - 26
* Items A - Z have priority 27 - 52

Output:
* For each item that appears in both compartments:
  * Convert to a priority
  * Sum the priorities and return this result

Part 2:
* Elves divided into groups of 3
* Only one item will be shared by all 3 team members
* Every 3 lines corresponds to a single group
'''


# INFILE = 'd3p1t1.txt'
INFILE = 'd3p1.txt'


import string


def priority(letter):
    '''
    ASCII a - z = 97 - 122, subtract 96 to get 1 - 26
    ASCII A - Z = 65 - 90, subtract 38 to get 27 - 52
    '''
    if letter in string.ascii_lowercase:
        return ord(letter) - 96
    elif letter in string.ascii_uppercase:
        return ord(letter) - 38
    else:
        raise ValueError(f'Expected a-z or A-Z, got {letter}.')


def part1(line):
    half = len(line)//2
    compartment1 = line[:half]
    compartment2 = line[half:]
    common = (set(compartment1) & set(compartment2)).pop()
    return priority(common)


def part2(group):
    badge = (set(group[0]) & set(group[1]) & set(group[2])).pop()
    return priority(badge)


def main():
    with open(INFILE) as infile:
        part1_total = 0
        part2_total = 0
        count = 0
        group = []
        for line in infile:
            count += 1
            line = line.strip()
            part1_total += part1(line)
            group.append(line)
            if count % 3 == 0:
                part2_total += part2(group)
                group.clear()


    print(f'\n{count} lines processed.')
    print(f'Total priority values of all common items:  {part1_total:,}')
    print(f'Total priority values of all badges:  {part2_total:,}\n')


if __name__ == '__main__':
    main()
