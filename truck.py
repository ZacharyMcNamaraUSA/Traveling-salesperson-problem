# t_graph.py by Zachary McNamara zmcnama@my.wgu.edu ID#001182706


class Truck:
    def __init__(self, label):
        self.label = label
        self.loaded_package_keys = []
        self.miles_driven = 0.0
        self.delivered_package_keys = []

    @property
    def loaded_package_keys(self):
        return self._loaded_package_keys

    @loaded_package_keys.setter
    def loaded_package_keys(self, keys):
        self._loaded_package_keys = keys

    @property
    def miles_driven(self):
        return self._miles_driven

    @miles_driven.setter
    def miles_driven(self, miles):
        self._miles_driven = miles


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




