#! /usr/bin/env python3


'''
Medicine for Rudolph
* Given replacement sequences:
    * e.g., H => HO
* Given starting molecule:
    * e.g., HOH
* Figure out what molecules could be generated with single replacement step:
    * e.g., HOH => HOOH, HOHO
'''


INFILE = 'd19.txt'
# INFILE = 'd19t1.txt'
# INFILE = 'd19t2.txt'
# INFILE = 'd19t1a.txt'
# INFILE = 'd19t2a.txt'


# Libraries:
from copy import copy
from pathlib import Path
from pprint import pprint
import re


def parse(line: str, replacements: dict[str, list[str]], molecule) -> None | str:
    match line.split():
        case [mol1, '=>', mol2]:
            if mol1 not in replacements:
                replacements[mol1] = [mol2]
            # Always make values a list to simplify logic:
            # elif not isinstance(replacements[mol1], list):
            #    replacements[mol1] = [replacements[mol1], mol2]
            else:
                replacements[mol1].append(mol2)
        case [mol]:
            if not molecule:
                return mol
            else:
                raise RuntimeError(f'molecule value already assigned ({molecule}) - '
                                   f'can\'t assign {mol}')
        case []:
            # Empty line - OK
            pass
        case _:
            raise ValueError(f'Unexpected value:  {line.split()}')

    # To make mypy happy:
    return None


def generate(molecule: str, replacements: dict[str, list[str]], generated: set[str]) -> None:
    # for index, element in enumerate(molecule):
    for match_obj in re.finditer(r'[A-Z][a-z]?|e', molecule):
        element = match_obj.group()
        if element in replacements:
            for replacement in replacements[element]:
                generated.add(molecule[:match_obj.span()[0]] + replacement +
                              molecule[match_obj.span()[1]:])


def revert(molecule: str, inverses: dict[str, str]) -> int:
    target = 'e'
    new_molecule = molecule
    rounds = 0

    while new_molecule != target:
        # Start with most complex molecules first:
        options = sorted(inverses.keys(), key=len, reverse=True)

        for option in options:
            size = len(option)
            start = 0
            while (index := new_molecule.find(option, start)) >= 0:
                new_molecule = (new_molecule[:index] + inverses[option] +
                                new_molecule[index + size:])
                start = index + size
                rounds += 1

    return rounds


def fabricate(molecule: str, replacements: dict[str, list[str]], fabrications: set[str],
              verbose: bool=True) -> int:
    rounds = 0
    seed = {'e'}
    current: set[str] = set()

    while molecule not in fabrications:
        targets = copy(current) if current else copy(seed)
        for target in targets:
            generate(target, replacements, current)
        rounds += 1
        fabrications |= current
        if verbose:
            print(f'Round {rounds}, number of fabrications:  {len(fabrications):,}')

    return rounds


def main(verbose: bool=True) -> None:
    mydir = Path(__file__).parent
    replacements: dict[str, list[str]] = {}
    molecule = ''

    with open(mydir/INFILE) as infile:
        for line in infile:
            if res := parse(line.strip(), replacements, molecule):
                molecule = res

    if verbose:
        print('Replacements:')
        pprint(replacements)
        print('\nMolecule:')
        pprint(molecule)

    # Part 1:
    # generated: set[str] = set()
    # generate(molecule, replacements, generated)

    # Reverse the direction in replacements:
    inverses: dict[str, str] = {}
    for key, values in replacements.items():
        for value in values:
            inverses[value] = key

    if verbose:
        print(f'\nInverses ({len(inverses)}):')
        pprint(inverses)

    # Part 2:
    # Doesn't work - way too slow, go in reverse direction
    # fabrications: set[str] = set()
    # rounds = fabricate(molecule, replacements, fabrications)

    rounds = revert(molecule, inverses)

    # if verbose:
        # print(f'\nGenerated molecules:')
        # pprint(generated)
        # print(f'\nFabricated molecules:')
        # pprint(fabrications)
    # print(f'\nFound {len(generated)} distinct molecules.')
    # print(f'\nFabricated {molecule} in {rounds} steps.')
    print(f'\nFrom {molecule} to e in {rounds} steps.')


if __name__ == '__main__':
    main()
