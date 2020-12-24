# graph.py by Zachary McNamara zmcnama@my.wgu.edu ID#001182706
from math import inf


class Vertex:
    def __init__(self, label):
        self.label = label
        self.distance = inf
        self.pred_vertex = None


class Graph:
    def __init__(self, vert_list=[]):
        self.adjacency_list = {}
        self.edge_weights = {}
        self.vertex_list = []

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []
        self.vertex_list.append(new_vertex)

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)
        # print("adding an edge between " + from_vertex.label +
        #       " to " + to_vertex.label + " of distance " + str(weight))

    def add_undirected_edge(self, vertex_a, vertex_b, weight):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def set_adjacent_vertexes(self, current_vertex, adjacents=[]):
        self.adjacency_list[current_vertex] = adjacents

    def get_vertex(self, label):
        for v in self.vertex_list:
            if v.label == label:
                return v

        return None

    def find_distance(self, current_v, target_v):
        try:
            return self.edge_weights[(current_v, target_v)]
        except KeyError:
            print("ERROR ERROR ERROR --- graph.py's find_distance --- ERROR ERROR ERROR")
            print("current_v={0} and target_v={1}".format(current_v.label, target_v.label))




