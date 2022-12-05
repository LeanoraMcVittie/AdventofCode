from typing import List
from utils.field.two_d import Field, Cell


class DPPathing(Field):
	def __init__(self, size) -> None:
		super(DPPathing, self).__init__(size, size, Cell)
		self.items[0][0].value = 0

	def pathfind(self, input_data) -> int:
		# this algorithm is missing a corner case that didn't come up in part1 - fixed in part2
		for cell in self.gen_cells(filterer=lambda x: x.x != 0 or x.y != 0):
			cell.value = int(input_data[cell.x][cell.y]) + min(c.value for c in self.gen_adjacent_cells(cell, include_diagonals=False) if c.value is not None)
			for c in self.gen_adjacent_cells(cell, include_diagonals=False, filterer=lambda x: x.value is not None):
				c.value = min(c.value, cell.value + int(input_data[c.x][c.y]))
		size = len(self.items) - 1
		return self.items[size][size].value


def run(input_data: List[str], **kwargs) -> int:
	return DPPathing(len(input_data)).pathfind(input_data)