from typing import List
from utils.field.two_d import Cell, Field
from utils.math import product
from functools import partial


# this part3 is a rewritten part2 to use the Fields class

class Vent(Cell):
	def __init__(self, x: int, y: int) -> None:
		super(Vent, self).__init__(x, y)
		self.visited = False

class Heightmap(Field):
	def __init__(self, heights: List[str]) -> None:
		super(Heightmap, self).__init__(len(heights), len(heights[0]), Vent)

		def add_value(vent: Vent) -> None:
			vent.value = int(heights[vent.x][vent.y])
			vent.visited = vent.value == 9

		self.apply(add_value)
	
	def is_low_point(self, vent: Vent) -> bool:
		return all(
			self.gen_adjacent_cells(
				vent, 
				False, 
				transform=lambda n: vent.value < n.value
			)
		)

	def get_basin_size(self, vent: Vent) -> int:
		vent.visited = True
		basin_size = 1
		return 1 + sum(
			size for size in
			self.gen_adjacent_cells(
				cell=vent,
				include_diagonals=False,
				filterer=lambda n: n.value > vent.value and not n.visited,
				transform=self.get_basin_size,
			)
		)

	def get_basin_sizes(self) -> List[int]:
		return [
			size for size in self.gen_cells(
				transform=lambda x: self.get_basin_size(x), 
				filterer=lambda x: self.is_low_point(x))
		]


def run(input_data: List[str]) -> int:
	heightmap = Heightmap(input_data)
	basins = heightmap.get_basin_sizes()
	basins.sort(reverse=True)
	return product(basins[:3])
 