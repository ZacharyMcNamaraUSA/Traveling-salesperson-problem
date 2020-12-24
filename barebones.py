# barebones.py by Zachary McNamara zmcnama@my.wgu.edu ID#001182706

import csv
from cmath import inf
from collections import deque
from datetime import datetime, timedelta
import package
import truck
import hashtable
from graph import Graph, Vertex

packages = hashtable.HashTable()
distances = hashtable.HashTable()
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

        for row in read_csv:  # For every row in CSV file
            key = row[1]

            distances.add(key, row)

        distance_csv.close()


# Function selects package(s) with a delivery deadline or special notes
def get_constrained_packages(p_list):
    # list of packs to return
    packs = []

    # loop through each package
    for constrained_index in range(1, p_list.count + 1):
        constrained_package = packages.get(constrained_index)

        # If the package has a specific delivery deadline or special notes, append its key to keys
        if constrained_package[5] != "EOD" or constrained_package[7] != "":
            packs.append(constrained_package)

    return packs


# Function returns a List of packages with the same address as target_address
# if no matching packages are found, return None
def packages_to_same_address(target_address, list_of_packages):
    same_address_packs = []
    for same_address_index in range(1, len(list_of_packages) + 1):
        test_package = list_of_packages[same_address_index - 1]
        if list_of_packages[same_address_index - 1][1] == target_address:
            same_address_packs.append(list_of_packages[same_address_index - 1])
    if len(same_address_packs) == 0:
        return None
    return same_address_packs


# Function determines the package needing to be delivered next using Nearest Neighbor algorithm
def find_nearest_neighbor(g, start_address, list_of_packages):
    smallest_distance = inf
    nearest_neighbor = None
    # loop through all packages in list_of_packages. Track the closest vertex's package
    for nearest_neighbor_index in range(1, len(list_of_packages) + 1):
        nearest_package = list_of_packages[nearest_neighbor_index - 1]
        dist = g.find_distance(g.get_vertex(nearest_package[1]), g.get_vertex(start_address))
        # if dist < smallest_distance, a new nearest neighbor has been found
        if dist < smallest_distance:
            smallest_distance = dist
            nearest_neighbor = nearest_package
    return nearest_neighbor


# Function determines the package delivery order for car and its list_of_packages
# Function uses find_nearest_neighbor function to determine which neighbor is correct.
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

        current_address = target_address

    return delivery_order


