# barebones.py by Zachary McNamara zmcnama@my.wgu.edu ID#001182706

import copy
import csv
import random
from cmath import inf
from typing import List, Any

import package
import truck
import hashtable
from graph import Graph, Vertex
import operator

packages = hashtable.HashTable()
distances = hashtable.HashTable()
joined = hashtable.HashTable()
at_station_packages: package = []
vertices = {}
hour = 8
minute = 0
truck_1 = truck.Truck("Truck 1")
truck_2 = truck.Truck("Truck 2")
truck_3 = truck.Truck("Truck 3")
trucks_all = [truck_2, truck_1, truck_3]
max_packages = 16
speed = 18
hub_address = "4001 South 700 East"


# Function create_package_hashtable populates the custom hashtable data structure for package info
#   receives and parses a csv file with wgups package info
def create_package_hashtable(filename):
    with open(filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')

        for row in read_csv:  # For every row in CSV file
            key = row[0]
            new_package = [key, row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
            packages.add(key, new_package)
            at_station_packages.append(new_package)

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

    # list of packages to return
    packs = []

    # loop through each package
    for p in range(1, p_list.count):
        pack = packages.get(p)

        # If the package has a specific delivery deadline or special notes, append its key to keys
        if pack[5] != "EOD" or pack[7] != "":
            packs.append(pack)

    return packs


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
    shortest_distance = start_vertex.distance
    current_vertex = end_vertex

    while current_vertex is not start_vertex:

        print("current_vertex.label={0}".format(current_vertex.label))
        path = " -> " + str(current_vertex.label) + " is {:.1f}".format(current_vertex.distance) + " miles" + path
        current_vertex = current_vertex.pred_vertex

    path = start_vertex.label + path
    return path


def main():

    # Creating the hashtable for the Packages CSV file
    create_package_hashtable("wgups_package_file.csv")

    # creates a list of keys for packages with delivery deadlines or special delivery notes
    constrained_packages = get_constrained_packages(packages)
    # print_constrained_info(constrained_packages)

    # Creating the hashtable for the distances between Cities CSV file
    create_distance_hashtable("wgups_distance_table.csv")

    for n in range(1, packages.count + 1):
        testing_index = packages.get(n)
        stop = distances.get(testing_index[1])[2]
        packages.add(stop, testing_index)

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

    # Try using greedy algorithm
    #       like closest neighbor

    global at_station_packages
    print("# of packages at station = {0}.\n\n".format(len(at_station_packages)))

    # First task is to load the trucks

    # put package #9 in Truck 3, the last truck to leave the depot
    p9 = packages.get(9)
    constrained_packages.remove(p9)
    at_station_packages.remove(p9)
    truck_3.loaded_packages.append(p9)

    # Load Truck 2 with the packages that can only go on truck 2
    t_constrained_packages = constrained_packages.copy()
    for p in constrained_packages:
        if "truck 2" in p[7]:
            t_constrained_packages.remove(p)
            at_station_packages.remove(p)
            truck_2.loaded_packages.append(p)
            truck_2.stops.append(g.get_vertex(p[1]))
            print("\tadding package={0}".format(p))

    constrained_packages = t_constrained_packages.copy()
    # loop through all packages at the station.
    # If they have a matching address to any package loaded in truck_2, load them as well.
    print("len(truck_2.loaded_packages)={0}".format(len(truck_2.loaded_packages)))
    t_at_station_packages = at_station_packages.copy()
    t_loaded_packages = truck_2.loaded_packages.copy()
    for loaded_p in truck_2.loaded_packages:
        # print("loaded_p={0}".format(loaded_p))
        for p in at_station_packages:
            # print("\tloaded_p, p[0] = ({0}, {1}".format(loaded_p, p[0]))
            if p[1] in loaded_p:
                # load package p
                try:
                    t_loaded_packages.append(p)
                    t_at_station_packages.remove(p)
                    constrained_packages.remove(p)
                    truck_2.stops.append(g.get_vertex(p[1]))
                except ValueError:
                    break
    at_station_packages = t_at_station_packages.copy()
    truck_2.loaded_packages = t_loaded_packages.copy()

    i = 0
    # load the rest of truck_2, as appropriate
    while len(truck_2.loaded_packages) < max_packages:

        # add packages, that are not constrained
        t_pack = at_station_packages[i]
        # print("\tt_pack={0}".format(t_pack))
        if t_pack in constrained_packages:
            i += 1
            continue

        try:
            at_station_packages.remove(t_pack)
            truck_2.loaded_packages.append(t_pack)
            truck_2.stops.append(g.get_vertex(t_pack[1]))
            print("\t\tLOAD Pack#{0} to truck2".format(t_pack[0]))
        except ValueError:
            print("\t\tValueError while loading the rest of truck-2")

    print("Truck_{0} has {1} packages loaded.\n\n".format(truck_2.label[-1], len(truck_2.loaded_packages)))

    # Truck_3 is the final truck to leave the depot - aka the remainder/misfit route.
    i = 0
    t_constrained_packages = constrained_packages.copy()
    for cp in constrained_packages:
        if "Delayed" in cp[7]:
            print("\t\tLoading package #{0}".format(cp[0]))
            truck_3.loaded_packages.append(cp)
            truck_3.stops.append(g.get_vertex(cp[1]))
            at_station_packages.remove(cp)
            t_constrained_packages.remove(cp)

    constrained_packages = list(t_constrained_packages)

    # If any packages at the station are going to same address as packages loaded in truck_3,
    #       load the packages, if they do not have an early delivery deadline
    for lp in truck_3.loaded_packages:
        for p in at_station_packages:
            if p[5] == "EOD" and p[1] == lp[1] and "Wrong address" not in p[7]:
                # load the package
                try:
                    truck_3.loaded_packages.append(p)
                    at_station_packages.remove(p)
                    truck_3.stops.append(g.get_vertex(p[1]))
                    print("\t\t  "
                          "LOAD Pack#{0} to truck_3".format(p[0]))
                except ValueError:
                    print("ERROR ERROR VALUE ERROR while loading truck_3")
                    break
    print("Truck_{0} has {1} packages loaded.".format(truck_3.number, len(truck_3.loaded_packages)))

    # Load truck 1 with any remaining time-sensitive deliveries (remaining in constrained_packages)
    print("\n\nTruck_1 has only {0} packages.".format(len(truck_1.loaded_packages)))
    for cp in constrained_packages:
        print("\t\tLoading package #{0}".format(cp[0]))
        truck_1.loaded_packages.append(cp)
        at_station_packages.remove(cp)

    # IF any packages share address or are very close to stops assigned, load them here.
    t_at_station_packages = at_station_packages.copy()
    for p in at_station_packages:
        print("\t\tLoading package #{0}".format(p[0]))
        truck_1.loaded_packages.append(p)
        t_at_station_packages.remove(p)
        truck_1.stops.append(g.get_vertex(p[1]))
        if len(t_at_station_packages) <= 0 or len(truck_1.loaded_packages) >= max_packages:
            break
    at_station_packages = list(t_at_station_packages)
    print("Truck {0} has {1} packages.".format(truck_1.label[-1], len(truck_1.loaded_packages)))

    # Load truck 3 with any packages left at station
    print("\n\nTruck_{0} has {1} packages loaded.".format(truck_3.number, len(truck_3.loaded_packages)))
    for p in t_at_station_packages:
        print("\t\tLoading package #{0}".format(p[0]))
        at_station_packages.remove(p)
        truck_3.loaded_packages.append(p)
        truck_3.stops.append(g.get_vertex(p[1]))
    print("Truck {0} has {1} packages.".format(truck_3.label[-1], len(truck_3.loaded_packages)))

    print("\n\n# of packages remain at station = {0}\n".format(len(at_station_packages)))

    g.add_directed_edge(vertex_26, vertex_26, 0.0)
    g.add_undirected_edge(vertex_26, vertex_25, 8.3)
    g.add_undirected_edge(vertex_26, vertex_24, 1.3)
    g.add_undirected_edge(vertex_26, vertex_23, 7.8)
    g.add_undirected_edge(vertex_26, vertex_22, 3.1)
    g.add_undirected_edge(vertex_26, vertex_21, 4.7)
    g.add_undirected_edge(vertex_26, vertex_20, 4.1)
    g.add_undirected_edge(vertex_26, vertex_19, 13.1)
    g.add_undirected_edge(vertex_26, vertex_18, 6.9)
    g.add_undirected_edge(vertex_26, vertex_17, 5.2)
    g.add_undirected_edge(vertex_26, vertex_16, 13.6)
    g.add_undirected_edge(vertex_26, vertex_15, 8.4)
    g.add_undirected_edge(vertex_26, vertex_14, 8.8)
    g.add_undirected_edge(vertex_26, vertex_13, 10.5)
    g.add_undirected_edge(vertex_26, vertex_12, 14.1)
    g.add_undirected_edge(vertex_26, vertex_11, 6.4)
    g.add_undirected_edge(vertex_26, vertex_10, 6.8)
    g.add_undirected_edge(vertex_26, vertex_9, 6.0)
    g.add_undirected_edge(vertex_26, vertex_8, 14.1)
    g.add_undirected_edge(vertex_26, vertex_7, 10.7)
    g.add_undirected_edge(vertex_26, vertex_6, 14.2)
    g.add_undirected_edge(vertex_26, vertex_5, 7.2)
    g.add_undirected_edge(vertex_26, vertex_4, 5.5)
    g.add_undirected_edge(vertex_26, vertex_3, 10.1)
    g.add_undirected_edge(vertex_26, vertex_2, 7.4)
    g.add_undirected_edge(vertex_26, vertex_1, 13.0)
    g.add_undirected_edge(vertex_26, vertex_0, 3.6)

    g.add_directed_edge(vertex_25, vertex_25, 0.0)
    g.add_undirected_edge(vertex_25, vertex_0, 5.0)
    g.add_undirected_edge(vertex_25, vertex_1, 4.4)
    g.add_undirected_edge(vertex_25, vertex_2, 2.8)
    g.add_undirected_edge(vertex_25, vertex_3, 10.1)
    g.add_undirected_edge(vertex_25, vertex_4, 5.4)
    g.add_undirected_edge(vertex_25, vertex_5, 3.5)
    g.add_undirected_edge(vertex_25, vertex_6, 5.1)
    g.add_undirected_edge(vertex_25, vertex_7, 6.2)
    g.add_undirected_edge(vertex_25, vertex_8, 2.8)
    g.add_undirected_edge(vertex_25, vertex_9, 3.2)
    g.add_undirected_edge(vertex_25, vertex_10, 11.0)
    g.add_undirected_edge(vertex_25, vertex_11, 3.7)
    g.add_undirected_edge(vertex_25, vertex_12, 2.8)
    g.add_undirected_edge(vertex_25, vertex_13, 6.4)
    g.add_undirected_edge(vertex_25, vertex_14, 6.5)
    g.add_undirected_edge(vertex_25, vertex_15, 5.7)
    g.add_undirected_edge(vertex_25, vertex_16, 6.2)
    g.add_undirected_edge(vertex_25, vertex_17, 5.1)
    g.add_undirected_edge(vertex_25, vertex_18, 4.3)
    g.add_undirected_edge(vertex_25, vertex_19, 1.8)
    g.add_undirected_edge(vertex_25, vertex_20, 6.0)
    g.add_undirected_edge(vertex_25, vertex_21, 7.9)
    g.add_undirected_edge(vertex_25, vertex_22, 6.8)
    g.add_undirected_edge(vertex_25, vertex_23, 10.6)
    g.add_undirected_edge(vertex_25, vertex_24, 7.0)

    g.add_directed_edge(vertex_24, vertex_24, 0.0)
    g.add_undirected_edge(vertex_24, vertex_0, 2.4)
    g.add_undirected_edge(vertex_24, vertex_1, 10.0)
    g.add_undirected_edge(vertex_24, vertex_2, 6.1)
    g.add_undirected_edge(vertex_24, vertex_3, 6.4)
    g.add_undirected_edge(vertex_24, vertex_4, 4.2)
    g.add_undirected_edge(vertex_24, vertex_5, 4.2)
    g.add_undirected_edge(vertex_24, vertex_6, 11.7)
    g.add_undirected_edge(vertex_24, vertex_7, 9.5)
    g.add_undirected_edge(vertex_24, vertex_8, 9.5)
    g.add_undirected_edge(vertex_24, vertex_9, 4.8)
    g.add_undirected_edge(vertex_24, vertex_10, 4.9)
    g.add_undirected_edge(vertex_24, vertex_11, 5.2)
    g.add_undirected_edge(vertex_24, vertex_12, 9.5)
    g.add_undirected_edge(vertex_24, vertex_13, 7.2)
    g.add_undirected_edge(vertex_24, vertex_14, 6.3)
    g.add_undirected_edge(vertex_24, vertex_15, 5.9)
    g.add_undirected_edge(vertex_24, vertex_16, 11.1)
    g.add_undirected_edge(vertex_24, vertex_17, 4.0)
    g.add_undirected_edge(vertex_24, vertex_18, 5.6)
    g.add_undirected_edge(vertex_24, vertex_19, 8.5)
    g.add_undirected_edge(vertex_24, vertex_20, 2.8)
    g.add_undirected_edge(vertex_24, vertex_21, 3.4)
    g.add_undirected_edge(vertex_24, vertex_22, 1.7)
    g.add_undirected_edge(vertex_24, vertex_23, 5.4)

    g.add_directed_edge(vertex_23, vertex_23, 0.0)
    g.add_undirected_edge(vertex_23, vertex_0, 6.4)
    g.add_undirected_edge(vertex_23, vertex_1, 6.9)
    g.add_undirected_edge(vertex_23, vertex_2, 9.7)
    g.add_undirected_edge(vertex_23, vertex_3, 0.6)
    g.add_undirected_edge(vertex_23, vertex_4, 6.0)
    g.add_undirected_edge(vertex_23, vertex_5, 9.0)
    g.add_undirected_edge(vertex_23, vertex_6, 8.2)
    g.add_undirected_edge(vertex_23, vertex_7, 4.2)
    g.add_undirected_edge(vertex_23, vertex_8, 11.5)
    g.add_undirected_edge(vertex_23, vertex_9, 7.8)
    g.add_undirected_edge(vertex_23, vertex_10, 0.4)
    g.add_undirected_edge(vertex_23, vertex_11, 6.9)
    g.add_undirected_edge(vertex_23, vertex_12, 11.5)
    g.add_undirected_edge(vertex_23, vertex_13, 4.4)
    g.add_undirected_edge(vertex_23, vertex_14, 4.8)
    g.add_undirected_edge(vertex_23, vertex_15, 5.6)
    g.add_undirected_edge(vertex_23, vertex_16, 7.5)
    g.add_undirected_edge(vertex_23, vertex_17, 5.5)
    g.add_undirected_edge(vertex_23, vertex_18, 6.5)
    g.add_undirected_edge(vertex_23, vertex_19, 11.4)
    g.add_undirected_edge(vertex_23, vertex_20, 6.4)
    g.add_undirected_edge(vertex_23, vertex_21, 7.9)
    g.add_undirected_edge(vertex_23, vertex_22, 4.5)

    g.add_directed_edge(vertex_22, vertex_22, 0.0)
    g.add_undirected_edge(vertex_22, vertex_0, 2.4)
    g.add_undirected_edge(vertex_22, vertex_1, 8.3)
    g.add_undirected_edge(vertex_22, vertex_2, 6.1)
    g.add_undirected_edge(vertex_22, vertex_3, 4.7)
    g.add_undirected_edge(vertex_22, vertex_4, 2.5)
    g.add_undirected_edge(vertex_22, vertex_5, 4.2)
    g.add_undirected_edge(vertex_22, vertex_6, 10.0)
    g.add_undirected_edge(vertex_22, vertex_7, 7.8)
    g.add_undirected_edge(vertex_22, vertex_8, 7.8)
    g.add_undirected_edge(vertex_22, vertex_9, 4.3)
    g.add_undirected_edge(vertex_22, vertex_10, 4.1)
    g.add_undirected_edge(vertex_22, vertex_11, 3.4)
    g.add_undirected_edge(vertex_22, vertex_12, 7.8)
    g.add_undirected_edge(vertex_22, vertex_13, 5.5)
    g.add_undirected_edge(vertex_22, vertex_14, 4.6)
    g.add_undirected_edge(vertex_22, vertex_15, 4.2)
    g.add_undirected_edge(vertex_22, vertex_16, 9.4)
    g.add_undirected_edge(vertex_22, vertex_17, 2.3)
    g.add_undirected_edge(vertex_22, vertex_18, 3.9)
    g.add_undirected_edge(vertex_22, vertex_19, 6.8)
    g.add_undirected_edge(vertex_22, vertex_20, 2.9)
    g.add_undirected_edge(vertex_22, vertex_21, 4.4)

    g.add_directed_edge(vertex_21, vertex_21, 0.0)
    g.add_undirected_edge(vertex_21, vertex_0, 3.4)
    g.add_undirected_edge(vertex_21, vertex_1, 10.9)
    g.add_undirected_edge(vertex_21, vertex_2, 5.0)
    g.add_undirected_edge(vertex_21, vertex_3, 7.5)
    g.add_undirected_edge(vertex_21, vertex_4, 5.2)
    g.add_undirected_edge(vertex_21, vertex_5, 6.9)
    g.add_undirected_edge(vertex_21, vertex_6, 12.7)
    g.add_undirected_edge(vertex_21, vertex_7, 10.4)
    g.add_undirected_edge(vertex_21, vertex_8, 10.3)
    g.add_undirected_edge(vertex_21, vertex_9, 5.8)
    g.add_undirected_edge(vertex_21, vertex_10, 8.3)
    g.add_undirected_edge(vertex_21, vertex_11, 6.2)
    g.add_undirected_edge(vertex_21, vertex_12, 10.3)
    g.add_undirected_edge(vertex_21, vertex_13, 8.2)
    g.add_undirected_edge(vertex_21, vertex_14, 7.4)
    g.add_undirected_edge(vertex_21, vertex_15, 6.9)
    g.add_undirected_edge(vertex_21, vertex_16, 12.0)
    g.add_undirected_edge(vertex_21, vertex_17, 5.0)
    g.add_undirected_edge(vertex_21, vertex_18, 6.6)
    g.add_undirected_edge(vertex_21, vertex_19, 9.3)
    g.add_undirected_edge(vertex_21, vertex_20, 2.0)

    g.add_directed_edge(vertex_20, vertex_20, 0.0)
    g.add_undirected_edge(vertex_20, vertex_0, 1.9)
    g.add_undirected_edge(vertex_20, vertex_1, 9.5)
    g.add_undirected_edge(vertex_20, vertex_2, 3.3)
    g.add_undirected_edge(vertex_20, vertex_3, 5.9)
    g.add_undirected_edge(vertex_20, vertex_4, 3.2)
    g.add_undirected_edge(vertex_20, vertex_5, 4.9)
    g.add_undirected_edge(vertex_20, vertex_6, 11.2)
    g.add_undirected_edge(vertex_20, vertex_7, 8.1)
    g.add_undirected_edge(vertex_20, vertex_8, 8.5)
    g.add_undirected_edge(vertex_20, vertex_9, 3.8)
    g.add_undirected_edge(vertex_20, vertex_10, 6.9)
    g.add_undirected_edge(vertex_20, vertex_11, 4.1)
    g.add_undirected_edge(vertex_20, vertex_12, 8.5)
    g.add_undirected_edge(vertex_20, vertex_13, 6.2)
    g.add_undirected_edge(vertex_20, vertex_14, 5.3)
    g.add_undirected_edge(vertex_20, vertex_15, 5.9)
    g.add_undirected_edge(vertex_20, vertex_16, 10.6)
    g.add_undirected_edge(vertex_20, vertex_17, 3.0)
    g.add_undirected_edge(vertex_20, vertex_18, 4.6)
    g.add_undirected_edge(vertex_20, vertex_19, 7.5)

    g.add_directed_edge(vertex_19, vertex_19, 0.0)
    g.add_undirected_edge(vertex_19, vertex_0, 6.5)
    g.add_undirected_edge(vertex_19, vertex_1, 4.8)
    g.add_undirected_edge(vertex_19, vertex_2, 4.3)
    g.add_undirected_edge(vertex_19, vertex_3, 10.6)
    g.add_undirected_edge(vertex_19, vertex_4, 6.5)
    g.add_undirected_edge(vertex_19, vertex_5, 3.5)
    g.add_undirected_edge(vertex_19, vertex_6, 3.2)
    g.add_undirected_edge(vertex_19, vertex_7, 6.7)
    g.add_undirected_edge(vertex_19, vertex_8, 1.0)
    g.add_undirected_edge(vertex_19, vertex_9, 4.1)
    g.add_undirected_edge(vertex_19, vertex_10, 11.5)
    g.add_undirected_edge(vertex_19, vertex_11, 3.7)
    g.add_undirected_edge(vertex_19, vertex_12, 1.0)
    g.add_undirected_edge(vertex_19, vertex_13, 6.9)
    g.add_undirected_edge(vertex_19, vertex_14, 6.8)
    g.add_undirected_edge(vertex_19, vertex_15, 6.4)
    g.add_undirected_edge(vertex_19, vertex_16, 7.2)
    g.add_undirected_edge(vertex_19, vertex_17, 4.9)
    g.add_undirected_edge(vertex_19, vertex_18, 4.4)

    g.add_directed_edge(vertex_18, vertex_18, 0.0)
    g.add_undirected_edge(vertex_18, vertex_0, 3.6)
    g.add_undirected_edge(vertex_18, vertex_1, 5.0)
    g.add_undirected_edge(vertex_18, vertex_2, 3.6)
    g.add_undirected_edge(vertex_18, vertex_3, 6.0)
    g.add_undirected_edge(vertex_18, vertex_4, 1.7)
    g.add_undirected_edge(vertex_18, vertex_5, 1.1)
    g.add_undirected_edge(vertex_18, vertex_6, 6.6)
    g.add_undirected_edge(vertex_18, vertex_7, 4.6)
    g.add_undirected_edge(vertex_18, vertex_8, 5.4)
    g.add_undirected_edge(vertex_18, vertex_9, 1.8)
    g.add_undirected_edge(vertex_18, vertex_10, 6.9)
    g.add_undirected_edge(vertex_18, vertex_11, 1.0)
    g.add_undirected_edge(vertex_18, vertex_12, 5.4)
    g.add_undirected_edge(vertex_18, vertex_13, 3.0)
    g.add_undirected_edge(vertex_18, vertex_14, 2.2)
    g.add_undirected_edge(vertex_18, vertex_15, 1.7)
    g.add_undirected_edge(vertex_18, vertex_16, 6.1)
    g.add_undirected_edge(vertex_18, vertex_17, 1.6)

    g.add_directed_edge(vertex_17, vertex_17, 0.0)
    g.add_undirected_edge(vertex_17, vertex_0, 2.0)
    g.add_undirected_edge(vertex_17, vertex_1, 6.0)
    g.add_undirected_edge(vertex_17, vertex_2, 4.1)
    g.add_undirected_edge(vertex_17, vertex_3, 5.3)
    g.add_undirected_edge(vertex_17, vertex_4, 0.5)
    g.add_undirected_edge(vertex_17, vertex_5, 1.9)
    g.add_undirected_edge(vertex_17, vertex_6, 7.7)
    g.add_undirected_edge(vertex_17, vertex_7, 5.1)
    g.add_undirected_edge(vertex_17, vertex_8, 5.9)
    g.add_undirected_edge(vertex_17, vertex_9, 2.3)
    g.add_undirected_edge(vertex_17, vertex_10, 6.2)
    g.add_undirected_edge(vertex_17, vertex_11, 1.2)
    g.add_undirected_edge(vertex_17, vertex_12, 5.9)
    g.add_undirected_edge(vertex_17, vertex_13, 3.2)
    g.add_undirected_edge(vertex_17, vertex_14, 2.4)
    g.add_undirected_edge(vertex_17, vertex_15, 1.6)
    g.add_undirected_edge(vertex_17, vertex_16, 7.1)

    g.add_directed_edge(vertex_16, vertex_16, 0.0)
    g.add_undirected_edge(vertex_16, vertex_0, 7.6)
    g.add_undirected_edge(vertex_16, vertex_1, 7.4)
    g.add_undirected_edge(vertex_16, vertex_2, 5.7)
    g.add_undirected_edge(vertex_16, vertex_3, 7.2)
    g.add_undirected_edge(vertex_16, vertex_4, 1.4)
    g.add_undirected_edge(vertex_16, vertex_5, 5.7)
    g.add_undirected_edge(vertex_16, vertex_6, 7.2)
    g.add_undirected_edge(vertex_16, vertex_7, 3.1)
    g.add_undirected_edge(vertex_16, vertex_8, 7.2)
    g.add_undirected_edge(vertex_16, vertex_9, 6.7)
    g.add_undirected_edge(vertex_16, vertex_10, 8.1)
    g.add_undirected_edge(vertex_16, vertex_11, 6.3)
    g.add_undirected_edge(vertex_16, vertex_12, 7.2)
    g.add_undirected_edge(vertex_16, vertex_13, 4.0)
    g.add_undirected_edge(vertex_16, vertex_14, 6.4)
    g.add_undirected_edge(vertex_16, vertex_15, 5.6)

    g.add_directed_edge(vertex_15, vertex_15, 0.0)
    g.add_undirected_edge(vertex_15, vertex_0, 3.7)
    g.add_undirected_edge(vertex_15, vertex_1, 4.5)
    g.add_undirected_edge(vertex_15, vertex_2, 5.8)
    g.add_undirected_edge(vertex_15, vertex_3, 4.4)
    g.add_undirected_edge(vertex_15, vertex_4, 2.7)
    g.add_undirected_edge(vertex_15, vertex_5, 3.8)
    g.add_undirected_edge(vertex_15, vertex_6, 5.8)
    g.add_undirected_edge(vertex_15, vertex_7, 3.4)
    g.add_undirected_edge(vertex_15, vertex_8, 6.6)
    g.add_undirected_edge(vertex_15, vertex_9, 4.0)
    g.add_undirected_edge(vertex_15, vertex_10, 5.4)
    g.add_undirected_edge(vertex_15, vertex_11, 2.9)
    g.add_undirected_edge(vertex_15, vertex_12, 6.6)
    g.add_undirected_edge(vertex_15, vertex_13, 1.5)
    g.add_undirected_edge(vertex_15, vertex_14, 0.6)

    g.add_directed_edge(vertex_14, vertex_14, 0.0)
    g.add_undirected_edge(vertex_14, vertex_0, 4.4)
    g.add_undirected_edge(vertex_14, vertex_1, 4.6)
    g.add_undirected_edge(vertex_14, vertex_2, 5.6)
    g.add_undirected_edge(vertex_14, vertex_3, 4.3)
    g.add_undirected_edge(vertex_14, vertex_4, 2.4)
    g.add_undirected_edge(vertex_14, vertex_5, 3.0)
    g.add_undirected_edge(vertex_14, vertex_6, 8.0)
    g.add_undirected_edge(vertex_14, vertex_7, 3.3)
    g.add_undirected_edge(vertex_14, vertex_8, 7.8)
    g.add_undirected_edge(vertex_14, vertex_9, 3.7)
    g.add_undirected_edge(vertex_14, vertex_10, 5.2)
    g.add_undirected_edge(vertex_14, vertex_11, 2.6)
    g.add_undirected_edge(vertex_14, vertex_12, 7.8)
    g.add_undirected_edge(vertex_14, vertex_13, 1.3)

    g.add_directed_edge(vertex_13, vertex_13, 0.0)
    g.add_undirected_edge(vertex_13, vertex_0, 5.2)
    g.add_undirected_edge(vertex_13, vertex_1, 3.0)
    g.add_undirected_edge(vertex_13, vertex_2, 6.5)
    g.add_undirected_edge(vertex_13, vertex_3, 3.9)
    g.add_undirected_edge(vertex_13, vertex_4, 3.2)
    g.add_undirected_edge(vertex_13, vertex_5, 3.9)
    g.add_undirected_edge(vertex_13, vertex_6, 4.2)
    g.add_undirected_edge(vertex_13, vertex_7, 1.6)
    g.add_undirected_edge(vertex_13, vertex_8, 7.6)
    g.add_undirected_edge(vertex_13, vertex_9, 4.6)
    g.add_undirected_edge(vertex_13, vertex_10, 4.9)
    g.add_undirected_edge(vertex_13, vertex_11, 3.5)
    g.add_undirected_edge(vertex_13, vertex_12, 7.3)

    g.add_directed_edge(vertex_12, vertex_12, 0.0)
    g.add_undirected_edge(vertex_12, vertex_0, 7.6)
    g.add_undirected_edge(vertex_12, vertex_1, 4.8)
    g.add_undirected_edge(vertex_12, vertex_2, 5.3)
    g.add_undirected_edge(vertex_12, vertex_3, 11.1)
    g.add_undirected_edge(vertex_12, vertex_4, 7.5)
    g.add_undirected_edge(vertex_12, vertex_5, 4.5)
    g.add_undirected_edge(vertex_12, vertex_6, 4.2)
    g.add_undirected_edge(vertex_12, vertex_7, 7.7)
    g.add_undirected_edge(vertex_12, vertex_8, 0.6)
    g.add_undirected_edge(vertex_12, vertex_9, 5.1)
    g.add_undirected_edge(vertex_12, vertex_10, 12.0)
    g.add_undirected_edge(vertex_12, vertex_11, 4.7)

    g.add_directed_edge(vertex_11, vertex_11, 0.0)
    g.add_undirected_edge(vertex_11, vertex_0, 3.2)
    g.add_undirected_edge(vertex_11, vertex_1, 5.3)
    g.add_undirected_edge(vertex_11, vertex_2, 3.0)
    g.add_undirected_edge(vertex_11, vertex_3, 6.4)
    g.add_undirected_edge(vertex_11, vertex_4, 1.5)
    g.add_undirected_edge(vertex_11, vertex_5, 0.8)
    g.add_undirected_edge(vertex_11, vertex_6, 6.9)
    g.add_undirected_edge(vertex_11, vertex_7, 4.8)
    g.add_undirected_edge(vertex_11, vertex_8, 4.7)
    g.add_undirected_edge(vertex_11, vertex_9, 1.1)
    g.add_undirected_edge(vertex_11, vertex_10, 7.3)

    g.add_directed_edge(vertex_10, vertex_10, 0.0)
    g.add_undirected_edge(vertex_10, vertex_0, 6.4)
    g.add_undirected_edge(vertex_10, vertex_1, 7.3)
    g.add_undirected_edge(vertex_10, vertex_2, 10.4)
    g.add_undirected_edge(vertex_10, vertex_3, 1.0)
    g.add_undirected_edge(vertex_10, vertex_4, 6.5)
    g.add_undirected_edge(vertex_10, vertex_5, 8.7)
    g.add_undirected_edge(vertex_10, vertex_6, 8.6)
    g.add_undirected_edge(vertex_10, vertex_7, 4.6)
    g.add_undirected_edge(vertex_10, vertex_8, 11.9)
    g.add_undirected_edge(vertex_10, vertex_9, 9.4)

    g.add_directed_edge(vertex_9, vertex_9, 0.0)
    g.add_undirected_edge(vertex_9, vertex_0, 2.8)
    g.add_undirected_edge(vertex_9, vertex_1, 6.3)
    g.add_undirected_edge(vertex_9, vertex_2, 1.6)
    g.add_undirected_edge(vertex_9, vertex_3, 7.3)
    g.add_undirected_edge(vertex_9, vertex_4, 2.6)
    g.add_undirected_edge(vertex_9, vertex_5, 1.5)
    g.add_undirected_edge(vertex_9, vertex_6, 8.0)
    g.add_undirected_edge(vertex_9, vertex_7, 9.3)
    g.add_undirected_edge(vertex_9, vertex_8, 4.8)

    g.add_directed_edge(vertex_8, vertex_8, 0.0)
    g.add_undirected_edge(vertex_8, vertex_0, 7.6)
    g.add_undirected_edge(vertex_8, vertex_1, 4.8)
    g.add_undirected_edge(vertex_8, vertex_2, 5.3)
    g.add_undirected_edge(vertex_8, vertex_3, 11.1)
    g.add_undirected_edge(vertex_8, vertex_4, 7.5)
    g.add_undirected_edge(vertex_8, vertex_5, 4.5)
    g.add_undirected_edge(vertex_8, vertex_6, 4.2)
    g.add_undirected_edge(vertex_8, vertex_7, 7.7)

    g.add_directed_edge(vertex_7, vertex_7, 0.0)
    g.add_undirected_edge(vertex_7, vertex_0, 8.6)
    g.add_undirected_edge(vertex_7, vertex_1, 2.8)
    g.add_undirected_edge(vertex_7, vertex_2, 6.3)
    g.add_undirected_edge(vertex_7, vertex_3, 4.0)
    g.add_undirected_edge(vertex_7, vertex_4, 5.1)
    g.add_undirected_edge(vertex_7, vertex_5, 4.3)
    g.add_undirected_edge(vertex_7, vertex_6, 4.0)

    g.add_directed_edge(vertex_6, vertex_6, 0.0)
    g.add_undirected_edge(vertex_6, vertex_0, 10.9)
    g.add_undirected_edge(vertex_6, vertex_1, 1.6)
    g.add_undirected_edge(vertex_6, vertex_2, 8.6)
    g.add_undirected_edge(vertex_6, vertex_3, 8.6)
    g.add_undirected_edge(vertex_6, vertex_4, 7.9)
    g.add_undirected_edge(vertex_6, vertex_5, 6.3)

    g.add_directed_edge(vertex_5, vertex_5, 0.0)
    g.add_undirected_edge(vertex_5, vertex_0, 3.5)
    g.add_undirected_edge(vertex_5, vertex_1, 4.8)
    g.add_undirected_edge(vertex_5, vertex_2, 2.8)
    g.add_undirected_edge(vertex_5, vertex_3, 6.9)
    g.add_undirected_edge(vertex_5, vertex_4, 1.9)

    g.add_directed_edge(vertex_4, vertex_4, 0.0)
    g.add_undirected_edge(vertex_4, vertex_0, 2.2)
    g.add_undirected_edge(vertex_4, vertex_1, 6.0)
    g.add_undirected_edge(vertex_4, vertex_2, 4.4)
    g.add_undirected_edge(vertex_4, vertex_3, 5.6)

    g.add_directed_edge(vertex_3, vertex_3, 0.0)
    g.add_undirected_edge(vertex_3, vertex_0, 11.0)
    g.add_undirected_edge(vertex_3, vertex_1, 6.4)
    g.add_undirected_edge(vertex_3, vertex_2, 9.2)

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

    # find the closest neighbor total distance
    for current_truck in trucks_all:
        print("Truck {0}.".format(current_truck.label[-1]))

        # if any packages share an address, make sure they are indexed sequentially
        #       scan the remaining packages for matching address.
        #       find one? Swap it with the ind+1

        # Arrange the packages in the list current_truck.loaded_packages such that
        #   the truck travels to its nearest neighbor next
        #           For every undelivered package in the truck,
        #           compare the edge weight of all other vertices (aka adjacent)
        #               Track the index of the package with the lowest edge weight.
        #               This package should be delivered next. (Nearest Neighbor)
        nearest_neighbor_distance = inf
        next_package_index = None
        temp_package_counter = 0
        # loop through all loaded_packages
        print("\tTruck {0} neighbor...".format(current_truck.label[-1]))
        for current_package_index in range(len(current_truck.loaded_packages)):
            print("\tcurrent_package_index={0}, package #{1}".format(current_package_index,
                                                             current_truck.loaded_packages[current_package_index][0]))
            # loop through all packages that have not been tested/adjusted yet.
            for testing_index in range(current_package_index + 1, len(current_truck.loaded_packages)):
                print("\t\ttesting_index={0}, package #{1}".format(testing_index,
                                                                   current_truck.loaded_packages[testing_index][0]))
                edge = g.find_distance(g.get_vertex(current_truck.location_address),
                                       g.get_vertex(current_truck.loaded_packages[testing_index][1]))
                if edge == 0.0:
                    print("\t\t\tNEW! SAME ADDRESS! Package #{0}".format(
                                    current_truck.loaded_packages[testing_index][0]))
                    nearest_neighbor_distance = edge
                    next_package_index = testing_index

                elif edge < nearest_neighbor_distance:
                    print("\t\t\tNEW CLOSEST PACKAGE! Package #{0}".format(current_truck.loaded_packages[testing_index][0]))
                    nearest_neighbor_distance = edge
                    next_package_index = testing_index
                # print("\t\t\t\tfrom {0} ----> {1} is:\t\t{2:.1f} miles".format(current_truck.location_address,
                #                                                        current_truck.loaded_packages[testing_index][1],
                #                                                        edge))
                print("\t\t\t\t\t\tNext is package #{0} @{1}, {2:.1f} miles away.".format(
                                        current_truck.loaded_packages[next_package_index][0],
                                        current_truck.loaded_packages[next_package_index][1],
                                        nearest_neighbor_distance))

            print("\t\tSWAP index [{0}]-pack#{1} <---> index [{2}]=pack#{3}".format(current_package_index,
                                                                current_truck.loaded_packages[current_package_index][0],
                                                                next_package_index,
                                                                current_truck.loaded_packages[next_package_index][0]))
            # Swap packages so the next Nearest Neighbor is before the yet-unsorted-packages
            current_truck.loaded_packages[current_package_index], current_truck.loaded_packages[next_package_index] = \
                current_truck.loaded_packages[next_package_index], current_truck.loaded_packages[current_package_index]

            # 'move' the truck to the new location.
            current_truck.miles_driven += nearest_neighbor_distance
            current_truck.location_address = current_truck.loaded_packages[next_package_index][1]

            temp_package_counter += 1
            print("\t\tOKAY! PACKAGE 'DELIVERED' to {0}".format(current_truck.location_address))
            print("\t\t\t{0}/{1} packages delivered.".format(temp_package_counter,
                                                             len(current_truck.loaded_packages)))
            print("\t\t\t{0:.1f} miles travelled.".format(current_truck.miles_driven))
            nearest_neighbor_distance = inf

        trip_home_distance = 0.0
        trip_home_distance = g.find_distance(g.get_vertex(current_truck.location_address),
                                             g.get_vertex(hub_address))
        print("\t\ttrip home is {0:.1f} miles... from {1}-->{2}".format(trip_home_distance,
                                                                        current_truck.location_address, hub_address))

        print("Truck {0} travelled {1:.1f} miles to deliver {2} packages.".format(current_truck.label[-1],
                                                                                  current_truck.miles_driven,
                                                                                  len(current_truck.loaded_packages)))

        print("\t\t{0} --> {1}".format(hub_address, current_truck.loaded_packages[0][1]))
        stop_num = 1
        for i in range(0, len(current_truck.loaded_packages) - 1):
            print("\t\t{0} --> {1} |\t\t{2:.1f} miles".format(current_truck.loaded_packages[i][1],
                                           current_truck.loaded_packages[i+1][1],
                                           g.find_distance(g.get_vertex(current_truck.loaded_packages[i][1]),
                                                           g.get_vertex(current_truck.loaded_packages[i+1][1]))))

    # END for current_truck in truck_all



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

        elif ans == "test":
            print("total packages = 40")
            print("Truck_{0} has {1} packages loaded.".format("2", len(truck_2.loaded_packages)))
            for lp in truck_2.loaded_packages:
                print("\t\tPack #{0} is here.".format(lp))

            print("Truck_{0} has {1} packages loaded.".format(truck_1.number, len(truck_1.loaded_packages)))
            for lp in truck_1.loaded_packages:
                print("\t\tPack #{0} is here.".format(lp))

            print("Truck_{0} has {1} packages loaded.".format(truck_3.number, len(truck_3.loaded_packages)))
            for lp in truck_3.loaded_packages:
                print("\t\tPack #{0} is here.".format(lp))

            print("\nat_station_packages len = {0}".format(len(at_station_packages)))
            for a in at_station_packages:
                print("\t{0}".format(a))
            print("# of packages at station = {0}\n".format(len(at_station_packages)))

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
            for p in constrained_packages:
                print(p)

            print("There are " + str(len(constrained_packages)) + " constrained Packages.")
        elif ans == "7":
            """ Find miles travelled by each truck """

            for t in trucks_all:
                print("Truck {0} delivered {1} packages, spanning {2:.1f} miles.".format(t.label[-1],
                                                                             len(t.loaded_packages), t.miles_driven))

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
