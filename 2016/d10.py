#! /usr/bin/env python3


'''
Bots and Chips
* Chips have a number
* Bots take action when have 2 chips
* Bots can either give chip to different bot or place in output bin
* Sometimes bots take chips from input bin
* Parse instructions and answer questions about end state
'''


INFILE = 'd10.txt'
# INFILE = 'd10t1.txt'


# Libraries
from copy import deepcopy
from dataclasses import dataclass
from math import prod
from pathlib import Path
from pprint import pprint


# Types:
@dataclass
class Bot:
    low: str|None = None
    high: str|None = None

    def add(self, val: str) -> None:
        if self.low is None:
            self.low = val
        elif self.high is None:
            if int(val) > int(self.low):
                self.high = val
            elif int(val) < int(self.low):
                self.high = self.low
                self.low = val
            elif val == self.low:
                raise ValueError(f'Expected new value ({val}) to be lower/higher '
                                 'then existing value')
        else:
            raise ValueError('Error:  Bot already has low and high values')

    def empty(self) -> None:
        self.low = None
        self.high = None

    def full(self) -> bool:
        return bool(self.low and self.high)


# Module:
def parse(line: str, instr: dict[str, tuple[str, str, str]], bots: dict[str, Bot]) -> None:
    '''
    Cases:
    * value # goes to bot #
    * bot # gives low to bot # and high to bot #
    * bot # gives low to output # and high to bot #
    * bot # gives low to bot # and high to output #
    * bot # gives low to output # and high to output #

    value 5 goes to bot 2
    bot 2 gives low to bot 1 and high to bot 0
    value 3 goes to bot 1
    bot 1 gives low to output 1 and high to bot 0
    bot 0 gives low to output 2 and high to output 0
    value 2 goes to bot 2
    '''
    match line.split():
        case 'value', val, 'goes', 'to', 'bot', botnum:
            if botnum in bots:
                bots[botnum].add(val)
            else:
                bots[botnum] = Bot(val)
        case ('bot', procbotnum, 'gives', 'low', 'to', 'bot', lowbotnum, 'and',
              'high', 'to', 'bot', highbotnum):
            if procbotnum in instr:
                raise ValueError(f'Error:  Bot {procbotnum} already in instruction set!')

            instr[procbotnum] = ('bb', lowbotnum, highbotnum)
        case ('bot', procbotnum, 'gives', 'low', 'to', 'output', lowoutnum, 'and',
              'high', 'to', 'bot', highbotnum):
            if procbotnum in instr:
                raise ValueError(f'Error:  Bot {procbotnum} already in instruction set!')

            instr[procbotnum] = ('ob', lowoutnum, highbotnum)
        case ('bot', procbotnum, 'gives', 'low', 'to', 'bot', lowbotnum, 'and',
              'high', 'to', 'output', highoutnum):
            if procbotnum in instr:
                raise ValueError(f'Error:  Bot {procbotnum} already in instruction set!')

            instr[procbotnum] = ('bo', lowbotnum, highoutnum)
        case ('bot', procbotnum, 'gives', 'low', 'to', 'output', lowoutnum, 'and',
              'high', 'to', 'output', highoutnum):
            if procbotnum in instr:
                raise ValueError(f'Error:  Bot {procbotnum} already in instruction set!')

            instr[procbotnum] = ('oo', lowoutnum, highoutnum)
        case _:
            raise ValueError(f'Unexpected input:  {line}')


def dispatch(bot: str, bots: dict[str, Bot], instr: dict[str, tuple[str, str, str]],
             outputs: dict[str, str]) -> None:
    dest, lval, hval = instr[bot]
    match dest:
        case 'oo':
            if lval in outputs:
                raise ValueError(f'Error:  Output bin {lval} already has value {outputs[lval]}.')
            if hval in outputs:
                raise ValueError(f'Error:  Output bin {hval} already has value {outputs[hval]}.')

            # Dispatch only called if Bot full, thus don't need None check:
            outputs[lval] = bots[bot].low   # type: ignore
            outputs[hval] = bots[bot].high  # type: ignore
        case 'ob':
            if lval in outputs:
                raise ValueError(f'Error:  Output bin {lval} already has value {outputs[lval]}.')

            outputs[lval] = bots[bot].low  # type: ignore
            if hval in bots:
                bots[hval].add(bots[bot].high)  # type: ignore
            else:
                bots[hval] = Bot(bots[bot].high)
        case 'bo':
            if hval in outputs:
                raise ValueError(f'Error:  Output bin {hval} already has value {outputs[hval]}.')

            if lval in bots:
                bots[lval].add(bots[bot].low)  # type: ignore
            else:
                bots[lval] = Bot(bots[bot].low)
            outputs[hval] = bots[bot].high  # type: ignore
        case 'bb':
            if lval in bots:
                bots[lval].add(bots[bot].low)  # type: ignore
            else:
                bots[lval] = Bot(bots[bot].low)
            if hval in bots:
                bots[hval].add(bots[bot].high)  # type: ignore
            else:
                bots[hval] = Bot(bots[bot].high)
        case _:
            raise ValueError(f'Unexpected destination:  {dest}')


def process(instr: dict[str, tuple[str, str, str]], bots: dict[str, Bot],
            outputs: dict[str, str], compares: dict[str, tuple[str, str]]) -> None:
    '''
    First pass - iterated through instructions.  Works on test case but not on
    actual data.  After re-reading the scenario, need to iteration through bots
    and only process a bot if it's full.
    '''
    loop = True
    while loop:
        loop = False
        # Make a copy as can't modify dictionary you're iterating through:
        loop_bots = deepcopy(bots)
        for bot, bvals in loop_bots.items():
            if bvals.full():
                loop = True

                # Record comparison:
                if bot in compares:
                    raise ValueError(f'Error:  bot {bot} already recorded in compares '
                                     f'({compares[bot]}).')

                # Only get here if Bot full, so don't need None check:
                compares[bot] = (bots[bot].low, bots[bot].high) # type: ignore

                # Look up bot instructions to dispatch values:
                dispatch(bot, bots, instr, outputs)
                bots[bot].empty()


def main(verbose: bool=True) -> None:
    instr: dict[str, tuple[str, str, str]] = {}
    bots: dict[str, Bot] = {}
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line.strip(), instr, bots)

    if verbose:
        print('Before:')
        print('Instructions:')
        pprint(instr)
        print('\nBots:')
        pprint(bots)

    outputs: dict[str, str] = {}
    compares: dict[str, tuple[str, str]] = {}
    process(instr, bots, outputs, compares)

    if verbose:
        print('\nAfter:')
        print('Bots:')
        pprint(bots)
        print('\nOutputs:')
        pprint(outputs)
        print('\nCompares:')
        pprint(compares)

    # Answer, part 1:
    val1 = '17'
    val2 = '61'
    for key, vals in compares.items():
        if vals[0] == val1 and vals[1] == val2 or (
            vals[0] == val2 and vals[1] == val1
        ):
            print(f'\nBot {key} compared {val1} and {val2} microchips.')

    # Answer, part 2:
    val = prod(int(outputs[i]) for i in ('0', '1', '2'))
    print(f'\nMultiplied value of outputs 0, 1, 2:  {val:,}')


if __name__ == '__main__':
    main()
