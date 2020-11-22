# t_graph.py by Zachary McNamara zmcnama@my.wgu.edu ID#001182706
from math import inf


class Vertex:
    def __init__(self, label, edges=[]):
        self.label = label
        self.edge_lengths = edges
        self.distance = inf
        self.pred_vertex = None

    @property
    def edge_lengths(self):
        return self._edge_lengths

    @edge_lengths.setter
    def edge_lengths(self, edges):
        self._edge_lengths = edges


class Graph:
    def __init__(self, vert_list=[]):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)
        # print("adding an edge between " + from_vertex.label +
        #       " to " + to_vertex.label + " of distance " + str(weight))

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def set_adjacent_vertexes(self, current_vertex, adjacents=[]):
        self.adjacency_list[current_vertex] = adjacents




