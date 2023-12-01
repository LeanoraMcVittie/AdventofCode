from typing import List
from utils.field.two_d import Cell, Field

class FabricSpot(Cell):
	def __init__(self, x: int, y: int) -> None:
		super().__init__(x, y)
		self.value = 0
	
	def wanted(self) -> None:
		self.value += 1

def run(input_data: List[str], **kwargs) -> int:
	field = Field(1000, 1000, FabricSpot)
	for claim in input_data:
		_, a = claim.split("@ ")
		coords, dims = a.split(": ")
		x, y = coords.split(",")
		xi, yi = dims.split("x")
		field.apply_cells_in_range(
			int(x), 
			int(x) + int(xi) - 1, 
			int(y), 
			int(y) + int(yi) - 1, 
			transform=lambda c: c.wanted()
		)
	return len(list(field.gen_cells(filterer=lambda c: c.value >= 2)))
