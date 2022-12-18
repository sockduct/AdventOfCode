#! /usr/bin/env python3


'''
Monkey in the Middle
* Monkeys playing keep away with your stuff!

Part 1 Input:
* Items each monkey has (my worry level for each)
* Operation shows how your worry level changes
  * new = old * 5; worry level 5x higher after monkey inspected item than before
* Test is how monkey decides what to do with item
  * true|false conditions show respective actions
* After each monkey inspects an item but before testing your worry level, your
  relief that monkey didn't damage item causes your worry level to be divided by
  3
* On a single monkey's turn, it inspects and throws all the items its holding
  one at a time in order
  * Monkey 0 goes first, then 1, ...
  * Process of each monkey taking a turn is a round
* When a monkey receives an item, it goes on the end of its list
* If monkey holding no items during its turn, it's skipped
'''


# INFILE = 'd11p1t1.txt'
INFILE = 'd11p1.txt'


# Standard Library
from collections.abc import Callable
from dataclasses import dataclass
from math import prod
from operator import add, mul


@dataclass
class Monkey:
    items: list[int]
    opact: Callable[[int, int], int]
    opval: int
    testval: int
    testtrue: int
    testfalse: int
    inspections: int = 0

    def calc(self, value):
        return self.opact(value, value) if self.opval == -2 else self.opact(value, self.opval)


def round(rnum, monkeys, worryreduce, verbose=False):
    if verbose:
        print(f'Round {rnum}:')

    for mnum, monkey in monkeys.items():
        if verbose:
            print(f'  Monkey {mnum}:')
        items = monkey.items
        monkey.items = []
        for item in items:
            monkey.inspections += 1
            if verbose:
                print(f'    Monkey {mnum} inspects item with worry level of {item}.')
            worrylevel = monkey.calc(item)
            if verbose:
                verb = 'multiplied' if monkey.opact is mul else 'increased'
                value = 'itself' if monkey.opval == -2 else str(monkey.opval)
                print(f'      Worry level is {verb} by {value} to {worrylevel}.')
            if worryreduce['worrydiv'] > 1:
                worrylevel //= worryreduce['worrydiv']
            else:
                worrylevel %= worryreduce['worrymod']
            if verbose:
                print(f'      Monkey gets bored with item.  Worry level is divided by {worrydiv} '
                      f'to {worrylevel}.')
            next_monkey = (monkey.testtrue if worrylevel and worrylevel % monkey.testval == 0
                            else monkey.testfalse)
            if verbose:
                verb = 'is' if next_monkey == monkey.testtrue else 'is not'
                print(f'      Current worry level {verb} divisible by {monkey.testval}.')
            monkeys[next_monkey].items.append(worrylevel)
            if verbose:
                print(f'      Item with worry level {worrylevel} is thrown to monkey {next_monkey}.')


def main(verbose=False):
    monkeys = {}
    testvals = set()
    with open(INFILE) as infile:
        monkeynum = -1
        monkeyattr = dict(items=[], opact=None, opval=0, testval=0, testtrue=-1, testfalse=-1)
        for line in infile:
            match line.split():
                case ['Monkey', num]:
                    monkeynum = int(num.strip(':'))
                case ['Starting', 'items:', *nums]:
                    monkeyattr['items'] = [int(i) for i in ''.join(nums).split(',')]
                case ['Operation:', 'new', '=', 'old', opact, opval]:
                    if opact == '*':
                        monkeyattr['opact'] = mul
                    elif opact == '+':
                        monkeyattr['opact'] = add
                    else:
                        raise ValueError(f'Expected +|*, got {opact}.')

                    try:
                        monkeyattr['opval'] = int(opval)
                    except ValueError as err:
                        # Handle case where opval is 'old' => use current item #
                        monkeyattr['opval'] = -2
                case ['Test:', 'divisible', 'by', testval]:
                    monkeyattr['testval'] = int(testval)
                    testvals.add(int(testval))
                case ['If', 'true:', 'throw', 'to', 'monkey', testtrue]:
                    monkeyattr['testtrue'] = int(testtrue)
                case ['If', 'false:', 'throw', 'to', 'monkey', testfalse]:
                    monkeyattr['testfalse'] = int(testfalse)

                    monkeys[monkeynum] = Monkey(**monkeyattr)
                    monkeynum = -1
                    monkeyattr = dict(items=[], opact=None, opval=0, testval=0, testtrue=-1, testfalse=-1)
                case []:
                    # Empty line
                    pass
                case _:
                    raise ValueError(f'Unexpcted line:  {line.strip()}')

    worryreduce = dict(worrydiv=3, worrymod=prod(testvals))

    # Debug
    if verbose:
        for value in monkeys.values():
            print(value)

    # For part 2:
    worryreduce['worrydiv'] = 1
    for rnum in range(1, 10_001):
        round(rnum, monkeys, worryreduce, verbose)

    inspections = []
    print()
    for mnum, monkey in monkeys.items():
        inspections.append(monkey.inspections)
        print(f'Monkey {mnum} inspected items {monkey.inspections} times.')

    monkey_biz = prod(sorted(inspections)[-2:])
    print(f'\nLevel of monkey business is {monkey_biz:,}.')


if __name__ == '__main__':
    main()
