# barebones.py by Zachary McNamara zmcnama@my.wgu.edu ID#001182706

import copy
import csv
from cmath import inf

import hashtable
import Package
from graph import Graph, Vertex
import operator

packages = hashtable.HashTable()
distances = hashtable.HashTable()
verts = hashtable.HashTable()
vertices = []
graph = Graph()
total_miles = 0.00
total_packages = 0
list_of_all_stops = []
hour = 8
minute = 0
regulars = []
truck_A = []
truck_B = []
truck_C = []
max_packages = 16
speed = 18



# Function create_package_hashtable populates the custom hashtable data structure for package info
#   receives and parses a csv file with wgups package info
def create_package_hashtable(filename):
    with open(filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        global total_packages

        for row in read_csv:  # For every row in CSV file
            key = row[0]
            new_package = [key, row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
            packages.add(key, new_package)
            total_packages += 1

        csv_file.close()


# Function populates the custom hashtable data structure for distance info
#   param: csv_filename is a csv file with wgups distance table information
def create_distance_hashtable(csv_filename):
    with open(csv_filename) as distance_csv:
        read_csv = csv.reader(distance_csv, delimiter=',')

        stop_count = 0
        for row in read_csv:  # For every row in CSV file
            edges = ""
            key = row[1]

            for i in range(4, len(row)):
                if row[i] != "":
                    edges += row[i] + ","
                    # print("\t\t" + str(edges))
            verts.add(key, edges)

            row.insert(0, str(stop_count))
            distances.add(key, row)
            stop_count += 1
            list_of_all_stops.append(key)

        distance_csv.close()


# Function finds the distance between 2 Stops
#   params: target destination and a previous destination (current location), defaults to HUB
#       a destination's key is its primary identifier in the HashTable distances
def lookup_distance(target, previous="4001 South 700 East"):
    tar = distances.get(target)
    prev = distances.get(previous)

    print("\n\n\nTARGET DESTINATION in lookup_distance: ")
    print(target)
    print(tar)
    print("\tPREVIOUS DESTINATION in lookup_distance: ")
    print(previous)
    print(prev)
    try:
        # print("tried lookup_dist")
        mi = 0.00

        mi = float(prev[5 + int(tar[0])])
    except ValueError:
        # print("ValueError in lookup_dist")
        mi = float(tar[5 + int(prev[0])])
    except TypeError:
        mi = 0.000
        # print(type(mi))
        print("TypeError in lookup_distance")
        print("tar=" + str(tar))
        print("prev=" + str(prev))

    # print("WHY NOT HERE???????????????????????????????????????")
    print("\t\tTraveling from " + prev[1] + prev[2] + " --> " +
          tar[1] + tar[2] + " is " + "{:.2f}".format(mi) + " miles.")

    return mi


def distance_of_route_as_ordered(packs):
    miles = 0.0
    undelivered = []
    for p in packs:
        # print(p)
        try:
            undelivered.append(p)
        except TypeError:
            print("I did not find a Package in distance_of_route.\tp is " + str(p))

    for num in range(len(packs)):
        # print("START")
        # print(packs[num])
        # print(distances.get(packs[num][1]))
        # print("Above me")
        # print("num=" + str(num))
        m = 0
        if num == 0:
            m = lookup_distance(packs[num][1])
        else:
            m: float = lookup_distance(packs[num][1], packs[num - 1][1])
        miles += m
        print("counting... miles=" "{:.2f}".format(miles))

    # print("This route travelled {:.1f}".format(miles) + " MILES and delivered "
    #               + str(len(undelivered)) + " packages.")

    return miles


# Function selects package(s) with a delivery deadline or special notes
def get_constrained_packages(p_list):
    keys = []
    for p in range(1, p_list.count):
        pack = packages.get(p)

        # This if condition reruns the loop if the Package pack is not constrained.
        #       Therefore, if the condition does not stop the loop, pack is a constrained Package
        if pack[5] == "EOD" and pack[7] == "":
            continue

        keys.append(pack)

    return keys


# Function prints constraints for any of the provided packages
def print_constrained_info(constrained_list):
    for pack in constrained_list:
        message = ""

        # This if condition reruns the loop if the Package pack is not constrained.
        #       Therefore, if the condition does not stop the loop, pack is a constrained Package
        if pack[5] == "EOD" and pack[7] == "":
            continue

        message += "Package " + pack[0] + "\n"

        # IF the Package must be delivered by a specific time
        if pack[5] != "EOD":
            message += "\t\tDelivery deadline is " + pack[5] + ".\n"

        # IF the Package has special instructions
        if pack[7] != "":
            message += "\t\tInstructions: " + pack[0] + ": " + pack[7] + ".\n"

        print(message)


def dijkstra_shortest_path(g, start_vertex):
    # Put all vertices in an unvisited queue.
    unvisited_queue = []
    for current_vertex in g.adjacency_list:
        unvisited_queue.append(current_vertex)
        current_vertex.distance = inf
    #     print("appending vertex'" + current_vertex.label + "' to unvisited_queue!")
    # print("len(unvisited_queue)=" + str(len(unvisited_queue)))

    # Start_vertex has a distance of 0 from itself
    start_vertex.distance = 0

    # One vertex is removed with each iteration; repeat until the list is
    # empty.
    while len(unvisited_queue) > 0:
        print("\n")

        # Visit vertex with minimum distance from start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            print("\tunvisited_queue[" + str(i) + "].distance={:0.1f}".format(unvisited_queue[i].distance))
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                print("\tnew smallest_index [i]=" + str(i))
                smallest_index = i
        print("\tpopping off unvisited_queue(smallest_index)=" + str(unvisited_queue[smallest_index].label) +
              " as NEW current_vertex")
        current_vertex = unvisited_queue.pop(smallest_index)

        # Check potential path lengths from the current vertex to all adjacent vertices.
        for adj_vertex in g.adjacency_list[current_vertex]:
            print("\n\t\tcurrent_vertex remains " + current_vertex.label)
            print("\t\t\tcompare with: adj_vertex=" + adj_vertex.label)

            try:
                edge_weight = g.edge_weights[(current_vertex, adj_vertex)]
                alternative_path_distance = current_vertex.distance + edge_weight
            except KeyError:
                print("No edge between current_v=" + current_vertex.label + " and adjacent_v=" + adj_vertex.label)
                continue

            print("\t\t\t\tDistance between current_v and adjacent_v is the edge_weight={:.1f}".format(edge_weight))
            print("\t\t\t\tReaching target/adjacent vertex: " + adj_vertex.label +
                  " could be alt_path_dist={:.1f}".format(alternative_path_distance) +
                  " vs. the previous best: {:.1f}".format(adj_vertex.distance))

            # If shorter path from start_vertex to adj_vertex is found,
            # update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                print("\t\t\t\tThis vertex is closer!!! Old:(" + adj_vertex.label
                      + ").distance={:.1f}".format(adj_vertex.distance) + "")
                print("\t\t\t\t\t\tNEW {:.1f}".format(alternative_path_distance) + " < " +
                      "old={:.1f}".format(adj_vertex.distance))
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex
            else:
                print("\t\t\t\t\t\tObviously {:.1f}".format(adj_vertex.distance) + " < " +
                      "{:.1f}".format(alternative_path_distance) + "--the alt path")


def get_shortest_path(start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = ""
    total_distance = 0.0
    current_vertex = end_vertex
    while current_vertex is not start_vertex:
        path = " -> " + str(current_vertex.label) + " is {:.1f}".format(current_vertex.distance) + " miles" + path

        current_vertex = current_vertex.pred_vertex

        total_distance = current_vertex.distance

    path = start_vertex.label + path
    return path, total_distance


def main():

    g = Graph()

    vertex_0 = Vertex("4001 South 700 East")
    vertex_1 = Vertex("1060 Dalton Ave S")
    vertex_2 = Vertex("1330 2100 S")
    vertex_3 = Vertex("1488 4800 S")
    vertex_4 = Vertex("177 W Price Ave")
    vertex_5 = Vertex("195 W Oakland Ave")
    vertex_6 = Vertex("2010 W 500 S")
    vertex_7 = Vertex("2300 Parkway Blvd")
    vertex_8 = Vertex("233 Canyon Rd")
    vertex_9 = Vertex("2530 S 500 E")
    vertex_10 = Vertex("2600 Taylorsville Blvd")
    vertex_11 = Vertex("2835 Main St")
    vertex_12 = Vertex("300 State St")
    vertex_13 = Vertex("3060 Lester St")
    vertex_14 = Vertex("3148 S 1100 W")
    vertex_15 = Vertex("3365 S 900 W")
    vertex_16 = Vertex("3575 W Valley Central Station bus Loop")
    vertex_17 = Vertex("3595 Main St")
    vertex_18 = Vertex("380 W 2880 S")
    vertex_19 = Vertex("410 S State St")
    vertex_20 = Vertex("4300 S 1300 E")
    vertex_21 = Vertex("4580 S 2300 E")
    vertex_22 = Vertex("5025 State St")
    vertex_23 = Vertex("5100 South 2700 West")
    vertex_24 = Vertex("5383 South 900 East #104")
    vertex_25 = Vertex("600 E 900 South")
    vertex_26 = Vertex("6351 South 900 East")

    g.add_vertex(vertex_0)
    g.add_vertex(vertex_1)
    g.add_vertex(vertex_2)
    g.add_vertex(vertex_3)
    g.add_vertex(vertex_4)
    g.add_vertex(vertex_5)
    g.add_vertex(vertex_6)
    g.add_vertex(vertex_7)
    g.add_vertex(vertex_8)
    g.add_vertex(vertex_9)
    g.add_vertex(vertex_10)
    g.add_vertex(vertex_11)
    g.add_vertex(vertex_12)
    g.add_vertex(vertex_13)
    g.add_vertex(vertex_14)
    g.add_vertex(vertex_15)
    g.add_vertex(vertex_16)
    g.add_vertex(vertex_17)
    g.add_vertex(vertex_18)
    g.add_vertex(vertex_19)
    g.add_vertex(vertex_20)
    g.add_vertex(vertex_21)
    g.add_vertex(vertex_22)
    g.add_vertex(vertex_23)
    g.add_vertex(vertex_24)
    g.add_vertex(vertex_25)
    g.add_vertex(vertex_26)

    g.add_directed_edge(vertex_26, vertex_26, 0.0)
    g.add_undirected_edge(vertex_26, vertex_24, 1.3)
    g.add_undirected_edge(vertex_26, vertex_22, 3.1)
    g.add_undirected_edge(vertex_26, vertex_20, 4.1)
    g.add_undirected_edge(vertex_26, vertex_18, 6.9)
    g.add_undirected_edge(vertex_26, vertex_0, 3.6)
    g.set_adjacent_vertexes(vertex_26, [vertex_24, vertex_22, vertex_20, vertex_18, vertex_0])

    g.add_directed_edge(vertex_25, vertex_25, 0.0)
    g.add_undirected_edge(vertex_25, vertex_0, 5.0)
    g.add_undirected_edge(vertex_25, vertex_2, 2.8)
    g.add_undirected_edge(vertex_25, vertex_5, 3.5)
    g.add_undirected_edge(vertex_25, vertex_8, 2.8)
    g.add_undirected_edge(vertex_25, vertex_9, 3.2)
    g.add_undirected_edge(vertex_25, vertex_11, 3.7)
    g.add_undirected_edge(vertex_25, vertex_12, 2.8)
    g.add_undirected_edge(vertex_25, vertex_19, 1.8)
    g.add_undirected_edge(vertex_25, vertex_20, 6.0)
    g.set_adjacent_vertexes(vertex_25, [vertex_0, vertex_2, vertex_5, vertex_8, vertex_9,
                                        vertex_11, vertex_12, vertex_19, vertex_20])

    g.add_directed_edge(vertex_24, vertex_24, 0.0)
    g.add_undirected_edge(vertex_24, vertex_0, 2.4)
    g.add_undirected_edge(vertex_24, vertex_4, 4.2)
    g.add_undirected_edge(vertex_24, vertex_9, 4.8)
    g.add_undirected_edge(vertex_24, vertex_10, 4.9)
    g.add_undirected_edge(vertex_24, vertex_17, 4.0)
    g.add_undirected_edge(vertex_24, vertex_20, 2.8)
    g.add_undirected_edge(vertex_24, vertex_21, 3.4)
    g.add_undirected_edge(vertex_24, vertex_22, 1.7)

    g.add_directed_edge(vertex_23, vertex_23, 0.0)
    g.add_undirected_edge(vertex_23, vertex_0, 6.4)
    g.add_undirected_edge(vertex_23, vertex_3, 0.6)
    g.add_undirected_edge(vertex_23, vertex_7, 4.2)
    g.add_undirected_edge(vertex_23, vertex_10, 0.4)
    g.add_undirected_edge(vertex_23, vertex_13, 4.4)
    g.add_undirected_edge(vertex_23, vertex_14, 4.8)
    g.add_undirected_edge(vertex_23, vertex_13, 4.5)

    g.add_directed_edge(vertex_22, vertex_22, 0.0)
    g.add_undirected_edge(vertex_22, vertex_0, 2.4)
    g.add_undirected_edge(vertex_22, vertex_4, 2.5)
    g.add_undirected_edge(vertex_22, vertex_5, 4.2)
    g.add_undirected_edge(vertex_22, vertex_9, 4.3)
    g.add_undirected_edge(vertex_22, vertex_10, 4.1)
    g.add_undirected_edge(vertex_22, vertex_11, 3.4)
    g.add_undirected_edge(vertex_22, vertex_15, 4.2)
    g.add_undirected_edge(vertex_22, vertex_17, 2.3)
    g.add_undirected_edge(vertex_22, vertex_20, 2.9)
    g.add_undirected_edge(vertex_22, vertex_21, 4.4)

    g.add_directed_edge(vertex_21, vertex_21, 0.0)
    g.add_undirected_edge(vertex_21, vertex_0, 3.4)
    g.add_undirected_edge(vertex_21, vertex_4, 5.2)
    g.add_undirected_edge(vertex_21, vertex_9, 5.8)
    g.add_undirected_edge(vertex_21, vertex_20, 2.0)

    g.add_directed_edge(vertex_20, vertex_20, 0.0)
    g.add_undirected_edge(vertex_20, vertex_0, 1.9)
    g.add_undirected_edge(vertex_20, vertex_2, 3.3)
    g.add_undirected_edge(vertex_20, vertex_4, 3.2)
    g.add_undirected_edge(vertex_20, vertex_5, 4.9)
    g.add_undirected_edge(vertex_20, vertex_8, 8.5)
    g.add_undirected_edge(vertex_20, vertex_9, 3.8)
    g.add_undirected_edge(vertex_20, vertex_11, 4.1)
    g.add_undirected_edge(vertex_20, vertex_17, 3.0)
    g.add_undirected_edge(vertex_20, vertex_18, 4.6)

    g.add_directed_edge(vertex_19, vertex_19, 0.0)
    g.add_undirected_edge(vertex_19, vertex_0, 6.5)
    g.add_undirected_edge(vertex_19, vertex_1, 4.8)
    g.add_undirected_edge(vertex_19, vertex_2, 4.3)
    g.add_undirected_edge(vertex_19, vertex_5, 3.5)
    g.add_undirected_edge(vertex_19, vertex_6, 3.2)
    g.add_undirected_edge(vertex_19, vertex_8, 1.0)
    g.add_undirected_edge(vertex_19, vertex_9, 4.1)
    g.add_undirected_edge(vertex_19, vertex_11, 3.7)
    g.add_undirected_edge(vertex_19, vertex_12, 1.0)
    g.add_undirected_edge(vertex_19, vertex_18, 4.4)

    g.add_directed_edge(vertex_18, vertex_18, 0.0)
    g.add_undirected_edge(vertex_18, vertex_0, 3.6)
    g.add_undirected_edge(vertex_18, vertex_2, 3.6)
    g.add_undirected_edge(vertex_18, vertex_4, 1.7)
    g.add_undirected_edge(vertex_18, vertex_5, 1.1)
    g.add_undirected_edge(vertex_18, vertex_9, 1.8)
    g.add_undirected_edge(vertex_18, vertex_11, 1.0)
    g.add_undirected_edge(vertex_18, vertex_13, 3.0)
    g.add_undirected_edge(vertex_18, vertex_14, 2.2)
    g.add_undirected_edge(vertex_18, vertex_15, 1.7)
    g.add_undirected_edge(vertex_18, vertex_16, 1.6)

    g.add_directed_edge(vertex_17, vertex_17, 0.0)
    g.add_undirected_edge(vertex_17, vertex_0, 2.0)
    g.add_undirected_edge(vertex_17, vertex_4, 0.5)
    g.add_undirected_edge(vertex_17, vertex_5, 1.9)
    g.add_undirected_edge(vertex_17, vertex_9, 2.3)
    g.add_undirected_edge(vertex_17, vertex_11, 1.2)
    g.add_undirected_edge(vertex_17, vertex_13, 3.2)
    g.add_undirected_edge(vertex_17, vertex_14, 2.4)
    g.add_undirected_edge(vertex_17, vertex_15, 1.6)

    g.add_directed_edge(vertex_16, vertex_16, 0.0)
    g.add_undirected_edge(vertex_16, vertex_0, 7.6)
    g.add_undirected_edge(vertex_16, vertex_4, 1.4)
    g.add_undirected_edge(vertex_16, vertex_12, 3.1)
    g.add_undirected_edge(vertex_16, vertex_13, 4.0)

    g.add_directed_edge(vertex_15, vertex_15, 0.0)
    g.add_undirected_edge(vertex_15, vertex_0, 3.7)
    g.add_undirected_edge(vertex_15, vertex_3, 4.4)
    g.add_undirected_edge(vertex_15, vertex_4, 2.7)
    g.add_undirected_edge(vertex_15, vertex_5, 3.8)
    g.add_undirected_edge(vertex_15, vertex_7, 3.4)
    g.add_undirected_edge(vertex_15, vertex_9, 4.0)
    g.add_undirected_edge(vertex_15, vertex_11, 2.9)
    g.add_undirected_edge(vertex_15, vertex_13, 1.5)
    g.add_undirected_edge(vertex_15, vertex_14, 0.6)

    g.add_directed_edge(vertex_14, vertex_14, 0.0)
    g.add_undirected_edge(vertex_14, vertex_0, 4.4)
    g.add_undirected_edge(vertex_14, vertex_4, 2.4)
    g.add_undirected_edge(vertex_14, vertex_5, 3.0)
    g.add_undirected_edge(vertex_14, vertex_7, 3.3)
    g.add_undirected_edge(vertex_14, vertex_11, 2.6)
    g.add_undirected_edge(vertex_14, vertex_13, 1.3)

    g.add_directed_edge(vertex_13, vertex_13, 0.0)
    g.add_undirected_edge(vertex_13, vertex_0, 5.2)
    g.add_undirected_edge(vertex_13, vertex_1, 3.0)
    g.add_undirected_edge(vertex_13, vertex_3, 3.9)
    g.add_undirected_edge(vertex_13, vertex_4, 3.2)
    g.add_undirected_edge(vertex_13, vertex_5, 3.9)
    g.add_undirected_edge(vertex_13, vertex_7, 1.6)
    g.add_undirected_edge(vertex_13, vertex_11, 3.5)

    g.add_directed_edge(vertex_12, vertex_12, 0.0)
    g.add_undirected_edge(vertex_12, vertex_0, 7.6)
    g.add_undirected_edge(vertex_12, vertex_1, 4.8)
    g.add_undirected_edge(vertex_12, vertex_6, 4.2)
    g.add_undirected_edge(vertex_12, vertex_8, 0.6)
    g.add_undirected_edge(vertex_12, vertex_11, 4.7)

    g.add_directed_edge(vertex_11, vertex_11, 0.0)
    g.add_undirected_edge(vertex_11, vertex_0, 3.2)
    g.add_undirected_edge(vertex_11, vertex_2, 3.0)
    g.add_undirected_edge(vertex_11, vertex_4, 1.5)
    g.add_undirected_edge(vertex_11, vertex_5, 0.8)
    g.add_undirected_edge(vertex_11, vertex_9, 1.1)

    g.add_directed_edge(vertex_10, vertex_10, 0.0)
    g.add_undirected_edge(vertex_10, vertex_0, 6.4)
    g.add_undirected_edge(vertex_10, vertex_3, 1.0)
    g.add_undirected_edge(vertex_10, vertex_7, 4.6)

    g.add_directed_edge(vertex_9, vertex_9, 0.0)
    g.add_undirected_edge(vertex_9, vertex_0, 2.8)
    g.add_undirected_edge(vertex_9, vertex_2, 1.6)
    g.add_undirected_edge(vertex_9, vertex_4, 2.6)
    g.add_undirected_edge(vertex_9, vertex_5, 1.5)
    g.add_undirected_edge(vertex_9, vertex_8, 4.8)

    g.add_directed_edge(vertex_8, vertex_8, 0.0)
    g.add_undirected_edge(vertex_8, vertex_0, 7.6)
    g.add_undirected_edge(vertex_8, vertex_1, 4.8)
    g.add_undirected_edge(vertex_8, vertex_5, 4.5)
    g.add_undirected_edge(vertex_8, vertex_6, 4.2)

    g.add_directed_edge(vertex_7, vertex_7, 0.0)
    g.add_undirected_edge(vertex_7, vertex_0, 8.6)
    g.add_undirected_edge(vertex_7, vertex_1, 2.8)
    g.add_undirected_edge(vertex_7, vertex_3, 4.0)
    g.add_undirected_edge(vertex_7, vertex_5, 4.3)
    g.add_undirected_edge(vertex_7, vertex_6, 4.0)

    g.add_directed_edge(vertex_6, vertex_6, 0.0)
    g.add_undirected_edge(vertex_6, vertex_0, 10.9)
    g.add_undirected_edge(vertex_6, vertex_1, 1.6)
    g.add_undirected_edge(vertex_6, vertex_5, 6.3)

    g.add_directed_edge(vertex_5, vertex_5, 0.0)
    g.add_undirected_edge(vertex_5, vertex_0, 3.5)
    g.add_undirected_edge(vertex_5, vertex_2, 2.8)
    g.add_undirected_edge(vertex_5, vertex_4, 1.9)

    g.add_directed_edge(vertex_4, vertex_4, 0.0)
    g.add_undirected_edge(vertex_4, vertex_0, 2.2)
    g.add_undirected_edge(vertex_4, vertex_2, 4.4)

    g.add_directed_edge(vertex_3, vertex_3, 0.0)
    g.add_undirected_edge(vertex_3, vertex_0, 11.0)
    g.add_undirected_edge(vertex_3, vertex_1, 6.4)

    g.add_undirected_edge(vertex_2, vertex_0, 3.8)
    g.add_undirected_edge(vertex_2, vertex_1, 7.1)
    g.add_directed_edge(vertex_2, vertex_2, 0.0)

    g.add_undirected_edge(vertex_1, vertex_0, 7.2)
    g.add_directed_edge(vertex_1, vertex_1, 0.0)

    g.add_directed_edge(vertex_0, vertex_0, 0.0)
    g.set_adjacent_vertexes(vertex_0, [vertex_1, vertex_2, vertex_3, vertex_4, vertex_5, vertex_6, vertex_7,
                                       vertex_8, vertex_9, vertex_10, vertex_11, vertex_12, vertex_13,
                                       vertex_14, vertex_15, vertex_16, vertex_17, vertex_18, vertex_19, vertex_20,
                                       vertex_21, vertex_22, vertex_23, vertex_24, vertex_25, vertex_26])

    # Creating the hashtable for the Packages CSV file
    create_package_hashtable("wgups_package_file.csv")
    # packages.print()

    # Creating the hashtable for the distances between Cities CSV file
    create_distance_hashtable("wgups_distance_table.csv")
    # distances.print()

    # Try using greedy algorithm
    #       like closest neighbor

    dijkstra_shortest_path(g, vertex_0)

    print("\n\n")

    # Sort the vertices by the label, for convenience; display shortest path for each vertex
    # from vertex_a.
    for v in sorted(g.adjacency_list, key=operator.attrgetter("label")):
        print("From g.adjacency_list, Vertex v=" + v.label)
        if v.pred_vertex is None and v is not vertex_0:
            print("\tHUB to %s: no path exists" % v.label)
        else:
            path = get_shortest_path(vertex_0, v)
            print("\tHUB to " + v.label + "... PATH:(" + path[0] + "), total distance of {:.1f}".format(path[1]) + " miles!")
            # print("\tHUB to %s: %s (total distance: %g)" % (v.label, get_shortest_path(vertex_0, v), v.distance))










    # This while loop controls the console menu users interact with
    while False:
        print("""
    Welcome to the menu! Enter your selection below 
        1. Find total miles traveled
        2. Get snapshot
        3. Print Packages HashTable
        4. Print Distances HashTable
        5. Graphics
        6. Show ALL constrained Packages
        7. Find miles travelled from selected Packages
        0. Exit/Quit
    """)
        ans = input("What would you like to do? INPUT: ")
        print()
        if ans == "1":
            """ Find Total miles travelled """

            current_best = 0.0
            best_distance = float("inf")

            # my_packages = select_random_packages(packages.count)
            # route_distance = distance_of_route_as_ordered(select_random_packages(packages.count))
            # print("route1_distance is {:.1f}".format(route_distance) + " MILES and delivered "
            #       + str(len(my_packages)) + " packages.")
            # current_best = route_distance

            if current_best < best_distance:
                best_distance = current_best
                print("NEW BEST RECORD!!! Only {:.1f}".format(best_distance) + " MILES")

        elif ans == "2":
            """ Show snapshot - the current status of each package """
            print("Get snapshot")
        elif ans == "3":
            """ shows package HashTable 
                    useful for internal testing """
            print("\nPACKAGE HashTable")
            packages.print()

        elif ans == "4":
            """ shows distances HashTable
                    useful for internal testing """
            print("\nHere's the HashTable of DISTANCES for you...")
            distances.print()
        elif ans == "5":
            """ graphically show a snapshot """

        elif ans == "6":
            """" Prints all Packages with constraints """
            # get the keys for priority packages
            constrained_keys = get_constrained_packages(packages)
            for p in constrained_keys:
                print(p)

            print("There are " + str(len(constrained_keys)) + " constrained Packages.")
        elif ans == "7":
            """ Find distance travelled to deliver these select packages
                    I am unsure why this is an input option and not its own function. """
            k = 0
            trip1 = []
            for item in range(packages.get_count()):
                k += 1
                # print("k % 4 = " + str(k%4))
                if k % 4 == 0:
                    continue
                trip1.append(packages.get(k)[0])

            distance_of_route_as_ordered(trip1)
        elif ans == "0":
            """ exit the program"""
            raise SystemExit
        else:
            """ If user enters an unanticipated option, they should be re-prompted for input"""
            print("Not a Valid Choice. Try again")


# Main for this Project
if __name__ == "__main__":
    main()





