# barebones.py by Zachary McNamara zmcnama@my.wgu.edu ID#001182706

import csv
from cmath import inf
from collections import deque
from datetime import datetime, timedelta, tzinfo
import time

import package
import truck
import hashtable
from graph import Graph, Vertex
import operator

packages = hashtable.HashTable()
distances = hashtable.HashTable()
joined = hashtable.HashTable()
global at_station_packages
at_station_packages: package = []
vertices = {}
hub_address = "4001 South 700 East"


# Function create_package_hashtable populates the custom hashtable data structure for package info
#   receives and parses a csv file with wgups package info
def create_package_hashtable(filename):
    with open(filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')

        for row in read_csv:  # For every row in CSV file
            key = row[0]
            new_package = [key, row[1], row[2], row[3], row[4], row[5], row[6], row[7], "At station"]
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
            key = row[1]

            # put the stop_count number in front
            row.insert(0, str(stop_count))
            distances.add(key, row)
            stop_count += 1

        distance_csv.close()


# Function selects package(s) with a delivery deadline or special notes
def get_constrained_packages(p_list):
    # list of packs to return
    packs = []

    # loop through each package
    for p in range(1, p_list.count + 1):
        pack = packages.get(p)

        # If the package has a specific delivery deadline or special notes, append its key to keys
        if pack[5] != "EOD" or pack[7] != "":
            packs.append(pack)

    return packs


# Function prints constraints for any of the provided packs
def print_constrained_info(constrained_list):
    for pack in constrained_list:
        message = ""

        # This if condition reruns the loop if the Package pack is not constrained.
        #       Therefore, if the condition does not stop the loop, pack is a constrained package
        #       The condition here is to ensure only specially constrained packs are returned
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
        path = " -> " + str(current_vertex.label) + " is {:.1f}".format(
            current_vertex.distance) + " miles_total_all_vehicles" + path
        current_vertex = current_vertex.pred_vertex

    path = start_vertex.label + path
    return path


def packages_to_same_address(target_address, list_of_packages):
    packs = []
    for p in list_of_packages:
        if p[1] == target_address:
            packs.append(p)
    if len(packs) == 0:
        return None
    return packs


def find_nearest_neighbor(g, start_address, list_of_packages):
    smallest_distance = inf
    nearest_neighbor = None
    for p in list_of_packages:
        dist = g.find_distance(g.get_vertex(p[1]), g.get_vertex(start_address))
        if dist < smallest_distance:
            # new nearest neighbor!!!
            smallest_distance = dist
            nearest_neighbor = p
    return nearest_neighbor


def path_order_nearest_neighbor(t_graph, car, list_of_packages):
    delivery_order = []
    # start at the current location of the car
    current_address = car.location_address
    t_list_of_packages = list_of_packages.copy()
    # loop until the delivery_order is complete - when it is full.
    while len(delivery_order) != len(list_of_packages):
        # find the nearest neighbor then append it to delivery_order
        t_pack = find_nearest_neighbor(t_graph, current_address, t_list_of_packages)
        target_address = t_pack[1]
        delivery_order.append(t_pack)
        t_list_of_packages.remove(t_pack)

        # if any packages have the same address as the package we just loaded, load them as well. 
        for p in t_list_of_packages:
            if p[1] == target_address:
                delivery_order.append(p)
                t_list_of_packages.remove(p)

        current_address = target_address

    return delivery_order


def populate_graph(t_graph):
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

    t_graph.add_vertex(vertex_0)
    t_graph.add_vertex(vertex_1)
    t_graph.add_vertex(vertex_2)
    t_graph.add_vertex(vertex_3)
    t_graph.add_vertex(vertex_4)
    t_graph.add_vertex(vertex_5)
    t_graph.add_vertex(vertex_6)
    t_graph.add_vertex(vertex_7)
    t_graph.add_vertex(vertex_8)
    t_graph.add_vertex(vertex_9)
    t_graph.add_vertex(vertex_10)
    t_graph.add_vertex(vertex_11)
    t_graph.add_vertex(vertex_12)
    t_graph.add_vertex(vertex_13)
    t_graph.add_vertex(vertex_14)
    t_graph.add_vertex(vertex_15)
    t_graph.add_vertex(vertex_16)
    t_graph.add_vertex(vertex_17)
    t_graph.add_vertex(vertex_18)
    t_graph.add_vertex(vertex_19)
    t_graph.add_vertex(vertex_20)
    t_graph.add_vertex(vertex_21)
    t_graph.add_vertex(vertex_22)
    t_graph.add_vertex(vertex_23)
    t_graph.add_vertex(vertex_24)
    t_graph.add_vertex(vertex_25)
    t_graph.add_vertex(vertex_26)

    t_graph.add_directed_edge(vertex_26, vertex_26, 0.0)
    t_graph.add_undirected_edge(vertex_26, vertex_25, 8.3)
    t_graph.add_undirected_edge(vertex_26, vertex_24, 1.3)
    t_graph.add_undirected_edge(vertex_26, vertex_23, 7.8)
    t_graph.add_undirected_edge(vertex_26, vertex_22, 3.1)
    t_graph.add_undirected_edge(vertex_26, vertex_21, 4.7)
    t_graph.add_undirected_edge(vertex_26, vertex_20, 4.1)
    t_graph.add_undirected_edge(vertex_26, vertex_19, 13.1)
    t_graph.add_undirected_edge(vertex_26, vertex_18, 6.9)
    t_graph.add_undirected_edge(vertex_26, vertex_17, 5.2)
    t_graph.add_undirected_edge(vertex_26, vertex_16, 13.6)
    t_graph.add_undirected_edge(vertex_26, vertex_15, 8.4)
    t_graph.add_undirected_edge(vertex_26, vertex_14, 8.8)
    t_graph.add_undirected_edge(vertex_26, vertex_13, 10.5)
    t_graph.add_undirected_edge(vertex_26, vertex_12, 14.1)
    t_graph.add_undirected_edge(vertex_26, vertex_11, 6.4)
    t_graph.add_undirected_edge(vertex_26, vertex_10, 6.8)
    t_graph.add_undirected_edge(vertex_26, vertex_9, 6.0)
    t_graph.add_undirected_edge(vertex_26, vertex_8, 14.1)
    t_graph.add_undirected_edge(vertex_26, vertex_7, 10.7)
    t_graph.add_undirected_edge(vertex_26, vertex_6, 14.2)
    t_graph.add_undirected_edge(vertex_26, vertex_5, 7.2)
    t_graph.add_undirected_edge(vertex_26, vertex_4, 5.5)
    t_graph.add_undirected_edge(vertex_26, vertex_3, 10.1)
    t_graph.add_undirected_edge(vertex_26, vertex_2, 7.4)
    t_graph.add_undirected_edge(vertex_26, vertex_1, 13.0)
    t_graph.add_undirected_edge(vertex_26, vertex_0, 3.6)

    t_graph.add_directed_edge(vertex_25, vertex_25, 0.0)
    t_graph.add_undirected_edge(vertex_25, vertex_0, 5.0)
    t_graph.add_undirected_edge(vertex_25, vertex_1, 4.4)
    t_graph.add_undirected_edge(vertex_25, vertex_2, 2.8)
    t_graph.add_undirected_edge(vertex_25, vertex_3, 10.1)
    t_graph.add_undirected_edge(vertex_25, vertex_4, 5.4)
    t_graph.add_undirected_edge(vertex_25, vertex_5, 3.5)
    t_graph.add_undirected_edge(vertex_25, vertex_6, 5.1)
    t_graph.add_undirected_edge(vertex_25, vertex_7, 6.2)
    t_graph.add_undirected_edge(vertex_25, vertex_8, 2.8)
    t_graph.add_undirected_edge(vertex_25, vertex_9, 3.2)
    t_graph.add_undirected_edge(vertex_25, vertex_10, 11.0)
    t_graph.add_undirected_edge(vertex_25, vertex_11, 3.7)
    t_graph.add_undirected_edge(vertex_25, vertex_12, 2.8)
    t_graph.add_undirected_edge(vertex_25, vertex_13, 6.4)
    t_graph.add_undirected_edge(vertex_25, vertex_14, 6.5)
    t_graph.add_undirected_edge(vertex_25, vertex_15, 5.7)
    t_graph.add_undirected_edge(vertex_25, vertex_16, 6.2)
    t_graph.add_undirected_edge(vertex_25, vertex_17, 5.1)
    t_graph.add_undirected_edge(vertex_25, vertex_18, 4.3)
    t_graph.add_undirected_edge(vertex_25, vertex_19, 1.8)
    t_graph.add_undirected_edge(vertex_25, vertex_20, 6.0)
    t_graph.add_undirected_edge(vertex_25, vertex_21, 7.9)
    t_graph.add_undirected_edge(vertex_25, vertex_22, 6.8)
    t_graph.add_undirected_edge(vertex_25, vertex_23, 10.6)
    t_graph.add_undirected_edge(vertex_25, vertex_24, 7.0)

    t_graph.add_directed_edge(vertex_24, vertex_24, 0.0)
    t_graph.add_undirected_edge(vertex_24, vertex_0, 2.4)
    t_graph.add_undirected_edge(vertex_24, vertex_1, 10.0)
    t_graph.add_undirected_edge(vertex_24, vertex_2, 6.1)
    t_graph.add_undirected_edge(vertex_24, vertex_3, 6.4)
    t_graph.add_undirected_edge(vertex_24, vertex_4, 4.2)
    t_graph.add_undirected_edge(vertex_24, vertex_5, 4.2)
    t_graph.add_undirected_edge(vertex_24, vertex_6, 11.7)
    t_graph.add_undirected_edge(vertex_24, vertex_7, 9.5)
    t_graph.add_undirected_edge(vertex_24, vertex_8, 9.5)
    t_graph.add_undirected_edge(vertex_24, vertex_9, 4.8)
    t_graph.add_undirected_edge(vertex_24, vertex_10, 4.9)
    t_graph.add_undirected_edge(vertex_24, vertex_11, 5.2)
    t_graph.add_undirected_edge(vertex_24, vertex_12, 9.5)
    t_graph.add_undirected_edge(vertex_24, vertex_13, 7.2)
    t_graph.add_undirected_edge(vertex_24, vertex_14, 6.3)
    t_graph.add_undirected_edge(vertex_24, vertex_15, 5.9)
    t_graph.add_undirected_edge(vertex_24, vertex_16, 11.1)
    t_graph.add_undirected_edge(vertex_24, vertex_17, 4.0)
    t_graph.add_undirected_edge(vertex_24, vertex_18, 5.6)
    t_graph.add_undirected_edge(vertex_24, vertex_19, 8.5)
    t_graph.add_undirected_edge(vertex_24, vertex_20, 2.8)
    t_graph.add_undirected_edge(vertex_24, vertex_21, 3.4)
    t_graph.add_undirected_edge(vertex_24, vertex_22, 1.7)
    t_graph.add_undirected_edge(vertex_24, vertex_23, 5.4)

    t_graph.add_directed_edge(vertex_23, vertex_23, 0.0)
    t_graph.add_undirected_edge(vertex_23, vertex_0, 6.4)
    t_graph.add_undirected_edge(vertex_23, vertex_1, 6.9)
    t_graph.add_undirected_edge(vertex_23, vertex_2, 9.7)
    t_graph.add_undirected_edge(vertex_23, vertex_3, 0.6)
    t_graph.add_undirected_edge(vertex_23, vertex_4, 6.0)
    t_graph.add_undirected_edge(vertex_23, vertex_5, 9.0)
    t_graph.add_undirected_edge(vertex_23, vertex_6, 8.2)
    t_graph.add_undirected_edge(vertex_23, vertex_7, 4.2)
    t_graph.add_undirected_edge(vertex_23, vertex_8, 11.5)
    t_graph.add_undirected_edge(vertex_23, vertex_9, 7.8)
    t_graph.add_undirected_edge(vertex_23, vertex_10, 0.4)
    t_graph.add_undirected_edge(vertex_23, vertex_11, 6.9)
    t_graph.add_undirected_edge(vertex_23, vertex_12, 11.5)
    t_graph.add_undirected_edge(vertex_23, vertex_13, 4.4)
    t_graph.add_undirected_edge(vertex_23, vertex_14, 4.8)
    t_graph.add_undirected_edge(vertex_23, vertex_15, 5.6)
    t_graph.add_undirected_edge(vertex_23, vertex_16, 7.5)
    t_graph.add_undirected_edge(vertex_23, vertex_17, 5.5)
    t_graph.add_undirected_edge(vertex_23, vertex_18, 6.5)
    t_graph.add_undirected_edge(vertex_23, vertex_19, 11.4)
    t_graph.add_undirected_edge(vertex_23, vertex_20, 6.4)
    t_graph.add_undirected_edge(vertex_23, vertex_21, 7.9)
    t_graph.add_undirected_edge(vertex_23, vertex_22, 4.5)

    t_graph.add_directed_edge(vertex_22, vertex_22, 0.0)
    t_graph.add_undirected_edge(vertex_22, vertex_0, 2.4)
    t_graph.add_undirected_edge(vertex_22, vertex_1, 8.3)
    t_graph.add_undirected_edge(vertex_22, vertex_2, 6.1)
    t_graph.add_undirected_edge(vertex_22, vertex_3, 4.7)
    t_graph.add_undirected_edge(vertex_22, vertex_4, 2.5)
    t_graph.add_undirected_edge(vertex_22, vertex_5, 4.2)
    t_graph.add_undirected_edge(vertex_22, vertex_6, 10.0)
    t_graph.add_undirected_edge(vertex_22, vertex_7, 7.8)
    t_graph.add_undirected_edge(vertex_22, vertex_8, 7.8)
    t_graph.add_undirected_edge(vertex_22, vertex_9, 4.3)
    t_graph.add_undirected_edge(vertex_22, vertex_10, 4.1)
    t_graph.add_undirected_edge(vertex_22, vertex_11, 3.4)
    t_graph.add_undirected_edge(vertex_22, vertex_12, 7.8)
    t_graph.add_undirected_edge(vertex_22, vertex_13, 5.5)
    t_graph.add_undirected_edge(vertex_22, vertex_14, 4.6)
    t_graph.add_undirected_edge(vertex_22, vertex_15, 4.2)
    t_graph.add_undirected_edge(vertex_22, vertex_16, 9.4)
    t_graph.add_undirected_edge(vertex_22, vertex_17, 2.3)
    t_graph.add_undirected_edge(vertex_22, vertex_18, 3.9)
    t_graph.add_undirected_edge(vertex_22, vertex_19, 6.8)
    t_graph.add_undirected_edge(vertex_22, vertex_20, 2.9)
    t_graph.add_undirected_edge(vertex_22, vertex_21, 4.4)

    t_graph.add_directed_edge(vertex_21, vertex_21, 0.0)
    t_graph.add_undirected_edge(vertex_21, vertex_0, 3.4)
    t_graph.add_undirected_edge(vertex_21, vertex_1, 10.9)
    t_graph.add_undirected_edge(vertex_21, vertex_2, 5.0)
    t_graph.add_undirected_edge(vertex_21, vertex_3, 7.5)
    t_graph.add_undirected_edge(vertex_21, vertex_4, 5.2)
    t_graph.add_undirected_edge(vertex_21, vertex_5, 6.9)
    t_graph.add_undirected_edge(vertex_21, vertex_6, 12.7)
    t_graph.add_undirected_edge(vertex_21, vertex_7, 10.4)
    t_graph.add_undirected_edge(vertex_21, vertex_8, 10.3)
    t_graph.add_undirected_edge(vertex_21, vertex_9, 5.8)
    t_graph.add_undirected_edge(vertex_21, vertex_10, 8.3)
    t_graph.add_undirected_edge(vertex_21, vertex_11, 6.2)
    t_graph.add_undirected_edge(vertex_21, vertex_12, 10.3)
    t_graph.add_undirected_edge(vertex_21, vertex_13, 8.2)
    t_graph.add_undirected_edge(vertex_21, vertex_14, 7.4)
    t_graph.add_undirected_edge(vertex_21, vertex_15, 6.9)
    t_graph.add_undirected_edge(vertex_21, vertex_16, 12.0)
    t_graph.add_undirected_edge(vertex_21, vertex_17, 5.0)
    t_graph.add_undirected_edge(vertex_21, vertex_18, 6.6)
    t_graph.add_undirected_edge(vertex_21, vertex_19, 9.3)
    t_graph.add_undirected_edge(vertex_21, vertex_20, 2.0)

    t_graph.add_directed_edge(vertex_20, vertex_20, 0.0)
    t_graph.add_undirected_edge(vertex_20, vertex_0, 1.9)
    t_graph.add_undirected_edge(vertex_20, vertex_1, 9.5)
    t_graph.add_undirected_edge(vertex_20, vertex_2, 3.3)
    t_graph.add_undirected_edge(vertex_20, vertex_3, 5.9)
    t_graph.add_undirected_edge(vertex_20, vertex_4, 3.2)
    t_graph.add_undirected_edge(vertex_20, vertex_5, 4.9)
    t_graph.add_undirected_edge(vertex_20, vertex_6, 11.2)
    t_graph.add_undirected_edge(vertex_20, vertex_7, 8.1)
    t_graph.add_undirected_edge(vertex_20, vertex_8, 8.5)
    t_graph.add_undirected_edge(vertex_20, vertex_9, 3.8)
    t_graph.add_undirected_edge(vertex_20, vertex_10, 6.9)
    t_graph.add_undirected_edge(vertex_20, vertex_11, 4.1)
    t_graph.add_undirected_edge(vertex_20, vertex_12, 8.5)
    t_graph.add_undirected_edge(vertex_20, vertex_13, 6.2)
    t_graph.add_undirected_edge(vertex_20, vertex_14, 5.3)
    t_graph.add_undirected_edge(vertex_20, vertex_15, 5.9)
    t_graph.add_undirected_edge(vertex_20, vertex_16, 10.6)
    t_graph.add_undirected_edge(vertex_20, vertex_17, 3.0)
    t_graph.add_undirected_edge(vertex_20, vertex_18, 4.6)
    t_graph.add_undirected_edge(vertex_20, vertex_19, 7.5)

    t_graph.add_directed_edge(vertex_19, vertex_19, 0.0)
    t_graph.add_undirected_edge(vertex_19, vertex_0, 6.5)
    t_graph.add_undirected_edge(vertex_19, vertex_1, 4.8)
    t_graph.add_undirected_edge(vertex_19, vertex_2, 4.3)
    t_graph.add_undirected_edge(vertex_19, vertex_3, 10.6)
    t_graph.add_undirected_edge(vertex_19, vertex_4, 6.5)
    t_graph.add_undirected_edge(vertex_19, vertex_5, 3.5)
    t_graph.add_undirected_edge(vertex_19, vertex_6, 3.2)
    t_graph.add_undirected_edge(vertex_19, vertex_7, 6.7)
    t_graph.add_undirected_edge(vertex_19, vertex_8, 1.0)
    t_graph.add_undirected_edge(vertex_19, vertex_9, 4.1)
    t_graph.add_undirected_edge(vertex_19, vertex_10, 11.5)
    t_graph.add_undirected_edge(vertex_19, vertex_11, 3.7)
    t_graph.add_undirected_edge(vertex_19, vertex_12, 1.0)
    t_graph.add_undirected_edge(vertex_19, vertex_13, 6.9)
    t_graph.add_undirected_edge(vertex_19, vertex_14, 6.8)
    t_graph.add_undirected_edge(vertex_19, vertex_15, 6.4)
    t_graph.add_undirected_edge(vertex_19, vertex_16, 7.2)
    t_graph.add_undirected_edge(vertex_19, vertex_17, 4.9)
    t_graph.add_undirected_edge(vertex_19, vertex_18, 4.4)

    t_graph.add_directed_edge(vertex_18, vertex_18, 0.0)
    t_graph.add_undirected_edge(vertex_18, vertex_0, 3.6)
    t_graph.add_undirected_edge(vertex_18, vertex_1, 5.0)
    t_graph.add_undirected_edge(vertex_18, vertex_2, 3.6)
    t_graph.add_undirected_edge(vertex_18, vertex_3, 6.0)
    t_graph.add_undirected_edge(vertex_18, vertex_4, 1.7)
    t_graph.add_undirected_edge(vertex_18, vertex_5, 1.1)
    t_graph.add_undirected_edge(vertex_18, vertex_6, 6.6)
    t_graph.add_undirected_edge(vertex_18, vertex_7, 4.6)
    t_graph.add_undirected_edge(vertex_18, vertex_8, 5.4)
    t_graph.add_undirected_edge(vertex_18, vertex_9, 1.8)
    t_graph.add_undirected_edge(vertex_18, vertex_10, 6.9)
    t_graph.add_undirected_edge(vertex_18, vertex_11, 1.0)
    t_graph.add_undirected_edge(vertex_18, vertex_12, 5.4)
    t_graph.add_undirected_edge(vertex_18, vertex_13, 3.0)
    t_graph.add_undirected_edge(vertex_18, vertex_14, 2.2)
    t_graph.add_undirected_edge(vertex_18, vertex_15, 1.7)
    t_graph.add_undirected_edge(vertex_18, vertex_16, 6.1)
    t_graph.add_undirected_edge(vertex_18, vertex_17, 1.6)

    t_graph.add_directed_edge(vertex_17, vertex_17, 0.0)
    t_graph.add_undirected_edge(vertex_17, vertex_0, 2.0)
    t_graph.add_undirected_edge(vertex_17, vertex_1, 6.0)
    t_graph.add_undirected_edge(vertex_17, vertex_2, 4.1)
    t_graph.add_undirected_edge(vertex_17, vertex_3, 5.3)
    t_graph.add_undirected_edge(vertex_17, vertex_4, 0.5)
    t_graph.add_undirected_edge(vertex_17, vertex_5, 1.9)
    t_graph.add_undirected_edge(vertex_17, vertex_6, 7.7)
    t_graph.add_undirected_edge(vertex_17, vertex_7, 5.1)
    t_graph.add_undirected_edge(vertex_17, vertex_8, 5.9)
    t_graph.add_undirected_edge(vertex_17, vertex_9, 2.3)
    t_graph.add_undirected_edge(vertex_17, vertex_10, 6.2)
    t_graph.add_undirected_edge(vertex_17, vertex_11, 1.2)
    t_graph.add_undirected_edge(vertex_17, vertex_12, 5.9)
    t_graph.add_undirected_edge(vertex_17, vertex_13, 3.2)
    t_graph.add_undirected_edge(vertex_17, vertex_14, 2.4)
    t_graph.add_undirected_edge(vertex_17, vertex_15, 1.6)
    t_graph.add_undirected_edge(vertex_17, vertex_16, 7.1)

    t_graph.add_directed_edge(vertex_16, vertex_16, 0.0)
    t_graph.add_undirected_edge(vertex_16, vertex_0, 7.6)
    t_graph.add_undirected_edge(vertex_16, vertex_1, 7.4)
    t_graph.add_undirected_edge(vertex_16, vertex_2, 5.7)
    t_graph.add_undirected_edge(vertex_16, vertex_3, 7.2)
    t_graph.add_undirected_edge(vertex_16, vertex_4, 1.4)
    t_graph.add_undirected_edge(vertex_16, vertex_5, 5.7)
    t_graph.add_undirected_edge(vertex_16, vertex_6, 7.2)
    t_graph.add_undirected_edge(vertex_16, vertex_7, 3.1)
    t_graph.add_undirected_edge(vertex_16, vertex_8, 7.2)
    t_graph.add_undirected_edge(vertex_16, vertex_9, 6.7)
    t_graph.add_undirected_edge(vertex_16, vertex_10, 8.1)
    t_graph.add_undirected_edge(vertex_16, vertex_11, 6.3)
    t_graph.add_undirected_edge(vertex_16, vertex_12, 7.2)
    t_graph.add_undirected_edge(vertex_16, vertex_13, 4.0)
    t_graph.add_undirected_edge(vertex_16, vertex_14, 6.4)
    t_graph.add_undirected_edge(vertex_16, vertex_15, 5.6)

    t_graph.add_directed_edge(vertex_15, vertex_15, 0.0)
    t_graph.add_undirected_edge(vertex_15, vertex_0, 3.7)
    t_graph.add_undirected_edge(vertex_15, vertex_1, 4.5)
    t_graph.add_undirected_edge(vertex_15, vertex_2, 5.8)
    t_graph.add_undirected_edge(vertex_15, vertex_3, 4.4)
    t_graph.add_undirected_edge(vertex_15, vertex_4, 2.7)
    t_graph.add_undirected_edge(vertex_15, vertex_5, 3.8)
    t_graph.add_undirected_edge(vertex_15, vertex_6, 5.8)
    t_graph.add_undirected_edge(vertex_15, vertex_7, 3.4)
    t_graph.add_undirected_edge(vertex_15, vertex_8, 6.6)
    t_graph.add_undirected_edge(vertex_15, vertex_9, 4.0)
    t_graph.add_undirected_edge(vertex_15, vertex_10, 5.4)
    t_graph.add_undirected_edge(vertex_15, vertex_11, 2.9)
    t_graph.add_undirected_edge(vertex_15, vertex_12, 6.6)
    t_graph.add_undirected_edge(vertex_15, vertex_13, 1.5)
    t_graph.add_undirected_edge(vertex_15, vertex_14, 0.6)

    t_graph.add_directed_edge(vertex_14, vertex_14, 0.0)
    t_graph.add_undirected_edge(vertex_14, vertex_0, 4.4)
    t_graph.add_undirected_edge(vertex_14, vertex_1, 4.6)
    t_graph.add_undirected_edge(vertex_14, vertex_2, 5.6)
    t_graph.add_undirected_edge(vertex_14, vertex_3, 4.3)
    t_graph.add_undirected_edge(vertex_14, vertex_4, 2.4)
    t_graph.add_undirected_edge(vertex_14, vertex_5, 3.0)
    t_graph.add_undirected_edge(vertex_14, vertex_6, 8.0)
    t_graph.add_undirected_edge(vertex_14, vertex_7, 3.3)
    t_graph.add_undirected_edge(vertex_14, vertex_8, 7.8)
    t_graph.add_undirected_edge(vertex_14, vertex_9, 3.7)
    t_graph.add_undirected_edge(vertex_14, vertex_10, 5.2)
    t_graph.add_undirected_edge(vertex_14, vertex_11, 2.6)
    t_graph.add_undirected_edge(vertex_14, vertex_12, 7.8)
    t_graph.add_undirected_edge(vertex_14, vertex_13, 1.3)

    t_graph.add_directed_edge(vertex_13, vertex_13, 0.0)
    t_graph.add_undirected_edge(vertex_13, vertex_0, 5.2)
    t_graph.add_undirected_edge(vertex_13, vertex_1, 3.0)
    t_graph.add_undirected_edge(vertex_13, vertex_2, 6.5)
    t_graph.add_undirected_edge(vertex_13, vertex_3, 3.9)
    t_graph.add_undirected_edge(vertex_13, vertex_4, 3.2)
    t_graph.add_undirected_edge(vertex_13, vertex_5, 3.9)
    t_graph.add_undirected_edge(vertex_13, vertex_6, 4.2)
    t_graph.add_undirected_edge(vertex_13, vertex_7, 1.6)
    t_graph.add_undirected_edge(vertex_13, vertex_8, 7.6)
    t_graph.add_undirected_edge(vertex_13, vertex_9, 4.6)
    t_graph.add_undirected_edge(vertex_13, vertex_10, 4.9)
    t_graph.add_undirected_edge(vertex_13, vertex_11, 3.5)
    t_graph.add_undirected_edge(vertex_13, vertex_12, 7.3)

    t_graph.add_directed_edge(vertex_12, vertex_12, 0.0)
    t_graph.add_undirected_edge(vertex_12, vertex_0, 7.6)
    t_graph.add_undirected_edge(vertex_12, vertex_1, 4.8)
    t_graph.add_undirected_edge(vertex_12, vertex_2, 5.3)
    t_graph.add_undirected_edge(vertex_12, vertex_3, 11.1)
    t_graph.add_undirected_edge(vertex_12, vertex_4, 7.5)
    t_graph.add_undirected_edge(vertex_12, vertex_5, 4.5)
    t_graph.add_undirected_edge(vertex_12, vertex_6, 4.2)
    t_graph.add_undirected_edge(vertex_12, vertex_7, 7.7)
    t_graph.add_undirected_edge(vertex_12, vertex_8, 0.6)
    t_graph.add_undirected_edge(vertex_12, vertex_9, 5.1)
    t_graph.add_undirected_edge(vertex_12, vertex_10, 12.0)
    t_graph.add_undirected_edge(vertex_12, vertex_11, 4.7)

    t_graph.add_directed_edge(vertex_11, vertex_11, 0.0)
    t_graph.add_undirected_edge(vertex_11, vertex_0, 3.2)
    t_graph.add_undirected_edge(vertex_11, vertex_1, 5.3)
    t_graph.add_undirected_edge(vertex_11, vertex_2, 3.0)
    t_graph.add_undirected_edge(vertex_11, vertex_3, 6.4)
    t_graph.add_undirected_edge(vertex_11, vertex_4, 1.5)
    t_graph.add_undirected_edge(vertex_11, vertex_5, 0.8)
    t_graph.add_undirected_edge(vertex_11, vertex_6, 6.9)
    t_graph.add_undirected_edge(vertex_11, vertex_7, 4.8)
    t_graph.add_undirected_edge(vertex_11, vertex_8, 4.7)
    t_graph.add_undirected_edge(vertex_11, vertex_9, 1.1)
    t_graph.add_undirected_edge(vertex_11, vertex_10, 7.3)

    t_graph.add_directed_edge(vertex_10, vertex_10, 0.0)
    t_graph.add_undirected_edge(vertex_10, vertex_0, 6.4)
    t_graph.add_undirected_edge(vertex_10, vertex_1, 7.3)
    t_graph.add_undirected_edge(vertex_10, vertex_2, 10.4)
    t_graph.add_undirected_edge(vertex_10, vertex_3, 1.0)
    t_graph.add_undirected_edge(vertex_10, vertex_4, 6.5)
    t_graph.add_undirected_edge(vertex_10, vertex_5, 8.7)
    t_graph.add_undirected_edge(vertex_10, vertex_6, 8.6)
    t_graph.add_undirected_edge(vertex_10, vertex_7, 4.6)
    t_graph.add_undirected_edge(vertex_10, vertex_8, 11.9)
    t_graph.add_undirected_edge(vertex_10, vertex_9, 9.4)

    t_graph.add_directed_edge(vertex_9, vertex_9, 0.0)
    t_graph.add_undirected_edge(vertex_9, vertex_0, 2.8)
    t_graph.add_undirected_edge(vertex_9, vertex_1, 6.3)
    t_graph.add_undirected_edge(vertex_9, vertex_2, 1.6)
    t_graph.add_undirected_edge(vertex_9, vertex_3, 7.3)
    t_graph.add_undirected_edge(vertex_9, vertex_4, 2.6)
    t_graph.add_undirected_edge(vertex_9, vertex_5, 1.5)
    t_graph.add_undirected_edge(vertex_9, vertex_6, 8.0)
    t_graph.add_undirected_edge(vertex_9, vertex_7, 9.3)
    t_graph.add_undirected_edge(vertex_9, vertex_8, 4.8)

    t_graph.add_directed_edge(vertex_8, vertex_8, 0.0)
    t_graph.add_undirected_edge(vertex_8, vertex_0, 7.6)
    t_graph.add_undirected_edge(vertex_8, vertex_1, 4.8)
    t_graph.add_undirected_edge(vertex_8, vertex_2, 5.3)
    t_graph.add_undirected_edge(vertex_8, vertex_3, 11.1)
    t_graph.add_undirected_edge(vertex_8, vertex_4, 7.5)
    t_graph.add_undirected_edge(vertex_8, vertex_5, 4.5)
    t_graph.add_undirected_edge(vertex_8, vertex_6, 4.2)
    t_graph.add_undirected_edge(vertex_8, vertex_7, 7.7)

    t_graph.add_directed_edge(vertex_7, vertex_7, 0.0)
    t_graph.add_undirected_edge(vertex_7, vertex_0, 8.6)
    t_graph.add_undirected_edge(vertex_7, vertex_1, 2.8)
    t_graph.add_undirected_edge(vertex_7, vertex_2, 6.3)
    t_graph.add_undirected_edge(vertex_7, vertex_3, 4.0)
    t_graph.add_undirected_edge(vertex_7, vertex_4, 5.1)
    t_graph.add_undirected_edge(vertex_7, vertex_5, 4.3)
    t_graph.add_undirected_edge(vertex_7, vertex_6, 4.0)

    t_graph.add_directed_edge(vertex_6, vertex_6, 0.0)
    t_graph.add_undirected_edge(vertex_6, vertex_0, 10.9)
    t_graph.add_undirected_edge(vertex_6, vertex_1, 1.6)
    t_graph.add_undirected_edge(vertex_6, vertex_2, 8.6)
    t_graph.add_undirected_edge(vertex_6, vertex_3, 8.6)
    t_graph.add_undirected_edge(vertex_6, vertex_4, 7.9)
    t_graph.add_undirected_edge(vertex_6, vertex_5, 6.3)

    t_graph.add_directed_edge(vertex_5, vertex_5, 0.0)
    t_graph.add_undirected_edge(vertex_5, vertex_0, 3.5)
    t_graph.add_undirected_edge(vertex_5, vertex_1, 4.8)
    t_graph.add_undirected_edge(vertex_5, vertex_2, 2.8)
    t_graph.add_undirected_edge(vertex_5, vertex_3, 6.9)
    t_graph.add_undirected_edge(vertex_5, vertex_4, 1.9)

    t_graph.add_directed_edge(vertex_4, vertex_4, 0.0)
    t_graph.add_undirected_edge(vertex_4, vertex_0, 2.2)
    t_graph.add_undirected_edge(vertex_4, vertex_1, 6.0)
    t_graph.add_undirected_edge(vertex_4, vertex_2, 4.4)
    t_graph.add_undirected_edge(vertex_4, vertex_3, 5.6)

    t_graph.add_directed_edge(vertex_3, vertex_3, 0.0)
    t_graph.add_undirected_edge(vertex_3, vertex_0, 11.0)
    t_graph.add_undirected_edge(vertex_3, vertex_1, 6.4)
    t_graph.add_undirected_edge(vertex_3, vertex_2, 9.2)

    t_graph.add_undirected_edge(vertex_2, vertex_0, 3.8)
    t_graph.add_undirected_edge(vertex_2, vertex_1, 7.1)
    t_graph.add_directed_edge(vertex_2, vertex_2, 0.0)

    t_graph.add_undirected_edge(vertex_1, vertex_0, 7.2)
    t_graph.add_directed_edge(vertex_1, vertex_1, 0.0)

    t_graph.add_directed_edge(vertex_0, vertex_0, 0.0)
    t_graph.set_adjacent_vertexes(vertex_0, [vertex_1, vertex_2, vertex_3, vertex_4, vertex_5, vertex_6, vertex_7,
                                             vertex_8, vertex_9, vertex_10, vertex_11, vertex_12, vertex_13,
                                             vertex_14, vertex_15, vertex_16, vertex_17, vertex_18, vertex_19,
                                             vertex_20,
                                             vertex_21, vertex_22, vertex_23, vertex_24, vertex_25, vertex_26])


# Main for this Project
if __name__ == "__main__":
    start_time = datetime.now()
    truck_1 = truck.Truck("TRUCK 1")
    truck_2 = truck.Truck("TRUCK 2")
    truck_3 = truck.Truck("TRUCK 3")
    vehicles = [truck_1, truck_2, truck_3]
    max_packages = 16
    speed = 18

    # Creating the hashtable for the Packages CSV file
    create_package_hashtable("wgups_package_file.csv")

    # print_constrained_info(constrained_packages)

    # Creating the hashtable for the distances between Cities CSV file
    create_distance_hashtable("wgups_distance_table.csv")

    # create the graph object to contain vertices
    g = Graph()

    # creates the vertices and their weighted adjacent edges
    populate_graph(g)

    # creates a list of keys for packs with delivery deadlines or special delivery notes
    constrained_packages = get_constrained_packages(packages)
    packages_still_at_the_station = at_station_packages.copy()

    # load the trucks
    # print("# of packs at station = {0}.\n\n".format(len(at_station_packages)))

    # Sort packages with special constraints, i.e. required truck, delays, delivery deadline
    t_packages_still_at_the_station = packages_still_at_the_station.copy()
    for p in packages_still_at_the_station:
        selected_truck = None

        # TRUCK 1: assign the 'group' of packages that must be delivered together to truck_1
        if "be delivered with" in p[7] or p[0] == "13":
            selected_truck = truck_1

        # TRUCK 3: assign the packages that are not ready to load to a truck that is not going out first (truck_3)
        elif "Delayed" in p[7] or "Wrong address" in p[7]:
            p[8] = "Delayed. Assign to " + truck_3.label
            t_packages_still_at_the_station.remove(p)
            truck_3.load_package(p)
            constrained_packages.remove(p)
            continue

        # TRUCK 2: load with the packs that can only go on truck_2
        elif "truck 2" in p[7]:
            selected_truck = truck_2
        try:
            p[8] = "Loaded in " + selected_truck.label
            t_packages_still_at_the_station.remove(p)
            selected_truck.load_package(p)
            constrained_packages.remove(p)
        except AttributeError:
            # an AttributeError occurs here if "selected_truck" is only initialized at declaration (to None)
            # This does not impact execution.
            pass
        except ValueError:
            # a ValueError occurs when the package is not in the list "constrained_packages".
            # This does not impact execution.
            pass

    packages_still_at_the_station = t_packages_still_at_the_station.copy()

    # loop through all packs at the station.
    # If they have a matching address to any package loaded in truck_2, load them as well.
    for loaded_p in truck_2.packages_list:

        same_destination_package_list = packages_to_same_address(loaded_p[1], packages_still_at_the_station)

        if same_destination_package_list is not None:
            for p in same_destination_package_list:
                try:
                    truck_2.load_package(p)
                    packages_still_at_the_station.remove(p)
                    constrained_packages.remove(p)
                except ValueError:
                    # a ValueError occurs when the package is not in the list "constrained_packages".
                    # This does not impact execution.
                    pass

    # TRUCK 1: load packages with a delivery deadline to truck_1
    # - DELIVERY DEADLINE LOADING - DELIVERY DEADLINE LOADING - DELIVERY DEADLINE LOADING - DELIVERY DEADLINE LOADING -
    for delivery_deadline_package in constrained_packages:
        # if the package has no deadline, is delayed, or already loaded, skip to the next package
        if (delivery_deadline_package[5] == "EOD") or ("Delayed" in delivery_deadline_package[7]) or \
                (delivery_deadline_package not in packages_still_at_the_station):
            continue
        # stop loading if the truck is full
        if len(truck_1.packages_list) >= max_packages:
            break
            truck_1.load_package(delivery_deadline_package)
            packages_still_at_the_station.remove(delivery_deadline_package)

        # if other packages at the station are going to the same address, load them as well.
        address = delivery_deadline_package[1]
        for p in packages_still_at_the_station:
            # break if the truck is full
            if len(truck_1.packages_list) >= max_packages:
                break
            if p[1] == address:
                try:
                    truck_1.load_package(p)
                    packages_still_at_the_station.remove(p)
                except ValueError:
                    pass

    # Now that Truck_1 is fully loaded, let's decide the order to deliver the packages in using Nearest Neighbor
    truck_1.location_address = hub_address
    path = path_order_nearest_neighbor(g, truck_1, truck_1.packages_list)
    truck_1.packages_list = path.copy()
    truck_1.delivery_order = deque(truck_1.packages_list)
    truck_1.location_address = hub_address

    # Finish loading Truck 2 with the nearest neighbor's package (of the unloaded packages)
    t_packages_still_at_the_station = packages_still_at_the_station.copy()
    while len(truck_2.packages_list) < max_packages:
        # find nearest neighbor
        pack = find_nearest_neighbor(g, truck_2.location_address, t_packages_still_at_the_station)
        address = pack[1]
        # add nearest neighbor package
        truck_2.load_package(pack)
        # 'move' the truck to that package's address
        truck_2.location_address = address
        # remove that package from the list we still need to sort
        t_packages_still_at_the_station.remove(pack)
    packages_still_at_the_station = t_packages_still_at_the_station.copy()

    # hiding_packages_list = list(truck_2.packages_list)
    # force_deliver_first = packages.get(18).copy()
    # hiding_packages_list.remove(force_deliver_first)
    # truck_2.location_address = force_deliver_first[1]
    # hardcoding_truck_2_path = path_order_nearest_neighbor(g, truck_2, hiding_packages_list)
    # hardcoding_truck_2_path.insert(0, force_deliver_first)
    # truck_2.delivery_order = deque(hardcoding_truck_2_path)
    # truck_2.packages_list = hardcoding_truck_2_path.copy()
    # truck_2.location_address = hub_address

    # # Reset truck_2 and reorder the loaded packages using Nearest Neighbor
    truck_2.location_address = hub_address
    path = path_order_nearest_neighbor(g, truck_2, truck_2.packages_list)
    truck_2.delivery_order = deque(path)
    truck_2.packages_list = path.copy()
    truck_2.location_address = hub_address

    # Truck_3 is the final truck to leave the depot - aka the remainder/misfit route.
    t_packages_at_station = packages_still_at_the_station.copy()
    for dp in t_packages_at_station:
        truck_3.load_package(dp)
        packages_still_at_the_station.remove(dp)

    truck_3.location_address = hub_address
    path = path_order_nearest_neighbor(g, truck_3, truck_3.packages_list)
    truck_3.delivery_order = deque(path)
    truck_3.packages_list = path.copy()
    truck_3.location_address = hub_address

    if len(packages_still_at_the_station) == 0:
        print("Every package has been loaded!\n")

    truck_1.time_tracker = datetime(2000, 1, 1, 8, 0, 0)
    # truck_2.time_tracker = datetime(2000, 1, 1, 9, 0, 0)
    # truck_3.time_tracker = whenever_a_truck_returns

    for current_truck in vehicles:
        print("\n{0} can leave as early as {1}".format(current_truck.label,
                                                       current_truck.time_tracker.strftime("%H:%M:%S %p")))
        current_truck.delivery_order = deque(current_truck.packages_list)
        t_delivery_order = current_truck.delivery_order.copy()
        current_location = current_truck.location_address

        # deliver the packages (in order left to right) & update that the package has been delivered
        for index in range(len(current_truck.delivery_order)):
            # truck 'goes' from current_location to delivery_address in 'trip_duration' seconds
            deliver_this_package = current_truck.delivery_order.popleft()
            delivery_address = deliver_this_package[1]
            edge = 0.0
            trip_duration = timedelta(0, 0)

            # find the distance travelled to calculate elapsed time
            # conditional to speed up execution if there is more than 1 package to a location.
            if current_location != delivery_address:
                edge = g.find_distance(g.get_vertex(current_location), g.get_vertex(delivery_address))
                trip_duration = timedelta(seconds=int(edge / current_truck.speed * 3600))
            delivery_time = current_truck.time_tracker + trip_duration
            deliver_this_package[8] = "{} will deliver at {}".format(current_truck.label,
                                                                     delivery_time.strftime("%H:%M:%S %p"))

            # once package is delivered, update the truck's address
            current_location = delivery_address

            print("\t\t{0},\t{1},\t{3:.1f} miles away\t\t-- {2}".
                  format("Pack #" + deliver_this_package[0], deliver_this_package[1],
                         deliver_this_package[8], edge))

            # for each truck object, keep track of the time
            current_truck.time_tracker += trip_duration

        # return truck to the HUB
        distance_to_hub = g.find_distance(g.get_vertex(current_truck.location_address), g.get_vertex(hub_address))
        return_to_hub_duration = timedelta(seconds=int(distance_to_hub / current_truck.speed * 3600))
        current_truck.time_tracker += return_to_hub_duration
        print("\tfinally, {0} returned to the HUB, address={1} -- {2:.1f} miles away -- delivered at {3}".format(
            current_truck.label, hub_address, distance_to_hub, current_truck.time_tracker.strftime("%H:%M:%S %p")))

        # truck_3 cannot leave until one driver has returned. Track which/when a truck returns
        first_truck_back = truck_1
        if truck_2.time_tracker < truck_1.time_tracker:
            first_truck_back = truck_2
        # set truck_3's departure time to the arrival of first_truck_back
        truck_3.time_tracker = first_truck_back.time_tracker

    end_time = datetime.now()
    time_diff = (end_time - start_time)
    print("\n\nExecution time: {} seconds.\n\n".format(time_diff))

    # This while loop controls the console menu users interact with
    while True:
        print("""
            Welcome to the menu! Enter your selection below 
                1. Lookup package info
                2. Get snapshot of every package
                3. Print packages status at a specified time
                4. Print info by Truck
                5. Recalculate the delivery order
                7. Find total miles travelled by each truck & sum
                0. Exit/Quit
            """)
        ans = input("What would you like to do? \nINPUT: ")
        # ans = "4"
        print()
        if ans == "1":
            """ Look up a user-specified package """

            lookup_package_id = int(input("Enter package ID #: "))
            user_package_lookup = packages.get(lookup_package_id)
            if user_package_lookup is None:
                print("We have no record of this package. Try again.")
                continue
            print(user_package_lookup)
        elif ans == "2":
            """ Show the current status of every package """

            for p in range(1, packages.count + 1):
                print(packages.get(p))

        elif ans == "3":
            """ print packages status at a user-specified time """

            try:
                time_text = input("Using format <HH:MM:SS> enter a time: ")
                # time_text = "08:55:50"
                status_time = datetime.strptime(time_text, "%H:%M:%S")

                print("You asked for a status update on EVERY package at {}...".format(
                    status_time.strftime("%H:%M:%S")))

                print("\nAll {0} assigned packages at {1}".format(truck_1.label, status_time.strftime("%H:%M:%S %p")))
                truck_1.print_packages_status(status_time)
                print("\nAll {0} assigned packages at {1}".format(truck_2.label, status_time.strftime("%H:%M:%S %p")))
                truck_2.print_packages_status(status_time)
                print("\nAll {0} assigned packages at {1}".format(truck_3.label, status_time.strftime("%H:%M:%S %p")))
                truck_3.print_packages_status(status_time)
            except ValueError:
                print("Incorrect entry. Please try again.")

        elif ans == "4":
            """ Print truck info """

            for printing_truck in vehicles:
                print("\n{0} was loaded with {1} packages.".format(printing_truck.label,
                                                                   len(printing_truck.packages_list)))
                print("\t\tLocation: {0}, there are {1} packages to deliver.".format(printing_truck.location_address,
                                                                                     len(
                                                                                         printing_truck.packages_list) - len(
                                                                                         printing_truck.delivered_packages)))
                print("\t\tThe entire delivery route covers {0:.1f} miles.".format(printing_truck.miles_driven))

                for pack in printing_truck.packages_list:
                    # this prints the entire package
                    # print("\t\t\tpackage #{0}: {1}".format(pack[0], pack))
                    # the following print has more human-friendly info, for testing purposes
                    print("\t\t\tpack #{0} \t@ {1}   \t{2}".format(pack[0], pack[1], pack[8]))

        elif ans == "5":
            """ re-calculate delivery order for all trucks"""

            # recalculate the delivery order and reset each truck
            for a_truck in vehicles:
                path = path_order_nearest_neighbor(g, a_truck, a_truck.packages_list)
                a_truck.delivery_order = deque(path)
                a_truck.packages_list = path.copy()
                a_truck.location_address = hub_address

        elif ans == "6":
            """" Prints all packs with constraints (delivery deadline or special notes) """
            # get the keys for all constrained packs
            for p in constrained_packages:
                print(p)

            print("There are " + str(len(constrained_packages)) + " constrained Packages.")

        elif ans == "7":
            """ Find miles_total_all_vehicles travelled by each truck """

            miles_total_all_vehicles = 0.0
            # find the sum of the total distance each truck travels in their round trips
            for current_truck in vehicles:
                t_packages = current_truck.packages_list.copy()
                # loop through each package that is loaded,
                #       tracking the DELIVERED TIME and miles_total_all_vehicles driven

                print("\n{}".format(current_truck.label))
                for pack in t_packages:
                    edge = g.find_distance(g.get_vertex(current_truck.location_address),
                                           g.get_vertex(pack[1]))
                    if edge != 0.0:
                        print("\t\t{0}-->{1} is \t\t{2:.1f} miles".format(current_truck.location_address,
                                                                          pack[1], edge))
                    else:
                        print("\t\t\t\t{0}-->{1} = same address".format(current_truck.location_address, pack[1]))
                    current_truck.deliver_package(pack, edge)

                # once every package has been delivered, return the truck to the HUB.
                print("\t---return to HUB---")
                trip_to_hub = g.find_distance(g.get_vertex(current_truck.location_address),
                                              g.get_vertex(hub_address))
                current_truck.miles_driven += trip_to_hub
                print("\t\t{0}-->{1} is \t\t{2:.1f} miles".format(current_truck.location_address,
                                                                  hub_address, trip_to_hub))
                current_truck.location_address = hub_address
                miles_total_all_vehicles += current_truck.miles_driven
                print("\t{0} drove a total of {1:.1f} miles".format(current_truck.label, current_truck.miles_driven))

            print("{0:.1f} miles_total_all_vehicles total".format(miles_total_all_vehicles))

        elif ans == "0":
            """ exit the program"""
            raise SystemExit
        else:
            """ If user enters an unanticipated option, they should be re-prompted for input"""
            print("Not a Valid Choice. Try again")
