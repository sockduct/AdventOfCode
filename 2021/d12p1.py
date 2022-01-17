#! /usr/bin/env python3.10

from dfs import dfs, construct_path, dfs_complete
from graph import Graph

INFILE = 'd12p1t1.txt'
# INFILE = 'd12p1t2.txt'
# INFILE = 'd12p1t3.txt'
# INFILE = 'd12p1.txt'


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


def main():
    cave_graph = Graph(directed=True)
    start = 'start'
    with open(INFILE) as infile:
        for edge in infile:
            start_vertex, end_vertex = edge.strip().split('-')
            if not (sv := cave_graph.get_vertex(start_vertex)):
                sv = cave_graph.insert_vertex(start_vertex)
            if not (ev := cave_graph.get_vertex(end_vertex)):
                ev = cave_graph.insert_vertex(end_vertex)
            if not cave_graph.get_edge(sv, ev):
                cave_graph.insert_edge(sv, ev)

    print(cave_graph)

    '''
    Need DFS-like approach or BFS-like approach
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
    if not (start_vert := cave_graph.get_vertex(start)):
        raise ValueError('Expected a vertex labelled {start}')


if __name__ == '__main__':
    main()
