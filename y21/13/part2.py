from typing import List
from utils.field.two_d import Cell, Field

class Dot(Cell):
	def __init__(self, x: int, y: int) -> None:
		super(Dot, self).__init__(x, y)
		self.value = " "

	def set_value(self) -> None:
		self.value = "█"


class Paper(Field):
	def __init__(self, coordinates: List[str]):
		self.coords = []
		max_x = 0
		max_y = 0
		for x,y in coordinates:
			if x > max_x: max_x = x
			if y > max_y: max_y = y
			self.coords.append((int(x), int(y)))

		super(Paper, self).__init__(
			max_x+1,
			max_y+1,
			Dot
		)

		for x, y in self.coords:
			self.items[x][y].set_value()

	def print(self) -> None:
		for y in range(len(self.items[0])):
			for x in range(len(self.items)):
				print(self.items[x][y].value, end="")
			print()


def run(input_data: List[str]) -> int:
	coordinates = []
	i = 0
	while input_data[i] != "":
		x, y = input_data[i].split(",")
		x = int(x)
		y = int(y)
		coordinates.append((x,y))
		i += 1
	i += 1
	while i < len(input_data):
		axis, val = input_data[i][11:].split("=")
		val = int(val)
		new_coordinates = []
		for x, y in coordinates:
			if axis == "x" and x > val:
				new_x = val - (x - val)
				if not (new_x,y) in new_coordinates:
					new_coordinates.append((new_x,y))
			elif axis == "y" and y > val:
				new_y = val - (y - val)
				if not (x,new_y) in new_coordinates:
					new_coordinates.append((x,new_y))
			elif (x,y) not in new_coordinates:
				new_coordinates.append((x,y))
		coordinates = new_coordinates
		i += 1

	paper = Paper(coordinates)
	paper.print()