#! /usr/bin/env python3.10

# INFILE = 'd6p1t1.txt'
INFILE = 'd6p1.txt'

def main(verbose=False):
    with open(INFILE) as ifile:
        fish_ages = [int(age) for age in ifile.read().strip().split(',')]

    lfish = {k: 0 for k in range(9)}
    for fish_age in fish_ages:
        lfish[fish_age] += 1

    # DAYS = 18
    # DAYS = 80
    # Doesn't work for large numbers because this is a quadratic algorithm:
    DAYS = 256
    for day in range(DAYS + 1):
        if day == 0:
            print(f'Initial state:  {lfish}')
        else:
            new_fish = lfish[0]
            for i in range(8):
                lfish[i] = lfish[i + 1]
            lfish[6] += new_fish
            lfish[8] = new_fish
            if verbose:
                daystr = 'days' if day > 1 else 'day'
                print(f'After {day:2} {daystr:4}:  {lfish}')
            elif day == 1:
                print('Days:  ', end='')
            elif day % 10 == 0:
                print(f'{day}', end='', flush=True)
            else:
                print('.', end='', flush=True)

    print(f'Lattern Fish Total:  {sum(lfish.values())}')

if __name__ == '__main__':
    main()
