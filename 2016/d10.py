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


# Types:
@dataclass
class Bot:
    low: int|None = None
    high: int|None = None

    def add(self, val: int):
        if self.low is None:
            self.low = val
        elif self.high is None:
            if val > self.low:
                self.high = val
            elif val < self.low:
                self.high = self.low
                self.low = val
            elif val == self.low:
                raise ValueError(f'Expected new value ({val}) to be lower/higher '
                                 'then existing value')
        else:
            raise ValueError('Error:  Bot already has low and high values')


# Module:
def parse(line: str, instr: dict[str, tuple[str, str]], bots: dict[str, Bot]) -> None:
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
            ...
        case ('bot', procbotnum, 'gives', 'low', 'to', 'bot', lowbotnum, 'and',
              'high', 'to', 'bot', highbotnum):
            ...
        case ('bot', procbotnum, 'gives', 'low', 'to', 'output', lowoutnum, 'and',
              'high', 'to', 'bot', highbotnum):
            ...
        case ('bot', procbotnum, 'gives', 'low', 'to', 'bot', lowbotnum, 'and',
              'high', 'to', 'output', highoutnum):
            ...
        case ('bot', procbotnum, 'gives', 'low', 'to', 'output', lowoutnum, 'and',
              'high', 'to', 'output', highoutnum):
            ...
        case _:
            raise ValueError(f'Unexpected input:  {line}')


def main() -> None:
    instr = {}
    bots = {}
    outputs = {}
    compares = {}
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line.strip())


if __name__ == '__main__':
    main()
