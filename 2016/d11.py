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

Extra comment with additional notes...
'''


# INFILE = 'd11.txt'
INFILE = 'd11t1.txt'
# INFILE = 'd11t2.txt'


# Libraries:
from pathlib import Path


# Types:
class Facility:
    '''
    This is like a singleton as it's using a class-level variable.

    Only need one data structure for challenge, so not bothering with setting
    up instances.
    '''
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

    def empty(self, level: int) -> bool:
        return not self.floors[level]['mcs'] and not self.floors[level]['rts']

    def set(self, mc_level: int, rtg_level: int=-1, *, bounds=True) -> set:
        if rtg_level == -1:
            rtg_level = mc_level

        if not 1 <= mc_level <= 4 or not 1 <= rtg_level <= 4:
            if bounds:
                raise IndexError(f'Expect floor from 1 - 4, got ({mc_level}, {rtg_level}).')
            else:
                return None

        return set(self.floors[mc_level]['mcs']) & set(self.floors[rtg_level]['rtgs'])


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


def move(facility: Facility, target: str, device: str, current: int, new: int) -> None:
    if device == 'both':
        devices = ('mcs', 'rtgs')
    elif device == 'mcs':
        devices = ('mcs',)
    elif device == 'rtgs':
        devices = ('rtgs',)
    else:
        raise ValueError(f'Expected mcs|rtgs|both, got:  {device}')

    for device in devices:
        facility.floors[current][device].remove(target)
        facility.floors[new][device].append(target)

    facility.floors[current]['e'] = False
    facility.floors[new]['e'] = True


def process(facility: Facility, verbose: bool=True) -> int:
    '''
    Algorithm - until everything on 4th floor:
    1) Find MC/RTG pair on lowest floor or 2nd to lowest or ...
        a) If no stand-alone MCs on next floor,
        b) And, no unpaired RTGs on current floor, move pair up
    2) Find RTGs on 2nd to lowest floor or 3rd to lowest or ...
        a) If matching MC on lowest floor, move MC up
    '''
    steps = 0
    bottom = 1

    ### Need way to deal with elevator
    while bottom < 4:
        matched_case = False
        for floor in range(bottom, 4):
            # Use case 1
            if (
                (pairs := facility.set(floor)) and
                not facility.floors[floor + 1]['mcs'] and
                not (set(facility.floors[floor]['rtgs']) - pairs)
            ):
                target = pairs.pop()
                move(facility, target, 'both', floor, floor + 1)
                steps += 1
                matched_case = True
                if verbose:
                    print(f'Current State:\n{facility}')
            # Use case 2
            elif (
                (pairs := facility.set(floor, floor + 1)) or
                (pairs := facility.set(floor, floor + 2, bounds=False))
            ):
                target = pairs.pop()
                move(facility, target, 'mcs', floor, floor + 1)
                steps += 1
                matched_case = True
                if verbose:
                    print(f'Current State:\n{facility}')

        if not matched_case:
            raise RuntimeError('Error in algorithm - no match found.')

        if facility.empty(bottom):
            bottom += 1

    return steps


def main() -> None:
    cwd = Path(__file__).parent
    facility = Facility()
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line, facility)

    print(f'\nStart:\n{facility}')
    steps = process(facility)

    print(f'\nTook {steps:,} steps.')


if __name__ == '__main__':
    main()
