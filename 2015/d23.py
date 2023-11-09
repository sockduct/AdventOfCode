#! /usr/bin/env python3


'''
CPU Instructions
* Computer with two registers:  a and b
* Registers can hold any non-negative number and start at 0
* Instructions - executed sequentially unless hit a jump:
    Instruction     Action
    hlf r           sets register r to half its current value
    tpl r           sets register r to triple its current value
    inc r           increments register r, adding 1 to it
    jmp offset      jump to instruction offset relative to itself
    jie r, offset   jump if register r is even ("jump if even")
    jio r, offset   jumps if register r is 1 ("jump if one", not odd)
* Offset - "+" or "-" immediately followed by number
'''


# INFILE = 'd23.txt'
INFILE = 'd23t1.txt'


# Libraries:
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint


# Types:
@dataclass(frozen=True)
class Instruction:
    name: str
    register: str|None = None
    offset: int|None = None


@dataclass
class CPU:
    a: int = 0
    b: int = 0


def parse(line: str, commands: list[Instruction]) -> None:
    match line.split():
        case cmd, 'a':
            commands.append(Instruction(name=cmd, register='a'))
        case cmd, 'b':
            commands.append(Instruction(name=cmd, register='b'))
        case cmd, num:
            commands.append(Instruction(name=cmd, offset=int(num)))
        case cmd, reg, num:
            commands.append(Instruction(name=cmd, register=reg.strip(','), offset=int(num)))
        case _:
            raise ValueError(f'Unexpected command sequence:  {line.strip()}')


def process(commands: list[Instruction], cpu: CPU) -> None:
    # Must be able to support jumps, so can't do basic iteration:
    counter = 0
    while True:
        instruction = commands[counter]
        match instruction:
            case instruction.name == ...
            # For each command - increment counter or jump?


def main() -> None:
    cwd = Path(__file__).parent
    commands: list[Instruction] = []
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line, commands)

    pprint(commands)

    cpu = CPU()
    process(commands, cpu)

    print(f'Final state:\nCPU register a:  {cpu.a:,}\nCPU register b:  {cpu.b:,}')


if __name__ == '__main__':
    main()
