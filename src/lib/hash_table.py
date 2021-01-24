# WGU Routing Program
# This program tries to find an optimal solution to 
# the delivery or 40 packages around Salt Lake City
# by WGUPS
# Author:       Casey Arnold
# Student ID:   000962933
# File: Hash_table.py
# Desc: This class implements a hash table in order to quickly retrieve, insert
# and update package objects

class HashTable:
    # initialise the hash -> O(n)
    def __init__(self, capacity = 10):
        self.table = []
        self.counter = 0

        for i in range(capacity):
            self.table.append([])


    # calculate hash key -> O(1)
    def _calculate_hash(self, key):
        return int(key) % len(self.table)

    # return size -> O(1)
    def size(self):
        return self.counter

    # find a key -> o(n)
    def get(self, key):
        hash_key = self._calculate_hash(key)

        if self.table[hash_key] is not None:
            for item in self.table[hash_key]:
                if item[0] == key:
                    return item[1]

        return None

    # return all packages -> o(n^2)
    def get_all(self):
        table = []

        for row in self.table:
            for item in row:
                table.append(item)

        table.sort()
        return table

    # get first package -> O(1)
    def get_first(self):
        return self.table[0][0][1]

    # add a package -> O(n)
    def insert(self, key, value):
        hash_key = self._calculate_hash(key)

        if self.table[hash_key] is not None:
            for item in self.table[hash_key]:
                if item[0] == key:
                    return None

        self.table[hash_key].append([key, value])
        self.counter += 1

    # update a package -> O(n)
    def update(self, key, value):
        hash_key = self._calculate_hash(key)

        if self.table[hash_key] is not None:
            for item in self.table[hash_key]:
                if item[0] == key:
                    item[1] = value
                    return value

        return None