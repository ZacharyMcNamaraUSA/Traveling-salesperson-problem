# barebones.py by Zachary McNamara zmcnama@my.wgu.edu ID#001182706

import copy
import csv
from cmath import inf

import package
import truck
import hashtable
from graph import Graph, Vertex
import operator

packages = hashtable.HashTable()
distances = hashtable.HashTable()
joined = hashtable.HashTable()
at_station_package_keys = []
vertices = {}
hour = 8
minute = 0
truck_1 = truck.Truck("Truck 1")
truck_2 = truck.Truck("Truck 2")
truck_3 = truck.Truck("Truck 3")
trucks_all = [truck_2, truck_1, truck_3]
max_packages = 16
speed = 18


# Function create_package_hashtable populates the custom hashtable data structure for package info
#   receives and parses a csv file with wgups package info
def create_package_hashtable(filename):
    with open(filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')

        for row in read_csv:  # For every row in CSV file
            key = row[0]
            new_package = [key, row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
            packages.add(key, new_package)
            at_station_package_keys.append(key)

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

            row.insert(0, str(stop_count))
            distances.add(key, row)
            stop_count += 1

        distance_csv.close()


# Function selects package(s) with a delivery deadline or special notes
def get_constrained_packages(p_list):

    # keys is a list of keys to be returned
    keys = []

    # loop through each package
    for p in range(1, p_list.count):
        pack = packages.get(p)

        # If the package has a specific delivery deadline or special notes, append its key to keys
        if pack[5] != "EOD" or pack[7] != "":
            keys.append(pack)

    return keys


# Function prints constraints for any of the provided packages
def print_constrained_info(constrained_list):
    for pack in constrained_list:
        message = ""

        # This if condition reruns the loop if the Package pack is not constrained.
        #       Therefore, if the condition does not stop the loop, pack is a constrained package
        #       The condition here is to ensure only specially constrained packages are returned
        if pack[5] == "EOD" and pack[7] == "":
            continue

        message += "package " + pack[0] + "\n"

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

        # Visit vertex with minimum distance from start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i

        current_vertex = unvisited_queue.pop(smallest_index)

        # Check potential path lengths from the current vertex to all adjacent vertices.
        for adj_vertex in g.adjacency_list[current_vertex]:

            try:
                edge_weight = g.edge_weights[(current_vertex, adj_vertex)]
                alternative_path_distance = current_vertex.distance + edge_weight
            except KeyError:
                print("PROBLEM! No edge between curr_v=" + current_vertex.label + " and adj_v=" + adj_vertex.label)
                continue

            # If shorter path from start_vertex to adj_vertex is found,
            # update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex


def get_shortest_path(start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = ""
    current_vertex = end_vertex

    while current_vertex is not start_vertex:
        path = " -> " + str(current_vertex.label) + " is {:.1f}".format(current_vertex.distance) + " miles" + path
        current_vertex = current_vertex.pred_vertex

    path = start_vertex.label + path
    return path


def main():

    # Creating the hashtable for the Packages CSV file
    create_package_hashtable("wgups_package_file.csv")

    # creates a list of keys for packages with delivery deadlines or special delivery notes
    constrained_keys = get_constrained_packages(packages)

    # Creating the hashtable for the distances between Cities CSV file
    create_distance_hashtable("wgups_distance_table.csv")

    for n in range(1, packages.count + 1):
        pack = packages.get(n)
        stop = distances.get(pack[1])[2]
        packages.add(stop, pack)

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

    # Try using greedy algorithm
    #       like closest neighbor

    dijkstra_shortest_path(g, vertex_0)

    assigned_vertexes = [vertex_0]

    # First task is to load the trucks

    # Load Truck 2 with the packages that can only go on truck 2
    for p in constrained_keys:
        if "truck 2" in p[7]:
            print("Loading package #{0} to truck 2.\n\t\t\t\taddress: {1}".format(p[0], p[1]))
            truck_2.loaded_package_keys.append(p[0])
            at_station_package_keys.remove(p[0])
            assigned_vertexes.append(g.get_vertex(p[1]))
            truck_2.miles_driven += g.get_vertex(p[1]).distance

    # if any package's address matches any address truck_2 is already stopping at, load it
    for n in at_station_package_keys:
        for k in truck_2.loaded_package_keys:
            pap = packages.get(n)
            if pap[1] in packages.get(k) and len(truck_2.loaded_package_keys) < max_packages:
                print("\tEZ pickings! package #{0} \n\t\t\t\taddress: {1}".format(pap[0], pap[1]))
                assigned_vertexes.append(pap[1])

    # loop through every truck to load them as appropriate
    #   trucks_all = [truck_2, truck_1, truck_3]
    for current_truck in trucks_all:
        print("Trying to load up {0}".format(current_truck.label))
        print("There are {0} packages remaining at the HUB.".format(len(at_station_package_keys)))

        count = 0
        # loop through every package that is loaded
        for n in current_truck.loaded_package_keys:

            if len(current_truck.loaded_package_keys) >= max_packages:
                print("We got a full load over here :(((((((((((((((((((((((((((((((((((")
                break

            count += 1
            print("\n\n\ncount: {0}".format(count))
            print("package #{0} has already been loaded".format(n))
            pack = packages.get(n)

            vert = g.get_vertex(pack[1])
            print("vert.label=" + vert.label)

            print("package #" + str(n) + " goes to " + vert.label)

            can = 0
            for adj in g.adjacency_list[vert]:
                can += 1
                print("can={0}".format(can))
                if adj == vert or g.get_vertex(adj.label) in assigned_vertexes:
                    continue

                print("\t\tadjacent vertex:\t" + adj.label)

                dist = g.edge_weights[(vert, adj)]
                print("\t\t\t\t\t\t\t\tdistance = {:.1f}".format(dist))

                if 3.5 >= dist > 0.0:
                    p = packages.get(adj.label)
                    print("p = packages.get(adj.label)...")
                    print(p)
                    print("p[0]={0} should be the key of the package that I am loading onto {1}".format(p[0],
                                                                                                        current_truck.label))
                    current_truck.loaded_package_keys.append(p[0])
                    at_station_package_keys.remove(p[0])
                    assigned_vertexes.append(g.get_vertex(p[1]))
                    print("loading {0} with package #{1}, address={2}, because it is only {3} miles away"
                          .format(current_truck.label, p[0], p[1], dist))

                    print("{0} now has {1} packages loaded.\n".format(current_truck.label,
                                                                      len(current_truck.loaded_package_keys)))

        # possibly reorder the packages in the truck here...
        # good way to decrease mileage

        # find packages to add until the truck is at maximum capacity
        #   break the loop if no acceptable packages are available



        # while len(current_truck.loaded_package_keys) < max_packages or len(at_station_package_keys) <= 0:














    # This while loop controls the console menu users interact with
    while True:
        print("""
    Welcome to the menu! Enter your selection below 
        1. Find shortest distance to every Stop
        2. Get snapshot
        3. Print Packages HashTable
        4. Print Distances HashTable
        5. Print joined HashTable [packages: distances]
        6. Show ALL constrained Packages
        7. Find miles travelled by each truck
        0. Exit/Quit
    """)
        ans = input("What would you like to do? INPUT: ")
        print()
        if ans == "1":
            """ Find shortest distance to every Stop """

            # Sort the vertices by the label, for convenience; display shortest path for each vertex
            # from vertex_a.
            for v in sorted(g.adjacency_list, key=operator.attrgetter("label")):
                print("From g.adjacency_list, Vertex v=" + v.label)
                if v.pred_vertex is None and v is not vertex_0:
                    print("\tHUB to %s: no path exists" % v.label)
                else:
                    path = get_shortest_path(vertex_0, v)
                    print("\tShortest path from " + vertex_0.label + " to " + v.label + ": (" + path + ").\n" +
                          "\t\tThis traverses {:.1f}".format(v.distance) + " miles!")

        elif ans == "2":
            """ Show snapshot - the current status of each package """

            # Idea for how to do snapshot, have a List of delivered packages? no. dict.
            #   key: package key = [truck that delivered it, stated delivery deadline, actual time delivered,
            #       any special notes - ideally there will be none but creating space for some is good for scalability

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
            """ Print joined HashTable """

            print("\n\n\n")

            p = packages.get(1)
            print(p)
            s = distances.get(p[1])
            print(s)
            # joined.get(p).print()

        elif ans == "6":
            """" Prints all packages with constraints (delivery deadline or special notes) """
            # get the keys for all constrained packages
            for p in constrained_keys:
                print(p)

            print("There are " + str(len(constrained_keys)) + " constrained Packages.")
        elif ans == "7":
            """ Find miles travelled by each truck """

            for t in trucks_all:
                print("{0} has {1} packages, spanning {2:.1f} miles.".format(t.label,
                                                                         len(t.loaded_package_keys), t.miles_driven))

            # pseudo-code...
            # for loop through each truck
            #       find where each package's delivery address line matches with a vertex
            #       the distance of each vertex to be delivered to is added together for that truck's total mileage

        elif ans == "0":
            """ exit the program"""
            raise SystemExit
        else:
            """ If user enters an unanticipated option, they should be re-prompted for input"""
            print("Not a Valid Choice. Try again")


# Main for this Project
if __name__ == "__main__":
    main()





