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
        if verbose:
            print(f'Round {rounds}')
        fabrications |= current

    return rounds


def main(verbose: bool=False) -> None:
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

    # Part 2:
    fabrications: set[str] = set()
    rounds = fabricate(molecule, replacements, fabrications)

    if verbose:
        # print(f'\nGenerated molecules:')
        # pprint(generated)
        print(f'\nFabricate molecules:')
        pprint(fabrications)
    # print(f'\nFound {len(generated)} distinct molecules.')
    print(f'\nFabricated {molecule} in {rounds} steps.')


if __name__ == '__main__':
    main()
