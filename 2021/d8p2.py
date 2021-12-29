#! /usr/bin/env python3.10

from pprint import pprint
import sys

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
Signal | Segment  (Normal)
----------------
   a   |   ?   |    aaaa
   b   |   ?   |   b    c
   c   |   ?   |   b    c
   d   |   ?   |    dddd
   e   |   ?   |   e    f
   f   |   ?   |   e    f
   g   |   ?   |    gggg
----------------

Example:
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
       --                                 ---- --- -------

Signal => Segment
cg => 1, c,g=c|f
gcb => 7, g,c,b=a|c|f
gfac => 4, g,f,a,c=b|c|d|f
cdgabef => 8, c,d,g,a,b,e,f=a|b|c|d|e|f|g

c => c  b,e,c,d,f,a
g => f
b => a
f => b
a => d
d => e
e => g
'''

# INFILE = 'd8p1t1.txt'
INFILE = 'd8p1.txt'

class SegmentDisplay():
    segment_count = {2: '1', 3: '7', 4: '4', 5: '235', 6: '069', 7: '8'}
    digit2segments = {0: 'abcefg', 1: 'cf', 2: 'acdeg', 3: 'acdfg', 4: 'bcdf',
                      5: 'abdfg', 6: 'abdefg', 7: 'acf', 8: 'abcdefg', 9: 'abcdfg'}
    segments2digit = dict(abcefg=0, cf=1, acdeg=2, acdfg=3, bcdf=4,
                          abdfg=5, abdefg=6, acf=7, abcdefg=8, abcdfg=9)
    # Note to self - cannot access class-level variables from comprehensions at class-level!!!
    # The comprehension has its own scope, and it can only access that or module scope
    # sequences = [(k, list(digit2segments[v])) for k, v in [(2, 1), (3, 7), (4, 4), (7, 8)]]

    def __init__(self, signals, display):
        self.signals = signals
        self.display = display

        self.segments = {k: [] for k in range(2, 8)}
        for signal in self.signals:
            self.segments[len(signal)].append(signal)

        # Signal output to segment mapping:
        self.output = {k: '' for k in 'abcdefg'}
        self.sequences = [(k, list(self.digit2segments[v])) for k, v in [(2, 1), (3, 7), (4, 4), (7, 8)]]

        res = self.map_outputs()
        if not res:
            print('Failed to map outputs to valid segments/digits...aborting!')
            sys.exit(1)
        self.signals2digits = self.map_signals2digits()

    def __repr__(self):
        return f'<SegmentDisplay([{self.signals[0]}, ...] => {self.display})>'

    def __str__(self):
        return ''.join(str(self.signals2digits[''.join(sorted(number))])
                    for number in self.display)

    def map_outputs(self, verbose=False):
        allocated = ''
        # Initial setup - map outputs based on digits 1, 7, 4, and 8 having
        # unique segment count:
        if allocated == '':
            for i, seq in self.sequences:
                for signal in self.segments[i][0]:
                    if self.output[signal] == '':
                        while seq[0] in allocated:
                            seq = self.rotate(seq)
                        self.output[signal] = seq[:]
                        allocated += seq[0]

        # Instead, sort by ascending number of values:
        output_sorted = dict(sorted(self.output.items(), key=lambda item: len(item[1])))
        output_keys = ''.join(output_sorted.keys())
        '''
        * After first pass, rather than going a-g, go least to most list items -
          e.g., 2, 2, 3, 4, 4, 7, 7 => maximizes probability of finding a valid sequence
        * Updated approach:
        1) Try first option
        2) Swap last two (5 & 6) and try again
        3) Swap 3 & 4, try again
        4) Swap 5 & 6, try again
        5) Swap 0 & 1, try again
        6) Swap 5 & 6, try again
        7) Swap 3 & 4, try again
        8) Swap 5 & 6, try again
        '''
        swap_pairs = [(5, 6), (3, 4), (5, 6), (0, 1), (5, 6), (3, 4), (5, 6)]
        allocated = [segment[0] for segment in output_sorted.values()]

        if self.validate_outputs(verbose):
            if verbose:
                output = dict(sorted(self.output.items(), key=lambda item: len(item[1])))
                pprint(output, sort_dicts=False)

            return True

        for swap_pair in swap_pairs:
            swapa, swapb = swap_pair
            self.output[output_keys[swapa]], self.output[output_keys[swapb]] = (
                self.output[output_keys[swapb]], self.output[output_keys[swapa]])

            if self.validate_outputs(verbose):
                if verbose:
                    output = dict(sorted(self.output.items(), key=lambda item: len(item[1])))
                    pprint(output, sort_dicts=False)

                return True

        return False

    def map_signals2digits(self):
        res = {
            signal: ''.join(self.output[digit][0] for digit in signal)
                for signal in self.signals
        }

        return {
            ''.join(sorted(k)): self.segments2digit[''.join(sorted(v))]
                for k, v in res.items()
        }

    def show(self):
        output = 'Signals to digits:  '
        for i, dict_tuple in enumerate(self.signals2digits.items()):
            k, v = dict_tuple
            output += f'{k}=>{v}, '
            if i == 4:
                output += '\n                    '

        displaydigits = [
            (''.join(sorted(number)), ''.join(str(self.signals2digits[''.join(sorted(number))])))
                    for number in self.display
        ]
        output += '\nDisplay to digits:  '
        for values in displaydigits:
            output += f'{values[0]}=>{values[1]}, '
        output += f'   ({self})'
        print(output)

    def validate_outputs(self, verbose=False):
        status = []
        for signal in self.signals:
            all_segments = [self.output[an_output][0] for an_output in signal]
            res = ''.join(sorted(all_segments)) in self.digit2segments.values()
            status.append(res)
            if verbose:
                print(f'{signal:>7} => {str(all_segments):<35} => valid_digit={res}')

        res = all(status)
        if verbose:
            print(f'All digits valid:  {res}')

        return res

    def rotate(self, seq):
        return seq[1:] + seq[:1]


def test_case():
    # data = 'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg'
    # data = 'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe'
    data = 'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc'
    # data = 'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb'
    signals, display = data.strip().split('|')
    signals = signals.split()
    display = display.split()
    print(f'Signals:  {signals}\nDisplay:  {display}')
    segment_display = SegmentDisplay(signals, display)
    # Monitor status:
    segment_display.show()
    return segment_display


def main():
    # test_case()

    with open(INFILE) as infile:
        segment_displays = []

        for line in infile:
            signals, display = line.strip().split('|')
            signals = signals.split()
            display = display.split()

            print(f'Signals:  {signals}\nDisplay:  {display}')
            segment_display = SegmentDisplay(signals, display)
            segment_displays.append(segment_display)
            # Monitor status:
            segment_display.show()
            print()

    total = 0
    for segment_display in segment_displays:
        current = str(segment_display)
        total += int(current)
        print(current)
    print(f'Total:  {total}')

    '''
    segments = {2, 3, 4, 7}
    total = sum(
        sum(len(digit) in segments for digit in segment_display.display)
            for segment_display in segment_displays
    )

    print(f'Total for target segments ({segments}):  {total}')
    '''


if __name__ == '__main__':
    main()
