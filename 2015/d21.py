#! /usr/bin/env python3


'''
RPG Simulator
* Battle between player and boss
* Player goes first - attacking, then boss attacks; repeat
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
from typing import NamedTuple
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from pprint import pprint


# Types:
@dataclass
class Character:
    name: str
    hp: int = 0
    damage: int = 0
    armor: int = 0


class Item(NamedTuple):
    offense: bool = True
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


def combat(player: Character, boss: Character) -> Character:
    while player.hp > 0 and boss.hp > 0:
        # Player attacks:
        boss.hp -= max(player.damage - boss.armor, 1)

        # Boss attacks:
        player.hp -= max(boss.damage - player.armor, 1)

    return boss if player.hp <= 0 else player


def main(verbose: bool=True) -> None:
    cwd = Path(__file__).parent
    boss = Character(name='boss')
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line, boss)

    player = Character(name='player', hp=100)

    weapons = {
        'dagger': Item(cost=8, damage=4),
        'shortsword': Item(cost=10, damage=5),
        'warhammer': Item(cost=25, damage=6),
        'longsword': Item(cost=40, damage=7),
        'greataxe': Item(cost=74, damage=8),
    }

    armor = {
        'leather': Item(offense=False, cost=13, armor=1),
        'chainmail': Item(offense=False, cost=31, armor=2),
        'splintmail': Item(offense=False, cost=53, armor=3),
        'bandedmail': Item(offense=False, cost=75, armor=4),
        'platemail': Item(offense=False, cost=102, armor=5),
    }

    rings = {
        'damage_ring1': Item(cost=25, damage=1),
        'damage_ring2': Item(cost=50, damage=2),
        'damage_ring3': Item(cost=100, damage=3),
        'defense_ring1': Item(offense=False, cost=20, armor=1),
        'defense_ring2': Item(offense=False, cost=40, armor=2),
        'defense_ring3': Item(offense=False, cost=80, armor=3)
    }

    store = weapons | armor | rings

    # Slightly inefficient as really want rings and remaining rings but not
    # sure how to do that.  Instead, just discard results with 2 of same ring:
    combinations = product(weapons, armor, rings, rings)

    options = {}
    for combination in combinations:
        # Discard duplicate rings - illegal combination:
        if combination[2] == combination[3]:
            continue

        cost = sum(store[item].cost for item in combination)
        offense = sum(store[item].damage for item in combination)
        defense = sum(store[item].armor for item in combination)

        # Conditions:
        ### player values must be >= what?
        ### boss.damage + boss.armor???

        # Duplicates - doesn't work:
        # options[(cost, offense, defense)] = combination
        options[combination] = (cost, offense, defense)

    if verbose:
        print('Boss:')
        pprint(boss)
        print('\nPlayer:')
        pprint(player)
        print('\nStore:')
        pprint(store)

    winner = combat(player, boss)

    print('Winner:')
    pprint(winner)


if __name__ == '__main__':
    main()
