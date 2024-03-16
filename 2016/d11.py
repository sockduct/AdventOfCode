#! /usr/bin/env python3


'''
Collect all RTGs and microchips and bring to 4th floor
* 4 floors
* elevator to move between floors, 1 at a time
    * starts on first floor
    * Can carry you and 2 items (any combination of RTGs/mcs)
    * Elevator requires at least 1 RTG/mc to work
* mc can't be on floor with another RTG (unless has its own RTG) or gets fried
* puzzle input has locations of each item
'''


# INFILE = 'd11.txt'
# INFILE = 'd11t1.txt'
INFILE = 'd11t2.txt'


# Libraries:
from dataclasses import dataclass
from pathlib import Path


# Types:
class Device:
    def isrtg(self):
        return False

    def ismc(self):
        return False


@dataclass
class RTG(Device):
    name: str

    def isrtg(self):
        return True


@dataclass
class MC(Device):
    name: str

    def ismc(self):
        return True


class Facility:
    floors = {1: {'mcs': [], 'rtgs': []},
              2: {'mcs': [], 'rtgs': []},
              3: {'mcs': [], 'rtgs': []},
              4: {'mcs': [], 'rtgs': []}}

    def __str__(self):
        for floor, (mcs, rtgs) in self.floors.items():
            print(f'{floor}:  Microchips - {", ".join(mcs.values())},  '
                  f'RTGs - {", ".join(rtgs.values())}')


# Module:
def get_devices(devices: list[str]) -> list[tuple[str, str]]:
    devlist = []

    initial = ' '.join(devices).split(',')
    for group in initial:
        match group.split():
            case ['a', name, device]:
                devlist.append((device, name))
            case ['and', 'a', name, device]:
                devlist.append((device, name))
            case _:
                raise ValueError(f'Unexpected group:  {group}')

    return devlist


def parse(line: str, facility: Facility, *, verbose: bool=True) -> None:
    '''
    The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
    The second floor contains a hydrogen generator.
    The second floor contains a cobalt generator, a curium generator, a ruthenium generator,
        and a plutonium generator.
    The third floor contains a lithium generator.
    The fourth floor contains nothing relevant.
    '''
    line = line.strip('.\n')
    match line.split():
        # Nothing:
        case ['The', floor, 'floor', 'contains', 'nothing', 'relevant']:
            if verbose:
                print(f'{floor.capitalize()} floor empty.')
        # One item:
        case ['The', floor, 'floor', 'contains', 'a', name, device]:
            if verbose:
                print(f'{floor.capitalize()} floor contains {device} - {name}.')
        # Two items:
        case ['The', floor, 'floor', 'contains', 'a', name1, device1, 'and', 'a', name2, device2]:
            if verbose:
                print(f'{floor.capitalize()} floor contains two devices:\n'
                      f'\t{device1} - {name1}\n'
                      f'\t{device2} - {name2}')
        # Multiple items:
        case ['The', floor, 'floor', 'contains', *devices]:
            devlist = get_devices(devices)
            if verbose:
                print(f'{floor.capitalize()} floor contains multiple devices:')
                for device, name in devlist:
                    print(f'\t{device} - {name}')
        # Error:
        case _:
            raise ValueError(f'Unexpected line:  {line}')


def main() -> None:
    cwd = Path(__file__).parent
    facility = Facility()
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line, facility)


if __name__ == '__main__':
    main()
