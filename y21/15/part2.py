from typing import List
from utils.field.two_d import Field, Cell


class DPPathing(Field):
	def __init__(self, size) -> None:
		super(DPPathing, self).__init__(size, size, Cell)
		self.items[0][0].value = 0

	def pathfind(self, cave) -> int:
		def update_value(cell):
			cell.value = cave.items[cell.x][cell.y].value + min(c.value for c in self.gen_adjacent_cells(cell, include_diagonals=False) if c.value is not None)
			for c in self.gen_adjacent_cells(cell, include_diagonals=False, filterer=lambda x: x.value is not None):
				if c.value > cell.value + cave.items[c.x][c.y].value:
					update_value(c)

		self.apply(filterer=lambda x: x.x != 0 or x.y != 0, transform=lambda x: update_value(x))
		size = len(self.items) - 1
		return self.items[size][size].value


class Cave(Field):
	def __init__(self, input_data: List[str]) -> None:
		l = len(input_data)
		super(Cave, self).__init__(l*5, l*5, Cell)
		for c in self.gen_cells():
			orig_value = int(input_data[c.x%l][c.y%l])
			unadjusted_value = (orig_value + int(c.x/l) + int(c.y/l)) % 9
			c.value = unadjusted_value if unadjusted_value else 9


def run(input_data: List[str]) -> int:
	cave = Cave(input_data)
	return DPPathing(len(input_data)*5).pathfind(cave)