from typing import List
from utils.field.two_d import Cell, Field


class FabricSpot(Cell):
	def __init__(self, x: int, y: int) -> None:
		super().__init__(x, y)
		self.value = 0
	
	def wanted(self, num: int) -> int:
		old_value = self.value
		self.value = num
		return old_value


def run(input_data: List[str], **kwargs) -> int:
	field = Field(1000, 1000, FabricSpot)
	no_overlaps = []
	for claim in input_data:
		n, a = claim.split("@ ")
		id = int(n[1:])
		coords, dims = a.split(": ")
		x, y = coords.split(",")
		xi, yi = dims.split("x")
		results = set(field.gen_cells_in_range(
			int(x), 
			int(x) + int(xi) - 1, 
			int(y), 
			int(y) + int(yi) - 1, 
			transform=lambda c: c.wanted(id)
		))
		if results == {0}:
			no_overlaps.append(id)
		else:
			for i in results: 
				if i in no_overlaps: no_overlaps.remove(i)
	if len(no_overlaps) != 1:
		raise Exception("wrong number of no-overlaps")
	return no_overlaps[0]