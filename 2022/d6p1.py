#! /usr/bin/env python3


'''
Tuning Trouble
* Fixing communications device
* Need to be able to detect start-of-packet marker
  * start-of-packet indicated by 4 characts which are all different

Part 1 Input:
* datastream buffer
* Identify first position where 4 most recently received characters are all different
* Report number of characters from beginning of buffer to end of 1st such 4 character
  marker

Part 2 (same input):
* Look for messages
  * Start-of-message marker consists of 14 distinct characters
* How many characters need to be processed before start-of-message marker found?
'''


# INFILE = 'd6p1t5.txt'
# INFILE = r'\working\github\sockduct\aoc\2022\d6p1t1.txt'
INFILE = 'd6p1.txt'


import queue


def find_offset(data, marker_size):
    q = queue.Queue(maxsize=marker_size)

    for pos, char in enumerate(data):
        if q.full():
            # marker_size unique characters?
            if q.qsize() == len(set(q.queue)):
                return pos

            # Make room for next character
            _ = q.get()
        q.put(char)


def main():
    with open(INFILE) as infile:
        data = infile.read().strip()

    sop_offset = find_offset(data, 4)
    som_offset = find_offset(data, 14)

    print(f'\nNumber of characters to end of first start-of-packet marker:  {sop_offset:,}')
    print(f'Number of characters to end of first start-of-message marker:  {som_offset:,}\n')


if __name__ == '__main__':
    main()
