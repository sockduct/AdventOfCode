#! /usr/bin/env python3


'''
Camp Cleanup
* Every section of camp has unique ID#
* Each elf assigned a range of section IDs
* Elf assignments overlap
* Elves make list of section assignments for each pair - input

Part 1 Output:
* How many assignment pairs where one range fully contains other?
  * e.g., 3-7,2-8 is an example of this

Part 2 Output:
* How many assignments overlap at all?
'''


# INFILE = 'd4p1t1.txt'
INFILE = 'd4p1.txt'


def main():
    with open(INFILE) as infile:
        subsets = 0
        overlapsets = 0
        count = 0
        for assignment_pair in infile:
            count += 1
            assignment1, assignment2 = assignment_pair.strip().split(',')
            a1_start, a1_stop = map(int, assignment1.split('-'))
            a2_start, a2_stop = map(int, assignment2.split('-'))
            a1set = set(range(a1_start, a1_stop + 1))
            a2set = set(range(a2_start, a2_stop + 1))

            # Part 1:
            if a1set.issubset(a2set) or a2set.issubset(a1set):
                subsets += 1

            # Part 2:
            if len(a1set & a2set) > 0:
                overlapsets += 1

    print(f'\nProcessed {count:,} lines.')
    print(f'There are {subsets:,} assignment pairs where one range fully contains the other.')
    print(f'There are {overlapsets:,} assignment pairs where one range overlaps the other.\n')


if __name__ == '__main__':
    main()
