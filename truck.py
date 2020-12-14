# t_graph.py by Zachary McNamara zmcnama@my.wgu.edu ID#001182706

from collections import deque
import datetime
import time


class Truck:
    def __init__(self, label):
        self.label = label
        self.packages_list = []
        self.delivery_order = deque
        self.speed = 18
        self.miles_driven = 0.0
        self.delivered_packages = []
        self.time_tracker = datetime.datetime(2000, 1, 1, 8, 0, 0)
        self.location_address = "4001 South 700 East"

    @property
    def packages_list(self):
        return self._packages_list

    @packages_list.setter
    def packages_list(self, packs):
        self._packages_list = packs

    @packages_list.deleter
    def packages_list(self):
        del self._packages_list

    @property
    def miles_driven(self):
        return self._miles_driven

    @miles_driven.setter
    def miles_driven(self, miles):
        self._miles_driven = miles

    @property
    def delivery_order(self):
        return self._delivery_order

    @delivery_order.setter
    def delivery_order(self, value):
        self._delivery_order = value

    @delivery_order.deleter
    def delivery_order(self):
        del self._delivery_order

    def load_package(self, package):
        max_index = len(package) - 1
        package[max_index] = "Loaded on " + self.label
        self._packages_list.append(package)

    def deliver_package(self, package, miles):
        self.delivered_packages.append(package)
        self.location_address = package[1]
        self._miles_driven += miles

    def print_packages_status(self, specified_datetime):
        for p in self.packages_list:
            time_string = p[8][-11:-3]
            delivered_time = datetime.datetime.strptime(time_string, "%H:%M:%S")

            # if the package has not been 'delivered' yet, it is still loaded.
            if delivered_time > specified_datetime:
                t_package = list(p)
                t_package[8] = "Loaded in " + self.label

                if "Delayed" in p[7]:
                    t_package = list(p)
                    t_package[8] = "Delay shipping. Assign to " + self.label
            else:
                t_package = list(p)
                t_package[8] = "Delivered by {} at ".format(self.label) + time_string

            print("\t\t{}".format(t_package))






