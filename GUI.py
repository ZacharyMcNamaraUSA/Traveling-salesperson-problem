# C950 PA by Zachary McNamara ID: 001182706
import copy
import csv
import random
import tkinter as tk
import hashtable
import turtle
from tkinter import *
from time import time

packages = hashtable.HashTable()
distances = hashtable.HashTable()
destinations = hashtable.HashTable()
stops = []
offset = 800
cities = 0
total_packages = 0


def create_package_hashtable(filename):
    with open(filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for row in read_csv:  # For every row in CSV file
            key = row[0]
            packages.add(key, row)
            global total_packages
            total_packages += 1
        csv_file.close()


def create_distance_hashtable(csv_filename):
    with open(csv_filename) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')

        for row in read_csv:  # For every row in CSV file
            global cities
            cities += 1
            key = row[0]
            # if "" in row:
            #     print("can ya hear the empty spaces?")
            #     print(row)
            distances.add(key, row)

        csvfile.close()


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
tk.Canvas.create_circle = _create_circle


def create_stops():
    with open('Coordinates.csv', newline='') as file:
        names = ["Destination", "Address", "CoordX", "CoordY", "Code"]
        reader = csv.DictReader(file, fieldnames=names)

        # Iterate through the Stop+Coordinates elements,
        #   Create a 'circle' for each one with its Code
        first_time = True
        for row in reader:
            if first_time:
                first_time = False
                continue
            else:
                element = [row["Destination"], row["CoordX"], row["CoordY"], row["Code"]]
                # print("Key: " + key)
                # print("Code is element 3 = " + code)

                stops.append(element)


# This function places a circle for each Stop with approximate coordinates -- NOT EXACT
def map_stops(map_stops_canvas, translate=0):
    #   Once all stops are plotted on the canvas, draw lines connecting the stops

    with open('Coordinates.csv', newline='') as file:
        names = ["Destination", "Address", "CoordX", "CoordY", "Code"]
        reader = csv.DictReader(file, fieldnames=names)

        # Iterate through the Stop+Coordinates elements,
        #   Create a 'circle' for each one with its Code
        first_time = True
        for row in reader:
            element = [row["Destination"], row["Address"], row["CoordX"], row["CoordY"], row["Code"]]
            key = row["Destination"]
            code = row["Code"]
            # print("Key: " + key)
            # print("Code is element 3 = " + code)

            if first_time:
                first_time = False
                continue
            else:
                try:
                    # Skip over Header line, which was added for increased readability

                    x = int(row["CoordX"]) + translate
                    y = int(row["CoordY"])

                    global stops
                    stops.append(element)

                    if key == "HUB":  # Making the HUB a unique color
                        map_stops_canvas.create_circle(x, y, 8, fill="red", outline="white", width=2)
                        map_stops_canvas.create_text(x, y - 20, fill="#329644", font="Times 18 bold", text=code)
                        continue
                    elif code == "V":
                        map_stops_canvas.create_line(x, y, x, y - 10, fill="black", width=2)  # , dash = 2
                        map_stops_canvas.create_circle(x, y, 8, fill="blue", outline="white", width=2)
                        map_stops_canvas.create_text(x, y + 20, fill="#329644", font="Arial 15 bold", text=row["Code"])
                    elif code <= "G" and code != "D":
                        map_stops_canvas.create_line(x, y, x - 10, y, fill="black", width=2)  # , dash = 2
                        map_stops_canvas.create_circle(x, y, 8, fill="blue", outline="white", width=2)
                        map_stops_canvas.create_text(x - 20, y, fill="#329644", font="Arial 15 bold", text=row["Code"])
                    else:
                        map_stops_canvas.create_line(x, y, x, y - 10, fill="black", width=2)  # , dash = 2
                        map_stops_canvas.create_circle(x, y, 8, fill="blue", outline="white", width=2)
                        map_stops_canvas.create_text(x, y - 20, fill="#329644", font="Times 15 bold", text=row["Code"])
                except ValueError:
                    print("Invalid value here")


def calculate_stops(selected):
    these_destionations = []

    for num in range(selected):
        # generator = random.randrange(0, selected)
        these_destionations.append(stops[num][0])
    return these_destionations


def connect_stops(canvas, stop1, stop2="4001 South 700 East", translate=offset, color="orange", width=4):
    with open('Coordinates.csv', newline='') as file:
        names = ["Destination", "Address", "CoordX", "CoordY", "Code"]
        reader = csv.DictReader(file, fieldnames=names)

        # Iterate through the Stop+Coordinates elements,
        #   Create a 'circle' for each one with its Code
        first_time = True
        stop1_x = 0
        stop1_y = 0
        stop2_x = 0
        stop2_y = 0

        for row in reader:
            # Skip over Header line, which was added for increased readability
            if first_time:
                first_time = False
                continue

            if row["Address"] == stop1:
                stop1_x = int(row["CoordX"]) + translate
                stop1_y = int(row["CoordY"])
            if row["Address"] == stop2:
                stop2_x = int(row["CoordX"]) + translate
                stop2_y = int(row["CoordY"])

        canvas.create_line(stop1_x, stop1_y, stop2_x, stop2_y, fill=color, width=width)      # , dash=30)
        print("Coord of stop1 = " + stop1 + "...\tX:" + str(stop1_x) + "\tY:" + str(stop1_y))
        print("\tCoord of stop2=" + stop2 + "...\tX:" + str(stop1_x) + "\tY:" + str(stop2_y))

    file.close()


def plot_route(canvas, selected_stops, package_hashtable, offset=0, color="orange", width=4):
    my_packs = copy.copy(selected_stops)
    print("the Packages we need to deliver")
    print(my_packs)
    current = "4001 South 700 East"
    target = ""
    for p in range(1, len(my_packs) + 1):
        print("p is " + str(p))
        n = my_packs.pop()
        print("popping " + str(n) + " off")
        target = package_hashtable.get(n)[1]
        print("target = " + target)
        connect_stops(canvas, target, current, offset, color, width)
        print("connecting " + current + " with " + target + ".")

        current = target

    # After delivering every package, return to the HUB
    #       target = HUB, from current location
    connect_stops(canvas, "4001 South 700 East", current, offset, color)


# # Menu
# class Menu:
#     def __init__(self, root):
#         self.root = root
#         self.canvas = Canvas(root, bg="black", width="1600", height="1000")
#
#         filename = tk.PhotoImage(file="map.png")
#         image = self.canvas.create_image(400, 400, image=filename)
#
#         map_stops(self.canvas)
#         map_stops(self.canvas, 800)
#
#     def run(self, root):
#         self.canvas = Canvas(root, bg="black", width="1600", height="1000")
#
#         e1 = Entry(self.canvas)
#         self.canvas.create_window(400, 10, window=e1)
#
#         self.show_map(self.canvas)
#         map_stops(self.canvas)
#
#         filename = tk.PhotoImage(file="map.png")
#         image = self.canvas.create_image(400, 400, image=filename)
#
#
#     def show_map(self, root):
#         canvas = Canvas(root, bg="black", width="1600", height="1000")
#
#         print("\n\nyou seeing hte map?\n\n")
#
#     def connect_stops(self, root, stop1, stop2):
#         canvas = Canvas(root, bg="black", width="1600", height="1000")
#         canvas.create_line(stop1[1], stop1[2], stop2[1], stop2[2], fill="pink", width=4, dash=14)  # , dash = 2
#
#     def plot_route(self, canvas, selected_stops):
#         pass


# Main for this Project
if __name__ == "__main__":
    # Creating the hashtable for the Packages CSV file
    create_package_hashtable("wgups_package_file.csv")
    # print("\nPACKAGE HashTable")
    # packages.print()

    # Creating the hashtable for the distances between Cities CSV file
    create_distance_hashtable("wgups_distance_table.csv")
    # print("\nHere's the HashTable of distances for you...")
    # distances.print()

    # Makes all my coordinates --- used in testing
    create_stops()

    root = Tk()

    vas = Canvas(root, bg="black", width="1600", height="1000")

    filename = tk.PhotoImage(file="map.png")
    image = vas.create_image(400, 400, image=filename)

    map_stops(vas)
    map_stops(vas, 800)

    # selected_stops = calculate_stops(10)
    # for each in selected_stops:
    #     print(each)
    # menu.plot_route(canvas, selected_stops)

    vas.pack()
    root.mainloop()
