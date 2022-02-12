#! /usr/bin/env python3.10


from graph import Graph


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
def main():
    matrix = []
    with open(INFILE) as infile:
        matrix.extend([int(e) for e in line.strip()] for line in infile)

    cavern = Graph(directed=True)
    for row, line in enumerate(matrix):
        cur_vertex = None
        for col, val in enumerate(line):
            left_vertex = cur_vertex
            cur_vertex = cavern.insert_vertex((row, col))
            if left_vertex:
                cavern.insert_edge(left_vertex, cur_vertex, val)
            if row > 0:
                up_vertex = cavern.get_vertex((row - 1, col))
                cavern.insert_edge(up_vertex, cur_vertex, val)

    from pprint import pprint
    pprint(matrix)
    print(f'\n{cavern}')


if __name__ == '__main__':
    main()
