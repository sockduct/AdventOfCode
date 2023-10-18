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


# Libraries:
from pathlib import Path
from pprint import pprint
import re


def parse(line: str, replacements: dict[str, str], molecule) -> None | str:
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


def generate(molecule: str, replacements: dict[str, str], generated: set[str]) -> None:
    # for index, element in enumerate(molecule):
    for match_obj in re.finditer(r'[A-Z][a-z]?', molecule):
        element = match_obj.group()
        if element in replacements:
            for replacement in replacements[element]:
                generated.add(molecule[:match_obj.span()[0]] + replacement +
                              molecule[match_obj.span()[1]:])


def main(verbose: bool=False) -> None:
    mydir = Path(__file__).parent
    replacements: dict[str, str] = {}
    molecule = ''

    with open(mydir/INFILE) as infile:
        for line in infile:
            res = parse(line.strip(), replacements, molecule)
            if res:
                molecule = res

    if verbose:
        print('Replacements:')
        pprint(replacements)
        print('\nMolecule:')
        pprint(molecule)

    generated: set[str] = set()
    res = generate(molecule, replacements, generated)

    if verbose:
        print(f'\nGenerated molecules:')
        pprint(generated)
    print(f'\nFound {len(generated)} distinct molecules')


if __name__ == '__main__':
    main()
