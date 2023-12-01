from typing import List
from utils.field.two_d import Cell, Coord, Field
from collections import Counter

class Space(Cell):
	def init_value(self) -> None:
		self.value = []

	def append_value(self, idx: int, dist: int) -> None:
		self.value.append((idx, dist))
	
	def set_closest(self) -> None:
		sorted_values = sorted(self.value, key=lambda v: v[1])
		if sorted_values[0][1] == sorted_values[1][1]:
			self.value = "."
		else:
			self.value = sorted_values[0][0]


def run(input_data: List[str], **kwargs) -> int:
	coords = []
	for datum in input_data:
		x, y = datum.split(", ")
		coords.append(Coord(int(x), int(y)))
	
	field = Field(500, 500, Space)
	for idx, coord in enumerate(coords):
		field.apply(
			transform=lambda c: c.append_value(idx, c.manhattan(coord))
		)
	field.apply(transform=lambda c: c.set_closest())
	infinites = set(
		field.gen_cells(
			transform=lambda c: c.value, 
			filterer=lambda c: (
				c.x == 0
				or c.y == 0
				or c.x == field.x_size - 1
				or c.y == field.y_size - 1
			)
		)
	)
	infinites.discard(".")
	for elem in Counter(
		field.gen_cells(transform=lambda c: c.value)
	).most_common():
		if elem[0] != "." and int(elem[0]) not in infinites:
			return elem[1]