# Package.py

class Package:
    def __init__(self):
        self.key = ""
        self.address = []
        self.delivery_time = ""
        self.weight = 0.0
        self.notes = ""
        self.x = 0
        self.y = 0
        self.size = 6

    @property
    def key(self):
        """ This is the key used to identify each Package in the HashTable """
        return self._key

    @key.setter
    def key(self, value):
        print("key setter called\nkey=" + value)
        self._key = value

    @key.deleter
    def key(self):
        print("key deleter called")
        del self._key

    @property
    def address(self):
        """ This is the address property """
        print("getter of address called")
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def delivery_time(self):
        """ This is the delivery time property """
        print("getter of delivery called")
        return self._delivery_time

    @delivery_time.setter
    def delivery_time(self, value):
        self._delivery_time = value

    @property
    def notes(self):
        """ Special delivery notes property """
        print("notes getter called")
        return self._instructions

    @notes.setter
    def notes(self, value):
        self._instructions = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    @property
    def x(self):
        print("x getter called")
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        print("y getter called")
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def print(self):
        print("Package " + self.key + ", " + self.address[0] + ", " + self.address[1] + ", " + self.address[2] + ", "
              + self.address[3] + ", " + self.delivery_time + ", " + self.notes + ".")

    # self.delivery_time = ""
    # self.instructions = ""
    # self.x = 0
    # self.y = 0

