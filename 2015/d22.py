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
from enum import Enum
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


class SpellCatalog(Enum):
    MISSILE = 'missile'
    DRAIN = 'drain'
    SHIELD = 'shield'
    POISON = 'poison'
    RECHARGE = 'recharge'


def parse(line: str, boss: Character) -> None:
    match line.strip().split(':'):
        case ['Hit Points', num]:
            boss.hp = int(num)
        case ['Damage', num]:
            boss.damage = int(num)
        case _:
            raise ValueError(f'Unexpected Value:  {line.strip()}')


def get_turns(player: Character, boss: Character, effects: dict[str, Effect],
              hard: bool=False) -> int:
    hp = player.hp
    armor = player.armor
    turns = 1
    shield_turns = effects['shield'].turns if 'shield' in effects else 0

    while True:
        # Pre-round
        if hard:
            hp -= 1

        # Player turn effect and boss turn effect (x2):
        shield_turns -= 2
        if shield_turns <= 0:
            armor = 0

        # Boss turn
        hp -= max(boss.damage - armor, 1)
        if hp <= 0:
            return turns

        if hard and hp == 1:
            return turns

        turns += 1


def get_damage(player: Character, effects: dict[str, Effect], turns: int) -> int:
    damage = 0
    mana = player.mana
    poison_turns = effects['poison'].turns if 'poison' in effects else 0

    for _ in range(turns):
        if poison_turns > 0:
            if poison_turns == 1:
                damage += spells['poison'].damage
                poison_turns -= 1
            else:
                damage += spells['poison'].damage * 2
                poison_turns -= 2

            if mana >= spells['missile'].cost:
                mana -= spells['missile'].cost
                damage += spells['missile'].damage
        elif mana >= spells['poison'].cost:
            mana -= spells['poison'].cost
            poison_turns += spells['poison'].turns

            # For boss turn:
            damage += spells['poison'].damage
            poison_turns -= 1
        elif mana >= spells['missile'].cost:
            mana -= spells['missile'].cost
            damage += spells['missile'].damage
        else:
            return damage

    return damage


def get_spell(player: Character, boss: Character, effects: dict[str, Effect],
              hard: bool=False) -> Spell:
    # When do we need to call recharge?
    # * Find mana threshold
    # When do we need to call drain?
    # * Find hp threshold
    remaining_turns = get_turns(player, boss, effects, hard)
    max_damage = get_damage(player, effects, remaining_turns)

    if (
        max_damage >= boss.hp and ('poison' not in effects or effects['poison'].turns == 1)
        and (player.mana >= spells['poison'].cost + (remaining_turns - 1) * spells['missile'].cost
             or 'recharge' in effects and player.mana + spells['recharge'].mana *
             spells['recharge'].turns >= spells['poison'].cost + (remaining_turns - 1)
             * spells['missile'].cost
        ) and (
            'poison' not in effects and spells['missile'].damage * remaining_turns < boss.hp
            or 'poison' in effects and spells['missile'].damage * remaining_turns +
            spells['poison'].damage * spells['poison'].turns < boss.hp
        )
    ):
        return spells['poison']
    elif max_damage >= boss.hp:
        return spells['missile']
    elif (
        remaining_turns >= 3 and ('poison' not in effects or effects['poison'].turns == 1)
        and (
            player.mana >= spells['poison'].cost + spells['recharge'].cost or
            'recharge' in effects and player.mana + spells['recharge'].mana *
            spells['recharge'].turns >= spells['poison'].cost + spells['recharge'].cost
        )
    ):
        return spells['poison']
    elif (
        'recharge' not in effects and player.mana < spells['poison'].cost +
        spells['recharge'].cost
    ):
        return spells['recharge']
    elif 'shield' not in effects or effects['shield'].turns == 1:
        return spells['shield']
    elif (
        'poison' in effects and boss.hp - spells['poison'].damage * 2 -
        spells['missile'].damage <= 0
    ):
        return spells['missile']
    elif player.hp - max(boss.damage - spells['shield'].armor, 1) <= 0:
        return spells['drain']
    elif 'poison' not in effects:
        return spells['poison']
    else:
        return spells['missile']