# Function creates all necessary vertices and their (un)directed edges
# for scalability, this function will need to be automated
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
    # start_time is used to track execution time of the program
    start_time = datetime.now()
    # declare and initialize all trucks then add them to List vehicles
    truck_1 = truck.Truck("TRUCK 1")
    truck_2 = truck.Truck("TRUCK 2")
    truck_3 = truck.Truck("TRUCK 3")
    vehicles = [truck_1, truck_2, truck_3]
    # given parameters state trucks may carry 16 max_packages and always move at speed of 18
    truck_1.max_packages = 16
    truck_2.max_packages = 16
    truck_3.max_packages = 16
    speed = 18

    # Creating the hashtable for the Packages CSV file
    create_package_hashtable("wgups_package_file.csv")

    # print_constrained_info(constrained_packages)

    # Creating the hashtable for the distances between Cities CSV file
    create_distance_hashtable("wgups_distance_table.csv")

    # create the graph object to contain vertices & edges
    g = Graph()

    # creates the vertices and their weighted adjacent edges
    populate_graph(g)

    # creates a list of packs with delivery deadlines or special delivery notes
    constrained_packages = list(get_constrained_packages(packages))

    packages_still_at_the_station = at_station_packages.copy()

    # Sort packages with special constraints, i.e. required truck, delays, delivery deadline
    for package_index in range(1, packages.count + 1):
        selected_truck = None
        testing_package = packages.get(package_index)

        # TRUCK 1: assign the 'group' of packages that must be delivered together to truck_1
        # SCALING NOTE: portion is 'hard-coded' to function for this data set only. edit for expansion.
        if "be delivered with" in testing_package[7]:
            selected_truck = truck_1

        # TRUCK 3: assign the packages that are not ready to load to truck_3 - a truck that is not going out first
        elif "Delayed" in testing_package[7] or "Wrong address" in testing_package[7]:
            testing_package[8] = "Delayed. Assign to " + truck_3.label
            packages_still_at_the_station.remove(testing_package)
            truck_3.load_package(testing_package)
            constrained_packages.remove(testing_package)
            continue

        # TRUCK 2: load with the packs that can only go on truck_2
        elif "truck 2" in testing_package[7] or testing_package[0] == "13":
            selected_truck = truck_2
        try:
            testing_package[8] = "Loaded in " + selected_truck.label
            packages_still_at_the_station.remove(testing_package)
            selected_truck.load_package(testing_package)
            constrained_packages.remove(testing_package)
        except AttributeError:
            # an AttributeError occurs here if "selected_truck" is not initialized after its declaration (to None)
            # This does not impact execution.
            pass
        except ValueError:
            # a ValueError occurs when the package is not in the list "constrained_packages".
            # This does not impact execution.
            pass

    # TRUCK 1: load packages with a delivery deadline to truck_1
    # - DELIVERY DEADLINE LOADING - DELIVERY DEADLINE LOADING - DELIVERY DEADLINE LOADING - DELIVERY DEADLINE LOADING -
    for delivery_deadline_package in constrained_packages:
        # if the package has no deadline, is delayed, or already loaded, continue on to the next package
        if (delivery_deadline_package[5] == "EOD") or ("Delayed" in delivery_deadline_package[7]) or \
                (delivery_deadline_package not in packages_still_at_the_station):
            continue
        # break loading if the truck is full, otherwise load delivery_deadline_package
        if len(truck_1.packages_list) >= truck_1.max_packages:
            break

        # if other packages at the station are going to the same address, load them as well.
        address = delivery_deadline_package[1]
        for testing_package in packages_still_at_the_station:
            # break if the truck is full
            if len(truck_1.packages_list) >= truck_1.max_packages:
                break
            if testing_package[1] == address:
                try:
                    truck_1.load_package(testing_package)
                    packages_still_at_the_station.remove(testing_package)
                except ValueError:
                    pass

    t_packages_still_at_the_station = packages_still_at_the_station.copy()
    # compare truck_2.packages_list with all packs at the station packages_still_at_the_station
    # If they have a matching address to any package loaded in truck_2, load them as well.
    for loaded_p in truck_2.packages_list:
        for testing_package in t_packages_still_at_the_station:
            # if loaded_p's address does not match
            if testing_package[1] != loaded_p[1]:
                continue
            try:
                truck_2.load_package(testing_package)
                t_packages_still_at_the_station.remove(testing_package)
                constrained_packages.remove(testing_package)
            except ValueError:
                # a ValueError occurs when the package is not in the list "constrained_packages".
                # This does not impact execution.
                pass

    # Now that Truck_1 is fully loaded, reorder the loaded packages using path_order_nearest_neighbor
    truck_1.location_address = hub_address
    path = path_order_nearest_neighbor(g, truck_1, truck_1.packages_list)
    truck_1.packages_list = path.copy()
    truck_1.delivery_order = deque(truck_1.packages_list)
    truck_1.location_address = hub_address

    # Finish loading Truck 2 with the next-best not yet loaded package using path_order_nearest_neighbor
    packages_still_at_the_station = t_packages_still_at_the_station.copy()
    while len(truck_2.packages_list) < truck_2.max_packages:
        # find nearest neighbor
        pack = find_nearest_neighbor(g, truck_2.location_address, t_packages_still_at_the_station)
        address = pack[1]
        # add nearest neighbor package
        truck_2.load_package(pack)
        # 'move' the truck to that package's address
        truck_2.location_address = address
        # remove that package from the list we still need to sort
        t_packages_still_at_the_station.remove(pack)
    # update List packages_still_at_the_station to reflect changes made loading truck_2
    packages_still_at_the_station = t_packages_still_at_the_station.copy()

    # Reset truck_2 and reorder the loaded packages using path_order_nearest_neighbor
    truck_2.location_address = hub_address
    path = path_order_nearest_neighbor(g, truck_2, truck_2.packages_list)
    truck_2.delivery_order = deque(path)
    truck_2.packages_list = path.copy()
    truck_2.location_address = hub_address

    # Truck_3 is the final truck to leave the depot - load it with any remaining packages
    t_packages_at_station = packages_still_at_the_station.copy()
    for dp in t_packages_at_station:
        truck_3.load_package(dp)
        packages_still_at_the_station.remove(dp)

    # Reset truck_3 and reorder the loaded packages using path_order_nearest_neighbor
    truck_3.location_address = hub_address
    path = path_order_nearest_neighbor(g, truck_3, truck_3.packages_list)
    truck_3.delivery_order = deque(path)
    truck_3.packages_list = path.copy()
    truck_3.location_address = hub_address

    # loop through all vehicles to calculate each package's delivery time using current_truck.time_tracker
    for current_truck in vehicles:
        # make delivery_order be a deque then use a temporary copy of it to determine estimated delivery times
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
        distance_to_hub = g.find_distance(g.get_vertex(current_location), g.get_vertex(hub_address))
        return_to_hub_duration = timedelta(seconds=int(distance_to_hub / current_truck.speed * 3600))
        current_truck.time_tracker += return_to_hub_duration
        print("finally, {0} returned to the HUB, address={1} -- {2:.1f} miles away -- at {3}\n".format(
            current_truck.label, hub_address, distance_to_hub, current_truck.time_tracker.strftime("%H:%M:%S %p")))

        # truck_3 cannot leave until one driver has returned. Track which/when a truck returns
        # set truck_3's time_tracker to its departure time, which is as soon as either truck_1 or truck_2 returns
        first_truck_back = truck_1
        if truck_2.time_tracker < truck_1.time_tracker:
            first_truck_back = truck_2
        # set truck_3's departure time to the arrival of first_truck_back
        truck_3.time_tracker = first_truck_back.time_tracker

    # after calculations, reset the time tracker for each truck.
    truck_1.time_tracker_reset()
    truck_2.time_tracker_reset()
    truck_3.time_tracker_reset()

    # calculate this program's execution time by comparing start_time and end_time
    end_time = datetime.now()
    time_diff = (end_time - start_time)
    print("\n\nExecution time: {} seconds.\n\n".format(time_diff))

    # This while loop controls the console menu which users interact with
    while True:
        print("""
            Welcome to the menu! Enter your selection below 
                1. Lookup package info
                2. Get snapshot of every package
                3. Print packages status at a specified time
                4. Recalculate the delivery order
                5. Print info by Truck
                6. Print info by Truck (visually simplified for users)
                7. Find total miles travelled by each truck & total sum
                0. Exit/Quit
            """)
        ans = input("What would you like to do? \nINPUT: ")
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

            for testing_package in range(1, packages.count + 1):
                print(packages.get(testing_package))

        elif ans == "3":
            """ print packages status at a user-specified time """

            try:
                time_text = input("Using format <HH:MM:SS> enter a time: ")
                status_time = datetime.strptime(time_text, "%H:%M:%S")

                print("You asked for a status update on EVERY package at {}...".format(
                    status_time.strftime("%H:%M:%S %testing_package")))

                print("\nAll {0} assigned packages at {1}".format(truck_1.label, status_time.strftime("%H:%M:%S %p")))
                truck_1.print_packages_status(status_time)
                print("\nAll {0} assigned packages at {1}".format(truck_2.label, status_time.strftime("%H:%M:%S %p")))
                truck_2.print_packages_status(status_time)
                print("\nAll {0} assigned packages at {1}".format(truck_3.label, status_time.strftime("%H:%M:%S %p")))
                truck_3.print_packages_status(status_time)
            except ValueError:
                print("Incorrect entry. Please try again.")

        elif ans == "4":
            """ re-calculate delivery order for all trucks"""

            # recalculate the delivery order and reset each truck
            for a_truck in vehicles:
                path = path_order_nearest_neighbor(g, a_truck, a_truck.packages_list)
                a_truck.delivery_order = deque(path)
                a_truck.packages_list = path.copy()
                a_truck.location_address = hub_address

        elif ans == "5" or ans == "6":
            """ Print truck info """

            # loop through all trucks in vehicles, print its package quantity, location, and the packages' info
            for printing_truck in vehicles:
                print("{0}\n"
                      "\t\tLocation: {1}, there are {2} packages to deliver.".format(printing_truck.label,
                                                                                     printing_truck.location_address,
                                                                                     len(printing_truck.packages_list)))
                for pack in printing_truck.packages_list:
                    if ans == "5":
                        # this prints the entire package
                        print("\t\t\tpackage #{0}: {1}".format(pack[0], pack))
                    else:   # if ans == "6"
                        # this print is more human-friendly, primarily for testing purposes
                        print("\t\t\tpack #{0} \t@ {1}   \t{2}".format(pack[0], pack[1], pack[8]))

        elif ans == "7":
            """ Find miles_total_all_vehicles travelled by each truck """

            # set all trackers to 0.0
            miles_total_all_vehicles = 0.0
            for current_t in vehicles:
                current_t.miles_driven = 0.0

            # find the sum of the total distance each truck travels in their round trips
            for current_truck in vehicles:
                t_packages = current_truck.packages_list.copy()
                # loop through each package that is loaded,
                #       tracking the DELIVERED TIME and miles_total_all_vehicles driven

                for pack in t_packages:
                    edge = g.find_distance(g.get_vertex(current_truck.location_address),
                                           g.get_vertex(pack[1]))
                    current_truck.deliver_package(pack, edge)

                # once every package has been delivered, return the truck to the HUB.
                trip_to_hub = g.find_distance(g.get_vertex(current_truck.location_address),
                                              g.get_vertex(hub_address))
                current_truck.miles_driven += trip_to_hub
                current_truck.location_address = hub_address
                miles_total_all_vehicles += current_truck.miles_driven
                print("\t{0} drove a total of {1:.1f} miles".format(current_truck.label, current_truck.miles_driven))
                # after calculations, reset current_truck.miles_driven to zero so future calculations are unaffected
                current_truck.miles_driven = 0.0

            print("\n{0:.1f} miles_total_all_vehicles total".format(miles_total_all_vehicles))

        elif ans == "0":
            """ exit the program"""
            raise SystemExit
        else:
            """ If user input is an unanticipated option, they should be re-prompted for input"""
            print("Not a Valid Choice. Try again")
