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


# Standard library:
from itertools import product
from pprint import pprint
import sys


# Local libraries:
# Ugly hack:
# sys.path.insert(0, '..')
sys.path.insert(0, r'\working\github\sockduct\aoc')
from ds import graph2
from ds.dfs import dfs, construct_path, dfs_complete


# INFILE = 'd12p1t1.txt'
INFILE = r'\working\github\sockduct\aoc\2022\d12p1t1.txt'
# INFILE = 'd12p1.txt'

FINISHED = False


class Counter():
    # Use class level variable instead of global one:
    __solution = 0

    def __repr__(self):
        return f'<Counter({self.__solution})>'

    def __str__(self):
        return f'{self.__solution}'

    def increment(self):
        # Use class instead of self or increments instance instead of class:
        Counter.__solution += 1


'''
Pseudo-code for backtrack:
Backtrack-DFS(a, k)
    if a = (a1, a2, ..., ak) is a solution:
        report it.
    else
        k = k + 1
        construct Sk, the set of candidates for position k of a
        for ak in Sk:
            Backtrack-DFS(a, k)
'''
def backtrack(vertices, edges, k, graph, end_vertex):
    '''Generate each possible configuration exactly once.  Model the
       combinatorial search solution as a list edges = (a1, a2, ..., an), where
       each element ai is selected from a finite ordered set Si.  The list
       represents a sequence of edges in a path in the graph, where ai contains
       the ith graph edge in the sequence.
    '''
    if is_a_solution(vertices, edges, k, graph, end_vertex):
        process_solution(vertices, edges, k, graph)
    else:
        k += 1
        candidates = construct_candidates(vertices, edges, k, graph)
        for edge in candidates:
            vertex = edge.opposite(vertices[k - 1])
            # No cycles to start:
            if vertex == vertices[0]:
                continue
            # Can't visit "small" (lowercase) verticies twice:
            # if vertex.label == vertex.label.lower() and vertex in vertices:
            if vertex in vertices:
                continue
            # make_move(vertices, k, graph)
            edges.append(edge)
            vertices.append(vertex)
            # end_make_move
            backtrack(vertices, edges, k, graph, end_vertex)
            # unmake_move(vertices, k, graph)
            edges.pop()
            vertices.pop()
            # end_unmake_move

            if (FINISHED):
                return  # terminate early


def construct_candidates(vertices, edges, k, graph):
    '''This routine returns a list c with the complete set of possible
       candidates for the kth position of edges, given the contents of the first
       k - 1 positions.
    '''
    # Retrieve the set of outgoing edges from last vertex and remove edges
    # already used:
    return list(set(graph.incident_edges(vertices[k - 1])) - set(edges))


def is_a_solution(vertices, edges, k, graph, end_vertex):
    '''This Boolean function tests whether the first k elements of list edges
       form a complete solution for the given problem.  In this case, a complete
       solution consists of edges starting from 'start' and ending with 'end'.
    '''
    return vertices[-1] == end_vertex


def make_move(vertices, k, graph):
    '''This routine enables us to modify a data structure in response to the
       latest move.  Such a data structure can always be rebuilt from scratch
       using the solution vector edges, but this can be inefficient when each
       move involves small incremental changes that can easily be undone.
    '''
    pass


def process_solution(vertices, edges, k, graph, verbose=False):
    '''This routine prints, counts, stores, or processes a complete solution
       once it is constructed.'''
    # God awful using global variable - fix this!!!
    solution = Counter()
    solution.increment()

    if verbose:
        print(f'Solution {k}:  {vertices}, ({edges})')
    else:
        print(f'Solution {solution}:  {", ".join(str(vertex) for vertex in vertices)}')


def unmake_move(vertices, k, graph):
    '''This routine enables us to clean up this data structure if we decide to
       take back the move.  Such a data structure can always be rebuilt from
       scratch using the solution vector edges, but this can be inefficient when
       each move involves small incremental changes that can easily be undone.
    '''
    pass


def get_dfs_edges(dfs_res):
    edge_path = 'Edge Path:  '
    edges = len(dfs_res) - 1
    for n, (key, value) in enumerate(dfs_res.items()):
        if value:
            edge_path += f'{value}'
            if n < edges:
                edge_path += ', '
        else:
            edge_path += f'from {key.label}>> '

    return edge_path


def getval(char):
    if char == 'S':
        return ord('a')
    elif char == 'E':
        return ord('z')
    elif 'a' <= char <= 'z':
        return ord(char)
    else:
        raise ValueError(f'Exepcted a-z|S|E, got {char}.')


