#! /usr/bin/env python3


'''
Perfect cookie recipe:
* Recipe uses 100 teaspoons of ingredients
* Take list of ingredients
* Each ingredient has:
    * capacity, durability, flavor, texture, calories
* Find total score of cookie by adding up each property and multiplying them
  together save calories:
    * ingredient_1_capacity * #_teaspoons + ingredient_2_capacity * #_teaspoons
      x ingredient_2_durability...
* Maximize score
* Note:  If any properties produce negative total, that becomes 0 causing that
         score to be 0.
'''


# INFILE = 'd15.txt'
INFILE = 'd15t1.txt'


# Libraries:
from dataclasses import dataclass
from functools import reduce
from operator import mul
from pprint import pprint


# Types:
@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse(line, ingredients):
    '''
    Example ingredient:
    Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    '''
    line = [s.strip(':,') for s in line.split()]
    name, _, capacity, _, durability, _, flavor, _, texture, _, calories = line
    ingredients.append(Ingredient(name=name, capacity=int(capacity), durability=int(durability),
                       flavor=int(flavor), texture=int(texture), calories=int(calories)))


def max_combo(ingredients):
    max_score = 0
    tsp = 100

    ingred1 = ingredients[0]
    ingred2 = ingredients[1]
    props = ('capacity', 'durability', 'flavor', 'texture')
    for i1 in range(1, tsp + 1):
        i2 = tsp - i1
        '''
        # Need to validate all results > 0:
        score = reduce(
            mul, (
                (getattr(ingred1, prop) * i1 + getattr(ingred2, prop) * i2)
                for prop in props
            )
        )
        '''
        properties = [
            getattr(ingred1, prop) * i1 + getattr(ingred2, prop) * i2
            for prop in props
        ]

        if all(prop > 0 for prop in properties):
            score = reduce(mul, properties)
            if score > max_score:
                max_score = score

    return max_score


def main():
    ingredients = []
    with open(INFILE) as infile:
        for line in infile:
            parse(line, ingredients)

    pprint(ingredients)

    res = max_combo(ingredients)

    print(f'Max score:  {res:,}')


if __name__ == '__main__':
    main()