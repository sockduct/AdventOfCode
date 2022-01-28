#! /usr/bin/env python3.10

from graph import Graph


INFILE = 'd12p1t1.txt'
# INFILE = 'd12p1t2.txt'
# INFILE = 'd12p1t3.txt'
# INFILE = 'd12p1.txt'


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


class SmallCaveFlag():
    # Use class level variable instead of global one:
    __reedged = False
    __vertex = None
    __visited_twice = False

    def __bool__(self):
        return self.__visited_twice

    def __repr__(self):
        return (f'<SmallCaveFlag(reedged={self.__reedged}, vertex={self.__vertex}, '
                f'visited_twice={self.__visited_twice})>')

    def __str__(self):
        return (f'({self.__reedged}, {self.__vertex}, {self.__visited_twice})')

    @property
    def reedged(self):
        '''Check if we already "re-edged" for the twice visited vertex'''
        return self.__reedged

    @reedged.setter
    def reedged(self, value):
        # Use class instead of self or increments instance instead of class:
        SmallCaveFlag.__reedged = value

    def reset(self):
        SmallCaveFlag.__reedged = False
        SmallCaveFlag.__vertex = None
        SmallCaveFlag.__visited_twice = False

    def toggle(self):
        # Use class instead of self or increments instance instead of class:
        SmallCaveFlag.__visited_twice = not SmallCaveFlag.__visited_twice

    @property
    def vertex(self):
        '''Get small cave vertex we can visit twice'''
        return self.__vertex

    @vertex.setter
    def vertex(self, value):
        SmallCaveFlag.__vertex = value

    @vertex.deleter
    def vertex(self):
        SmallCaveFlag.__vertex = None


def backtrack(vertices, edges, k, graph, end_vertex):
    '''Generate each possible configuration exactly once.  Model the
       combinatorial search solution as a list edges = (a1, a2, ..., an), where
       each element ai is selected from a finite ordered set Si.  The list
       represents a sequence of edges in a path in the graph, where ai contains
       the ith graph edge in the sequence.
    '''
    flag = SmallCaveFlag()

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

            # Can only visit a single "small" (lowercase) vertex twice:
            if vertex.label == vertex.label.lower() and vertex in vertices:
                if flag:
                    continue

                flag.toggle()
                flag.vertex = vertex

            '''
            Need to be smart about choosing "small" cave to visit twice:
            Example:  start, A, b, A, b, A, c, A, end
            Possible approach:
            * When visit small cave, if has outgoing degree > 1, then allow
              revisiting it
            * Tricky part is have to re-insert edges to it - in above example,
              when leave b and return to A, have to re-add A==>b and b==>A
              edges
            * May be corner cases too - have to test
            * In addition, when unmake_move, need to figure out how to "reset"
              the flag to defaults for next path iteration
            '''
            # make_move(vertices, k, graph)
            edges.append(edge)
            last_vertex = vertices[-1]
            vertices.append(vertex)
            # If we go from a small cave to a big cave and flag == False and
            # the small cave has a degree > 1, remove incoming and outgoing
            # edges between them from edges
            if (last_vertex != vertices[0] and vertex != end_vertex and
                    last_vertex.label == last_vertex.label.lower() and
                    vertex.label != vertex.label.lower() and not flag and
                    graph.degree(last_vertex) > 1):
                if (outedge := graph.get_edge(last_vertex, vertex)) in edges:
                    edges.remove(outedge)
                if (inedge := graph.get_edge(vertex, last_vertex)) in edges:
                    edges.remove(inedge)
            # end_make_move

            backtrack(vertices, edges, k, graph, end_vertex)

            # unmake_move(vertices, k, graph)
            if len(edges) > 1:
                edges.pop()
            removed_vertex = vertices.pop()
            if removed_vertex == flag.vertex:
                flag.reset()
            # end_unmake_move


def construct_candidates(vertices, edges, k, graph):
    '''This routine returns a list c with the complete set of possible
       candidates for the kth position of edges, given the contents of the first
       k - 1 positions.
    '''
    flag = SmallCaveFlag()

    # Normal case
    if not flag or flag.reedged:
        return list(set(graph.incident_edges(vertices[k - 1])) - set(edges))

    flag.reedged = True
    return list((set(graph.incident_edges(vertices[k - 1])) - set(edges)) |
                set(graph.incident_edges(flag.vertex)))


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

    if not ((start_vertex := cave_graph.get_vertex(start)) and
            (end_vertex := cave_graph.get_vertex(end))):
        raise ValueError('Expected a vertices labelled {start} and {end}')
    backtrack([start_vertex], [], 0, cave_graph, end_vertex)


if __name__ == '__main__':
    main()
