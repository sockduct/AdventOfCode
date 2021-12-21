#! /usr/bin/env python3.10

'''
* Seven Segment Digit Display
  * Each row has 4 digits:

4-Digt Display Segments:
0 (6):  1 (2):  2 (5):  3 (5):  4 (4):
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

5 (5):  6 (6):  7 (3):  8 (7):  9 (6):
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

Segments:
2: 1 (1)
3: 1 (7)
4: 1 (4)
5: 3 (2, 3, 5)
6: 3 (0, 6, 9)
7: 7 (8)

Problem:
* a-g outputs mixed up
* Must determine which output signals correspond to which display segments
* Each line contains ten unique signal patterns (corresponding to 0-9), followed
  by a |, followed by a 4-digit output value (4 groups of codes)
* Hints:
  * 1 is the only digit that uses two segments
  * 4 is the only digit that uses four segments
  * 7 is the only digit that uses three segments

Goal:
================
Signal | Segment
----------------
   a   |   ?   |
   b   |   ?   |
   c   |   ?   |
   d   |   ?   |
   e   |   ?   |
   f   |   ?   |
   g   |   ?   |
----------------
'''

# INFILE = 'd8p1t1.txt'
INFILE = 'd8p1.txt'

'''
Example:
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
       --                                 ---- --- -------

Signal => Segment
cg => 1, c,g=c|f
gcb => 7, g,c,b=a|c|f
gfac => 4, g,f,a,c=b|c|d|f
cdgabef => 8, c,d,g,a,b,e,f=a|b|c|d|e|f|g
'''

class SegmentDisplay():
    segments = {2: '1', 3: '7', 4: '4', 5: '235', 6: '069', 7: '8'}

    def __init__(self, signals, display):
        self.signals = signals
        self.display = display
        self.output = {k: '' for k in 'abcdefg'}

def main():
    with open(INFILE) as infile:
        segment_displays = []

        for line in infile:
            signals, display = line.strip().split('|')
            signals = signals.split()
            display = display.split()

            segment_displays.append(SegmentDisplay(signals, display))

    segments = {2, 3, 4, 7}
    total = sum(
        sum(len(digit) in segments for digit in segment_display.display)
            for segment_display in segment_displays
    )

    print(f'Total for target segments ({segments}):  {total}')

if __name__ == '__main__':
    main()
