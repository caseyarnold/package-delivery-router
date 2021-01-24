# WGU Routing Program
# This program tries to find an optimal solution to 
# the delivery or 40 packages around Salt Lake City
# by WGUPS
# Author:       Casey Arnold
# Student ID:   000962933
# File: Distances.py
# Desc: This file calculates the distances between stops on the truck routes
# as well as managing the place data and adding timestamps to packages as they
# are delivered

import csv
from csv_loader import get_hash_table
from lib.time_clock import TimeClock
places = []
distances = []
h = get_hash_table()

# add all the place data into a list -> O(n)
with open('data/places.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        row[0] = int(row[0])
        places.append(row)

# add all distance data into a list -> O(n)
with open('data/distances.csv') as file:
    reader = csv.reader(file, delimiter=',')

    for row in reader:
        if row[1] == '':
            continue

        distances.append(row)

# get the shortest route possible given a list, O(n^2)
# returns : , _sorted, _sorted_distances, _total_distance
def get_shortest_route(_list, priorities = []):
    #return lists
    _sorted = []
    _sorted_distances = []
    _total_distance = float(0)

    # find closest to to first hub
    if len(priorities) == 0: 
        min_distance_to_hub = float('inf')
        min_index_to_hub = -1

        for i in _list:
            distance = get_distance(0, get_place(i))
            if distance < min_distance_to_hub:
                min_distance_to_hub = distance
                min_index_to_hub = i

        _sorted.append(min_index_to_hub)
        _list.remove(min_index_to_hub)
        _sorted_distances.append(min_distance_to_hub)
        _total_distance += min_distance_to_hub
    else:
        min_distance_to_hub = float('inf')
        min_index_to_hub = -1

        for i in priorities:
            distance = get_distance(0, get_place(i))
            if distance < min_distance_to_hub:
                min_distance_to_hub = distance
                min_index_to_hub = i

        _sorted.append(min_index_to_hub)
        _list.remove(min_index_to_hub)
        _sorted_distances.append(min_distance_to_hub)
        _total_distance += min_distance_to_hub
        priorities.remove(min_index_to_hub)

    while len(priorities) != 0:
        # get latest sorted item
        cur = _sorted[-1]
        min_distance = float('inf')
        min_index = -1

        for i in priorities:
            distance = get_distance(get_place(cur), get_place(i))
            if distance < min_distance:
                min_distance = distance
                min_index = i

        _sorted.append(min_index)
        _list.remove(min_index)
        priorities.remove(min_index)
        _sorted_distances.append(min_distance)
        _total_distance += min_distance

    # now do the rest
    while len(_list) != 0:
        # get latest sorted item
        cur = _sorted[-1]
        min_distance = float('inf')
        min_index = -1

        for i in _list:
            distance = get_distance(get_place(cur), get_place(i))
            if distance < min_distance:
                min_distance = distance
                min_index = i

        _sorted.append(min_index)
        _list.remove(min_index)
        _sorted_distances.append(min_distance)
        _total_distance += min_distance

    return _sorted, _sorted_distances, _total_distance



# find the place given the package id -> O(n)
def get_place(pkg_id):
    if pkg_id == 0:
        return 0

    addr = h.get(pkg_id).addr

    for place in places:
        if place[2] == addr:
            return place[0]

    return -1

# return place list -> O(1)
def get_places():
    return places

# return distances list -> O(1)
def get_distances():
    return distances

# add timestamps to notes -> O(n)
def add_timestamps(obj, start_time, h):
    hour, minute = start_time.split(':')
    t = TimeClock(int(hour), int(minute))
    i = 0
    for index in obj[1]:
        pkg = obj[0][i]
        time = t.next(index)
        i+=1
        h.get(pkg).update('delivered_at', time).update('delivery_start', TimeClock(start_time))

# Calculate the total distance -> O(1)
def get_distance(row, col):
    distance = distances[row-1][col-1]
    
    if distance == '':
        try:
            distance = distances[col-1][row-1] 

        except IndexError:
            distance = 0

    return float(distance)
