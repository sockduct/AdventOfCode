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
        'Age fish a day, reset and procreate after age < 0'
        self.age -= 1
        if self.age == -1:
            self.age = LatternFish.STARTING_AGE
            return True
        return False

def main(verbose=False):
    with open(INFILE) as ifile:
        fish_ages = ''.join(ifile.read().strip().split(','))

    # fish = [LatternFish(fish_age) for fish_age in fish_ages]

    DAYS = 18
    # DAYS = 80
    # Doesn't work for large numbers because this is a quadratic algorithm:
    # DAYS = 256
    new_fish = 0
    for day in range(DAYS + 1):
        if day == 0:
            # print(f'Initial state:  {", ".join(map(str, fish))}')
            print(f'Initial state:  {fish_ages}')
        else:
            '''
            new_fish = sum(lf.inc() for lf in fish)
            for _ in range(new_fish):
                fish.append(LatternFish())
            if verbose:
                daystr = 'days' if day > 1 else 'day'
                print(f'After {day:2} {daystr:4}:  {", ".join(map(str, fish))}')
            elif day == 1:
                print('Days:  ', end='')
            elif day % 10 == 0:
                print(f'{day}', end='', flush=True)
            else:
                print('.', end='', flush=True)
            '''
            if new_fish:
                fish_ages += '9' * new_fish
            diff_num = '1' * len(fish_ages)
            fish_ages = str(int(fish_ages) - int(diff_num))
            zeroes = fish_ages.count('0')
            if zeroes:
                fish_ages = fish_ages.replace('0', '7')
                new_fish = zeroes

            daystr = 'days' if day > 1 else 'day'
            print(f'After {day:2} {daystr:4}:  {fish_ages}')

    # print(f'Lattern Fish Total:  {len(fish)}')
    print(f'Lattern Fish Total:  {len(fish_ages)}')

if __name__ == '__main__':
    main()
