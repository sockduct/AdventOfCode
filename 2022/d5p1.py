#! /usr/bin/env python3


'''
Supply Stacks
* Supplies stored in stacks of marked crates
* There's a crane that can move the crates between stacks

Part 1 Input:
* There's a drawing of starting stacks of crates
  * From stack drawing, create stacks
  * Then there's a sequence of steps - complete these on the stacks
  * Elves need to know which crate is on top of each stack
    * e.g., if top crates are "C", "M", and "Z" then output is:  CMZ
'''


# INFILE = 'd5p1t1.txt'
# INFILE = r'\working\github\sockduct\aoc\2022\d5p1t1.txt'
INFILE = 'd5p1.txt'


from copy import deepcopy
from regex import findall, fullmatch


def get_top_crates_str(stacks):
    return ''.join(value[-1] for value in stacks.values())


def move_crates_part1(amount, start_crate, end_crate, stacks):
    for _ in range(1, int(amount) + 1):
        crate = stacks[f's{str(start_crate)}'].pop()
        stacks[f's{str(end_crate)}'].append(crate)


def move_crates_part2(amount, start_crate, end_crate, stacks):
    for i in range(int(amount), 0, -1):
        crate = stacks[f's{str(start_crate)}'].pop(-i)
        stacks[f's{str(end_crate)}'].append(crate)


def main():
    crates_pattern = r'(?:\[|\s)(\w|\s)(?:\]|\s)\s'
    stack_pattern = r'(?:\s*\d+\s*)+'
    with open(INFILE) as infile:
        lines = infile.readlines()
        linenum = 0
        while True:
            line = lines[linenum]
            if fullmatch(stack_pattern, line):
                stackbase = linenum
                stacknames = line.strip().split()
                stacks = {f's{stackname}': [] for stackname in stacknames}
                break
            linenum += 1

        for i in range(stackbase - 1, -1, -1):
            crateline = findall(crates_pattern, lines[i])
            for i, crate in enumerate(crateline, start=1):
                if crate.strip():
                    stacks[f's{str(i)}'].append(crate)

        stacks2 = deepcopy(stacks)

        # Confirm line after stackbase is blank:
        if lines[stackbase + 1].strip():
            raise ValueError(f'Expected line {stackbase + 1} to be blank.')

        # Directive processing
        for i in range(stackbase + 2, len(lines)):
            action_pattern = r'move\s+(\d+)\s+from\s+(\d+)\s+to\s+(\d+)\s*'
            amount, start_crate, end_crate = fullmatch(action_pattern, lines[i]).groups()
            move_crates_part1(amount, start_crate, end_crate, stacks)
            move_crates_part2(amount, start_crate, end_crate, stacks2)

    # Find crate on top of each stack and concatenate letters into a string
    result1 = get_top_crates_str(stacks)
    result2 = get_top_crates_str(stacks2)

    print(f'\nTop Crates, part 1:  {result1}')
    print(f'Top Crates, part 2:  {result2}\n')

    # Debugging:
    for k, v in stacks.items():
        print(f'{k}:  {", ".join(v)}')


if __name__ == '__main__':
    main()
