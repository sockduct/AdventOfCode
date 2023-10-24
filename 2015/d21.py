#! /usr/bin/env python3


'''
RPG Simulator
* Battle between player and boss
* Player goes first - attacking, then boss attacks
* Damage per attack = attacker's damage score - defender's armor score but
  always at least 1
* Whoever gets to 0 hit points first loses

Player starts with 0 damage, 0 armor, 100 hit points, and unlimited gold
* Can buy anything from store but store only has one of each item
* Must buy exactly one weapon
* Can optionally buy one armor
* Can optionally buy one or two rings

Store:
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3

What is the least amount of gold the player can spend and still win?
'''


INFILE = 'd21.txt'


# Libraries:
from enum import Enum
from typing import NamedTuple
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint


# Types:
class Armament(Enum):
    offense = 1
    defense = 2


@dataclass
class Character:
    hp: int = 0
    damage: int = 0
    armor: int = 0


class Item(NamedTuple):
    type: Armament
    cost: int = 0
    damage: int = 0
    armor: int = 0


def parse(line: str, boss: Character) -> None:
    match line.strip().split(':'):
        case ['Hit Points', num]:
            boss.hp = int(num)
        case ['Damage', num]:
            boss.damage = int(num)
        case ['Armor', num]:
            boss.armor = int(num)
        case _:
            raise ValueError(f'Unexpected Value:  {line.strip()}')


def main() -> None:
    cwd = Path(__file__).parent
    boss = Character()
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line, boss)

    player = Character(hp=100)

    store = {
        dagger=Item(type=offense, cost=8, damage=4),
        shortsword=Item(type=offense, cost=10, damage=5),
        warhammer=Item(type=offense, cost=25, damage=6),
        longsword=Item(type=offense, cost=40, damage=7),
        greataxe=Item(type=offense, cost=74, damage=8),
        leather=Item(type=defense, cost=13, armor=1),
        chainmail=Item(type=defense, cost=31, armor=2),
        splintmail=Item(type=defense, cost=53, armor=3),
        bandedmail=Item(type=defense, cost=75, armor=4),
        platemail=Item(type=defense, cost=102, armor=5),
        damage_ring1=Item(type=offense, cost=25, damage=1),
        damage_ring2=Item(type=offense, cost=50, damage=2),
        damage_ring3=Item(type=offense, cost=100, damage=3),
        defense_ring1=Item(type=defense, cost=20, armor=1),
        defense_ring2=Item(type=defense, cost=40, armor=2),
        defense_ring3=Item(type=defense, cost=80, armor=3)
    }

    print('Boss:')
    pprint(boss)
    print('\nPlayer:')
    pprint(player)
    print('\nStore:')
    pprint(store)


if __name__ == '__main__':
    main()
