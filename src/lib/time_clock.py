# WGU Routing Program
# This program tries to find an optimal solution to 
# the delivery or 40 packages around Salt Lake City
# by WGUPS
# Author:       Casey Arnold
# Student ID:   000962933
# File: Time_Clock.py
# Desc: This simple class makes it easy to compare times and calculate the time a truck 
# will arrive at the next site based upon its distance from it

from datetime import timedelta
class TimeClock:
	# set up object, O(1)
	def __init__(self, hours, minutes = ''):
		if isinstance(hours, str):
			if hours == 'eod' or hours == 'EOD':
				hours = 23
				minutes = 59
			else:
				hours, minutes = hours.split(':')
				minutes = minutes.split(' ')[0]

		self.hours = int(hours)
		self.minutes = int(minutes)
		self.average_speed = 18 # mph

	# return time as string -> O(1)
	def __str__(self):
		return str(self.to_timedelta())

	# return actual time object -> O(1)
	def to_timedelta(self):
		return timedelta(hours=self.hours, minutes=self.minutes)

	# calculate the next time via distance and return a new object based on it -> O(1)
	def next(self, distance):
		add_minutes = int(distance / self.average_speed * 60)
		add_hours = int(add_minutes / 60)
		add_minutes = add_minutes % 60

		self.minutes = self.minutes + add_minutes
		self.hours = self.hours + add_hours

		return TimeClock(self.hours, self.minutes)