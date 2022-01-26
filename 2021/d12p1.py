#! /usr/bin/env python3.10

from dfs import dfs, construct_path, dfs_complete
from graph import Graph


# INFILE = 'd12p1t1.txt'
# INFILE = 'd12p1t2.txt'
# INFILE = 'd12p1t3.txt'
INFILE = 'd12p1.txt'

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
            if vertex.label == vertex.label.lower() and vertex in vertices:
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


def main(verbose=False):
    cave_graph = Graph(directed=True)
    start = 'start'
    end = 'end'
    with open(INFILE) as infile:
        for edge in infile:
            start_vertex, end_vertex = edge.strip().split('-')
            if not (sv := cave_graph.get_vertex(start_vertex)):
                sv = cave_graph.insert_vertex(start_vertex)
            if not (ev := cave_graph.get_vertex(end_vertex)):
                ev = cave_graph.insert_vertex(end_vertex)
            if not cave_graph.get_edge(sv, ev):
                cave_graph.insert_edge(sv, ev)

    if verbose:
        print(cave_graph)

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
    if not ((start_vertex := cave_graph.get_vertex(start)) and
            (end_vertex := cave_graph.get_vertex(end))):
        raise ValueError('Expected a vertices labelled {start} and {end}')
    backtrack([start_vertex], [], 0, cave_graph, end_vertex)


if __name__ == '__main__':
    main()
