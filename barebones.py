# barebones.py by Zachary McNamara zmcnama@my.wgu.edu ID#001182706

import copy
import csv
import hashtable
import Package
from graph import Graph, Vertex
import operator

packages = hashtable.HashTable()
distances = hashtable.HashTable()
verts = hashtable.HashTable()
vertexes = []
graph = Graph()
total_miles = 0.00
total_packages = 0
list_of_all_stops = []
hour = 8
minute = 0
regulars = []
truck_A = []
truck_B = []


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
    #     print("appending vertex'" + current_vertex.label + "' to unvisited_queue!")
    # print("len(unvisited_queue)=" + str(len(unvisited_queue)))

    # Start_vertex has a distance of 0 from itself
    start_vertex.distance = 0

    # One vertex is removed with each iteration; repeat until the list is
    # empty.
    while len(unvisited_queue) > 0:
        print("there are more unvisited vertexes still")
        for v in unvisited_queue:
            print(v.label)

        # Visit vertex with minimum distance from start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)
        # print("type of current_vertex=" + str(type(current_vertex)))

        # Check potential path lengths from the current vertex to all neighbors.
        for adj_vertex in g.adjacency_list[current_vertex]:
            # print("\n\n\nentering for loop..\n\n\n")
            # print("adv_vertex=" + str(adj_vertex))
            # print("current_vertex=" + current_vertex.label)
            # print("adj_vertex=" + adj_vertex.label)
            edge_weight = float(g.edge_weights[(current_vertex, adj_vertex)])
            # print("edge_weight=" + str(edge_weight))
            # print("edge_weight type: " + str(type(edge_weight)))
            # print("current_vertex.distance type: " + str(type(current_vertex.distance)))
            # print("current_vertex.distance=" + str(current_vertex.distance))

            alternative_path_distance = current_vertex.distance + edge_weight

            # If shorter path from start_vertex to adj_vertex is found,
            # update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                print("Alt_path_dist < adj_vertex.distance....\n\tA closer vertex has been found."
                      "Update the infos. Set the pred_vertex!!!\n\t\tcurrent: " + current_vertex.label +
                      " -> " + adj_vertex.label + " is now the shortest path. dist of " + str(alternative_path_distance))
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex
                # print("type of adj_vertex.pred_vertex=" + str(type(adj_vertex.pred_vertex)))
            else:
                # print("this is not a shorter path")
                pass


def get_shortest_path(start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = ""
    current_vertex = end_vertex
    while current_vertex is not start_vertex:
        # print("current_vertex is " + str(type(current_vertex)))
        path = " -> " + str(current_vertex.label) + path
        current_vertex = current_vertex.pred_vertex
    path = start_vertex.label + path
    return path


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
    vertexes.append(vertex_0)
    vertexes.append(vertex_1)
    vertexes.append(vertex_2)
    vertexes.append(vertex_3)
    vertexes.append(vertex_4)
    vertexes.append(vertex_5)
    vertexes.append(vertex_6)
    vertexes.append(vertex_7)
    vertexes.append(vertex_8)
    vertexes.append(vertex_9)
    vertexes.append(vertex_10)
    vertexes.append(vertex_11)
    vertexes.append(vertex_12)
    vertexes.append(vertex_13)
    vertexes.append(vertex_14)
    vertexes.append(vertex_15)
    vertexes.append(vertex_16)
    vertexes.append(vertex_17)
    vertexes.append(vertex_18)
    vertexes.append(vertex_19)
    vertexes.append(vertex_20)
    vertexes.append(vertex_21)
    vertexes.append(vertex_22)
    vertexes.append(vertex_23)
    vertexes.append(vertex_24)
    vertexes.append(vertex_25)
    vertexes.append(vertex_26)

    for v in vertexes:
        g.add_vertex(v, vertexes)





    # Creating the hashtable for the Packages CSV file
    create_package_hashtable("wgups_package_file.csv")
    # packages.print()

    # Creating the hashtable for the distances between Cities CSV file
    create_distance_hashtable("wgups_distance_table.csv")
    # distances.print()




    # set secondary_stop default to the HUB
    secondary_stop = distances.get("4001 South 700 East")
    # this loops through all stops

    # This loop does keeps track of the vertex being worked on.
    #       Necessary so that the
    cnt = 1
    for v in range(0, len(vertexes)):
        vert_tracker = v-1
        if vert_tracker < 0:
            vert_tracker = 0
        vert1 = vertexes[v]
        vert2 = vertexes[vert_tracker]

        # print("\n\nbegin next iteration...")
        # print("1st vertex =" + vert1.label)
        # print("\t2nd vertex=" + vert2.label)
        #
        # print("vertexes[" + str(v) + "].label: " + vertexes[v].label)
        stop = distances.get(vertexes[v].label)
        # print("stop #" + str(cnt) + " is type: " + str(type(stop)))
        cnt += 1
        # print("stop follows below...")
        # print(stop)

        # This loop goes through the WEIGHT of the edge
        #       between vert1 and all vert2 in vertexes with a smaller index
        for s in range(5, len(stop)):
            vert2 = vertexes[vert_tracker]

            if stop[s] == "0.0":
                # print("trying to make weight='" + stop[s] + "'.")
                weight = float(stop[s])
                # print("weight type: " + str(type(weight)))
                # print("\tLink this edge to ITSELF with distance of 0.0")
                # print("\t\tg.add_undirected_edge(stop=" + vert1.label + ", prev_stop=" + vert1.label +
                #       ", weight=" + stop[s])
                g.add_undirected_edge(vert1, vert1, stop[s])
            elif stop[s] != "":
                # print("trying to make weight='" + stop[s] + "'.")
                weight = float(stop[s])
                # print("weight type: " + str(type(weight)))
                # print("\tg.add_undirected_edge(stop=" + vert1.label + ", prev_stop=" + vert2.label +
                #       ", weight=" + stop[s])
                g.add_undirected_edge(vert1, vert2, float(stop[s]))

            vert_tracker -= 1
            vert2 = vertexes[vert_tracker]
            # print("Changing vert2 to be vert2.label=" + vert2.label)




    dijkstra_shortest_path(g, vertex_0)

    # Sort the vertices by the label, for convenience; display shortest path for each vertex
    # from vertex_a.
    for v in sorted(g.adjacency_list, key=operator.attrgetter("label")):
        print("From g.adjacency_list, Vertex v=" + v.label)
        if v.pred_vertex is None and v is not vertex_0:
            print("\tHUB to %s: no path exists" % v.label)
            if v is not vertex_0:
                print("\t\t\tThere is no previous vertex for v=" + v.label)
        else:
            # print("\tv is a " + str(type(v)))
            # print("\tvertex_0 is a " + str(type(vertex_0)))
            print("\tHUB to %s: %s (total weight: %g)" % (v.label, get_shortest_path(vertex_0, v), v.distance))

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





