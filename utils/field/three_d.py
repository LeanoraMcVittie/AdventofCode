from typing import Any, Callable, Generator, List, Optional, Union


class Cell:
	def __init__(self, x: int, y: int, z: int) -> None:
		self.value = None
		self.x = x
		self.y = y
		self.z = z

class Field:
	items: List[List[List[Cell]]]

	def __init__(self, x_size: int, y_size: int, z_size: int, cell_class: Callable) -> None:
		self.items = [
			[
				[
					cell_class(x, y, z) for z in range(z_size)
				] 
				for y in range(y_size)
			]
			for x in range(x_size)
		]

	def get(self, x: int, y: int, z: int, default: Any = None) -> Union[Optional[Cell], Any]:
		if x < 0 or y < 0 or z < 0:
			return default
		try:
			return self.items[x][y][z]
		except IndexError:
			return default

	def gen_adjacent_cells(
		self, 
		cell: Cell,
		include_diagonals: bool = True, 
		transform: Callable = lambda x: x,
		filterer: Callable = lambda x: True,
	) -> Generator[Cell, None, None]:
		for x in range(cell.x-1, cell.x+2):
			for y in range(cell.y-1, cell.y+2):
				for z in range(cell.z-1, cell.z+2):
					neighbor = self.get(x, y, z)
					if (
						neighbor is not None
						and neighbor != cell
						and (
							include_diagonals
							or neighbor.x == cell.x
							or neighbor.y == cell.y
							or neighbor.z == cell.z
						)
						and filterer(neighbor)
					):
						yield transform(neighbor)

	def gen_cells(
		self, 
		transform: Callable = lambda x: x, 
		filterer: Callable = lambda x: True
	) -> Generator[Cell, None, None]:
		for x in range(len(self.items)):
			for y in range(len(self.items[0])):
				for z in range(len(self.items[0][0])):
					if filterer(self.items[x][y][z]):
						yield transform(self.items[x][y][z])


	def apply(
		self, 
		transform: Callable, 
		filterer: Callable = lambda x: True,
	) -> None:
		 [cell for cell in self.gen_cells(transform, filterer)]
