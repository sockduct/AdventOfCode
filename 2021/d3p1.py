#! /usr/bin/env python3.10

# INFILE = 'd3p1t1.txt'
INFILE = 'd3p1.txt'

def process(diagrpt):
    gamma_rate = 0
    epsilon_rate = 0
    powercon = 0
    bintrack = None

    '''
    00101
    Position: 0..max
    * 0 or 1
    * count for each digit
    '''
    for number in diagrpt:
        if bintrack is None:
            bintrack = [{'0': 0, '1': 0} for _ in range(len(number))]
        for index, digit in enumerate(number):
            bintrack[index][digit] += 1

    binres_mcb = ''.join(
        '0' if digits['0'] > digits['1'] else '1' for digits in bintrack
    )
    gamma_rate = int(binres_mcb, 2)
    binres_lcb = ''.join(
        '0' if digits['0'] < digits['1'] else '1' for digits in bintrack
    )
    epsilon_rate = int(binres_lcb, 2)

    print(f'Results:\ngamma rate:  {gamma_rate}\n'
          f'epsilon rate:  {epsilon_rate}\n'
          f'Power Consumption:  {gamma_rate * epsilon_rate}')

def main():
    with open(INFILE) as ifile:
        diagrpt = [line.strip() for line in ifile]

    res = process(diagrpt)

if __name__ == '__main__':
    main()
