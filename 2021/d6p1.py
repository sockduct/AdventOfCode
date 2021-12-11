#! /usr/bin/env python3.10

INFILE = 'd6p1t1.txt'
# INFILE = 'd6p1.txt'

class LatternFish():
    DEFAULT_NEW_AGE = 8
    STARTING_AGE = 6

    def __init__(self, age=DEFAULT_NEW_AGE):
        self.age = age

    def __repr__(self):
        return f'<LatternFish(age={self.age})>'

    def __str__(self):
        return f'{self.age}'

    def inc(self):
        self.age -= 1
        if self.age == 0:
            self.age = LatternFish.STARTING_AGE

def main():
    with open(INFILE) as ifile:
        fish_ages = [int(age) for age in ifile.read().strip().split(',')]

    fish = [LatternFish(fish_age) for fish_age in fish_ages]

    for day in range(19):
        if day == 0:
            print(f'Initial state:  {", ".join(map(str, fish))}')
        else:
            daystr = 'days' if day > 1 else 'day'
            print(f'After {day:2} {daystr:4}:  {", ".join(map(str, fish))}')

if __name__ == '__main__':
    main()
