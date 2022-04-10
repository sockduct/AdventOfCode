'''
Based on graph.py from:
Data Structures and Algorithms in Python
Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
John Wiley & Sons, 2013
'''
class Graph:
    """Representation of a simple graph using an adjacency map."""

    def __init__(self, directed=False):
        """Create an empty graph (undirected, by default).

        Graph is directed if optional paramter is set to True.
        """
        self._outgoing = {}
        # Only create second map for directed graph; use alias for undirected:
        self._incoming = {} if directed else self._outgoing

        # Enforce unique labels for vertices:
        self._vlabels = {}

    def __repr__(self):
        # vertices = ', '.join(sorted(repr(k) for k in self.vertices()))
        graph = '<Graph('
        if self.is_directed():
            graph += 'directed, '
        graph += f'{self.vertex_count()} vertices with {self.edge_count()} edges)>'

        return graph

    def __str__(self):
        max_width = 5
        directed = 'Directed Graph' if self.is_directed() else 'Undirected Graph'
        vertices = self.format_output(self.vertices(), max_width)
        edges = self.format_output(self.edges(), max_width - 2)
        return f'{directed}\nVertices:    {vertices}\n     Edges:    {edges}'

    def _validate_vertex(self, v):
        """Verify that v is a Vertex of this graph."""
        if not isinstance(v, self.Vertex):
            raise TypeError('Vertex expected')

        if v not in self._outgoing:
            raise ValueError('Vertex does not belong to this graph.')

    def degree(self, v, outgoing=True):
        """Return number of (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to count incoming edges.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def edge_count(self):
        """Return the number of edges in the graph."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # for undirected graphs, make sure not to double-count edges
        return total if self.is_directed() else total // 2

    def edges(self):
        """Return a set of all edges of the graph."""
        result = set()             # avoid double-reporting edges of undirected graph
        # Add edges to result set:
        for vertex_out in self._outgoing.values():
            result.update(vertex_out.values())

        if self.is_directed():
            for vertex_in in self._incoming.values():
                result.update(vertex_in.values())

        return result

    def format_output(self, values, max_width=5):
        raw_values = sorted(repr(k) for k in values)
        fmt_values = ''
        if (values := len(raw_values)) > max_width:
            for cur_val in range(0, values, max_width):
                end_val = min(cur_val + max_width, values)
                fmt_values += ', '.join(raw_values[cur_val:end_val])
                if end_val != values:
                    fmt_values += '\n                     '
        else:
            fmt_values = ', '.join(raw_values)

        return fmt_values

    def get_edge(self, u, v):
        """Return the edge from u to v, or None if not adjacent."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)                # returns None if v not adjacent

    def get_vertex(self, label):
        return self._vlabels.get(label)

    def incident_edges(self, v, outgoing=True):
        """Return all (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to request incoming edges.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        yield from adj[v].values()

    def insert_edge(self, u, v, label=None):
        """Insert and return a new Edge from u to v with auxiliary label.

        Raise a ValueError if u and v are not vertices of the graph.
        Raise a ValueError if u and v are already adjacent.
        """
        if self.get_edge(u, v) is not None:            # includes error checking
            raise ValueError('u and v are already adjacent')

        directed = self.is_directed()
        e_out = self.Edge(u, v, label, directed)

        self._outgoing[u][v] = e_out
        self._incoming[v][u] = e_out

        if directed:
            e_in = self.Edge(v, u, label, directed)
            self._outgoing[v][u] = e_in
            self._incoming[u][v] = e_in

    def insert_uni_edge(self, u, v, label=None):
        """insert and return a new edge from u to v with auxiliary label.

        raise a ValueError if u and v are not vertices of the graph.
        raise a ValueError if u and v are already adjacent.
        """
        if self.get_edge(u, v) is not None:            # includes error checking
            raise ValueError('u and v are already adjacent')

        directed = self.is_directed()
        e_out = self.Edge(u, v, label, directed)

        self._outgoing[u][v] = e_out
        if not directed:
            self._incoming[v][u] = e_out

        if directed:
            e_in = self.Edge(v, u, label, directed)
            # self._outgoing[v][u] = e_in
            self._incoming[u][v] = e_in

    def insert_vertex(self, label):
        """Insert and return a new Vertex with label."""
        if label in self._vlabels:
            raise KeyError('Vertex label must be unique')

        v = self.Vertex(label)
        self._vlabels[label] = v
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}                # need distinct map for incoming edges

        return v

    def is_directed(self):
        """Return True if this is a directed graph; False if undirected.

        Property is based on the original declaration of the graph, not its contents.
        """
        return self._incoming is not self._outgoing # directed if maps are distinct

    def vertex_count(self):
        """Return the number of vertices in the graph."""
        return len(self._outgoing)

    def vertices(self):
        """Return an iteration of all vertices of the graph."""
        return self._outgoing.keys()

    class Edge:
        """Lightweight edge structure for a graph."""

        # Edge label optional:
        def __init__(self, u, v, label='', directed=False):
            """Do not call constructor directly. Use Graph's insert_edge(u, v, label)."""
            self._origin = u
            self._destination = v
            self._label = label
            self._directed = directed

        def endpoints(self):
            """Return (u, v) tuple for vertices u and v."""
            return (self._origin, self._destination)

        def opposite(self, v):
            """Return the vertex that is opposite v on this edge."""
            if not isinstance(v, Graph.Vertex):
                raise TypeError('v must be a Vertex')

            if v is self._destination:
                return self._origin
            elif v is self._origin:
                return self._destination
            else:
                raise ValueError(f'v not incident to edge({self._label})')

        @property
        def label(self):
            """Return label associated with this edge."""
            return self._label

        @label.setter
        def label(self, value):
            self._label = value

        @label.deleter
        def label(self):
            self._label = ''

        # Allow vertex to be a map/set key:
        def __hash__(self):
            return hash((self._origin, self._destination))

        def __repr__(self):
            if self._directed:
                connstr = f'==({self._label})==>' if self._label else '==>'
            else:
                connstr = f'<==({self._label})==>' if self._label else '<==>'
            return f'<Edge({self._origin}{connstr}{self._destination})>'

        def __str__(self):
            if self._directed:
                connstr = f'==({self._label})==>' if self._label else '==>'
            else:
                connstr = f'<==({self._label})==>' if self._label else '<==>'
            return f'({self._origin}{connstr}{self._destination})'

    class Vertex:
        """Lightweight vertex structure for a graph."""

        # Require label for a vertex:
        def __init__(self, label):
            """Do not call constructor directly. Use Graph's insert_vertex(label)."""
            self._label = label

        @property
        def label(self):
            """Return label associated with this vertex."""
            return self._label

        @label.setter
        def label(self, value):
            self._label = value

        @label.deleter
        def label(self):
            self._label = ''

        # Allow vertex to be a map/set key:
        def __hash__(self):
            return hash(id(self))

        def __repr__(self):
            return f'<Vertex({self._label})>'

        def __str__(self):
            return str(self._label)
