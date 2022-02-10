#! /usr/bin/env python3.10


INFILE = 'd15p1t1.txt'
# INFILE = 'd15p1.txt'


'''
Map:
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

Directions:
* Start in top left
* Destination is bottom right
* No diagonal movement, only left/right or up/down
* Number in each position is risk level
* Don't count risk level from starting position unless you "enter" it
* Add risk of each position you enter
* Find path with lowest total risk

Thoughts on Approach:
* Actual data is 100x100 matrix - probably too big for backtracking
* Thinking this is a weighted graph problem
* Convert number matrix into weighted graph and then use Dijkstra's shortest
  path first algorithm to find least cost path
'''
class Map():
    def __init__(self, matrix):
        self.matrix = matrix

    def __repr__(self):
        output = '/| Map: |\\\n'
        for row in self.matrix:
            output += row
            output += '\n'

        return output


def main():
    matrix = []
    with open(INFILE) as infile:
        for line in infile:
            matrix.append(line.strip())

    map = Map(matrix)
    print(map)


if __name__ == '__main__':
    main()
