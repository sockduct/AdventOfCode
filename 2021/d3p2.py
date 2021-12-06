#! /usr/bin/env python3.10

# INFILE = 'd3p1t1.txt'
INFILE = 'd3p1.txt'

def bindigcnt(binlist):
    bintrack = None

    for number in binlist:
        if bintrack is None:
            bintrack = [{'0': 0, '1': 0} for _ in range(len(number))]
        for index, digit in enumerate(number):
            bintrack[index][digit] += 1

    return bintrack

def process(diagrpt):
    oxgen = 0
    co2gen = 0
    lifesup = 0

    '''
    00101
    Position: 0..max
    * 0 or 1
    * count for each digit
    '''
    diag1 = diagrpt.copy()
    bintrack = bindigcnt(diagrpt)
    diag2 = []
    index = 0
    # Can't enumerate because changing out bintrack:
    while index < len(bintrack) and len(diag1) > 1:
        digits = bintrack[index]
        for ent in diag1:
            if (digits['0'] > digits['1'] and ent[index] == '0' or
                    digits['1'] >= digits['0'] and ent[index] == '1'):
                diag2.append(ent)
        diag1 = diag2
        bintrack = bindigcnt(diag1)
        diag2 = []
        index += 1
    oxgen = int(diag1[0], 2)

    diag1 = diagrpt.copy()
    bintrack = bindigcnt(diagrpt)
    diag2 = []
    index = 0
    while index < len(bintrack) and len(diag1) > 1:
        digits = bintrack[index]
        for ent in diag1:
            if (digits['0'] <= digits['1'] and ent[index] == '0' or
                    digits['1'] < digits['0'] and ent[index] == '1'):
                diag2.append(ent)
        diag1 = diag2
        bintrack = bindigcnt(diag1)
        diag2 = []
        index += 1
    co2gen = int(diag1[0], 2)

    print(f'Results:\noxygen generator rating:  {oxgen}\n'
          f'CO2 scrubber rating:  {co2gen}\n'
          f'Life support rating:  {oxgen * co2gen}')

def main():
    with open(INFILE) as ifile:
        diagrpt = [line.strip() for line in ifile]

    res = process(diagrpt)

if __name__ == '__main__':
    main()
