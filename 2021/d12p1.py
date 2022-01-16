#! /usr/bin/env python3.10

from pprint import pprint

from graph import Graph

INFILE = 'd12p1t1.txt'
# INFILE = 'd12p1t2.txt'
# INFILE = 'd12p1t3.txt'
# INFILE = 'd12p1.txt'


def main():
    cave_graph = Graph()
    with open(INFILE) as infile:
        for edge in infile:
            start_vertex, end_vertex = edge.split('-')
            # Check if already present?
            sv = cave_graph.insert_vertex(start_vertex)
            ev = cave_graph.insert_vertex(end_vertex)
            cave_graph.insert_edge(sv, ev)

    pprint(cave_graph.__dict__)


if __name__ == '__main__':
    main()
