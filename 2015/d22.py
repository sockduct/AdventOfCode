#! /usr/bin/env python3


'''
Wizard Simulator
* Take turns attacking - 1st player, then boss
* Note:  Boss' attacks always do at least 1 damage
* Attack via spells which cost mana - if don't have enough mana, player loses
* What is the least amount of mana you can spend and still win the fight? (Do
  not include mana recharge effects as "spending" negative mana.)

Spells:
* Magic Missile - costs 53 mana, instant, 4 damage
* Drain - costs 73 mana, instant, 2 damage, heals 2 hit points
* Shield - costs 113 mana, effect, 6 turns, increases armor by 7
* Poison - costs 173 mana, effect, 6 turns, 3 damage
* Recharge - costs 229 mana, effect, 5 turns, increases mana by 101
'''


INFILE = 'd22.txt'


# Libraries:
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import NamedTuple


# Types:
@dataclass
class Character:
    name: str
    hp: int = 0
    armor: int = 0
    damage: int = 0
    mana: int = 0


# Using NamedTuple because immutable:
class Spell(NamedTuple):
    effect: bool = False
    temp: bool = False
    turns: int = 0
    cost: int = 0
    damage: int = 0
    armor: int = 0
    heal: int = 0
    mana: int = 0


@dataclass
class Effect:
    name: str
    turns: int = 0
    temp: bool = False
    damage: int = 0
    armor: int = 0
    mana: int = 0


class ManaOut(BaseException):
    pass


# Globals:
spells = {
    'missile': Spell(cost=53, damage=4),
    'drain': Spell(cost=73, damage=2, heal=2),
    'shield': Spell(cost=113, effect=True, turns=6, temp=True, armor=7),
    'poison': Spell(cost=173, effect=True, turns=6, damage=3),
    'recharge': Spell(cost=229, effect=True, turns=5, mana=101),
}


def parse(line: str, boss: Character) -> None:
    match line.strip().split(':'):
        case ['Hit Points', num]:
            boss.hp = int(num)
        case ['Damage', num]:
            boss.damage = int(num)
        case _:
            raise ValueError(f'Unexpected Value:  {line.strip()}')


def process(effects: dict[int, Effect], boss: Character, player: Character,
            verbose: bool=True) -> None:
    effectq: deque[tuple[int, Effect]] = deque()

    effectq.extend(effects.items())

    while effectq:
        index, effect = effectq.pop()

        if verbose:
            print(f'Processing effect {effect}...')

        boss.hp -= effect.damage
        player.mana += effect.mana
        effect.turns -= 1
        player.armor = effect.armor if effect.temp and effect.armor >= 1 else 0

        if effect.turns == 0:
            effects.pop(index)


def combat(boss: Character, player: Character, casts: tuple[str, ...],
           verbose: bool=True) -> tuple[Character, int]:
    turn = 0
    mana_total = 0
    effects: dict[int, Effect] = {}

    while player.hp > 0 and boss.hp > 0:
        turn += 1

        # Player attacks:
        spell_name = casts[turn - 1]
        spell = spells[spell_name]

        mana_total += spell.cost
        player.mana -= spell.cost
        if player.mana < 0:
            raise ManaOut(f'Player has insufficient mana to cast {spell_name} ({player.mana})'
                          ' - game over!')

        if verbose:
            print(f'\nTurn {turn}')

        if effects:
            process(effects, boss, player)
        elif verbose:
            print(f'No effects present for Player turn {turn}.')

        if verbose:
            print(f'Player casts {spell_name}...')

        if spell.effect:
            index = len(effects)
            effects[index] = Effect(name=spell_name, turns=spell.turns, temp=spell.temp,
                                    damage=spell.damage, armor=spell.armor, mana=spell.mana)
        else:
            boss.hp -= spell.damage
            player.hp += spell.heal

        # Boss turn:
        if effects:
            process(effects, boss, player)
        elif verbose:
            print(f'No effects present for Boss turn {turn}.')

        if boss.hp <= 0:
            break
        elif verbose:
            print('Boss attacks...')

        player.hp -= max(boss.damage - player.armor, 1)

        # End of turn:
        if verbose:
            print(f'End of turn {turn}\nPlayer:  {player}\nBoss:  {boss}')

    winner = boss if player.hp <= 0 else player

    return winner, mana_total


def main(verbose: bool=True) -> None:
    '''
    cwd = Path(__file__).parent
    boss = Character(name='boss')
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line, boss)

    player = Character(name='player', hp=50, mana=500)
    '''

    # Testing:
    player = Character(name='player', hp=10, mana=250)
    boss = Character(name='boss', hp=13, damage=8)
    casts = ('poison', 'missile')

    if verbose:
        print(f'Player:  {player}')
        print(f'Boss:  {boss}')
        print('Spells:')
        pprint(spells)

    try:
        winner, mana_total = combat(boss, player, casts)
    except ManaOut as err:
        print(err)

    if verbose:
        print(f'\nPlayer:  {player}\nBoss:  {boss}')
    print(f'\nWinner:  {winner}')
    print(f'Player expended {mana_total} mana.')


if __name__ == '__main__':
    main()
