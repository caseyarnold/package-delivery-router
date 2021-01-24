# WGU Routing Program
# This program tries to find an optimal solution to 
# the delivery or 40 packages around Salt Lake City
# by WGUPS
# Author:       Casey Arnold
# Student ID:   000962933
# File: Package.py
# Desc: This class acts as a simple wrapper for package objects in order to easily
# group the information

class Package:
    # initialize package object -> O(1)
    def __init__(self, id, addr, city, state, postal, delivery, size, note, delivery_start = '',
                 delivered_at = ''):

        self.id = id
        self.addr = addr
        self.city = city
        self.state = state
        self.postal = postal
        self.delivery = delivery
        self.size = size
        self.note = note
        self.delivery_start = delivery_start
        self.delivered_at = delivered_at
        self.delivery_status = ''

    # update an attribute of the package -> O(n)
    def update(self, attribute, value = ''): 
        if type(attribute) is dict: 
            for key, val in attribute.items():
                setattr(self, key, val)
        else:
            setattr(self, attribute, value)

        return self