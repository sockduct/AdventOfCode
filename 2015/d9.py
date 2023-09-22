#! /usr/bin/env python3


'''
Read in list of cities:
City1 to City2 = # (distance)

Calculate shortest path to visit all cities exactly once
* Can start from any city
'''


INFILE = 'd9.txt'
# INFILE = 'd9t1.txt'


# Libraries
from pathlib import Path

# Local Libraries
import ds.graph2 as graph


def get_shortest_path(g, vertices, start):
    vi = g.get_vertex(start)
    if remaining := vertices - {start}:
        res = {vr: g.get_edge(vi, g.get_vertex(vr)).label for vr in remaining}
        new_start_vertex, distance = sorted(res.items(), key=lambda x: x[1])[0]
        return distance + get_shortest_path(g, remaining, new_start_vertex)
    else:
        return 0


def find_shortest_path(g):
    vertices = set(g._vlabels.keys())

    distances = {
        vertex: get_shortest_path(g, vertices, vertex) for vertex in vertices
    }
    return min(distances.values())


def parse(line, city_graph):
    city1, _, city2, _, distance = line.split()

    for city in (city1, city2):
        if city not in city_graph._vlabels.keys():
            city_graph.insert_vertex(city)

    city_graph.insert_edge(city_graph.get_vertex(city1), city_graph.get_vertex(city2),
                           int(distance))


def main():
    city_graph = graph.Graph()
    with open(Path(__file__).parent/INFILE) as infile:
        for line in infile:
            parse(line, city_graph)

    shortest = find_shortest_path(city_graph)
    print(f'Shortest distance:  {shortest}')


if __name__ == '__main__':
    main()
