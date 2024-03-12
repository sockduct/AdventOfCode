#! /usr/bin/env python3


'''
Bots and Chips
* Chips have a number
* Bots take action when have 2 chips
* Bots can either give chip to different bot or place in output bin
* Sometimes bots take chips from input bin
* Parse instructions and answer questions about end state
'''


# INFILE = 'd10.txt'
INFILE = 'd10t1.txt'


# Libraries
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint


# Types:
@dataclass
class Bot:
    low: str|None = None
    high: str|None = None

    def add(self, val: str):
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
        return self.low and self.high


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


def process(instr: dict[str, tuple[str, str, str]], bots: dict[str, Bot],
            outputs: dict[str, str], compares: dict[str, tuple[str, str]]) -> None:
    '''
    ### Rather than iterating through instructions, iterate through bots and only
    ### process if they are full!
    '''
    for bot, (dest, lval, hval) in instr.items():
        if not bots[bot].full():
            raise IndexError(f'Error:  bot {bot} ({bots[bot]}) not full.')

        # Record comparison:
        if bot in compares:
            raise ValueError(f'Error:  bot {bot} already recorded in compares ({compares[bot]}).')
        compares[bot] = (bots[bot].low, bots[bot].high)

        match dest:
            case 'oo':
                if lval in outputs:
                    raise ValueError(f'Error:  Output bin {lval} already has value {outputs[lval]}.')
                if hval in outputs:
                    raise ValueError(f'Error:  Output bin {hval} already has value {outputs[hval]}.')

                outputs[lval] = bots[bot].low
                outputs[hval] = bots[bot].high
            case 'ob':
                if lval in outputs:
                    raise ValueError(f'Error:  Output bin {lval} already has value {outputs[lval]}.')

                outputs[lval] = bots[bot].low
                if hval in bots:
                    bots[hval].add(bots[bot].high)
                else:
                    bots[hval] = Bot(bots[bot].high)
            case 'bo':
                if hval in outputs:
                    raise ValueError(f'Error:  Output bin {hval} already has value {outputs[hval]}.')

                if lval in bots:
                    bots[lval].add(bots[bot].low)
                else:
                    bots[lval] = Bot(bots[bot].low)
                outputs[hval] = bots[bot].high
            case 'bb':
                if lval in bots:
                    bots[lval].add(bots[bot].low)
                else:
                    bots[lval] = Bot(bots[bot].low)
                if hval in bots:
                    bots[hval].add(bots[bot].high)
                else:
                    bots[hval] = Bot(bots[bot].high)
            case _:
                raise ValueError(f'Unexpected destination:  {dest}')

        bots[bot].empty()


def main(verbose: bool=True) -> None:
    instr = {}
    bots = {}
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line.strip(), instr, bots)

    if verbose:
        print('Instructions:')
        pprint(instr)
        print('\nBots:')
        pprint(bots)

    outputs = {}
    compares = {}
    process(instr, bots, outputs, compares)

    if verbose:
        print('Bots:')
        pprint(bots)
        print('\nOutputs:')
        pprint(outputs)
        print('\nCompares:')
        pprint(compares)


if __name__ == '__main__':
    main()
