#! /usr/bin/env python3


'''
Hill Climbing Algorithm

Part 1 Input:
* Heightmap of surrounding area
  * top view grid of a-z, with a=lowest elevation, z=highest
  * Current position=S (elevation=a), Best signal position=E (elevation=z)
  * Get from S to E in as few steps as possible
  * Can move up/down/left/right
  * Elevation of destination square can be at most one higher (but can be much lower)
* What is the fewest steps required to move from S to E, following above rules?
'''


# Third party libraries:
import numpy as np

# Local libraries:
from ..ds import graph2


INFILE = 'd19p1t1.txt'
# INFILE = 'd19p1.txt'


def main():
    ### Next step - read each line into numpy matrix/ndarray
    with open(INFILE) as infile:
        ...


if __name__ == '__main__':
    main()
