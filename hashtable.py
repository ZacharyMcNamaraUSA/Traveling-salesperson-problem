#hashtable.py


class HashTable:

    def __init__(self):
        self.size = 10
        self.map = [None] * self.size
        self.count = 0

    # Function to calculate the hash_value, given a key
    # This function uses ASCII values over package IDs to ease potential changes
    def get_hash(self, key) -> int:
        hashed = 0

        for char in str(key):
            hashed += ord(char)
        return hashed % 10

    # Function to add an element to the hashtable
    def add(self, key, value):
        key_hash = self.get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
        else:
            for package in self.map[key_hash]:
                if package[0] == key:
                    package[1] = value
            self.map[key_hash].append(key_value)
        self.count += 1
        print("\t\tAdded something!\nkey=" + key + "\t\t")

    # Function to retrieve an element, if it is stored in the hashtable
    def get(self, key):
        key_hash = self.get_hash(key)
        if self.map[key_hash] is not None:
            for item in self.map[key_hash]:
                if item[0] == str(key):
                    # print("YOU FOUND THE CORRECT ONE by matching the KEY!\t" + item[0] + " = " + str(key))
                    return item[1]
        return None

    def delete(self, key):
        key_hash = self.get_hash(key)

        if self.map[key_hash] is None:
            return False
        for item in range(0, len(self.map[key_hash])):
            if self.map[key_hash][item][0] == key:
                self.map[key_hash].pop[item]
                return True

    def print(self):
        for item in self.map:
            if item is not None:
                print(str(item))
            else:
                # print("this HashTable has no value(s) here")
                pass

    def get_count(self):
        return self.count

    def get_hashed_list(self, key):
        for item in self.map:
            if item is not None:
                return str(item)
            else:
                return None

    def __next__(self, key):
        self.num += 1
        try:
            num = self.num
            self.num += 1
            return num
        except IndexError:
            raise StopIteration
    next = __next__

    def __iter__(self):
        return self




    # def keys(self):
    #     my_list = []
    #     if self is None:
    #         return None
    #     else:
    #         for element in range(0, len(self.map)):
    #             for item in self.map[element]:
    #                 my_list.append([item[0], item[1][1]])
    #         return my_list






