#! /usr/bin/env python3.10

INFILE = 'd6p1t1.txt'
# INFILE = 'd6p1.txt'

'''
Lots of thought and effort to improve upon d6p1 approach and this is actually
slower!!!
'''
def main(verbose=False):
    with open(INFILE) as ifile:
        fish_ages = ''.join(ifile.read().strip().split(','))

    # DAYS = 18
    # DAYS = 80
    DAYS = 256
    new_fish = 0
    for day in range(DAYS + 1):
        if day == 0:
            print(f'Initial state:  {", ".join(fish_ages)}')
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
            new_fish = 0
            zeroes = fish_ages.count('0')
            if zeroes:
                fish_ages = fish_ages.replace('0', '7')
                new_fish = zeroes
            if new_fish:
                fish_ages += '9' * new_fish
            diff_num = '1' * len(fish_ages)
            fish_ages = str(int(fish_ages) - int(diff_num))
            if len(fish_ages) < len(diff_num):
                fish_ages = '0' * (len(diff_num) - len(fish_ages)) + fish_ages

            if verbose:
                daystr = 'days' if day > 1 else 'day'
                print(f'After {day:2} {daystr:4}:  {fish_ages}')
            elif day == 1:
                print('Days:  ', end='')
            elif day % 10 == 0:
                print(f'{day}', end='', flush=True)
            else:
                print('.', end='', flush=True)

    print(f'Lattern Fish Total:  {len(fish_ages)}')

if __name__ == '__main__':
    main()
