# WGU Routing Program
# This program tries to find an optimal solution to 
# the delivery or 40 packages around Salt Lake City
# by WGUPS
# Author:       Casey Arnold
# Student ID:   000962933
# File: csv_loader.py
# Desc: This file loads the trucks into the hash table and assigns the packages to the trucks

from lib.hash_table import HashTable
from lib.package import Package
import csv

packages = []
first_delivery = [13, 14, 19, 15, 16, 20, 31, 40, 29, 30]  # first truck delivery
second_delivery = [3, 6, 1, 25, 36, 38, 18, 37, 34] # second truck delivery
third_delivery = [9, 28, 32] # third truck delivery
first_priorities = [15, 13, 14, 19, 16]
second_priorities = [6, 1, 25, 37, 34]
third_priorities = []
package_table = []

added_to_queue = [] 

# O(n), insert every package (along w object) into hash table
with open('data/packages.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.reader(file, delimiter=',')

    h = HashTable()

    for row in reader:
        pkg_id = int(row[0])
        pkg_addr = row[1]
        pkg_city = row[2]
        pkg_state = row[3]
        pkg_postal = row[4]
        pkg_delivery = row[5]
        pkg_size = row[6]
        pkg_note = row[7]
        value = Package(pkg_id, pkg_addr, pkg_city, pkg_state, pkg_postal,
                    pkg_delivery, pkg_size, pkg_note)
     
        if pkg_id not in first_delivery and pkg_id not in second_delivery and pkg_id not in third_delivery:
            packages.append(pkg_id)


        # Insert value into the hash table
        h.insert(pkg_id, value)
        package_table.append([pkg_id, pkg_addr])

    
# add all remaining packages that didn't have a special note to the delivery truck queues -> O(n)
for pkg_id in packages:
    if len(first_delivery) < 16:
        first_delivery.append(pkg_id)

    elif len(second_delivery) < 16:
        second_delivery.append(pkg_id)

    else:
        third_delivery.append(pkg_id)

# return hash table object -> O(1)
def get_hash_table():
    return h

# return package table list -> O(1)
def get_package_table():
    return package_table

# return first delivery list -> O(1)
def get_first_delivery():
    return first_delivery, first_priorities

# return second delivery list -> O(1)
def get_second_delivery():
    return second_delivery, second_priorities

# return third delivery list -> O(1)
def get_third_delivery():
    return third_delivery, third_priorities


