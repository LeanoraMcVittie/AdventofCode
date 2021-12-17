from typing import List
import itertools as it

class Probe:
	min_x: int
	max_x: int
	min_y: int
	max_y: int

	def __init__(self, x_velocity, y_velocity) -> None:
		self.x = 0
		self.y = 0
		self.x_velocity = x_velocity
		self.y_velocity = y_velocity

	def step(self) -> bool:
		self.x += self.x_velocity
		self.y += self.y_velocity
		if self.x_velocity < 0:
			self.x_velocity += 1
		if self.x_velocity > 0:
			self.x_velocity -= 1
		self.y_velocity -= 1
		return not self.overshot()

	def in_range(self) -> bool:
		if self.x >= self.min_x and self.x <= self.max_x and self.y >= self.min_y and self.y <= self.max_y:
			return True
		return False

	def overshot(self) -> bool:
		if self.x > self.max_x or self.y < self.min_y:
			return True
		return False

def get_min_x_velocity(min_x_target, max_x_target):
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

	min_x_velocity = get_min_x_velocity(min_x, max_x)
	max_x_velocity = max_x

	max_y_velocity = abs(min_y) - 1
	min_y_velocity = min_y

	Probe.max_x = max_x
	Probe.max_y = max_y
	Probe.min_x = min_x
	Probe.min_y = min_y

	count = 0
	for vx, vy in it.product(range(min_x_velocity, max_x_velocity + 1), range(min_y_velocity, max_y_velocity + 1)):
		probe = Probe(vx, vy)
		while probe.step():
			if probe.in_range():
				count += 1
				break
	return count
