#! /usr/bin/env python3


'''
Cathod-Ray Tube
* CPU Instructions:
  * noop - nothing, 1 cycle
  * addx # - add # to register, 2 cycles

                       1         2         3
Position:    0123456789012345678901234567890123456789
Cycle   1 -> ######################################## <- Cycle  40
Cycle  41 -> ######################################## <- Cycle  80
Cycle  81 -> ######################################## <- Cycle 120
Cycle 121 -> ######################################## <- Cycle 160
Cycle 161 -> ######################################## <- Cycle 200
Cycle 201 -> ######################################## <- Cycle 240
'''


# INFILE = 'd10p1t1.txt'
# INFILE = 'd10p1t2.txt'
# INFILE = r'\working\github\sockduct\aoc\2022\d10p1t1.txt'
INFILE = 'd10p1.txt'


def cycle(proc, intervals, sigres, verbose):
    proc['cycle'] += 1
    signal_strength(proc, intervals, sigres, verbose)
    draw(proc, verbose)


def draw(proc, verbose=False):
    pos = (proc['cycle'] % 40) - 1
    if (proc['reg'] - 1) <= pos <= (proc['reg'] + 1):
        proc['screen'].append('#')
    else:
        proc['screen'].append('.')

    if proc['cycle'] % 40 == 0:
        proc['screen'].append('\n')

    if verbose:
        print(f"Display:\n{''.join(proc['screen'])}")

def signal_strength(proc, intervals, sigres, verbose=False):
    '''proc['cycle'] * proc['reg'] = signal strength'''
    if verbose:
        print(f"Cycle:  {proc['cycle']:3,}, Register:  {proc['reg']:3,}")

    if proc['cycle'] in intervals:
        sigres.append(proc['cycle'] * proc['reg'])


def main(verbose=False):
    with open(INFILE) as infile:
        proc = dict(reg=1, cycle=0, screen = [])
        intervals = (20, 60, 100, 140, 180, 220)
        sigres = []
        command = 0

        signal_strength(proc, intervals, sigres, verbose)
        for line in infile:
            cmd = line.split()
            command += 1

            match cmd:
                case ['noop']:
                    cycle(proc, intervals, sigres, verbose)
                case ['addx', num]:
                    cycle(proc, intervals, sigres, verbose)
                    cycle(proc, intervals, sigres, verbose)
                    proc['reg'] += int(num)
                case _:
                    raise ValueError(f'Expected noop|addx, got {cmd}.')

    print(f"\nProcessor completed {proc['cycle']:,} cycles, register is {proc['reg']:,}.")
    print(f'Sum of signal strengths:  {sum(sigres):,} ({sigres})')
    print(f"Display:\n{''.join(proc['screen'])}")
    print(f'Processed {command:,} commands.\n')


if __name__ == '__main__':
    main(verbose=False)
