from typing import Any, Callable, Generator, List, Optional, Union


class Cell:
	def __init__(self, x: int, y: int, z: int, w: int) -> None:
		self.value = False
		self.x = x
		self.y = y
		self.z = z
		self.w = w

class Field:
	items: List[List[List[Cell]]]

	def __init__(self, x_size: int, y_size: int, z_size: int, w_size: int) -> None:
		self.x_size = x_size
		self.y_size = y_size
		self.z_size = y_size
		self.w_size = w_size
		self.items = [
			[
				[
					[
						Cell(x, y, z, w) for w in range(w_size)
					] 
					for z in range(z_size) 
				]
				for y in range(y_size)
			]
			for x in range(x_size)
		]

	@classmethod
	def create_from_input(cls, input_data: List[str]) -> "GameField":
		x_size = len(input_data)
		y_size = len(input_data[0])
		gamefield = cls(x_size+14, y_size+14, 14, 14)

		def add_value(cube: Cell) -> None:
			cube.value = input_data[cube.x-7][cube.y-7] == "#"

		gamefield.apply(
			filterer = lambda x: (
				x.x in range(7, 7+x_size) 
				and x.y in range(7, 7+y_size) 
				and x.z == 7
				and x.w == 7
			),
			transform = add_value,
		)

		return gamefield

	@classmethod
	def cycle(cls, old: "GameField") -> "GameField":
		new = cls(old.x_size, old.y_size, old.z_size, old.w_size)

		def update_value(new_cube: Cell) -> None:
			old_cube = old.get(new_cube.x, new_cube.y, new_cube.z, new_cube.w)
			if not old_cube:
				new_cube.value = False
				return
			n_count = sum(
				1 for n in old.gen_adjacent_cells(
					cell=old_cube,
					filterer=lambda x: x.value,
				)
			)
			if n_count < 2 or n_count > 3:
				new_cube.value = False
			elif old_cube.value:
				new_cube.value = True
			else:
				new_cube.value = n_count == 3

		new.apply(transform=update_value)
		return new

	def get(self, x: int, y: int, z: int, w: int, default: Any = None) -> Union[Optional[Cell], Any]:
		if x < 0 or y < 0 or z < 0 or w < 0:
			return default
		try:
			return self.items[x][y][z][w]
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
					for w in range(cell.w-1, cell.w+2):
						neighbor = self.get(x, y, z, w)
						if (
							neighbor is not None
							and neighbor != cell
							and (
								include_diagonals
								or neighbor.x == cell.x
								or neighbor.y == cell.y
								or neighbor.z == cell.z
								or neighbor.w == cell.w
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
					for w in range(len(self.items[0][0][0])):
						if filterer(self.items[x][y][z][w]):
							yield transform(self.items[x][y][z][w])


	def apply(
		self, 
		transform: Callable, 
		filterer: Callable = lambda x: True,
	) -> None:
		 [cell for cell in self.gen_cells(transform, filterer)]

	def count(self) -> int:
		return sum(1 for cube in self.gen_cells(filterer = lambda x: x.value))


def run(input_data: List[str], **kwargs) -> int:
	gamefield = Field.create_from_input(input_data)
	for _ in range(6):
		gamefield = Field.cycle(gamefield)
	return gamefield.count()