def vlink(topology, matrix, row, rows, col, cols):
    '''Link left, right, up, down vertices'''
    current = getval(matrix[row][col].label[-1])
    # Up:
    if (up := row - 1) > 0:
        above = getval(matrix[up][col].label[-1])
        if above - current <= 1:
            topology.insert_uni_edge(matrix[row][col], matrix[up][col], 1)
    # Down:
    if (down := row + 1) < rows:
        below = getval(matrix[down][col].label[-1])
        if below - current <= 1:
            topology.insert_uni_edge(matrix[row][col], matrix[down][col], 1)
    # Left:
    if (left := col - 1) > 0:
        toleft = getval(matrix[row][left].label[-1])
        if toleft - current <= 1:
            topology.insert_uni_edge(matrix[row][col], matrix[row][left], 1)
    # Right:
    if (right := col + 1) < cols:
        toright = getval(matrix[row][right].label[-1])
        if toright - current <= 1:
            topology.insert_uni_edge(matrix[row][col], matrix[row][right], 1)


def display(topology, rows, cols):
    vertices = {vertex.label[:2]: vertex.label for vertex in topology.vertices()}

    for row in range(rows):
        for col in range(cols):
            vertex = topology.get_vertex(vertices[(row, col)])
            print(f'{vertex}', end='')
            if col + 1 < cols:
                vertex_right = topology.get_vertex(vertices[(row, col + 1)])
                if (topology.get_edge(vertex, vertex_right) and
                        topology.get_edge(vertex_right, vertex)):
                    print(' <=> ', end='')
                elif topology.get_edge(vertex, vertex_right):
                    print(' ==> ', end='')
                elif topology.get_edge(vertex_right, vertex):
                    print(' <== ', end='')
                else:
                    print('  x  ', end='')
        print()
        if row + 1 < rows:
            for col in range(cols):
                vertex = topology.get_vertex(vertices[(row, col)])
                vertex_below = topology.get_vertex(vertices[(row + 1, col)])
                if (topology.get_edge(vertex, vertex_below) and
                        topology.get_edge(vertex_below, vertex)):
                    print('  \/   /\       ', end='')
                elif topology.get_edge(vertex, vertex_below):
                    print('  \/            ', end='')
                elif topology.get_edge(vertex_below, vertex):
                    print('       /\       ', end='')
                else:
                    print('    x           ', end='')
            print()


def main():
    topology = graph2.Graph(directed=True)
    matrix = []
    with open(INFILE) as infile:
        for row_count, line in enumerate(infile):
            row = []
            row.extend(
                topology.insert_vertex((row_count, col_count, char))
                    for col_count, char in enumerate(line.strip())
            )
            matrix.append(row)

    # Debugging:
    # pprint(matrix)

    rows = len(matrix)
    cols = len(matrix[0])
    for row, col in product(range(rows), range(cols)):
        if matrix[row][col].label[-1] == 'S':
            start = matrix[row][col]
        elif matrix[row][col].label[-1] == 'E':
            end = matrix[row][col]
        vlink(topology, matrix, row, rows, col, cols)

    # Debugging:
    # print(topology)
    # pprint(list(topology.vertices()))
    # pprint(topology.edges())
    display(topology, rows, cols)

    '''
    Need DFS-like approach
    * Treat as directed graph, for edge set of edges add both directions
    * From vertex 'start', find all possible edges
    * What about collecting edge combinations from DFS starting from each
      possible vertex?
      * From 'start', recursively descend until get to 'end'
      * Cannot go back to start (no cycles)
      * Keep track of edge path - e.g., start->A, A->c, c->A, A->end
        -or-
      * Keep track of vertex path - e.g., start, A, c, end
      * Keep track of visited edges - need all permutations of unique edge
        combinations to get from 'start' to 'end'

    * Some failed approaches:
    * 1:  DFS gives a spanning tree, but not the solution for this challenge
    if not (start_vert := cave_graph.get_vertex(start)):
        raise ValueError('Expected a vertex labelled {start}')
    dfs_res = dfs(cave_graph, start_vert)
    print(get_dfs_edges(dfs_res))

    * 2:  Only interested in starting from start vertex:
    for vertex in cave_graph.vertices():
        dfs_res = dfs(cave_graph, vertex)
        print(get_dfs_edges(dfs_res))
    '''
    # backtrack([start], [], 0, topology, end)


if __name__ == '__main__':
    main()
