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
import math
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
    name: str
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
    'missile': Spell(name='missile', cost=53, damage=4),
    'drain': Spell(name='drain', cost=73, damage=2, heal=2),
    'shield': Spell(name='shield', cost=113, effect=True, turns=6, temp=True, armor=7),
    'poison': Spell(name='poison', cost=173, effect=True, turns=6, damage=3),
    'recharge': Spell(name='recharge', cost=229, effect=True, turns=5, mana=101),
}


def parse(line: str, boss: Character) -> None:
    match line.strip().split(':'):
        case ['Hit Points', num]:
            boss.hp = int(num)
        case ['Damage', num]:
            boss.damage = int(num)
        case _:
            raise ValueError(f'Unexpected Value:  {line.strip()}')


def process(effects: dict[str, Effect], boss: Character, player: Character,
            verbose: bool=True) -> None:
    effectq: deque[Effect] = deque()

    effectq.extend(effects.values())

    '''
    if verbose:
        print('Current effects:')
        pprint(effects)
    '''

    while effectq:
        effect = effectq.pop()

        boss.hp -= effect.damage
        player.mana += effect.mana
        effect.turns -= 1

        if effect.temp and effect.armor >= 1:
            player.armor = effect.armor if effect.turns >= 1 else 0

        if verbose:
            print(f'Processed effect {effect.name} - ', end='')
            if effect.turns >= 1:
                print(f'it will persist for {effect.turns} more turns.')
            else:
                print('effect expired.')

        if effect.turns == 0:
            effects.pop(effect.name)


def announce(cround: int, boss: Character, player: Character, current: Character) -> None:
    if current is player:
        print(f'\nRound {cround}')
        print('--Player Turn--')
    else:
        print('--Boss Turn--')

    print(f'Player:  {player}')
    print(f'Boss:  {boss}')


def combat_turn(boss: Character, player: Character, current: Character, cround: int,
                effects: dict[str, Effect], spell: Spell|None=None, verbose: bool=True) -> None:
    if effects:
        process(effects, boss, player)
    elif verbose:
        print(f'No effects present for Player turn, round {cround}.')

    if current is player:
        if spell:
            if verbose:
                print(f'Player casts {spell.name}...')

            if spell.effect:
                effects[spell.name] = Effect(name=spell.name, turns=spell.turns, temp=spell.temp,
                                            damage=spell.damage, armor=spell.armor, mana=spell.mana)
            else:
                boss.hp -= spell.damage
                player.hp += spell.heal
        else:
            raise ValueError('Attempt to execute player turn without passing spell!')


def attack(player: Character, boss: Character) -> bool:
    damage = 0

    crounds = math.ceil(player.hp/boss.damage)
    effect_turns = 2 * crounds - 1

    spells['poison'].damage


def get_spells(player: Character, boss: Character) -> tuple[str]:
    '''
    Come up with list of spells for player to cast

    Goal:  Calculate the least amount of mana player can spend and still win the
           fight.
    Notes:
        * Do not include mana recharge effects as "spending" negative mana.
        * Attack via spells which cost mana - if don't have enough mana, player
          loses

    Use player hp, boss hp, and boss damage for calculations.
    Intertwined tasks:
        1) Calculate spells to kill boss before he kills player
        2) Ensure have sufficient mana for spells
        3) If insufficient mana must factor in using recharge

    Initial strategy:
    * Attack until either run out of mana or die - win?
    * No, then...
    '''
    # Start with examples - this routine should come up with same spells.
    works = attack(player, boss)

    # Need to return tuple of spells for player to cast...


def combat(boss: Character, player: Character, casts: tuple[str, ...],
           verbose: bool=True) -> tuple[Character, int]:
    cround = 0
    mana_total = 0
    effects: dict[str, Effect] = {}

    while player.hp > 0 and boss.hp > 0:
        cround += 1

        # Player turn::
        if verbose:
            announce(cround, boss, player, player)

        spell = spells[casts[cround - 1]]
        if not spell:
            raise ValueError('Attempted combat round without supplying player spell!')

        mana_total += spell.cost
        player.mana -= spell.cost
        if player.mana < 0:
            raise ManaOut(f'Player has insufficient mana to cast {spell.name} ({player.mana})'
                          ' - game over!')

        combat_turn(boss, player, player, cround, effects, spell)

        # Boss turn:
        if verbose:
            announce(cround, boss, player, boss)

        combat_turn(boss, player, boss, cround, effects)

        if boss.hp <= 0:
            break

        player.hp -= (boss_damage := max(boss.damage - player.armor, 1))

        if verbose:
            print(f'Boss attacks for {boss_damage}')

    winner = boss if player.hp <= 0 else player

    if verbose:
        print('\nFinal stats:')
        print(f'Player:  {player}')
        print(f'Boss:  {boss}')

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
    # boss = Character(name='boss', hp=13, damage=8)
    boss = Character(name='boss', hp=14, damage=8)
    # casts = ('poison', 'missile')
    # casts = ('recharge', 'shield', 'drain', 'poison', 'missile')

    if verbose:
        print(f'Player:  {player}')
        print(f'Boss:  {boss}')
        print('Spells:')
        pprint(spells)

    try:
        winner, mana_total = combat(boss, player)
    except ManaOut as err:
        print(err)

    print(f'\nWinner:  {winner}')
    print(f'Player expended {mana_total} mana.')


if __name__ == '__main__':
    main()