def simulate(casts: deque[str], player: Character, boss: Character, hard: bool=False,
             verbose: bool=False) -> tuple[bool, str|object]:
    '''
    Simulate combat.
    Return status:
    * True = Player won, empty string
    * False = Player lost, string in ('mana', 'hp) - what player ran out of
    '''
    cround = 0
    test_player = Character(name=player.name, hp=player.hp, mana=player.mana)
    test_boss = Character(name=boss.name, hp=boss.hp, damage=boss.damage)
    effects: dict[str, Effect] = {}

    while test_player.hp > 0 and test_boss.hp > 0:
        cround += 1
        # spell = get_spell(test_player, test_boss, effects, hard)
        # casts.append(spell.name)
        if casts:
            spell = spells[casts.popleft()]
        else:
            return False, 'nospell'

        try:
            _ = combat_round(test_boss, test_player, effects, spell, cround, hard, verbose, True)
        except ManaOut:
            # return False, 'mana', casts
            return False, 'mana'

    # return (False, 'hp', casts) if test_player.hp <= 0 else (True, '', casts)
    return (False, 'hp') if test_player.hp <= 0 else (True, test_player.mana)


def get_spells(casts: list[str], player: Character, boss: Character,
               solutions: set[tuple[str, ...]], castpos: int, castmax: int,
               hard: bool=False, verbose: bool=False) -> None:
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
    * Too complex...

    Brute force approach:
    Best path:  Poison -> Recharge -> Shield -> Poison -> Recharge -> Drain ->
                Poison -> Drain -> Magic Missile

    Back track approach:
    * Find solution and save
    * Backtrack to shield and try drain instead?

    Solution - follow brute force/backtracking using backtracking algorithm from
    The Algorithm Design Manual 3rd edition, Ch. 9
    '''
    # Start with examples - this routine should come up with same spells.
    for spell in SpellCatalog:
        # Limit growth:
        if castpos >= castmax:
            break

        if len(casts) == castpos:
            casts.append(spell.value)
        else:
            casts[castpos] = spell.value

        if len(casts) == 2:
            print(f'{casts=}')

        won, data = simulate(deque(casts), player, boss, hard, verbose)

        if won:
            if verbose:
                print(f'Found solution using {data} mana:  {casts}')

            solutions.add(tuple(casts))
        else:
            # Failed branch - next:
            if data in ('hp', 'mana'):
                continue

            # Otherwise keeping looking:
            if casts:
                castpos += 1

            get_spells(casts, player, boss, solutions, castpos, castmax, hard, verbose)
            castpos -= 1

    # None of the spells worked:
    if casts:
        casts.pop()


def get_spells2(casts: list[str], solutions: set[tuple[str, ...]],
                castpos: int, castmax: int, verbose: bool=False) -> None:
    for spell in SpellCatalog:
        # Limit growth:
        if castpos >= castmax:
            break

        if len(casts) == castpos:
            casts.append(spell.value)
        else:
            casts[castpos] = spell.value

        solutions.add(tuple(casts))

        if casts:
            castpos += 1

        get_spells2(casts, solutions, castpos, castmax, verbose)
        castpos -= 1

    # None of the spells worked:
    if casts:
        casts.pop()


def process(effects: dict[str, Effect], boss: Character, player: Character,
            verbose: bool=False) -> None:
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
                effects: dict[str, Effect], spell: Spell|None=None, verbose: bool=False,
                simulate_turn: bool=False) -> None:
    if effects:
        process(effects, boss, player, verbose=verbose)
    elif verbose:
        print(f'No effects present for Player turn, round {cround}.')

    if current is player:
        if spell:
            if verbose:
                print(f'Player casts {spell.name}...')

            if spell.effect and spell.name not in effects:
                effects[spell.name] = Effect(name=spell.name, turns=spell.turns, temp=spell.temp,
                                            damage=spell.damage, armor=spell.armor, mana=spell.mana)
            elif spell.effect:
                if not simulate_turn:
                    raise RuntimeError('Attempt to cast spell with effect that\'s already active!')
                return

            else:
                boss.hp -= spell.damage
                player.hp += spell.heal
        else:
            raise ValueError('Attempt to execute player turn without passing spell!')


def combat_round(boss: Character, player: Character, effects: dict[str, Effect], spell: Spell,
                 cround: int, hard: bool=False, verbose: bool=False,
                 simulate_round: bool=False) -> int:
    mana = 0

    # Player turn::
    if verbose:
        announce(cround, boss, player, player)

    if hard:
        player.hp -= 1
        if player.hp <= 0:
            if verbose:
                print('Player dies in pre-round.')
            return mana

    mana += spell.cost
    player.mana -= spell.cost
    if player.mana < 0:
        raise ManaOut(f'Player has insufficient mana to cast {spell.name} ({player.mana})'
                        ' - game over!')

    combat_turn(boss, player, player, cround, effects, spell, verbose, simulate_round)
    if boss.hp <= 0:
        if verbose:
            print('Boss dies from player attack.')
        return mana

    # Boss turn:
    if verbose:
        announce(cround, boss, player, boss)

    combat_turn(boss, player, boss, cround, effects, spell=None, verbose=verbose)
    if boss.hp <= 0:
        if verbose:
            print('Boss dies from effect.')
        return mana

    player.hp -= (boss_damage := max(boss.damage - player.armor, 1))

    if verbose:
        print(f'Boss attacks for {boss_damage}')

    return mana


def combat(boss: Character, player: Character, casts: tuple[str, ...],
           hard: bool=False, verbose: bool=False) -> tuple[Character, int]:
    cround = 0
    mana_total = 0
    effects: dict[str, Effect] = {}

    while player.hp > 0 and boss.hp > 0:
        cround += 1
        spell = spells[casts[cround - 1]]
        mana_total += combat_round(boss, player, effects, spell, cround, hard, verbose)

    winner = boss if player.hp <= 0 else player

    if verbose:
        print('\nFinal stats:')
        print(f'Player:  {player}')
        print(f'Boss:  {boss}')

    return winner, mana_total


def get_best(solutions: set[tuple[str, ...]], verbose: bool=False) -> tuple[str, ...]:
    spell_sets = {}
    for solution in solutions:
        mana_total = sum(spells[spell].cost for spell in solution)
        spell_sets[mana_total] = solution

    if verbose:
        print('Valid spell sequences for player win:')
        pprint(spell_sets, width=120)

    least_mana = sorted(spell_sets.keys())[0]
    return spell_sets[least_mana]


def main() -> None:
    # Overall program settings:
    verbose = False
    hard = True

    cwd = Path(__file__).parent
    boss = Character(name='boss')
    with open(cwd/INFILE) as infile:
        for line in infile:
            parse(line, boss)

    player = Character(name='player', hp=50, mana=500)

    # Testing:
    # player = Character(name='player', hp=10, mana=250)
    # player = Character(name='player', hp=20, mana=250)
    # boss = Character(name='boss', hp=13, damage=8)
    # boss = Character(name='boss', hp=14, damage=8)
    # boss = Character(name='boss', hp=24, damage=8)
    # casts = ('poison', 'missile')
    # casts = ('recharge', 'shield', 'drain', 'poison', 'missile')

    casts = []
    castpos = 0
    castmax = 10
    solutions = set()
    get_spells(casts, player, boss, solutions, castpos, castmax, hard, verbose)
    # get_spells2(casts, solutions, castpos, castmax, verbose)

    verbose = True
    # Choose best solution:
    casts = get_best(solutions, verbose)
    '''
    if verbose:
        print(f'{len(solutions)} valid spell sequences for player win:')
        pprint(solutions, width=120)
    '''

    if verbose:
        print(f'Player:  {player}')
        print(f'Boss:  {boss}')
        print('Spells:')
        pprint(spells)

    try:
        winner, mana_total = combat(boss, player, casts, hard, verbose)
    except ManaOut as err:
        print(err)

    print(f'\nWinner:  {winner}')
    print(f'Player expended {mana_total} mana.')


if __name__ == '__main__':
    main()
