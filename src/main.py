# WGU Routing Program
# This program tries to find an optimal solution to 
# the delivery or 40 packages around Salt Lake City
# by WGUPS
# Author:       Casey Arnold
# Student ID:   000962933
# File: Main.py
# Desc: This file manages the user interface of the program, taking user input and
# retrieving useful information based on that input for the user

from csv_loader import get_hash_table, get_first_delivery, get_second_delivery, get_third_delivery
import distances
import copy 
from datetime import timedelta
from lib.time_clock import TimeClock

# get hash table
h = get_hash_table()

# get the first, second and third optimized delivery routes
first = get_first_delivery()
second = get_second_delivery()
third = get_third_delivery()

total_distance = 0

# add the timestamps to the hashtable based on the furhter optimized routes ; compute total_distance
dist = distances.get_shortest_route(first[0], first[1])
total_distance += dist[2]
distances.add_timestamps(dist, '8:00', h)
# add the timestamps to the hashtable based on the furhter optimized routes ; compute total distance
dist = distances.get_shortest_route(second[0], second[1])
total_distance += dist[2]
distances.add_timestamps(dist, '9:10', h)

# add the timestamps to the hashtable based on the furhter optimized routes  ; compute total distance
dist = distances.get_shortest_route(third[0], third[1])
total_distance += dist[2]
distances.add_timestamps(dist, '12:00', h)


# Until the code manually breaks the loop, we will continue to allow the user to use the interactive prompt
while True:

    command = input('What would you like to do first? 1 = Lookup Single Package, 2 = Get All Packages, E = exit: ')

    # first case, searching a single package
    if command == '1':
        pkg_id = int(input('Enter the package ID: '))
        time = input('What time would you like to view as? (EOD or (hh:mm): ')

        # find the package by id and create a copy of it that is safe to alter based on user's desired time ; O(1)
        package = h.get(pkg_id)
        package = copy.deepcopy(package)

        package_time = package.delivered_at.to_timedelta()

        if time == 'eod' or time == 'EOD':
            time = TimeClock('23:59').to_timedelta()
        else:
            time = TimeClock(time).to_timedelta()

        start_time = package.delivery_start.to_timedelta()

        # if the comparsion time is before the delivered time, it is either
        # in transit or at the hub
        if time < start_time:
            delivery_status = 'At HQ'
        elif time > start_time and package_time > time:
        	delivery_status = 'In transit'
        else:
            delivery_status = f'Delivered at {package_time}'

        if pkg_id == 9 and time > TimeClock(10, 20).to_timedelta():
            package.addr = '410 S State St.'
            package.city = 'Salt Lake City'
            package.postal = '84111'
            package.note = 'Address Corrected At 10:20am'

        print(f"""
ID: {pkg_id} 
Address: {package.addr}, {package.city} {package.state} {package.postal} 
Delivery Due: {package.delivery} 
Note: {package.note}""")
        if package.delivery != 'EOD':
            if TimeClock(package.delivery).to_timedelta() < package.delivered_at.to_timedelta(): # LATE
                print('\033[91m', delivery_status, '\033[0m')
            else: # on time
                print('\033[92m', delivery_status, '\033[0m')
        else:
            print(delivery_status)

    # second case, show all packages -> O(n)
    elif command == '2':
        input_time = input('What time would you like to view as? (EOD or (hh:mm): ')

        for item in h.get_all():
            package = item[1]
            lateFlag = False
            delivered_at = package.delivered_at.to_timedelta()
            due_time = package.delivery.split(' ')[0]
            due_time = TimeClock(due_time).to_timedelta()
            
            if input_time != 'EOD' and input_time != 'eod':

                curr_time = TimeClock(input_time).to_timedelta()

                start_time = package.delivery_start.to_timedelta()
                # if the comparsion time is before the delivered time, it is either
                # in transit or at the hub
                if curr_time < delivered_at and curr_time < start_time:
                    package.delivery_status = 'At HQ'
                elif curr_time > start_time and delivered_at > curr_time:
                	package.delivery_status = 'In transit'
                else:
                    package.delivery_status = f'Delivered at {delivered_at}'

            if delivered_at > due_time:
                lateFlag = True

            if input_time == 'eod' or input_time == 'EOD':
                delivery_status = f'Delivered at {package.delivered_at}'
            else:
                delivery_status = package.delivery_status

            if lateFlag == True and package.delivery != 'EOD': # LATE
                delivery_status = '\033[91m' + delivery_status + '\033[0m'
            elif lateFlag == False and package.delivery != 'EOD': # ON TIME
                delivery_status = '\033[92m' + delivery_status + '\033[0m'

            print(f"ID: {package.id}, Due At: {package.delivery}, Status: {delivery_status}")
        print(f'The estimated distance for the 3 trucks today is {int(total_distance)} miles')

    else:
        break
