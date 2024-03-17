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
INFILE = 'd11t1.txt'
# INFILE = 'd11t2.txt'


# Libraries:
from pathlib import Path


# Types:
class Facility:
    floors = {4: {'e': False, 'mcs': [], 'rtgs': []},
              3: {'e': False, 'mcs': [], 'rtgs': []},
              2: {'e': False, 'mcs': [], 'rtgs': []},
              1: {'e': True, 'mcs': [], 'rtgs': []}}

    def __str__(self):
        output = ''
        for floor, items in self.floors.items():
            e = '|Elevator|' if items['e'] else '|        |'
            mcs = ', '.join(items['mcs']) if items['mcs'] else 'None'
            rtgs = ', '.join(items['rtgs']) if items['rtgs'] else 'None'
            output += f'{floor}:  {e} Microchips - {mcs}, RTGs - {rtgs}\n'

        return output


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


def add(floor: str, devlist: list[tuple[str, str]], facility: Facility) -> None:
    for device, name in devlist:
        if device == 'microchip':
            target = 'mcs'
            # Remove trailing "-compatible":
            name = name.split('-')[0]
        elif device == 'generator':
            target = 'rtgs'
        else:
            raise ValueError(f'Expected mcs|rtgs, got:  {device}')
        match floor:
            case 'first':
                facility.floors[1][target].append(name)
            case 'second':
                facility.floors[2][target].append(name)
            case 'third':
                facility.floors[3][target].append(name)
            case 'fourth':
                facility.floors[4][target].append(name)
            case _:
                raise ValueError(f'Expected first|second|third|fourth, got:  {floor}')


def parse(line: str, facility: Facility, *, verbose: bool=True) -> None:
    '''
    Test Case:
    The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
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
            add(floor, [(device, name)], facility)
        # Two items:
        case ['The', floor, 'floor', 'contains', 'a', name1, device1, 'and', 'a', name2, device2]:
            if verbose:
                print(f'{floor.capitalize()} floor contains two devices:\n'
                      f'\t{device1} - {name1}\n'
                      f'\t{device2} - {name2}')
            add(floor, [(device1, name1), (device2, name2)], facility)
        # Multiple items:
        case ['The', floor, 'floor', 'contains', *devices]:
            devlist = get_devices(devices)
            if verbose:
                print(f'{floor.capitalize()} floor contains multiple devices:')
                for device, name in devlist:
                    print(f'\t{device} - {name}')
            add(floor, devlist, facility)
        # Error:
        case _:
            raise ValueError(f'Unexpected line:  {line}')


def process(facility: Facility) -> None:
    '''
    Algorithm:
    * Find MC/RTG pair on lowest floor and move to 4th floor
    * Repeat until everything on 4th floor
    '''
    steps = 0
    bottom = 1

    while bottom < 4:
        if pairs := set(facility.floors[bottom]['mcs']) & set(facility.floors[bottom]['rtgs']):
            pair = True
        else:
            for floor in range(bottom, 5):
                if pairs := set(facility.floors[bottom]['mcs']) & set(facility.floors[floor]['rtgs']):
                    pair = False
                    break
                raise RuntimeError('Error in algorithm - no match found.')

        # Next floor can't have mcs or if mc present, must be paired with its RTG:
        if pair and not facility.floors[bottom + 1]['mcs']:
            steps += 1
            target = pairs.pop()
            for device in ('mcs', 'rtgs'):
                facility.floors[bottom][device].remove(target)
                facility.floors[bottom + 1][device].append(target)
        else:
            ...


def main() -> None:
    cwd = Path(__file__).parent
    facility = Facility()
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line, facility)

    print(f'\nStart:\n{facility}')


if __name__ == '__main__':
    main()
