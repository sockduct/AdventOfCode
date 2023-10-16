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


# INFILE = 'd19.txt'
INFILE = 'd19t1.txt'


# Libraries:
from pathlib import Path
from pprint import pprint


def parse(line: str, replacements: dict[str, str], molecule) -> None | str:
    match line.split():
        case [mol1, '=>', mol2]:
            replacements[mol1] = mol2
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
    ...


def main(verbose: bool=True) -> None:
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
        print(f'Generated molecules:')
        pprint(generated)
    print(f'Found {len(generated)} distinct molecules')


if __name__ == '__main__':
    main()
