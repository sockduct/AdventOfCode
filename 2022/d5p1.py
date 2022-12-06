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
INFILE = r'\working\github\sockduct\aoc\2022\d5p1t1.txt'
# INFILE = 'd5p1.txt'


from regex import findall, fullmatch


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

        # Confirm line after stackbase is blank:
        if lines[stackbase + 1].strip():
            raise ValueError(f'Expected line {stackbase + 1} to be blank.')

        # Directive processing
        for i in range(stackbase + 2, len(lines)):
            # regex parse line
            # carry out directives...
            ...

    for k, v in stacks.items():
        print(f'{k}:  {", ".join(v)}')


if __name__ == '__main__':
    main()
