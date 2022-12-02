#! /usr/bin/env python3


# INFILE = 'd1p1t1.txt'
# INFILE = 'd1p1.txt'
INFILE = '/working/github/sockduct/aoc/2022/d1p1.txt'
'''
cal#1-elf#1
cal#2-elf#1
...

cal#1-elf#2

cal#1-elf#3

...
'''


def main():
    elves = []
    with open(INFILE) as infile:
        total = 0
        for calories in infile:
            if calories := calories.strip():
                total += int(calories)
            else:
                elves.append(total)
                total = 0

    most_calories = max(elves)
    print(f'\nElf {elves.index(most_calories) + 1} has the most calories ({most_calories:,})'
          f' out of {len(elves)} elves.')

    sorted_calories = sorted(elves)
    top3_calories = sum(sorted_calories[-3:])
    print(f'\n{"=" * 80}\n')
    print('The elves with the top 3 calorie totals are ', end='')
    for i in range(-3, 0):
        amount = sorted_calories[i]
        print(f'{elves.index(amount) + 1} ({amount:,}), ', end='')
    print(f'for a total of {top3_calories:,}.\n')


if __name__ == '__main__':
    main()
