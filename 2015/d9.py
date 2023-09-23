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
from itertools import pairwise, permutations
from pathlib import Path

# Local Libraries
import ds.graph2 as graph


def get_opt_path(g, vertices, start, reverse=False, verbose=False):
    vi = g.get_vertex(start)
    if remaining := vertices - {start}:
        res = {vr: g.get_edge(vi, g.get_vertex(vr)).label for vr in remaining}
        if verbose:
            goal = 'Max' if reverse else 'Min'
            print(f'{goal} from {start}:  {res}')
        new_start_vertex, distance = sorted(res.items(), key=lambda x: x[1], reverse=reverse)[0]
        return distance + get_opt_path(g, remaining, new_start_vertex, reverse)
    else:
        if verbose:
            print()
        return 0


def find_optimal_path(g, opt=min, reverse=False, verbose=False):
    vertices = set(g._vlabels.keys())

    distances = {
        vertex: get_opt_path(g, vertices, vertex, reverse) for vertex in vertices
    }
    if verbose:
        print(f'{distances=}')
    return opt(distances.values())


def find_all_paths(g):
    vertices = list(g._vlabels.keys())
    paths = permutations(vertices)

    distances = []
    for path in paths:
        distance = sum(
            g.get_edge(g.get_vertex(v1), g.get_vertex(v2)).label
            for v1, v2 in pairwise(path)
        )
        distances.append(distance)

    print(f'Minimum distance:  {min(distances)}\nMaximum distance:  {max(distances)}')


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

    shortest = find_optimal_path(city_graph)
    longest = find_optimal_path(city_graph, max, True)
    find_all_paths(city_graph)
    print(f'Shortest distance:  {shortest}\nLongest distance:  {longest}')


if __name__ == '__main__':
    main()
