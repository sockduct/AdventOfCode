#! /usr/bin/env python3


'''
Reindeer Olympics - Race
* Reindeer can either be flying at max speed or resting and do so in whole
  second intervals
* Read in reindeer info from file with max speed and rest requirements and
  calculate how far each one went in given time
* What is the farthest distance any reindeer has traveled?
'''


INFILE = 'd14.txt'
# INFILE = 'd14t1.txt'


# Libraries:
from pathlib import Path
from pprint import pprint


def parse(line, reindeer):
    line = line.strip('\n.')
    name, _, _, speed, _, _, workint, *_, restint, _ = line.split()
    reindeer[name] = dict(speed=int(speed), workint=int(workint), restint=int(restint))


def max_dist(reindeer, dist):
    max_dist = 0

    for deer in reindeer:
        combined = reindeer[deer]['workint'] + reindeer[deer]['restint']
        intervals, remainder = divmod(dist, combined)
        deer_dist = intervals * reindeer[deer]['speed'] * reindeer[deer]['workint']

        if 0 < remainder < reindeer[deer]['workint']:
            deer_dist += reindeer[deer]['speed'] * remainder
        elif remainder >= reindeer[deer]['workint']:
            deer_dist += reindeer[deer]['speed'] * reindeer[deer]['workint']

        if deer_dist > max_dist:
            max_dist = deer_dist

    return max_dist


def main():
    reindeer = {}
    with open(Path(__file__).parent/INFILE) as infile:
        for line in infile:
            parse(line, reindeer)

    pprint(reindeer)

    # Farthest reindeer?
    # dist = 1_000
    dist = 2_503
    res = max_dist(reindeer, dist)

    print(f'Farthest reindeer went {res:,} km.')


if __name__ == '__main__':
    main()
