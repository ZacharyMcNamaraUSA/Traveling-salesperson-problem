# Main.py

import copy
import csv
import random
import tkinter as tk
from tkinter import font as tkFont
import hashtable
from decimal import *
import turtle
from time import time
import GUI as g
import Package

packages = hashtable.HashTable()
distances = hashtable.HashTable()
total_miles = 0.00
total_packages = 0
total_stops = 0
regulars = []
truck_A = []
truck_B = []

# "HUB", "International Peace Gardens", "Sugar House Park",
#                 "Taylorsville-Bennion Heritage City Gov Off", "Salt Lake City Division of Health Services", ]


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
    with open(csv_filename) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        stop_count = 0
        for row in read_csv:  # For every row in CSV file
            key = row[1]
            # print(row[1])
            row.insert(0, str(stop_count))
            distances.add(key, row)

            stop_count += 1
            # print(row)

        csvfile.close()


# Function finds the distance between 2 Stops
#   params: target destination and a previous destination (current location), defaults to HUB
#       a destination's key is its primary identifier in the HashTable distances
def lookup_distance(target, previous="4001 South 700 East"):
    tar = distances.get(target)
    # print("TARGET DESTINATION in lookup_distance: ")
    # print(tar)
    prev = distances.get(previous)
    # print("\tPREVIOUS DESTINATION in lookup_distance: ")
    # print(prev)
    try:
        mi = 0.00

        mi = float(prev[5 + int(tar[0])])
    except ValueError:
        mi = float(tar[5 + int(prev[0])])
    except TypeError:
        mi = 0.0
        print(type(mi))
        print("unacceptable")

    # print("Traveling from " + prev[1] + " --> " + tar[1] + " is " + "{:.2f}".format(mi) + " miles.")

    return mi


def distance_of_route_as_ordered(packs):
    miles = 0
    undelivered = []
    for p in packs:
        if packages.get(p) is not None or p is None:
            undelivered.append(packages.get(p)[1])
        else:
            print("I did not find a Package in distance_of_route.\tp is " + str(p))
    for num in range(len(undelivered)):
        m = 0
        if num == 0:
            m = lookup_distance(undelivered[num])
        else:
            m: float = lookup_distance(undelivered[num], undelivered[num -1])
        miles += m

    # print("This route travelled {:.1f}".format(miles) + " MILES and delivered "
    #               + str(len(undelivered)) + " packages.")

    return miles


# Selects packages for internal testing purposes
# returns the selected packages, default max "limit" is 16
def select_random_packages(limit=16):
    selected = []
    if limit >= packages.count or limit <= 0:
        limit = packages.count

    # This loop selects up to "limit" Packages, in order
    for p in range(1, packages.count+1):
        selected.append(packages.get(p)[0])

        # A truck can carry a maximum of 16 Packages
        if len(selected) >= limit:
            break

    random.shuffle(selected)

    return selected


# This function was never finished. See Diijkstra's Shortest Path Algorithm (greedy algorithm)
# Finds the closest, by distance, delivery location
def find_closest_destination(addresses, current_address="4001 South 700 East"):
    # I just need to look at the distances hashtable using current_address as a key
    closest = ""

    location_index = 0
    location = ""
    # Finding the location_index of my current_address
    for i in range(len(addresses)):
        print("i = " + str(i))
        print("Addresses[" + str(i) + "] " + addresses[i])
        location = distances.get(addresses[i])
        print(location)

        for d in location:
            if d == "":
                location_index = i
                break
            else:
                # print("distance " + d)
                pass

        print("location_index is " + str(location_index))

    print("\n\n\nDIFFERENT LOOP THINGY????\n\n\n")

    # lowest_distance = 0
    # # Search through every Package in addresses
    # for p in range(len(addresses)):
    #     # Compare this Package's destination to our current location
    #     print("p=" + str(p))
    #     print("package_key_list[p]=" + addresses[p])
    #     distances.get(addresses[p])

    return closest


# Adds a list of packages "my_packs" to the designated Truck "car"
#   Packages are tracked by their key, the 1st element in the delivery address  i.e. distances.get(i)[1]
def load_truck(car, load_packs):

    for i in load_packs:
        car.append(i)

    return car


# Function visually shows a new route on the provided tkinter Canvas
def try_a_new_random_route(canvas):
    print("TEST A RANDOM ROUTE")
    # Make a temp list of Packages by randomly selecting all Packages
    my_packages = select_random_packages()
    route1_distance = distance_of_route_as_ordered(my_packages)
    print("route1_distance is {:.1f}".format(route1_distance) + " MILES and delivered "
          + str(len(my_packages)) + " packages.")
    print(my_packages)
    g.plot_route(canvas, my_packages, packages, 800)
    canvas.pack()


