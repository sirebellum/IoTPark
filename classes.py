import math

class Car:

	ID = 1 #Unique car ID

	def __init__(self, upper_x, upper_y, lower_x, lower_y):
		self.x = (upper_x + lower_x)/2
		self.y = (upper_y + lower_y)/2
		self.size = math.sqrt( pow((upper_x - lower_x), 2) + pow((upper_y - lower_y), 2) )
		self.delta_pos = 0.1 * self.size
		self.id = Car.ID
		Car.ID = Car.ID + 1