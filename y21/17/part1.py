from typing import List

class Probe:
	def __init__(self, x_velocity, y_velocity) -> None:
		self.x = 0
		self.y = 0
		self.x_velocity = x_velocity
		self.y_velocity = y_velocity

	def step(self) -> None:
		self.x += self.x_velocity
		self.y += self.y_velocity
		if self.x_velocity < 0:
			self.x_velocity += 1
		if self.x_velocity > 0:
			self.x_velocity -= 1
		self.y_velocity -= 1

def min_x_velocity(min_x_target, max_x_target):
	x_pos = 0
	i = 0
	while True:
		x_pos += i
		if x_pos > max_x_target:
			raise Exception("this calcualtion won't work")
		if x_pos > min_x_target:
			return i
		i += 1

def max_y_pos(y_velocity):
	pos = 0
	while y_velocity > 0:
		pos += y_velocity
		y_velocity -= 1
	return pos

def run(input_data: List[str]) -> int:
	x_range, y_range = input_data[0][15:].split(", y=")
	min_x, max_x = x_range.split("..")
	min_y, max_y = y_range.split("..")
	min_x = int(min_x)
	max_x = int(max_x)
	min_y = int(min_y)
	max_y = int(max_y)

	x_velocity = min_x_velocity(min_x, max_x)
	y_velocity = abs(min_y) - 1
	return max_y_pos(y_velocity)
