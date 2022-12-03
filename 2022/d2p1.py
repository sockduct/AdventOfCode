#! /usr/bin/env python3


'''
Rock Paper Scissors Contest
* Rock beats Scissors
* Scissors beats Paper
* Paper beats Rock

Input:
* 1st column = opponent play
  * A = Rock
  * B = Paper
  * C = Scissors
* 2nd column = my play (Part 1)
  * X = Rock
  * Y = Paper
  * Z = Scissors
* 2nd column = my play (Part 2)
  * X = Lose
  * Y = Draw
  * Z = Win

Scoring:
* Single round:
  * Shape selected:
    * Rock = 1
    * Paper = 2
    * Scissors = 3
  * Outcome:
    * Lost = 0
    * Draw = 3
    * Win = 6
'''


# INFILE = 'd2p1t1.txt'
INFILE = 'd2p1.txt'


def part1(cols):
    match cols:
        case ['A', 'X']:
            shape_score = 1
            outcome_score = 3
        case ['A', 'Y']:
            shape_score = 2
            outcome_score = 6
        case ['A', 'Z']:
            shape_score = 3
            outcome_score = 0
        case ['B', 'X']:
            shape_score = 1
            outcome_score = 0
        case ['B', 'Y']:
            shape_score = 2
            outcome_score = 3
        case ['B', 'Z']:
            shape_score = 3
            outcome_score = 6
        case ['C', 'X']:
            shape_score = 1
            outcome_score = 6
        case ['C', 'Y']:
            shape_score = 2
            outcome_score = 0
        case ['C', 'Z']:
            shape_score = 3
            outcome_score = 3
        case _:
            raise ValueError(f'Expected A|B|C, X|Y|Z.  Got {cols}.')

    return shape_score, outcome_score


def part2(cols):
    match cols:
        case ['A', 'X']:
            shape_selected = 'C'
            shape_score = 3
            outcome_score = 0
        case ['A', 'Y']:
            shape_selected = 'A'
            shape_score = 1
            outcome_score = 3
        case ['A', 'Z']:
            shape_selected = 'B'
            shape_score = 2
            outcome_score = 6
        case ['B', 'X']:
            shape_selected = 'A'
            shape_score = 1
            outcome_score = 0
        case ['B', 'Y']:
            shape_selected = 'B'
            shape_score = 2
            outcome_score = 3
        case ['B', 'Z']:
            shape_selected = 'C'
            shape_score = 3
            outcome_score = 6
        case ['C', 'X']:
            shape_selected = 'B'
            shape_score = 2
            outcome_score = 0
        case ['C', 'Y']:
            shape_selected = 'C'
            shape_score = 3
            outcome_score = 3
        case ['C', 'Z']:
            shape_selected = 'A'
            shape_score = 1
            outcome_score = 6
        case _:
            raise ValueError(f'Expected A|B|C, X|Y|Z.  Got {cols}.')

    return shape_selected, shape_score, outcome_score


def main():
    with open(INFILE) as infile:
        part1_score = 0
        part2_score = 0
        rounds = 0
        for line in infile:
            rounds += 1
            cols = line.strip().split()

            part1_score += sum(part1(cols))
            part2_res = part2(cols)
            part2_score += sum(part2_res[-2:])

    print(f'\n{rounds:,} rounds:')
    print(f'* Part 1 total score of {part1_score:,}')
    print(f'* Part 2 total score of {part2_score:,}\n')


if __name__ == '__main__':
    main()