# DIFFERENCE BETWEEN try_a_new_random_route and try_a_random_route is NOT KNOWN
# Function visually shows a new route on the provided tkinter Canvas
def try_a_random_route(canvas):
    print("TEST A RANDOM ROUTE")
    # Make a temp list of Packages by randomly selecting all Packages
    my_packages = select_random_packages()
    route1_distance = distance_of_route_as_ordered(my_packages)
    print(my_packages)
    g.plot_route(canvas, my_packages, packages, 800)
    g.plot_route(canvas, my_packages, packages, 0)

    print("route1_distance is {:.1f}".format(route1_distance) + " MILES and delivered "
          + str(len(my_packages)) + " packages.")

    canvas.pack()


# Function selects package(s) with a delivery deadline or special notes
def get_constrained_package_keys(p_list):
    keys = []
    for p in range(1, p_list.count):
        message = ""
        pack = packages.get(p)

        # This if condition reruns the loop if the Package pack is not constrained.
        #       Therefore, if the condition does not stop the loop, pack is a constrained Package
        if pack[5] == "EOD" and pack[7] == "":
            continue

        keys.append(pack[1])
        message += "Package " + pack[0] + "\n"

    return keys


# Function prints constraints for any of the provided packages
def print_constrained_info(constrained_list):
    for p in range(1, len(constrained_list)):
        message = ""
        pack = packages.get(p)

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


def main():
    # Creating the hashtable for the Packages CSV file
    create_package_hashtable("wgups_package_file.csv")

    # Creating the hashtable for the distances between Cities CSV file
    # create_distance_hashtable("wgups_distance_table.csv")

    # get the key for priority packages
    constrained = get_constrained_package_keys(packages)
    print_constrained_info(constrained)




    # This while loop controls the console menu users interact with
    while True:
        print("""
              Enter " " to rerun 
              1. Find total miles traveled
              2. Get snapshot
              3. Print Packages HashTable
              4. Print Distances HashTable
              5. Graphics
              6. Show ALL constrained Packages
              7. Find miles travelled from selected Packages
              0. Exit/Quit
              """)
        ans = input("What would you like to do? ")
        if ans == "1":
            """ Find Total miles travelled """
            my_packages = select_random_packages(packages.count)
            route_distance = distance_of_route_as_ordered(select_random_packages(packages.count))
            print("route1_distance is {:.1f}".format(route_distance) + " MILES and delivered "
                  + str(len(my_packages)) + " packages.")
            current_best = route_distance
            if current_best < best_distance:
                best_distance = current_best
                print("NEW BEST RECORD!!! Only {:.1f}".format(best_distance) + " MILES")





        current_best = 0.0
        best_distance = float("inf")

        # Find the key for each Package with constraints on its delivery
        constrained_keys = get_constrained_package_keys(packages)
        print("There are " + str(len(constrained_keys)) + " constrained Packages, all printed below.")
        print(constrained_keys)

        # Distribute the Packages with earlier delivery times to the first 2 loads
        load1 = []
        for n in constrained_keys:
            print("n is:" + n + ". See?")
            print(packages.get(n))

        print(packages.get("410 S State St"))

        my_packages = select_random_packages(packages.count)
        route_distance = distance_of_route_as_ordered(select_random_packages(packages.count))
        print("route1_distance is {:.1f}".format(route_distance) + " MILES and delivered "
              + str(len(my_packages)) + " packages.")
        current_best = route_distance
        if current_best < best_distance:
            best_distance = current_best
            print("NEW BEST RECORD!!! Only {:.1f}".format(best_distance) + " MILES")






        elif ans == " ":
            main()
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
            g.create_stops()

            root = tk.Tk()
            root.title = "WGUPS"
            vas = tk.Canvas(root, bg="black", width="1600", height="850")
            vas.pack()

            filename = tk.PhotoImage(file="map.png")
            image = vas.create_image(400, 400, image=filename)

            g.map_stops(vas)
            g.map_stops(vas, g.offset)

            helv36 = tkFont.Font(family="Helvetica", size=20, weight="bold")
            quit_button = tk.Button(root, text="Press Here to return to program", font=helv36, bg="gray", width=42,
                                    height=8,
                                    borderwidth=35, command=root.destroy)
            quit_button.pack(side=tk.LEFT)
            run_another_route_button = tk.Button(root, text="Test another delivery route", font=helv36, bg="gray",
                                                 width=42,
                                                 height=8, borderwidth=35, command=try_a_new_random_route(vas))
            run_another_route_button.pack(side=tk.BOTTOM)

            root.mainloop()

            # print("The distance between " + dest1 + " and " + "the HUB is " + str(miles) + " miles.")
        elif ans == "6":
            """" Prints all Packages with constraints """
            constrained_keys = get_constrained_package_keys(packages)

            print("There are " + str(len(constrained_keys)) + " constrained Packages.")
            print(constrained_keys)
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
            break
        else:
            """ If user enters an unanticipated option, they should be re-prompted for input"""
            print("Not a Valid Choice. Try again")


# Main for this Project
if __name__ == "__main__":
    main()





