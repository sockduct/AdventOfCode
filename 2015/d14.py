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
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint


# Types:
@dataclass
class Reindeer:
    speed: int
    on: int
    rest: int
    dist: int = 0
    score: int = 0


def parse(line, reindeer):
    line = line.strip('\n.')
    name, _, _, speed, _, _, on, *_, rest, _ = line.split()
    reindeer[name] = Reindeer(speed=int(speed), on=int(on), rest=int(rest))


def max_dist(reindeer, dist):
    max_dist = 0

    for deer in reindeer:
        combined = reindeer[deer].on + reindeer[deer].rest
        intervals, remainder = divmod(dist, combined)
        deer_dist = intervals * reindeer[deer].speed * reindeer[deer].on

        if 0 < remainder < reindeer[deer].on:
            deer_dist += reindeer[deer].speed * remainder
        elif remainder >= reindeer[deer].on:
            deer_dist += reindeer[deer].speed * reindeer[deer].on

        if deer_dist > max_dist:
            max_dist = deer_dist

    return max_dist


def score2(reindeer, dist):
    '''
    Revised scoring system:
    * 1 point to reindeer in the lead after each second
        * If multiple reindeer tied for 1st, they each get 1 point
    * How many points does winning reindeer have?
    '''
    max_dist = 0
    cur_dist = {}

    for time in range(1, dist + 1):
        # Calculate current distance for each reindeer:
        for deer in reindeer:
            combined = reindeer[deer].on + reindeer[deer].rest
            if 0 < time % combined <= reindeer[deer].on:
                reindeer[deer].dist += reindeer[deer].speed

            if reindeer[deer].dist > max_dist:
                max_dist = reindeer[deer].dist

        # Add point to leader(s):
        for deer in reindeer:
            if reindeer[deer].dist == max_dist:
                reindeer[deer].score += 1

    max_points = 0
    for deer in reindeer:
        if reindeer[deer].score > max_points:
            max_points = reindeer[deer].score

    return max_points


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
    res2 = score2(reindeer, dist)

    print(f'Farthest reindeer went {res:,} km.')
    print(f'Reindeer with most points has {res2:,} points.')


if __name__ == '__main__':
    main()
