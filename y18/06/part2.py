from typing import List
from utils.field.two_d import Cell, Coord, Field
from collections import Counter

class Space(Cell):
	def init_value(self) -> None:
		self.value = 0

	def add_value(self, dist: int) -> None:
		self.value += dist


def run(input_data: List[str], **kwargs) -> int:
	coords = []
	for datum in input_data:
		x, y = datum.split(", ")
		coords.append(Coord(int(x), int(y)))
	
	field = Field(500, 500, Space)
	for coord in coords:
		field.apply(
			transform=lambda c: c.add_value(c.manhattan(coord))
		)
	return field.apply(filterer=lambda c: c.value < 10000)